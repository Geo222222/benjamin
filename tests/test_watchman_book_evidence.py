import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from benjamin import (
    CapitalEnvelope,
    CapitalSourceRef,
    CapitalStateInput,
    ReconciliationStatus,
    SourceQuality,
    ValuationPolicyRef,
    assess_capital_state,
    build_capital_state,
    watchman_capital_assessment_draft,
)

T0 = datetime(2026, 9, 3, 22, 0, tzinfo=timezone.utc)
T1 = T0 + timedelta(seconds=1)
T2 = T0 + timedelta(seconds=2)


def _state():
    source = CapitalSourceRef(
        source_id="SRC-BOOK-WATCH",
        source_kind="CUSTODIAN_ACCOUNT_SNAPSHOT",
        account_id="ACC-BOOK-WATCH",
        observed_at=T0,
        known_at=T0,
        content_hash="a" * 64,
        quality=SourceQuality.VALID,
    )
    policy = ValuationPolicyRef(
        policy_id="VAL-BOOK-WATCH",
        version="1.0.0",
        content_hash="b" * 64,
    )
    return build_capital_state(
        CapitalStateInput(
            capital_structure_id="CAP-BOOK-WATCH",
            base_currency="USD",
            as_of=T0,
            known_at=T1,
            valuation_policy=policy,
            account_ids=("ACC-BOOK-WATCH",),
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
            risk_budget_remaining=Decimal("20000"),
            current_drawdown_fraction=Decimal("0.09"),
        )
    )


def _envelope():
    return CapitalEnvelope(
        capital_structure_id="CAP-BOOK-WATCH",
        responsibility_ref="RESP-BOOK-WATCH-1",
        version="1.0.0",
        watch_drawdown_fraction=Decimal("0.05"),
        correction_drawdown_fraction=Decimal("0.08"),
        emergency_drawdown_fraction=Decimal("0.12"),
    )


def test_book_draft_binds_exact_capital_and_envelope_lineage_without_raw_provider_payloads() -> None:
    state = _state()
    assessment = assess_capital_state(state, _envelope(), assessed_at=T2)
    draft = watchman_capital_assessment_draft(
        assessment,
        correlation_id="CORR-001",
        causation_receipt_id="BOOK-CAPSTATE-001",
    )
    payload = json.loads(draft.payload.decode("utf-8"))

    assert draft.event_type == "WATCHMAN.CAPITAL_ASSESSMENT"
    assert draft.subject_id == assessment.assessment_id
    assert payload["capital_state_id"] == state.capital_state_id
    assert payload["capital_state_hash"] == state.content_hash
    assert payload["envelope_id"] == _envelope().envelope_id
    assert payload["envelope_hash"] == _envelope().content_hash()
    assert payload["state"] == "CORRECTION_REQUIRED"
    assert payload["requirements"]
    assert "source_refs" not in payload
    assert "account_ids" not in payload
    assert "provider" not in draft.payload.decode("utf-8").lower()
