from datetime import datetime, timezone
from decimal import Decimal

import pytest

from benjamin import (
    AuthorizationError,
    BenjaminControlPlane,
    DecisionStatus,
    OrderSide,
    Recommendation,
    RiskPolicy,
    RiskStatus,
    authorize,
    decide,
    evaluate,
)


def rec(quantity: str = "2") -> Recommendation:
    return Recommendation(
        recommendation_id="REC-001",
        fund_id="FIRSTFRUITS",
        instrument="TEST-ASSET",
        side=OrderSide.BUY,
        quantity=Decimal(quantity),
        thesis_ref="EVIDENCE-001",
        created_at=datetime.now(timezone.utc),
    )


class RecordingPublisher:
    def __init__(self) -> None:
        self.drafts = []

    def publish(self, draft):
        self.drafts.append(draft)
        return f"BOOK-{len(self.drafts):03d}"


def test_rejected_steward_decision_cannot_be_authorized() -> None:
    decision = decide(rec(), status=DecisionStatus.REJECTED, reason="thesis insufficient")
    risk = evaluate(decision, RiskPolicy(allowed_instruments=frozenset({"TEST-ASSET"})))
    assert risk.status is RiskStatus.BLOCK
    with pytest.raises(AuthorizationError):
        authorize(decision, risk)


def test_watchman_block_overrides_steward_approval() -> None:
    decision = decide(rec("11"), status=DecisionStatus.APPROVED, reason="approved by steward")
    risk = evaluate(
        decision,
        RiskPolicy(allowed_instruments=frozenset({"TEST-ASSET"}), max_order_quantity=Decimal("10")),
    )
    assert risk.status is RiskStatus.BLOCK
    with pytest.raises(AuthorizationError, match="Watchman blocked"):
        authorize(decision, risk)


def test_passed_decision_produces_exact_authorization() -> None:
    decision = decide(rec("3"), status=DecisionStatus.APPROVED, reason="within mandate")
    risk = evaluate(
        decision,
        RiskPolicy(allowed_instruments=frozenset({"TEST-ASSET"}), max_order_quantity=Decimal("10")),
    )
    request = authorize(decision, risk)
    assert request.instrument == decision.instrument
    assert request.side == decision.side
    assert request.quantity == decision.quantity
    assert request.decision_id == decision.decision_id
    assert request.risk_id == risk.risk_id
    assert len(request.idempotency_key) == 64


def test_modification_requires_explicit_changed_quantity() -> None:
    recommendation = rec("5")
    with pytest.raises(ValueError):
        decide(recommendation, status=DecisionStatus.MODIFIED, reason="reduce risk")
    decision = decide(
        recommendation,
        status=DecisionStatus.MODIFIED,
        reason="reduce risk",
        quantity=Decimal("2"),
    )
    assert decision.quantity == Decimal("2")


def test_control_plane_requires_epinnox_book_receipt() -> None:
    publisher = RecordingPublisher()
    plane = BenjaminControlPlane(publisher)
    with pytest.raises(ValueError, match="Book receipt"):
        plane.process(
            rec(),
            recommendation_receipt_id="",
            correlation_id="LIFE-001",
            decision_status=DecisionStatus.APPROVED,
            decision_reason="approve",
            risk_policy=RiskPolicy(allowed_instruments=frozenset({"TEST-ASSET"})),
        )
    assert publisher.drafts == []


def test_control_plane_records_decision_risk_and_authorization_before_handoff() -> None:
    publisher = RecordingPublisher()
    plane = BenjaminControlPlane(publisher)
    result = plane.process(
        rec("3"),
        recommendation_receipt_id="EPINNOX-BOOK-001",
        correlation_id="LIFE-001",
        decision_status=DecisionStatus.APPROVED,
        decision_reason="within mandate",
        risk_policy=RiskPolicy(
            allowed_instruments=frozenset({"TEST-ASSET"}),
            max_order_quantity=Decimal("10"),
        ),
    )

    assert result.authorization is not None
    assert [draft.event_type for draft in publisher.drafts] == [
        "BENJAMIN.DECISION",
        "BENJAMIN.RISK",
        "BENJAMIN.AUTHORIZATION",
    ]
    assert publisher.drafts[0].causation_receipt_id == "EPINNOX-BOOK-001"
    assert publisher.drafts[1].causation_receipt_id == "BOOK-001"
    assert publisher.drafts[2].causation_receipt_id == "BOOK-002"
    assert result.evidence.authorization_receipt_id == "BOOK-003"


def test_watchman_block_is_recorded_but_never_authorized() -> None:
    publisher = RecordingPublisher()
    result = BenjaminControlPlane(publisher).process(
        rec("11"),
        recommendation_receipt_id="EPINNOX-BOOK-001",
        correlation_id="LIFE-002",
        decision_status=DecisionStatus.APPROVED,
        decision_reason="desired",
        risk_policy=RiskPolicy(
            allowed_instruments=frozenset({"TEST-ASSET"}),
            max_order_quantity=Decimal("10"),
        ),
    )
    assert result.authorization is None
    assert result.evidence.authorization_receipt_id is None
    assert [draft.event_type for draft in publisher.drafts] == ["BENJAMIN.DECISION", "BENJAMIN.RISK"]
