from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from benjamin import (
    ActionClass,
    CapitalEnvelope,
    CapitalSourceRef,
    CapitalStateInput,
    EconomicPathType,
    ProjectionEvidenceRef,
    ProjectionScenarioKind,
    ProjectionStatus,
    ReconciliationStatus,
    SourceQuality,
    ValuationPolicyRef,
    WatchmanState,
    assess_projected_capital_state,
    build_candidate_economic_path,
    build_capital_state,
    build_scenario_capital_effect,
    compile_projected_capital_state,
)
from benjamin.projection_compiler import ProjectionCompilerError

T0 = datetime(2026, 9, 4, 0, 30, tzinfo=timezone.utc)
T1 = T0 + timedelta(seconds=1)
T2 = T0 + timedelta(seconds=2)
T3 = T0 + timedelta(seconds=3)
T4 = T0 + timedelta(minutes=2)


def state():
    return build_capital_state(
        CapitalStateInput(
            capital_structure_id="CAP-COMP-001",
            base_currency="USD",
            as_of=T0,
            known_at=T1,
            valuation_policy=ValuationPolicyRef("VAL-COMP", "1", "b" * 64),
            account_ids=("ACC-COMP",),
            source_refs=(
                CapitalSourceRef(
                    "SRC-COMP",
                    "CUSTODIAN_ACCOUNT_SNAPSHOT",
                    "ACC-COMP",
                    T0,
                    T0,
                    "a" * 64,
                    SourceQuality.VALID,
                ),
            ),
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


def path():
    return build_candidate_economic_path(
        state(),
        responsibility_ref="RESP-COMP-001",
        path_type=EconomicPathType.INCREASE_SPOT,
        action_class=ActionClass.RISK_INCREASING,
        economic_root_id="ASSET.BTC",
        expression_refs=("CRYPTO.SPOT.BTC-USD",),
        target_notional_change_base=Decimal("10000"),
        max_capital_commitment_base=Decimal("10100"),
        target_horizon_seconds=60,
        purpose="increase BTC exposure",
        intelligence_refs=("ZLJ.INTELLIGENCE/INT-001",),
        created_at=T2,
        valid_until=T4,
    )


def evidence(kind):
    return ProjectionEvidenceRef(
        evidence_id="EVID-%s" % kind.value,
        evidence_kind="ZLJ_QUESTION_SPECIFIC_EXPERT_OUTPUT",
        observed_at=T0,
        known_at=T2,
        content_hash=(kind.value.encode("utf-8").hex() * 64)[:64],
    )


def effect(kind, *, pnl="0", cost="10", cash_delta="-10000", gross_delta="10000", drawdown="0.03", commitment="10010", notional="10000", status=ProjectionStatus.QUALIFIED):
    if status is ProjectionStatus.UNAVAILABLE:
        return build_scenario_capital_effect(
            path(),
            scenario_kind=kind,
            status=status,
            estimator_version="effect-estimator-v1",
            known_at=T3,
            evidence_refs=(),
            market_pnl_change_base=None,
            execution_cost_base=None,
            financing_cost_base=None,
            available_cash_delta_before_costs_base=None,
            obligations_delta_base=None,
            gross_market_exposure_delta_base=None,
            derivative_notional_delta_base=None,
            collateral_delta_base=None,
            initial_margin_delta_base=None,
            maintenance_margin_delta_base=None,
            risk_budget_remaining_delta_base=None,
            projected_drawdown_fraction=None,
            projected_notional_change_base=None,
            capital_commitment_base=None,
            missing_effects=("MARKET_PNL",),
        )
    return build_scenario_capital_effect(
        path(),
        scenario_kind=kind,
        status=status,
        estimator_version="effect-estimator-v1",
        known_at=T3,
        evidence_refs=(evidence(kind),),
        market_pnl_change_base=Decimal(pnl),
        execution_cost_base=Decimal(cost),
        financing_cost_base=Decimal("0"),
        available_cash_delta_before_costs_base=Decimal(cash_delta),
        obligations_delta_base=Decimal("0"),
        gross_market_exposure_delta_base=Decimal(gross_delta),
        derivative_notional_delta_base=Decimal("0"),
        collateral_delta_base=Decimal("0"),
        initial_margin_delta_base=Decimal("0"),
        maintenance_margin_delta_base=Decimal("0"),
        risk_budget_remaining_delta_base=Decimal("-5000"),
        projected_drawdown_fraction=Decimal(drawdown),
        projected_notional_change_base=Decimal(notional),
        capital_commitment_base=Decimal(commitment),
    )


def compile_default(**overrides):
    values = {
        ProjectionScenarioKind.EXPECTED: effect(ProjectionScenarioKind.EXPECTED, pnl="500", drawdown="0.02"),
        ProjectionScenarioKind.ADVERSE: effect(ProjectionScenarioKind.ADVERSE, pnl="-1000", cost="25", drawdown="0.05", commitment="10025"),
        ProjectionScenarioKind.EXECUTION_STRESS: effect(ProjectionScenarioKind.EXECUTION_STRESS, pnl="-300", cost="75", drawdown="0.04", commitment="10075"),
    }
    values.update(overrides)
    return compile_projected_capital_state(
        state(),
        path(),
        effects=tuple(values.values()),
        projector_version="capital-projector-v1",
        known_at=T3,
        valid_until=T4 - timedelta(seconds=1),
    )


def test_compiler_applies_economic_effects_without_provider_native_units() -> None:
    projected = compile_default()
    expected = projected.scenario(ProjectionScenarioKind.EXPECTED)
    assert expected.net_asset_value == Decimal("140490")
    assert expected.available_cash == Decimal("49990")
    assert expected.gross_market_exposure == Decimal("50000")
    assert expected.risk_budget_remaining == Decimal("20000")
    wire = projected.to_wire()
    text = str(wire).lower()
    assert "contract_count" not in text
    assert "lot_size" not in text
    assert projected.candidate_path_ref == path().path_id


def test_scenario_effect_is_bound_to_exact_candidate_path() -> None:
    other = build_candidate_economic_path(
        state(),
        responsibility_ref="RESP-COMP-001",
        path_type=EconomicPathType.INCREASE_SPOT,
        action_class=ActionClass.RISK_INCREASING,
        economic_root_id="ASSET.ETH",
        expression_refs=("CRYPTO.SPOT.ETH-USD",),
        target_notional_change_base=Decimal("10000"),
        max_capital_commitment_base=Decimal("10100"),
        target_horizon_seconds=60,
        purpose="increase ETH exposure",
        intelligence_refs=("INT-ETH",),
        created_at=T2,
        valid_until=T4,
    )
    with pytest.raises(ProjectionCompilerError, match="different candidate path"):
        compile_projected_capital_state(
            state(),
            other,
            effects=(
                effect(ProjectionScenarioKind.EXPECTED),
                effect(ProjectionScenarioKind.ADVERSE),
                effect(ProjectionScenarioKind.EXECUTION_STRESS),
            ),
            projector_version="v1",
            known_at=T3,
            valid_until=T4 - timedelta(seconds=1),
        )


def test_execution_stress_capital_commitment_breach_blocks_candidate_even_if_envelope_is_safe() -> None:
    stress = effect(
        ProjectionScenarioKind.EXECUTION_STRESS,
        cost="150",
        commitment="10250",
        notional="10000",
        drawdown="0.03",
    )
    projected = compile_default(**{ProjectionScenarioKind.EXECUTION_STRESS: stress})
    stress_scenario = projected.scenario(ProjectionScenarioKind.EXECUTION_STRESS)
    assert "MAX_CAPITAL_COMMITMENT_EXCEEDED" in stress_scenario.path_constraint_breaches

    env = CapitalEnvelope(
        capital_structure_id="CAP-COMP-001",
        responsibility_ref="RESP-COMP-001",
        version="1",
        watch_drawdown_fraction=Decimal("0.10"),
        correction_drawdown_fraction=Decimal("0.15"),
        emergency_drawdown_fraction=Decimal("0.20"),
    )
    assessment = assess_projected_capital_state(
        state(),
        projected,
        env,
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T3 + timedelta(seconds=1),
    )
    assert assessment.state is WatchmanState.CORRECTION_REQUIRED
    assert assessment.candidate_permitted is False
    assert "CANDIDATE_PATH_CONSTRAINT_BREACH" in assessment.reasons


def test_over_target_notional_is_explicit_candidate_constraint_breach() -> None:
    adverse = effect(ProjectionScenarioKind.ADVERSE, notional="11000", commitment="10000")
    projected = compile_default(**{ProjectionScenarioKind.ADVERSE: adverse})
    assert "TARGET_NOTIONAL_CHANGE_EXCEEDED" in projected.scenario(ProjectionScenarioKind.ADVERSE).path_constraint_breaches


def test_unavailable_expert_effect_stays_unavailable_and_watchman_fails_closed_for_new_risk() -> None:
    unavailable = effect(ProjectionScenarioKind.ADVERSE, status=ProjectionStatus.UNAVAILABLE)
    projected = compile_default(**{ProjectionScenarioKind.ADVERSE: unavailable})
    assert projected.scenario(ProjectionScenarioKind.ADVERSE).status is ProjectionStatus.UNAVAILABLE
    env = CapitalEnvelope(
        capital_structure_id="CAP-COMP-001",
        responsibility_ref="RESP-COMP-001",
        version="1",
        watch_drawdown_fraction=Decimal("0.10"),
        correction_drawdown_fraction=Decimal("0.15"),
        emergency_drawdown_fraction=Decimal("0.20"),
    )
    assessment = assess_projected_capital_state(
        state(), projected, env,
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T3 + timedelta(seconds=1),
    )
    assert assessment.state is WatchmanState.CONSTRAINED
    assert assessment.candidate_permitted is False


def test_qualified_effect_cannot_be_built_from_degraded_evidence() -> None:
    degraded = ProjectionEvidenceRef(
        evidence_id="EVID-DEGRADED",
        evidence_kind="EXECUTION_MODEL",
        observed_at=T0,
        known_at=T2,
        content_hash="c" * 64,
        quality=ProjectionStatus.DEGRADED,
    )
    with pytest.raises(ProjectionCompilerError, match="requires qualified evidence"):
        build_scenario_capital_effect(
            path(),
            scenario_kind=ProjectionScenarioKind.EXPECTED,
            status=ProjectionStatus.QUALIFIED,
            estimator_version="v1",
            known_at=T3,
            evidence_refs=(degraded,),
            market_pnl_change_base=Decimal("0"),
            execution_cost_base=Decimal("0"),
            financing_cost_base=Decimal("0"),
            available_cash_delta_before_costs_base=Decimal("0"),
            obligations_delta_base=Decimal("0"),
            gross_market_exposure_delta_base=Decimal("0"),
            derivative_notional_delta_base=Decimal("0"),
            collateral_delta_base=Decimal("0"),
            initial_margin_delta_base=Decimal("0"),
            maintenance_margin_delta_base=Decimal("0"),
            risk_budget_remaining_delta_base=Decimal("0"),
            projected_drawdown_fraction=Decimal("0.02"),
            projected_notional_change_base=Decimal("10000"),
            capital_commitment_base=Decimal("10000"),
        )


def test_compiler_rejects_projection_after_candidate_path_expiry() -> None:
    with pytest.raises(ProjectionCompilerError, match="candidate path is expired"):
        compile_projected_capital_state(
            state(), path(),
            effects=(
                effect(ProjectionScenarioKind.EXPECTED),
                effect(ProjectionScenarioKind.ADVERSE),
                effect(ProjectionScenarioKind.EXECUTION_STRESS),
            ),
            projector_version="v1",
            known_at=T4,
            valid_until=T4 + timedelta(seconds=1),
        )
