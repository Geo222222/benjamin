from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from benjamin import (
    ActionClass,
    CapitalEnvelope,
    CapitalSourceRef,
    CapitalStateInput,
    DecisionValidityStatus,
    DecisionValidityWatch,
    ReconciliationStatus,
    SourceQuality,
    ValuationPolicyRef,
    WatchMode,
    WatchmanState,
    assess_capital_state,
    build_capital_state,
)

T0 = datetime(2026, 9, 3, 21, 0, tzinfo=timezone.utc)
T1 = T0 + timedelta(seconds=1)
T2 = T0 + timedelta(seconds=2)


def source(*, quality=SourceQuality.VALID) -> CapitalSourceRef:
    return CapitalSourceRef(
        source_id="SRC-WATCH-001",
        source_kind="CUSTODIAN_ACCOUNT_SNAPSHOT",
        account_id="ACC-001",
        observed_at=T0,
        known_at=T0,
        content_hash="a" * 64,
        quality=quality,
    )


def policy() -> ValuationPolicyRef:
    return ValuationPolicyRef(
        policy_id="VAL-WATCH-001",
        version="1.0.0",
        content_hash="b" * 64,
    )


def state_input(**overrides) -> CapitalStateInput:
    values = {
        "capital_structure_id": "CAP-WATCH-001",
        "base_currency": "USD",
        "as_of": T0,
        "known_at": T1,
        "valuation_policy": policy(),
        "account_ids": ("ACC-001",),
        "source_refs": (source(),),
        "reconciliation_status": ReconciliationStatus.RECONCILED,
        "cash_balance": Decimal("100000"),
        "available_cash": Decimal("50000"),
        "spot_asset_value": Decimal("80000"),
        "derivative_mark_value": Decimal("0"),
        "other_asset_value": Decimal("0"),
        "receivables": Decimal("0"),
        "unsettled_receivables": Decimal("0"),
        "liabilities": Decimal("0"),
        "unsettled_payables": Decimal("0"),
        "accrued_fees": Decimal("0"),
        "accrued_financing": Decimal("0"),
        "operational_reserve": Decimal("5000"),
        "minimum_liquidity_required": Decimal("15000"),
        "pending_redemptions": Decimal("5000"),
        "pending_withdrawals": Decimal("0"),
        "pending_distributions": Decimal("0"),
        "pending_inflows": Decimal("0"),
        "collateral_committed": Decimal("10000"),
        "initial_margin": Decimal("10000"),
        "maintenance_margin": Decimal("5000"),
        "spot_gross_exposure": Decimal("80000"),
        "derivative_gross_notional": Decimal("20000"),
        "gross_market_exposure": Decimal("100000"),
        "net_market_exposure": Decimal("70000"),
        "realized_pnl": Decimal("0"),
        "unrealized_pnl": Decimal("0"),
        "participant_equity": Decimal("180000"),
        "risk_budget_remaining": Decimal("25000"),
        "current_drawdown_fraction": Decimal("0.02"),
    }
    values.update(overrides)
    return CapitalStateInput(**values)


def envelope(**overrides) -> CapitalEnvelope:
    values = {
        "capital_structure_id": "CAP-WATCH-001",
        "responsibility_ref": "RESP-AGGRESSIVE-1.0",
        "version": "1.0.0",
        "watch_drawdown_fraction": Decimal("0.05"),
        "correction_drawdown_fraction": Decimal("0.08"),
        "emergency_drawdown_fraction": Decimal("0.12"),
        "watch_liquidity_coverage": Decimal("1.50"),
        "correction_liquidity_coverage": Decimal("1.00"),
        "emergency_liquidity_coverage": Decimal("0.50"),
        "watch_gross_exposure_multiple": Decimal("1.00"),
        "correction_gross_exposure_multiple": Decimal("1.25"),
        "emergency_gross_exposure_multiple": Decimal("1.75"),
        "watch_derivative_notional_multiple": Decimal("0.50"),
        "correction_derivative_notional_multiple": Decimal("0.75"),
        "emergency_derivative_notional_multiple": Decimal("1.00"),
        "watch_collateral_multiple": Decimal("0.25"),
        "correction_collateral_multiple": Decimal("0.40"),
        "emergency_collateral_multiple": Decimal("0.60"),
    }
    values.update(overrides)
    return CapitalEnvelope(**values)


def assess(**state_overrides):
    state = build_capital_state(state_input(**state_overrides))
    return assess_capital_state(state, envelope(), assessed_at=T2)


def test_healthy_capital_allows_normal_autonomy() -> None:
    result = assess()
    assert result.state is WatchmanState.HEALTHY
    assert result.reasons == ("CAPITAL_INSIDE_ENVELOPE",)
    assert result.permitted_action_classes == (
        ActionClass.RISK_INCREASING,
        ActionClass.RISK_NEUTRAL,
        ActionClass.RISK_REDUCING,
    )
    assert result.emergency_directives == ()


def test_watch_state_warns_without_removing_normal_action_classes() -> None:
    result = assess(current_drawdown_fraction=Decimal("0.06"))
    assert result.state is WatchmanState.WATCH
    assert "DRAWDOWN_WATCH_BOUNDARY" in result.reasons
    assert ActionClass.RISK_INCREASING in result.permitted_action_classes


def test_degraded_capital_truth_constrains_new_risk_without_implying_correction() -> None:
    result = assess(
        source_refs=(source(quality=SourceQuality.STALE),),
        stale_fields=("cash_balance",),
    )
    assert result.state is WatchmanState.CONSTRAINED
    assert "CAPITAL_STATE_DEFENSIVE_ONLY" in result.reasons
    assert ActionClass.RISK_INCREASING not in result.permitted_action_classes
    assert ActionClass.RISK_REDUCING in result.permitted_action_classes


def test_redemption_can_move_capital_from_defensive_only_into_correction_required() -> None:
    result = assess(pending_redemptions=Decimal("30000"))
    assert result.state is WatchmanState.CORRECTION_REQUIRED
    assert "CAPITAL_STATE_DEFENSIVE_ONLY" in result.reasons
    assert "LIQUIDITY_COVERAGE_CORRECTION" in result.reasons


def test_drawdown_correction_requires_return_inside_watch_boundary() -> None:
    result = assess(current_drawdown_fraction=Decimal("0.09"))
    assert result.state is WatchmanState.CORRECTION_REQUIRED
    requirement = next(item for item in result.requirements if item.metric == "current_drawdown_fraction")
    assert requirement.operator == "<="
    assert requirement.target == "0.05"
    assert requirement.current == "0.09"
    assert ActionClass.RISK_INCREASING not in result.permitted_action_classes


def test_emergency_drawdown_only_allows_risk_reduction_or_protective_action() -> None:
    result = assess(current_drawdown_fraction=Decimal("0.13"))
    assert result.state is WatchmanState.EMERGENCY
    assert result.permitted_action_classes == (
        ActionClass.RISK_REDUCING,
        ActionClass.EMERGENCY_PROTECTIVE,
    )
    assert "FREEZE_NEW_RISK" in result.emergency_directives
    assert "REDUCE_TO_SAFE_EXPOSURE" in result.emergency_directives


def test_liquidity_obligations_are_watched_against_available_cash() -> None:
    result = assess(
        available_cash=Decimal("20000"),
        operational_reserve=Decimal("5000"),
        minimum_liquidity_required=Decimal("10000"),
        pending_redemptions=Decimal("10000"),
    )
    # 20k available / 25k required = 0.8 coverage -> correction required.
    assert result.state is WatchmanState.CORRECTION_REQUIRED
    requirement = next(item for item in result.requirements if item.metric == "liquidity_coverage")
    assert requirement.current == "0.8"
    assert requirement.target == "1.50"


def test_invalidated_benjamin_decision_forces_reassessment_not_a_watchman_trade() -> None:
    state = build_capital_state(state_input())
    validity = DecisionValidityWatch(
        decision_id="DEC-001",
        status=DecisionValidityStatus.INVALIDATED,
        checked_at=T1,
        reason="ZLJ_INVALIDATION_CONDITION_MET",
        evidence_ref="ZLJ.INTELLIGENCE/INT-001",
    )
    result = assess_capital_state(
        state,
        envelope(),
        assessed_at=T2,
        decision_validity=validity,
    )
    assert result.state is WatchmanState.CORRECTION_REQUIRED
    assert "ACTIVE_DECISION_INVALIDATED" in result.reasons
    requirement = next(item for item in result.requirements if item.metric == "active_decision_validity")
    assert requirement.target == "REASSESSED_OR_CLOSED"
    assert "BENJAMIN_MUST_REASSESS_POSITION_PATH" == requirement.reason


def test_future_decision_validity_evidence_is_rejected() -> None:
    state = build_capital_state(state_input())
    validity = DecisionValidityWatch(
        decision_id="DEC-001",
        status=DecisionValidityStatus.INVALIDATED,
        checked_at=T2 + timedelta(seconds=1),
        reason="FUTURE_EVIDENCE",
    )
    with pytest.raises(ValueError, match="future decision-validity evidence"):
        assess_capital_state(state, envelope(), assessed_at=T2, decision_validity=validity)


def test_assessment_is_content_addressed_and_replay_deterministic() -> None:
    state = build_capital_state(state_input())
    first = assess_capital_state(state, envelope(), assessed_at=T2, mode=WatchMode.LIVE)
    second = assess_capital_state(state, envelope(), assessed_at=T2, mode=WatchMode.LIVE)
    assert first == second
    assert first.assessment_id.startswith("WATCH-")
    assert len(first.content_hash) == 64


def test_envelope_must_belong_to_capital_structure() -> None:
    state = build_capital_state(state_input())
    wrong = envelope(capital_structure_id="CAP-OTHER")
    with pytest.raises(ValueError, match="does not belong"):
        assess_capital_state(state, wrong, assessed_at=T2)


def test_threshold_order_is_fail_closed() -> None:
    with pytest.raises(ValueError, match="drawdown thresholds"):
        envelope(
            watch_drawdown_fraction=Decimal("0.10"),
            correction_drawdown_fraction=Decimal("0.08"),
        )
    with pytest.raises(ValueError, match="liquidity coverage thresholds"):
        envelope(
            watch_liquidity_coverage=Decimal("0.50"),
            correction_liquidity_coverage=Decimal("1.00"),
        )


def test_non_positive_equity_is_emergency() -> None:
    result = assess(
        cash_balance=Decimal("100"),
        available_cash=Decimal("100"),
        spot_asset_value=Decimal("0"),
        gross_market_exposure=Decimal("0"),
        derivative_gross_notional=Decimal("0"),
        collateral_committed=Decimal("0"),
        liabilities=Decimal("100"),
        participant_equity=Decimal("0"),
        operational_reserve=Decimal("0"),
        minimum_liquidity_required=Decimal("0"),
        pending_redemptions=Decimal("0"),
    )
    assert result.state is WatchmanState.EMERGENCY
    assert "NON_POSITIVE_NET_ASSET_VALUE" in result.reasons
