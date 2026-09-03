from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from benjamin import (
    ActionClass,
    CapitalEnvelope,
    CapitalSourceRef,
    CapitalStateInput,
    ProjectedCapitalScenario,
    ProjectionEvidenceRef,
    ProjectionScenarioKind,
    ProjectionStatus,
    ReconciliationStatus,
    SourceQuality,
    ValuationPolicyRef,
    WatchmanState,
    assess_projected_capital_state,
    build_capital_state,
    build_projected_capital_state,
)

T0 = datetime(2026, 9, 3, 23, 30, tzinfo=timezone.utc)
T1 = T0 + timedelta(seconds=1)
T2 = T0 + timedelta(seconds=2)
T3 = T0 + timedelta(seconds=30)


def base_state():
    source = CapitalSourceRef(
        source_id="SRC-PRE-001",
        source_kind="CUSTODIAN_ACCOUNT_SNAPSHOT",
        account_id="ACC-PRE-001",
        observed_at=T0,
        known_at=T0,
        content_hash="a" * 64,
        quality=SourceQuality.VALID,
    )
    return build_capital_state(
        CapitalStateInput(
            capital_structure_id="CAP-PRE-001",
            base_currency="USD",
            as_of=T0,
            known_at=T1,
            valuation_policy=ValuationPolicyRef("VAL-PRE", "1", "b" * 64),
            account_ids=("ACC-PRE-001",),
            source_refs=(source,),
            reconciliation_status=ReconciliationStatus.RECONCILED,
            cash_balance=Decimal("100000"),
            available_cash=Decimal("50000"),
            spot_asset_value=Decimal("50000"),
            operational_reserve=Decimal("5000"),
            minimum_liquidity_required=Decimal("10000"),
            gross_market_exposure=Decimal("50000"),
            spot_gross_exposure=Decimal("50000"),
            participant_equity=Decimal("150000"),
            risk_budget_remaining=Decimal("25000"),
            current_drawdown_fraction=Decimal("0.02"),
        )
    )


def envelope():
    return CapitalEnvelope(
        capital_structure_id="CAP-PRE-001",
        responsibility_ref="RESP-PRE-001",
        version="1.0.0",
        watch_drawdown_fraction=Decimal("0.05"),
        correction_drawdown_fraction=Decimal("0.08"),
        emergency_drawdown_fraction=Decimal("0.12"),
        watch_liquidity_coverage=Decimal("1.50"),
        correction_liquidity_coverage=Decimal("1.00"),
        emergency_liquidity_coverage=Decimal("0.50"),
        watch_gross_exposure_multiple=Decimal("0.75"),
        correction_gross_exposure_multiple=Decimal("1.00"),
        emergency_gross_exposure_multiple=Decimal("1.50"),
    )


def evidence(name):
    return ProjectionEvidenceRef(
        evidence_id=name,
        evidence_kind="ZLJ_INTELLIGENCE",
        observed_at=T0,
        known_at=T1,
        content_hash=(name.encode("utf-8").hex() * 64)[:64],
    )


def scenario(kind, *, drawdown="0.03", gross="70000", status=ProjectionStatus.QUALIFIED):
    if status is ProjectionStatus.UNAVAILABLE:
        return ProjectedCapitalScenario(
            kind=kind,
            status=status,
            net_asset_value=None,
            available_cash=None,
            obligations_total=None,
            gross_market_exposure=None,
            derivative_gross_notional=None,
            collateral_committed=None,
            initial_margin=None,
            maintenance_margin=None,
            risk_budget_remaining=None,
            drawdown_fraction=None,
            evidence_refs=(),
            missing_metrics=("ALL",),
        )
    return ProjectedCapitalScenario(
        kind=kind,
        status=status,
        net_asset_value=Decimal("150000"),
        available_cash=Decimal("45000"),
        obligations_total=Decimal("15000"),
        gross_market_exposure=Decimal(gross),
        derivative_gross_notional=Decimal("0"),
        collateral_committed=Decimal("0"),
        initial_margin=Decimal("0"),
        maintenance_margin=Decimal("0"),
        risk_budget_remaining=Decimal("20000"),
        drawdown_fraction=Decimal(drawdown),
        evidence_refs=(evidence("EVID-%s" % kind.value),),
    )


def projection(*, adverse=None, stress=None):
    return build_projected_capital_state(
        base_state(),
        candidate_path_ref="PATH-BTC-001",
        responsibility_ref="RESP-PRE-001",
        projector_version="projector-v1",
        known_at=T2,
        valid_until=T3,
        scenarios=(
            scenario(ProjectionScenarioKind.EXPECTED),
            adverse or scenario(ProjectionScenarioKind.ADVERSE, drawdown="0.04"),
            stress or scenario(ProjectionScenarioKind.EXECUTION_STRESS, drawdown="0.04"),
        ),
    )


def test_all_safe_required_scenarios_permit_risk_increasing_candidate() -> None:
    result = assess_projected_capital_state(
        base_state(), projection(), envelope(),
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T2 + timedelta(seconds=1),
    )
    assert result.state is WatchmanState.HEALTHY
    assert result.candidate_permitted is True
    assert len(result.scenario_assessments) == 3


def test_unsafe_adverse_scenario_governs_even_when_expected_is_safe() -> None:
    result = assess_projected_capital_state(
        base_state(),
        projection(adverse=scenario(ProjectionScenarioKind.ADVERSE, drawdown="0.09")),
        envelope(),
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T2 + timedelta(seconds=1),
    )
    assert result.state is WatchmanState.CORRECTION_REQUIRED
    assert result.candidate_permitted is False
    assert "CANDIDATE_ACTION_CLASS_NOT_PERMITTED" in result.reasons
    assert any(reason.startswith("ADVERSE:") for reason in result.reasons)


def test_execution_stress_can_block_an_attractive_expected_path() -> None:
    stressed = scenario(ProjectionScenarioKind.EXECUTION_STRESS, gross="170000")
    result = assess_projected_capital_state(
        base_state(), projection(stress=stressed), envelope(),
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T2 + timedelta(seconds=1),
    )
    assert result.state is WatchmanState.CORRECTION_REQUIRED
    assert result.candidate_permitted is False
    stress_result = next(item for item in result.scenario_assessments if item.scenario_kind is ProjectionScenarioKind.EXECUTION_STRESS)
    assert "PROJECTED_GROSS_MARKET_EXPOSURE_MULTIPLE_CORRECTION" in stress_result.reasons


def test_unavailable_required_scenario_fails_closed_for_new_risk_but_preserves_reduction() -> None:
    unavailable = scenario(ProjectionScenarioKind.ADVERSE, status=ProjectionStatus.UNAVAILABLE)
    projected = projection(adverse=unavailable)
    increasing = assess_projected_capital_state(
        base_state(), projected, envelope(),
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T2 + timedelta(seconds=1),
    )
    reducing = assess_projected_capital_state(
        base_state(), projected, envelope(),
        candidate_action_class=ActionClass.RISK_REDUCING,
        assessed_at=T2 + timedelta(seconds=1),
    )
    assert increasing.state is WatchmanState.CONSTRAINED
    assert increasing.candidate_permitted is False
    assert reducing.state is WatchmanState.CONSTRAINED
    assert reducing.candidate_permitted is True


def test_expired_projection_is_rejected() -> None:
    with pytest.raises(ValueError, match="expired"):
        assess_projected_capital_state(
            base_state(), projection(), envelope(),
            candidate_action_class=ActionClass.RISK_INCREASING,
            assessed_at=T3,
        )


def test_projection_must_still_bind_current_authoritative_capital_state() -> None:
    projected = projection()
    changed = build_capital_state(
        CapitalStateInput(
            **{
                **{
                    "capital_structure_id": "CAP-PRE-001",
                    "base_currency": "USD",
                    "as_of": T0,
                    "known_at": T1,
                    "valuation_policy": ValuationPolicyRef("VAL-PRE", "1", "b" * 64),
                    "account_ids": ("ACC-PRE-001",),
                    "source_refs": (
                        CapitalSourceRef("SRC-PRE-001", "CUSTODIAN_ACCOUNT_SNAPSHOT", "ACC-PRE-001", T0, T0, "a" * 64),
                    ),
                    "reconciliation_status": ReconciliationStatus.RECONCILED,
                },
                "cash_balance": Decimal("100001"),
                "available_cash": Decimal("50000"),
                "spot_asset_value": Decimal("50000"),
                "operational_reserve": Decimal("5000"),
                "minimum_liquidity_required": Decimal("10000"),
                "gross_market_exposure": Decimal("50000"),
                "spot_gross_exposure": Decimal("50000"),
                "participant_equity": Decimal("150001"),
                "risk_budget_remaining": Decimal("25000"),
                "current_drawdown_fraction": Decimal("0.02"),
            }
        )
    )
    with pytest.raises(ValueError, match="no longer current"):
        assess_projected_capital_state(
            changed, projected, envelope(),
            candidate_action_class=ActionClass.RISK_INCREASING,
            assessed_at=T2 + timedelta(seconds=1),
        )


def test_pre_action_assessment_is_content_addressed_and_not_execution_authority() -> None:
    first = assess_projected_capital_state(
        base_state(), projection(), envelope(),
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T2 + timedelta(seconds=1),
    )
    second = assess_projected_capital_state(
        base_state(), projection(), envelope(),
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T2 + timedelta(seconds=1),
    )
    assert first == second
    wire = first.to_wire()
    assert wire["truth_boundary"]["authoritative_capital_state"] is False
    assert wire["truth_boundary"]["execution_authorization"] is False
    assert wire["truth_boundary"]["hand_instruction"] is False
