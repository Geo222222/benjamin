from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

from .domain import AuthorizedExecutionRequest, InvestmentDecision, RiskDecision


@dataclass(frozen=True)
class EvidenceDraft:
    """Producer-side draft for the private Big Book evidence gateway.

    `payload` is producer-side source material used by the publisher to create or
    verify a digest. The Big Book must not persist these raw bytes merely because
    they were supplied to the gateway.
    """

    event_type: str
    evidence_class: str
    privacy_class: str
    visibility_scope: tuple[str, ...]
    subject_id: str
    payload: bytes
    payload_ref: str | None
    correlation_id: str
    causation_receipt_id: str | None


class EvidencePublisher(Protocol):
    """Private Big Book producer gateway implemented by a signer/vault adapter."""

    def publish(self, draft: EvidenceDraft) -> str: ...


def _canonical(value: dict[str, object]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def decision_draft(
    decision: InvestmentDecision,
    *,
    correlation_id: str,
    causation_receipt_id: str,
) -> EvidenceDraft:
    payload = _canonical(
        {
            "decision_id": decision.decision_id,
            "recommendation_id": decision.recommendation_id,
            "fund_id": decision.fund_id,
            "instrument": decision.instrument,
            "side": decision.side.value,
            "quantity": format(decision.quantity, "f"),
            "status": decision.status.value,
            "reason": decision.reason,
            "decided_at": decision.decided_at.isoformat(),
        }
    )
    return EvidenceDraft(
        event_type="BENJAMIN.DECISION",
        evidence_class="ECONOMIC",
        privacy_class="CONFIDENTIAL_EVIDENCE",
        visibility_scope=("BENJAMIN_STEWARD", "BENJAMIN_WATCHMAN", "BENJAMIN_AUDITOR"),
        subject_id=decision.decision_id,
        payload=payload,
        payload_ref=None,
        correlation_id=correlation_id,
        causation_receipt_id=causation_receipt_id,
    )


def risk_draft(
    risk: RiskDecision,
    *,
    correlation_id: str,
    causation_receipt_id: str,
) -> EvidenceDraft:
    payload = _canonical(
        {
            "risk_id": risk.risk_id,
            "decision_id": risk.decision_id,
            "status": risk.status.value,
            "reasons": list(risk.reasons),
            "checked_at": risk.checked_at.isoformat(),
        }
    )
    return EvidenceDraft(
        event_type="BENJAMIN.RISK",
        evidence_class="ECONOMIC",
        privacy_class="CONFIDENTIAL_EVIDENCE",
        visibility_scope=("BENJAMIN_WATCHMAN", "BENJAMIN_AUTHORITY", "BENJAMIN_AUDITOR"),
        subject_id=risk.risk_id,
        payload=payload,
        payload_ref=None,
        correlation_id=correlation_id,
        causation_receipt_id=causation_receipt_id,
    )


def authorization_draft(
    request: AuthorizedExecutionRequest,
    *,
    correlation_id: str,
    causation_receipt_id: str,
) -> EvidenceDraft:
    return EvidenceDraft(
        event_type="BENJAMIN.AUTHORIZATION",
        evidence_class="ECONOMIC",
        privacy_class="CONFIDENTIAL_EVIDENCE",
        visibility_scope=("BENJAMIN_AUTHORITY", "HAND_VERIFIER", "BENJAMIN_AUDITOR"),
        subject_id=request.authorization_id,
        payload=_canonical(request.to_wire()),
        payload_ref=None,
        correlation_id=correlation_id,
        causation_receipt_id=causation_receipt_id,
    )
