from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class DecisionStatus(StrEnum):
    APPROVED = "APPROVED"
    MODIFIED = "MODIFIED"
    REJECTED = "REJECTED"


class RiskStatus(StrEnum):
    PASS = "PASS"
    BLOCK = "BLOCK"


@dataclass(frozen=True, slots=True)
class Recommendation:
    recommendation_id: str
    fund_id: str
    instrument: str
    side: OrderSide
    quantity: Decimal
    thesis_ref: str
    created_at: datetime

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("recommendation quantity must be positive")
        if not self.recommendation_id or not self.fund_id or not self.instrument:
            raise ValueError("recommendation identifiers must be non-empty")
        if not self.thesis_ref:
            raise ValueError("recommendation must reference evidence/thesis")


@dataclass(frozen=True, slots=True)
class InvestmentDecision:
    decision_id: str
    recommendation_id: str
    fund_id: str
    instrument: str
    side: OrderSide
    quantity: Decimal
    status: DecisionStatus
    reason: str
    decided_at: datetime

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("decision quantity must be positive")
        if not self.reason:
            raise ValueError("decision reason is required")


@dataclass(frozen=True, slots=True)
class RiskDecision:
    risk_id: str
    decision_id: str
    status: RiskStatus
    reasons: tuple[str, ...]
    checked_at: datetime

    def __post_init__(self) -> None:
        if not self.reasons:
            raise ValueError("risk decision must contain at least one reason")


@dataclass(frozen=True, slots=True)
class AuthorizedExecutionRequest:
    schema_version: str
    authorization_id: str
    idempotency_key: str
    fund_id: str
    instrument: str
    side: OrderSide
    quantity: Decimal
    decision_id: str
    risk_id: str
    issued_at: datetime
    expires_at: datetime

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("authorized quantity must be positive")
        if self.expires_at <= self.issued_at:
            raise ValueError("authorization must expire after issuance")

    def to_wire(self) -> dict[str, str]:
        return {
            "schema_version": self.schema_version,
            "authorization_id": self.authorization_id,
            "idempotency_key": self.idempotency_key,
            "fund_id": self.fund_id,
            "instrument": self.instrument,
            "side": self.side.value,
            "quantity": format(self.quantity, "f"),
            "decision_id": self.decision_id,
            "risk_id": self.risk_id,
            "issued_at": self.issued_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
        }
