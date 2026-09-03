from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from benjamin import (
    ActionClass,
    CapitalSourceRef,
    CapitalStateInput,
    EconomicPathType,
    ReconciliationStatus,
    SourceQuality,
    ValuationPolicyRef,
    build_candidate_economic_path,
    build_capital_state,
)

T0 = datetime(2026, 9, 4, 0, 0, tzinfo=timezone.utc)
T1 = T0 + timedelta(seconds=1)
T2 = T0 + timedelta(seconds=2)
T3 = T0 + timedelta(minutes=5)


def state():
    return build_capital_state(
        CapitalStateInput(
            capital_structure_id="CAP-PATH-001",
            base_currency="USD",
            as_of=T0,
            known_at=T1,
            valuation_policy=ValuationPolicyRef("VAL-PATH", "1", "b" * 64),
            account_ids=("ACC-PATH",),
            source_refs=(
                CapitalSourceRef(
                    "SRC-PATH",
                    "CUSTODIAN_ACCOUNT_SNAPSHOT",
                    "ACC-PATH",
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
            minimum_liquidity_required=Decimal("10000"),
            spot_gross_exposure=Decimal("40000"),
            gross_market_exposure=Decimal("40000"),
            participant_equity=Decimal("140000"),
            risk_budget_remaining=Decimal("25000"),
            current_drawdown_fraction=Decimal("0.02"),
        )
    )


def test_spot_increase_is_content_addressed_and_provider_neutral() -> None:
    path = build_candidate_economic_path(
        state(),
        responsibility_ref="RESP-001",
        path_type=EconomicPathType.INCREASE_SPOT,
        action_class=ActionClass.RISK_INCREASING,
        economic_root_id="ASSET.BTC",
        expression_refs=("CRYPTO.SPOT.BTC-USD",),
        target_notional_change_base=Decimal("10000"),
        max_capital_commitment_base=Decimal("10050"),
        target_horizon_seconds=300,
        purpose="increase BTC economic exposure while preserving liquidity",
        intelligence_refs=("ZLJ.INTELLIGENCE/INT-001",),
        relationship_state_refs=("RELSTATE-BTC-001",),
        created_at=T2,
        valid_until=T3,
    )
    wire = path.to_wire()
    assert path.path_id.startswith("PATH-")
    assert len(path.content_hash) == 64
    assert wire["target_notional_change"]["unit"] == "BASE_CURRENCY_NOTIONAL"
    assert wire["max_capital_commitment"]["unit"] == "BASE_CURRENCY_VALUE"
    assert wire["truth_boundary"]["provider_order"] is False
    assert wire["truth_boundary"]["provider_native_quantity"] is False
    text = str(wire).lower()
    assert "contract_count" not in text
    assert "lot_size" not in text
    assert "api_key" not in text


def test_hold_is_zero_change_and_risk_neutral() -> None:
    path = build_candidate_economic_path(
        state(),
        responsibility_ref="RESP-001",
        path_type=EconomicPathType.HOLD,
        action_class=ActionClass.RISK_NEUTRAL,
        economic_root_id="PORTFOLIO",
        expression_refs=(),
        target_notional_change_base=Decimal("0"),
        max_capital_commitment_base=Decimal("0"),
        target_horizon_seconds=60,
        purpose="preserve capital while no superior qualified path exists",
        intelligence_refs=(),
        created_at=T2,
        valid_until=T3,
    )
    assert path.target_notional_change_base == Decimal("0")


def test_increase_path_cannot_masquerade_as_risk_reducing() -> None:
    with pytest.raises(ValueError, match="increase path must be classified"):
        build_candidate_economic_path(
            state(),
            responsibility_ref="RESP-001",
            path_type=EconomicPathType.INCREASE_DERIVATIVE,
            action_class=ActionClass.RISK_REDUCING,
            economic_root_id="ASSET.BTC",
            expression_refs=("CRYPTO.PERP.BTC-USD",),
            target_notional_change_base=Decimal("10000"),
            max_capital_commitment_base=Decimal("2000"),
            target_horizon_seconds=60,
            purpose="invalid classification",
            intelligence_refs=("INT-001",),
            created_at=T2,
            valid_until=T3,
        )


def test_reduce_path_must_be_risk_reducing() -> None:
    with pytest.raises(ValueError, match="reduce/exit/liquidity path"):
        build_candidate_economic_path(
            state(),
            responsibility_ref="RESP-001",
            path_type=EconomicPathType.REDUCE_SPOT,
            action_class=ActionClass.RISK_NEUTRAL,
            economic_root_id="ASSET.BTC",
            expression_refs=("CRYPTO.SPOT.BTC-USD",),
            target_notional_change_base=Decimal("5000"),
            max_capital_commitment_base=Decimal("0"),
            target_horizon_seconds=60,
            purpose="invalid classification",
            intelligence_refs=(),
            created_at=T2,
            valid_until=T3,
        )


def test_hedge_requires_classification_evidence() -> None:
    with pytest.raises(ValueError, match="classification evidence"):
        build_candidate_economic_path(
            state(),
            responsibility_ref="RESP-001",
            path_type=EconomicPathType.HEDGE,
            action_class=ActionClass.RISK_REDUCING,
            economic_root_id="ASSET.BTC",
            expression_refs=("CRYPTO.PERP.BTC-USD",),
            target_notional_change_base=Decimal("5000"),
            max_capital_commitment_base=Decimal("1000"),
            target_horizon_seconds=60,
            purpose="hedge existing BTC exposure",
            intelligence_refs=("INT-001",),
            created_at=T2,
            valid_until=T3,
        )


def test_benjamin_cannot_self_classify_a_candidate_as_emergency_protective() -> None:
    with pytest.raises(ValueError, match="cannot self-classify"):
        build_candidate_economic_path(
            state(),
            responsibility_ref="RESP-001",
            path_type=EconomicPathType.HEDGE,
            action_class=ActionClass.EMERGENCY_PROTECTIVE,
            economic_root_id="ASSET.BTC",
            expression_refs=("CRYPTO.PERP.BTC-USD",),
            target_notional_change_base=Decimal("5000"),
            max_capital_commitment_base=Decimal("1000"),
            target_horizon_seconds=60,
            purpose="invalid emergency self classification",
            intelligence_refs=("INT-001",),
            classification_evidence_refs=("WATCHMAN.REQUIREMENT/REQ-001",),
            created_at=T2,
            valid_until=T3,
        )


def test_path_cannot_exist_before_base_capital_state_was_knowable() -> None:
    with pytest.raises(ValueError, match="before base Capital State"):
        build_candidate_economic_path(
            state(),
            responsibility_ref="RESP-001",
            path_type=EconomicPathType.HOLD,
            action_class=ActionClass.RISK_NEUTRAL,
            economic_root_id="PORTFOLIO",
            expression_refs=(),
            target_notional_change_base=Decimal("0"),
            max_capital_commitment_base=Decimal("0"),
            target_horizon_seconds=60,
            purpose="invalid timing",
            intelligence_refs=(),
            created_at=T0,
            valid_until=T3,
        )


def test_ref_order_does_not_change_candidate_identity() -> None:
    kwargs = dict(
        responsibility_ref="RESP-001",
        path_type=EconomicPathType.HEDGE,
        action_class=ActionClass.RISK_REDUCING,
        economic_root_id="ASSET.BTC",
        expression_refs=("PERP", "SPOT"),
        target_notional_change_base=Decimal("5000"),
        max_capital_commitment_base=Decimal("1000"),
        target_horizon_seconds=60,
        purpose="hedge",
        intelligence_refs=("INT-B", "INT-A"),
        relationship_state_refs=("REL-B", "REL-A"),
        classification_evidence_refs=("CLASS-B", "CLASS-A"),
        created_at=T2,
        valid_until=T3,
    )
    first = build_candidate_economic_path(state(), **kwargs)
    second = build_candidate_economic_path(
        state(),
        **{
            **kwargs,
            "expression_refs": tuple(reversed(kwargs["expression_refs"])),
            "intelligence_refs": tuple(reversed(kwargs["intelligence_refs"])),
            "relationship_state_refs": tuple(reversed(kwargs["relationship_state_refs"])),
            "classification_evidence_refs": tuple(reversed(kwargs["classification_evidence_refs"])),
        },
    )
    assert first.content_hash == second.content_hash
