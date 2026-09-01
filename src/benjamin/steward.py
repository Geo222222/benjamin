from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from .domain import DecisionStatus, InvestmentDecision, Recommendation


def decide(
    recommendation: Recommendation,
    *,
    status: DecisionStatus,
    reason: str,
    quantity: Decimal | None = None,
    now: datetime | None = None,
) -> InvestmentDecision:
    """Create explicit portfolio intent from an Epinnox recommendation.

    A MODIFIED decision must state the modified quantity. APPROVED preserves the
    recommendation quantity unless an explicit equal quantity is supplied.
    """
    if status is DecisionStatus.MODIFIED and quantity is None:
        raise ValueError("MODIFIED decisions require an explicit quantity")
    if status is DecisionStatus.APPROVED and quantity not in (None, recommendation.quantity):
        raise ValueError("use MODIFIED when changing recommended quantity")

    decided_quantity = recommendation.quantity if quantity is None else quantity
    if decided_quantity <= 0:
        raise ValueError("decision quantity must be positive")

    return InvestmentDecision(
        decision_id=f"DEC-{uuid4()}",
        recommendation_id=recommendation.recommendation_id,
        fund_id=recommendation.fund_id,
        instrument=recommendation.instrument,
        side=recommendation.side,
        quantity=decided_quantity,
        status=status,
        reason=reason,
        decided_at=now or datetime.now(timezone.utc),
    )
