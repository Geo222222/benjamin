from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

from .domain import AuthorizedExecutionRequest, InvestmentDecision, RiskDecision
from .watchman_capital import WatchmanAssessment


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


def watchman_capital_assessment_draft(
    assessment: WatchmanAssessment,
    *,
    correlation_id: str,
    causation_receipt_id: str,
) -> EvidenceDraft:
    """Minimum-necessary Book testimony for a material Watchman state change.

    The payload binds the exact Capital State and Capital Envelope hashes used by
    Watchman. It deliberately does not copy account credentials, provider raw
    payloads, or ZLJ market histories into The Book.
    """

    wire = assessment.to_wire()
    payload = _canonical(
        {
            "schema_version": wire["schema_version"],
            "assessment_id": assessment.assessment_id,
            "content_hash": assessment.content_hash,
            "mode": assessment.mode.value,
            "capital_structure_id": assessment.capital_structure_id,
            "capital_state_id": assessment.capital_state_id,
            "capital_state_hash": assessment.capital_state_hash,
            "capital_state_as_of": assessment.capital_state_as_of.isoformat(),
            "envelope_id": assessment.envelope_id,
            "envelope_hash": assessment.envelope_hash,
            "responsibility_ref": assessment.responsibility_ref,
            "state": assessment.state.value,
            "reasons": list(assessment.reasons),
            "requirements": [item.to_wire() for item in assessment.requirements],
            "permitted_action_classes": [item.value for item in assessment.permitted_action_classes],
            "emergency_directives": list(assessment.emergency_directives),
            "decision_validity": wire["decision_validity"],
            "assessed_at": assessment.assessed_at.isoformat(),
        }
    )
    return EvidenceDraft(
        event_type="WATCHMAN.CAPITAL_ASSESSMENT",
        evidence_class="ECONOMIC",
        privacy_class="CONFIDENTIAL_EVIDENCE",
        visibility_scope=("BENJAMIN_STEWARD", "BENJAMIN_WATCHMAN", "BENJAMIN_AUDITOR", "BOOK_AUDITOR"),
        subject_id=assessment.assessment_id,
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
