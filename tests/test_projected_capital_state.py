from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from benjamin import (
    CapitalSourceRef,
    CapitalStateInput,
    ProjectedCapitalScenario,
    ProjectionEvidenceRef,
    ProjectionScenarioKind,
    ProjectionStatus,
    ReconciliationStatus,
    SourceQuality,
    ValuationPolicyRef,
    build_capital_state,
    build_projected_capital_state,
)

T0 = datetime(2026, 9, 3, 23, 0, tzinfo=timezone.utc)
T1 = T0 + timedelta(seconds=1)
T2 = T0 + timedelta(seconds=2)
T3 = T0 + timedelta(seconds=30)


def _base_state():
    source = CapitalSourceRef(
        source_id="SRC-PROJ-001",
        source_kind="CUSTODIAN_ACCOUNT_SNAPSHOT",
        account_id="ACC-PROJ-001",
        observed_at=T0,
        known_at=T0,
        content_hash="a" * 64,
        quality=SourceQuality.VALID,
    )
    policy = ValuationPolicyRef(
        policy_id="VAL-PROJ-001",
        version="1.0.0",
        content_hash="b" * 64,
    )
    return build_capital_state(
        CapitalStateInput(
            capital_structure_id="CAP-PROJ-001",
            base_currency="USD",
            as_of=T0,
            known_at=T1,
            valuation_policy=policy,
            account_ids=("ACC-PROJ-001",),
            source_refs=(source,),
            reconciliation_status=ReconciliationStatus.RECONCILED,
            cash_balance=Decimal("100000"),
            available_cash=Decimal("60000"),
            spot_asset_value=Decimal("40000"),
            operational_reserve=Decimal("5000"),
            minimum_liquidity_required=Decimal("10000"),
            spot_gross_exposure=Decimal("40000"),
            gross_market_exposure=Decimal("40000"),
            participant_equity=Decimal("140000"),
            risk_budget_remaining=Decimal("25000"),
            current_drawdown_fraction=Decimal("0.02"),
        )
    )


def _evidence(name: str, *, known_at=T1, observed_at=T0, kind="ZLJ_INTELLIGENCE") -> ProjectionEvidenceRef:
    return ProjectionEvidenceRef(
        evidence_id=name,
        evidence_kind=kind,
        observed_at=observed_at,
        known_at=known_at,
        content_hash=(name.encode("utf-8").hex() * 64)[:64],
        quality=ProjectionStatus.QUALIFIED,
    )


def _scenario(kind: ProjectionScenarioKind, *, drawdown="0.03", gross="60000", evidence=None):
    return ProjectedCapitalScenario(
        kind=kind,
        status=ProjectionStatus.QUALIFIED,
        net_asset_value=Decimal("139500"),
        available_cash=Decimal("40000"),
        obligations_total=Decimal("15000"),
        gross_market_exposure=Decimal(gross),
        derivative_gross_notional=Decimal("0"),
        collateral_committed=Decimal("0"),
        initial_margin=Decimal("0"),
        maintenance_margin=Decimal("0"),
        risk_budget_remaining=Decimal("18000"),
        drawdown_fraction=Decimal(drawdown),
        evidence_refs=(evidence or _evidence("EVID-%s" % kind.value),),
    )


def _projection(*, adverse_drawdown="0.06"):
    return build_projected_capital_state(
        _base_state(),
        candidate_path_ref="PATH-BTC-SPOT-INCREASE-001",
        responsibility_ref="RESP-AGGRESSIVE-1.0",
        projector_version="capital-projector-v1",
        known_at=T2,
        valid_until=T3,
        scenarios=(
            _scenario(ProjectionScenarioKind.EXPECTED, drawdown="0.03"),
            _scenario(ProjectionScenarioKind.ADVERSE, drawdown=adverse_drawdown, gross="65000"),
            _scenario(ProjectionScenarioKind.EXECUTION_STRESS, drawdown="0.04", gross="62000"),
        ),
    )


def test_projection_is_content_addressed_and_explicitly_non_authoritative() -> None:
    first = _projection()
    second = _projection()
    assert first == second
    assert first.projection_id.startswith("PROJCAP-")
    assert len(first.content_hash) == 64
    wire = first.to_wire()
    assert wire["truth_boundary"]["authoritative_capital_state"] is False
    assert wire["truth_boundary"]["may_advance_capital_state_pointer"] is False
    assert wire["truth_boundary"]["requires_post_execution_reconciliation"] is True
    assert first.base_capital_state_hash == _base_state().content_hash


def test_required_expected_adverse_and_execution_stress_scenarios_are_enforced() -> None:
    with pytest.raises(ValueError, match="missing required projection scenarios"):
        build_projected_capital_state(
            _base_state(),
            candidate_path_ref="PATH-001",
            responsibility_ref="RESP-001",
            projector_version="v1",
            known_at=T2,
            valid_until=T3,
            scenarios=(_scenario(ProjectionScenarioKind.EXPECTED),),
        )


def test_qualified_scenario_cannot_hide_missing_safety_metric() -> None:
    with pytest.raises(ValueError, match="qualified projected scenario is missing metrics"):
        ProjectedCapitalScenario(
            kind=ProjectionScenarioKind.ADVERSE,
            status=ProjectionStatus.QUALIFIED,
            net_asset_value=Decimal("100"),
            available_cash=Decimal("50"),
            obligations_total=Decimal("10"),
            gross_market_exposure=None,
            derivative_gross_notional=Decimal("0"),
            collateral_committed=Decimal("0"),
            initial_margin=Decimal("0"),
            maintenance_margin=Decimal("0"),
            risk_budget_remaining=Decimal("10"),
            drawdown_fraction=Decimal("0.1"),
            evidence_refs=(_evidence("EVID-MISSING"),),
        )


def test_unavailable_scenario_cannot_publish_partial_numeric_state() -> None:
    with pytest.raises(ValueError, match="must not publish partial numeric state"):
        ProjectedCapitalScenario(
            kind=ProjectionScenarioKind.ADVERSE,
            status=ProjectionStatus.UNAVAILABLE,
            net_asset_value=Decimal("100"),
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
            missing_metrics=("available_cash",),
        )


def test_projection_rejects_future_known_evidence() -> None:
    future = _evidence("EVID-FUTURE", known_at=T2 + timedelta(seconds=1))
    with pytest.raises(ValueError, match="known after projection known_at"):
        build_projected_capital_state(
            _base_state(),
            candidate_path_ref="PATH-001",
            responsibility_ref="RESP-001",
            projector_version="v1",
            known_at=T2,
            valid_until=T3,
            scenarios=(
                _scenario(ProjectionScenarioKind.EXPECTED, evidence=future),
                _scenario(ProjectionScenarioKind.ADVERSE),
                _scenario(ProjectionScenarioKind.EXECUTION_STRESS),
            ),
        )


def test_post_base_authoritative_capital_fact_requires_a_new_real_capital_state() -> None:
    changed_capital = _evidence(
        "EVID-NEW-CAPITAL",
        observed_at=T0 + timedelta(milliseconds=500),
        known_at=T1,
        kind="AUTHORITATIVE_CAPITAL_FACT",
    )
    with pytest.raises(ValueError, match="post-base capital facts"):
        build_projected_capital_state(
            _base_state(),
            candidate_path_ref="PATH-001",
            responsibility_ref="RESP-001",
            projector_version="v1",
            known_at=T2,
            valid_until=T3,
            scenarios=(
                _scenario(ProjectionScenarioKind.EXPECTED, evidence=changed_capital),
                _scenario(ProjectionScenarioKind.ADVERSE),
                _scenario(ProjectionScenarioKind.EXECUTION_STRESS),
            ),
        )


def test_different_adverse_experience_changes_projection_identity() -> None:
    mild = _projection(adverse_drawdown="0.06")
    severe = _projection(adverse_drawdown="0.11")
    assert mild.content_hash != severe.content_hash
    assert mild.projection_id != severe.projection_id


def test_projection_expiry_is_fail_closed() -> None:
    with pytest.raises(ValueError, match="valid_until must be after known_at"):
        build_projected_capital_state(
            _base_state(),
            candidate_path_ref="PATH-001",
            responsibility_ref="RESP-001",
            projector_version="v1",
            known_at=T2,
            valid_until=T2,
            scenarios=(
                _scenario(ProjectionScenarioKind.EXPECTED),
                _scenario(ProjectionScenarioKind.ADVERSE),
                _scenario(ProjectionScenarioKind.EXECUTION_STRESS),
            ),
        )
