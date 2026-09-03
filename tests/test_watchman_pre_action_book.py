import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from benjamin import (
    ActionClass,
    CapitalEnvelope,
    CapitalSourceRef,
    CapitalStateInput,
    ProjectedCapitalScenario,
    ProjectionEvidenceRef,
    ProjectionScenarioKind,
    ReconciliationStatus,
    SourceQuality,
    ValuationPolicyRef,
    assess_projected_capital_state,
    build_capital_state,
    build_projected_capital_state,
    watchman_pre_action_assessment_draft,
)

T0 = datetime(2026, 9, 3, 23, 45, tzinfo=timezone.utc)
T1 = T0 + timedelta(seconds=1)
T2 = T0 + timedelta(seconds=2)
T3 = T0 + timedelta(seconds=30)


def _state():
    return build_capital_state(
        CapitalStateInput(
            capital_structure_id="CAP-PRE-BOOK",
            base_currency="USD",
            as_of=T0,
            known_at=T1,
            valuation_policy=ValuationPolicyRef("VAL-PRE-BOOK", "1", "b" * 64),
            account_ids=("ACC-PRE-BOOK",),
            source_refs=(
                CapitalSourceRef(
                    "SRC-PRE-BOOK",
                    "CUSTODIAN_ACCOUNT_SNAPSHOT",
                    "ACC-PRE-BOOK",
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
            gross_market_exposure=Decimal("40000"),
            spot_gross_exposure=Decimal("40000"),
            participant_equity=Decimal("140000"),
            risk_budget_remaining=Decimal("25000"),
            current_drawdown_fraction=Decimal("0.02"),
        )
    )


def _scenario(kind, drawdown):
    evidence = ProjectionEvidenceRef(
        evidence_id="EVID-%s" % kind.value,
        evidence_kind="ZLJ_INTELLIGENCE",
        observed_at=T0,
        known_at=T1,
        content_hash=(kind.value.encode("utf-8").hex() * 64)[:64],
    )
    return ProjectedCapitalScenario(
        kind=kind,
        status=evidence.quality,
        net_asset_value=Decimal("139000"),
        available_cash=Decimal("45000"),
        obligations_total=Decimal("10000"),
        gross_market_exposure=Decimal("60000"),
        derivative_gross_notional=Decimal("0"),
        collateral_committed=Decimal("0"),
        initial_margin=Decimal("0"),
        maintenance_margin=Decimal("0"),
        risk_budget_remaining=Decimal("18000"),
        drawdown_fraction=Decimal(drawdown),
        evidence_refs=(evidence,),
    )


def test_book_draft_proves_which_projection_and_scenario_governed_without_becoming_authorization() -> None:
    state = _state()
    projection = build_projected_capital_state(
        state,
        candidate_path_ref="PATH-PRE-BOOK",
        responsibility_ref="RESP-PRE-BOOK",
        projector_version="projector-v1",
        known_at=T2,
        valid_until=T3,
        scenarios=(
            _scenario(ProjectionScenarioKind.EXPECTED, "0.03"),
            _scenario(ProjectionScenarioKind.ADVERSE, "0.09"),
            _scenario(ProjectionScenarioKind.EXECUTION_STRESS, "0.04"),
        ),
    )
    envelope = CapitalEnvelope(
        capital_structure_id="CAP-PRE-BOOK",
        responsibility_ref="RESP-PRE-BOOK",
        version="1",
        watch_drawdown_fraction=Decimal("0.05"),
        correction_drawdown_fraction=Decimal("0.08"),
        emergency_drawdown_fraction=Decimal("0.12"),
    )
    assessment = assess_projected_capital_state(
        state,
        projection,
        envelope,
        candidate_action_class=ActionClass.RISK_INCREASING,
        assessed_at=T2 + timedelta(seconds=1),
    )
    draft = watchman_pre_action_assessment_draft(
        assessment,
        correlation_id="CORR-PRE-BOOK",
        causation_receipt_id="BOOK-PROJECTION-001",
    )
    payload = json.loads(draft.payload.decode("utf-8"))

    assert draft.event_type == "WATCHMAN.PRE_ACTION_ASSESSMENT"
    assert payload["projection_id"] == projection.projection_id
    assert payload["projection_hash"] == projection.content_hash
    assert payload["base_capital_state_hash"] == state.content_hash
    assert payload["candidate_permitted"] is False
    adverse = next(item for item in payload["scenario_assessments"] if item["scenario_kind"] == "ADVERSE")
    assert adverse["state"] == "CORRECTION_REQUIRED"
    assert payload["truth_boundary"]["execution_authorization"] is False
    assert payload["truth_boundary"]["hand_instruction"] is False
    assert "source_refs" not in payload
    assert "account_ids" not in payload
