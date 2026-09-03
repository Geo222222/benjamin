from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from benjamin import (
    CapitalSourceRef,
    CapitalStateInput,
    ReconciliationStatus,
    RoutingReadiness,
    SourceQuality,
    ValuationPolicyRef,
    build_capital_state,
)

T0 = datetime(2026, 9, 3, 20, 0, tzinfo=timezone.utc)
T1 = T0 + timedelta(seconds=1)


def source(*, quality=SourceQuality.VALID, observed_at=T0, known_at=T0) -> CapitalSourceRef:
    return CapitalSourceRef(
        source_id="SRC-001",
        source_kind="CUSTODIAN_ACCOUNT_SNAPSHOT",
        account_id="ACC-001",
        observed_at=observed_at,
        known_at=known_at,
        content_hash="a" * 64,
        quality=quality,
    )


def policy() -> ValuationPolicyRef:
    return ValuationPolicyRef(
        policy_id="VAL-US-DOLLAR-LIQUID-001",
        version="1.0.0",
        content_hash="b" * 64,
    )


def state_input(**overrides) -> CapitalStateInput:
    values = {
        "capital_structure_id": "CAP-POOL-001",
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
        "derivative_mark_value": Decimal("-2000"),
        "other_asset_value": Decimal("10000"),
        "receivables": Decimal("5000"),
        "unsettled_receivables": Decimal("3000"),
        "liabilities": Decimal("7000"),
        "unsettled_payables": Decimal("2000"),
        "accrued_fees": Decimal("1000"),
        "accrued_financing": Decimal("500"),
        "operational_reserve": Decimal("5000"),
        "minimum_liquidity_required": Decimal("15000"),
        "pending_redemptions": Decimal("10000"),
        "pending_withdrawals": Decimal("2000"),
        "pending_distributions": Decimal("1000"),
        "pending_inflows": Decimal("25000"),
        "collateral_committed": Decimal("12000"),
        "initial_margin": Decimal("12000"),
        "maintenance_margin": Decimal("8000"),
        "spot_gross_exposure": Decimal("80000"),
        "derivative_gross_notional": Decimal("40000"),
        "gross_market_exposure": Decimal("120000"),
        "net_market_exposure": Decimal("60000"),
        "realized_pnl": Decimal("3500"),
        "unrealized_pnl": Decimal("-1200"),
        "participant_equity": Decimal("185500"),
        "risk_budget_remaining": Decimal("25000"),
        "current_drawdown_fraction": Decimal("0.042"),
    }
    values.update(overrides)
    return CapitalStateInput(**values)


def test_capital_state_is_deterministic_and_content_addressed() -> None:
    first = build_capital_state(state_input())
    second = build_capital_state(state_input())
    assert first == second
    assert first.capital_state_id == second.capital_state_id
    assert len(first.content_hash) == 64
    assert first.capital_state_id.startswith("CAPSTATE-")


def test_capital_state_derives_accounting_truth_without_counting_pending_inflows() -> None:
    state = build_capital_state(state_input())

    # Assets: 100000 cash + 80000 spot + 10000 other + 5000 receivable + 3000 unsettled.
    # Negative derivative mark becomes a liability, not an asset.
    assert state.gross_assets == Decimal("198000")
    assert state.gross_liabilities == Decimal("12500")
    assert state.net_asset_value == Decimal("185500")

    # 50k provider-available cash - 5k reserve - 15k minimum liquidity
    # - 10k redemptions - 2k withdrawals - 1k distributions = 17k.
    assert state.liquidity_available_for_deployment == Decimal("17000")
    assert state.risk_capital_available == Decimal("17000")
    assert state.pending_inflows == Decimal("25000")
    assert state.routing_readiness is RoutingReadiness.FULL


def test_risk_budget_caps_deployable_risk_capital() -> None:
    state = build_capital_state(state_input(risk_budget_remaining=Decimal("4000")))
    assert state.liquidity_available_for_deployment == Decimal("17000")
    assert state.risk_capital_available == Decimal("4000")


def test_pending_redemption_can_force_defensive_only_routing() -> None:
    state = build_capital_state(state_input(pending_redemptions=Decimal("30000")))
    assert state.liquidity_available_for_deployment == Decimal("0")
    assert state.risk_capital_available == Decimal("0")
    assert state.routing_readiness is RoutingReadiness.DEFENSIVE_ONLY
    assert "NO_RISK_CAPITAL_AVAILABLE" in state.readiness_reasons


def test_reconciliation_discrepancy_forces_defensive_only_not_fake_health() -> None:
    state = build_capital_state(
        state_input(
            reconciliation_status=ReconciliationStatus.DISCREPANCY,
            discrepancy_refs=("REC-DIFF-001",),
        )
    )
    assert state.routing_readiness is RoutingReadiness.DEFENSIVE_ONLY
    assert "RECONCILIATION_DISCREPANCY" in state.readiness_reasons
    assert "OPEN_RECONCILIATION_DISCREPANCY" in state.readiness_reasons


def test_stale_or_missing_capital_truth_disallows_new_risk() -> None:
    state = build_capital_state(
        state_input(
            source_refs=(source(quality=SourceQuality.STALE),),
            stale_fields=("cash_balance",),
            missing_fields=("pending_redemptions",),
        )
    )
    assert state.routing_readiness is RoutingReadiness.DEFENSIVE_ONLY
    assert "CAPITAL_SOURCE_STALE" in state.readiness_reasons
    assert "STALE_CAPITAL_FIELDS" in state.readiness_reasons
    assert "MISSING_CAPITAL_FIELDS" in state.readiness_reasons


def test_unavailable_reconciliation_blocks_routing() -> None:
    state = build_capital_state(
        state_input(reconciliation_status=ReconciliationStatus.UNAVAILABLE)
    )
    assert state.routing_readiness is RoutingReadiness.BLOCKED
    assert state.readiness_reasons == ("RECONCILIATION_UNAVAILABLE",)


def test_all_sources_unavailable_blocks_routing() -> None:
    state = build_capital_state(
        state_input(source_refs=(source(quality=SourceQuality.UNAVAILABLE),))
    )
    assert state.routing_readiness is RoutingReadiness.BLOCKED
    assert state.readiness_reasons == ("ALL_CAPITAL_SOURCES_UNAVAILABLE",)


def test_non_positive_nav_blocks_routing() -> None:
    state = build_capital_state(
        state_input(
            cash_balance=Decimal("100"),
            available_cash=Decimal("100"),
            spot_asset_value=Decimal("0"),
            other_asset_value=Decimal("0"),
            receivables=Decimal("0"),
            unsettled_receivables=Decimal("0"),
            derivative_mark_value=Decimal("0"),
            liabilities=Decimal("100"),
            unsettled_payables=Decimal("0"),
            accrued_fees=Decimal("0"),
            accrued_financing=Decimal("0"),
            participant_equity=Decimal("0"),
        )
    )
    assert state.net_asset_value == Decimal("0")
    assert state.routing_readiness is RoutingReadiness.BLOCKED
    assert state.readiness_reasons == ("NON_POSITIVE_NET_ASSET_VALUE",)


def test_future_observation_is_rejected_as_lookahead() -> None:
    future_source = source(observed_at=T0 + timedelta(seconds=2), known_at=T0 + timedelta(seconds=2))
    with pytest.raises(ValueError, match="after as_of"):
        state_input(source_refs=(future_source,), known_at=T0 + timedelta(seconds=3))


def test_information_unknown_at_state_time_is_rejected() -> None:
    late_source = source(observed_at=T0, known_at=T0 + timedelta(seconds=2))
    with pytest.raises(ValueError, match="known after state known_at"):
        state_input(source_refs=(late_source,), known_at=T1)


def test_negative_booked_asset_or_obligation_is_rejected() -> None:
    with pytest.raises(ValueError, match="pending_redemptions cannot be negative"):
        state_input(pending_redemptions=Decimal("-1"))


def test_available_cash_cannot_exceed_cash_balance() -> None:
    with pytest.raises(ValueError, match="available_cash cannot exceed"):
        state_input(cash_balance=Decimal("10"), available_cash=Decimal("11"))


def test_valuation_policy_is_part_of_state_identity() -> None:
    original = build_capital_state(state_input())
    changed = build_capital_state(
        state_input(
            valuation_policy=ValuationPolicyRef(
                policy_id="VAL-US-DOLLAR-LIQUID-001",
                version="1.0.1",
                content_hash="c" * 64,
            )
        )
    )
    assert original.content_hash != changed.content_hash
    assert original.capital_state_id != changed.capital_state_id


def test_wire_contract_preserves_readiness_and_lineage() -> None:
    state = build_capital_state(state_input())
    wire = state.to_wire()
    assert wire["routing_readiness"] == "FULL"
    assert wire["valuation_policy"]["version"] == "1.0.0"
    assert wire["source_refs"][0]["source_id"] == "SRC-001"
    assert wire["pending_inflows"] == "25000"
    assert wire["risk_capital_available"] == "17000"
