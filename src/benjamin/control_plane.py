from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .authority import authorize
from .domain import (
    AuthorizedExecutionRequest,
    DecisionStatus,
    InvestmentDecision,
    Recommendation,
    RiskDecision,
    RiskStatus,
)
from .evidence import EvidencePublisher, authorization_draft, decision_draft, risk_draft
from .steward import decide
from .watchman import RiskPolicy, evaluate


@dataclass(frozen=True, slots=True)
class EvidenceLineage:
    recommendation_receipt_id: str
    decision_receipt_id: str
    risk_receipt_id: str
    authorization_receipt_id: str | None


@dataclass(frozen=True, slots=True)
class ControlPlaneResult:
    decision: InvestmentDecision
    risk: RiskDecision
    authorization: AuthorizedExecutionRequest | None
    evidence: EvidenceLineage


class BenjaminControlPlane:
    """Evidence-required authority path from Epinnox recommendation to Hand authorization."""

    def __init__(self, publisher: EvidencePublisher) -> None:
        self._publisher = publisher

    def process(
        self,
        recommendation: Recommendation,
        *,
        recommendation_receipt_id: str,
        correlation_id: str,
        decision_status: DecisionStatus,
        decision_reason: str,
        risk_policy: RiskPolicy,
        quantity: Decimal | None = None,
    ) -> ControlPlaneResult:
        if not recommendation_receipt_id:
            raise ValueError("Epinnox recommendation must already have a Book receipt")
        if not correlation_id:
            raise ValueError("correlation_id is required")

        decision = decide(
            recommendation,
            status=decision_status,
            reason=decision_reason,
            quantity=quantity,
        )
        decision_receipt = self._publisher.publish(
            decision_draft(
                decision,
                correlation_id=correlation_id,
                causation_receipt_id=recommendation_receipt_id,
            )
        )

        risk = evaluate(decision, risk_policy)
        risk_receipt = self._publisher.publish(
            risk_draft(
                risk,
                correlation_id=correlation_id,
                causation_receipt_id=decision_receipt,
            )
        )

        authorization = None
        authorization_receipt = None
        if decision.status is not DecisionStatus.REJECTED and risk.status is RiskStatus.PASS:
            authorization = authorize(decision, risk)
            authorization_receipt = self._publisher.publish(
                authorization_draft(
                    authorization,
                    correlation_id=correlation_id,
                    causation_receipt_id=risk_receipt,
                )
            )

        return ControlPlaneResult(
            decision=decision,
            risk=risk,
            authorization=authorization,
            evidence=EvidenceLineage(
                recommendation_receipt_id=recommendation_receipt_id,
                decision_receipt_id=decision_receipt,
                risk_receipt_id=risk_receipt,
                authorization_receipt_id=authorization_receipt,
            ),
        )
