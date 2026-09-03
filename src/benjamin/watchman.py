from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from .domain import DecisionStatus, InvestmentDecision, RiskDecision, RiskStatus


@dataclass(frozen=True)
class RiskPolicy:
    """Minimal deterministic B0 policy.

    Future policy modules can add exposure, liquidity, jurisdiction, mandate,
    counterparty, and investor-capital controls without weakening this gate.
    """

    allowed_instruments: frozenset[str] = field(default_factory=frozenset)
    prohibited_instruments: frozenset[str] = field(default_factory=frozenset)
    max_order_quantity: Decimal | None = None


def evaluate(
    decision: InvestmentDecision,
    policy: RiskPolicy,
    *,
    now: datetime | None = None,
) -> RiskDecision:
    reasons: list[str] = []

    if decision.status not in {DecisionStatus.APPROVED, DecisionStatus.MODIFIED}:
        reasons.append("STEWARD_DECISION_NOT_ACTIONABLE")

    if decision.instrument in policy.prohibited_instruments:
        reasons.append("INSTRUMENT_PROHIBITED")

    if policy.allowed_instruments and decision.instrument not in policy.allowed_instruments:
        reasons.append("INSTRUMENT_NOT_ALLOWED")

    if policy.max_order_quantity is not None and decision.quantity > policy.max_order_quantity:
        reasons.append("ORDER_QUANTITY_LIMIT_EXCEEDED")

    if reasons:
        status = RiskStatus.BLOCK
    else:
        status = RiskStatus.PASS
        reasons.append("B0_POLICY_PASS")

    return RiskDecision(
        risk_id=f"RSK-{uuid4()}",
        decision_id=decision.decision_id,
        status=status,
        reasons=tuple(reasons),
        checked_at=now or datetime.now(timezone.utc),
    )
