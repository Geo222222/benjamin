from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from .domain import (
    AuthorizedExecutionRequest,
    DecisionStatus,
    InvestmentDecision,
    RiskDecision,
    RiskStatus,
)


class AuthorizationError(RuntimeError):
    pass


def authorize(
    decision: InvestmentDecision,
    risk: RiskDecision,
    *,
    ttl_seconds: int = 300,
    now: datetime | None = None,
) -> AuthorizedExecutionRequest:
    """Create the only B0 artifact The Hand is permitted to execute."""
    if decision.status not in {DecisionStatus.APPROVED, DecisionStatus.MODIFIED}:
        raise AuthorizationError("Steward decision is not actionable")
    if risk.decision_id != decision.decision_id:
        raise AuthorizationError("risk decision does not cover this decision")
    if risk.status is not RiskStatus.PASS:
        raise AuthorizationError("Watchman blocked the decision")
    if ttl_seconds <= 0:
        raise AuthorizationError("authorization TTL must be positive")

    issued_at = now or datetime.now(timezone.utc)
    material = "|".join(
        [
            decision.decision_id,
            risk.risk_id,
            decision.fund_id,
            decision.instrument,
            decision.side.value,
            format(decision.quantity, "f"),
        ]
    )
    idempotency_key = hashlib.sha256(material.encode("utf-8")).hexdigest()

    return AuthorizedExecutionRequest(
        schema_version="1.0",
        authorization_id=f"AUTH-{uuid4()}",
        idempotency_key=idempotency_key,
        fund_id=decision.fund_id,
        instrument=decision.instrument,
        side=decision.side,
        quantity=decision.quantity,
        decision_id=decision.decision_id,
        risk_id=risk.risk_id,
        issued_at=issued_at,
        expires_at=issued_at + timedelta(seconds=ttl_seconds),
    )
