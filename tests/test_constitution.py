from datetime import datetime, timezone
from decimal import Decimal

import pytest

from benjamin import (
    AuthorizationError,
    Book,
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


def test_book_corrections_append_instead_of_mutating_history() -> None:
    book = Book()
    original = book.append("DECISION", "DEC-1", {"status": "APPROVED"})
    correction = book.correct(original, "operator typo", {"status": "REJECTED"})

    assert len(book.entries) == 2
    assert book.entries[0] == original
    assert correction.previous_hash == original.entry_hash
    assert correction.payload["corrects_entry_hash"] == original.entry_hash
    assert book.verify() is True
