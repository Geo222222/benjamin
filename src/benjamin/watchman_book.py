from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .authority import authorize
from .book_bridge import BenjaminBookSigner, BookBridgeError, canonical_json
from .book_outbox import BookOutbox
from .domain import AuthorizedExecutionRequest, InvestmentDecision, RiskDecision, RiskStatus
from .watchman import RiskPolicy, evaluate


class WatchmanBookError(ValueError):
    pass


class WatchmanBookSigner(BenjaminBookSigner):
    """Ed25519 signer restricted to Watchman's constitutional namespace.

    This class reuses only the Protocol v2 envelope mechanics. It must be
    instantiated with Watchman's own private key and can never sign BENJAMIN.*,
    ZLJ.*, or HAND.* evidence.
    """

    PRODUCER = "Watchman"
    PREFIX = "WATCHMAN."


class WatchmanBookOutbox(BookOutbox):
    """Durable outbox that accepts Watchman evidence and nothing else."""

    def __init__(self, root: Path) -> None:
        super().__init__(root, producer="Watchman", event_prefix="WATCHMAN.")


@dataclass(frozen=True, slots=True)
class WatchmanBookAttachment:
    risk: RiskDecision
    authorization: AuthorizedExecutionRequest | None
    payload: bytes
    envelope: dict[str, object]
    outbox_record: dict[str, Any]


def _require_aware(value: datetime, field: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise WatchmanBookError(f"{field} must be timezone-aware")


def _validate_authorization_matches(
    decision: InvestmentDecision,
    risk: RiskDecision,
    authorization: AuthorizedExecutionRequest,
) -> None:
    if authorization.decision_id != decision.decision_id:
        raise WatchmanBookError("authorization does not cover the Benjamin decision")
    if authorization.risk_id != risk.risk_id:
        raise WatchmanBookError("authorization does not cover this Watchman evaluation")
    if authorization.instrument != decision.instrument:
        raise WatchmanBookError("authorization instrument differs from Benjamin decision")
    if authorization.side is not decision.side:
        raise WatchmanBookError("authorization side differs from Benjamin decision")
    if authorization.quantity != decision.quantity:
        raise WatchmanBookError("authorization quantity differs from Benjamin decision")
    if authorization.issued_at != risk.checked_at:
        raise WatchmanBookError("authorization issuance must equal Watchman evaluation time")
    if authorization.expires_at <= risk.checked_at:
        raise WatchmanBookError("authorization must expire after Watchman evaluation")


def build_watchman_governance_payload(
    decision: InvestmentDecision,
    risk: RiskDecision,
    *,
    decision_receipt_id: str,
    policy_version: str,
    authorization: AuthorizedExecutionRequest | None = None,
    capability: str = "ORDER_EXECUTION",
) -> bytes:
    """Build the typed WATCHMAN.AUTHORIZATION/BLOCK payload.

    The payload reports deterministic governance truth. It does not execute the
    capability and does not grant Benjamin authority to speak for Watchman.
    """
    if not decision_receipt_id:
        raise WatchmanBookError("decision_receipt_id is required")
    if not policy_version:
        raise WatchmanBookError("policy_version is required")
    if risk.decision_id != decision.decision_id:
        raise WatchmanBookError("Watchman evaluation does not cover this Benjamin decision")
    _require_aware(decision.decided_at, "decision.decided_at")
    _require_aware(risk.checked_at, "risk.checked_at")

    check_status = "PASS" if risk.status is RiskStatus.PASS else "BLOCK"
    checks = [
        {"check_id": reason, "status": check_status, "reason": reason}
        for reason in risk.reasons
    ]

    constraints: dict[str, str] | None
    expires_at: str | None
    result: str
    if risk.status is RiskStatus.PASS:
        if authorization is None:
            raise WatchmanBookError("passing Watchman evaluation requires authorization constraints")
        if not capability:
            raise WatchmanBookError("capability is required for authorization")
        _validate_authorization_matches(decision, risk, authorization)
        result = "AUTHORIZE"
        constraints = {
            "capability": capability,
            "instrument": authorization.instrument,
            "side": authorization.side.value,
            "quantity": format(authorization.quantity, "f"),
            "idempotency_key": authorization.idempotency_key,
        }
        expires_at = authorization.expires_at.isoformat()
    else:
        if authorization is not None:
            raise WatchmanBookError("blocked Watchman evaluation cannot carry authorization")
        result = "BLOCK"
        constraints = None
        expires_at = None

    return canonical_json(
        {
            "schema_version": "1.0",
            "governance_id": risk.risk_id,
            "decision_receipt_id": decision_receipt_id,
            "decision_id": decision.decision_id,
            "result": result,
            "policy_version": policy_version,
            "checks": checks,
            "capability_constraints": constraints,
            "evaluated_at": risk.checked_at.isoformat(),
            "expires_at": expires_at,
        }
    )


def prepare_watchman_book_attachment(
    decision: InvestmentDecision,
    *,
    decision_receipt_id: str,
    risk_policy: RiskPolicy,
    policy_version: str,
    signer: WatchmanBookSigner,
    outbox: WatchmanBookOutbox,
    correlation_id: str | None = None,
    ttl_seconds: int = 300,
    now: datetime | None = None,
    produced_at: datetime | None = None,
    capability: str = "ORDER_EXECUTION",
) -> WatchmanBookAttachment:
    """Evaluate, sign, and persist one Watchman governance fact before delivery.

    A passing legacy B1 authorization is retained as the source of exact
    capability constraints during the transition. The signed v2 authority is
    WATCHMAN.AUTHORIZATION; a block is WATCHMAN.BLOCK. No Hand invocation occurs.
    """
    if not decision_receipt_id:
        raise WatchmanBookError("Benjamin decision must already have a Book receipt")
    risk = evaluate(decision, risk_policy, now=now)
    authorization: AuthorizedExecutionRequest | None = None
    if risk.status is RiskStatus.PASS:
        authorization = authorize(decision, risk, ttl_seconds=ttl_seconds, now=risk.checked_at)

    payload = build_watchman_governance_payload(
        decision,
        risk,
        decision_receipt_id=decision_receipt_id,
        policy_version=policy_version,
        authorization=authorization,
        capability=capability,
    )
    event_type = (
        "WATCHMAN.AUTHORIZATION" if risk.status is RiskStatus.PASS else "WATCHMAN.BLOCK"
    )
    receipt_id = f"BOOK-{risk.risk_id}"
    emitted_at = produced_at or risk.checked_at
    _require_aware(emitted_at, "produced_at")
    payload_digest = hashlib.sha256(payload).hexdigest()
    visibility_scope = (
        ("WATCHMAN_AUTHORITY", "HAND_VERIFIER", "BENJAMIN_AUDITOR")
        if risk.status is RiskStatus.PASS
        else ("WATCHMAN_AUTHORITY", "BENJAMIN_STEWARD", "BENJAMIN_AUDITOR")
    )
    envelope = signer.sign_v2_envelope(
        receipt_id=receipt_id,
        event_type=event_type,
        evidence_class="CONSTITUTIONAL",
        subject_id=risk.risk_id,
        occurred_at=risk.checked_at,
        known_at=risk.checked_at,
        produced_at=emitted_at,
        source_event_at=decision.decided_at,
        valid_from=risk.checked_at if risk.status is RiskStatus.PASS else None,
        valid_until=authorization.expires_at if authorization is not None else None,
        payload_digest=payload_digest,
        payload_ref=f"vault://watchman/governance/{risk.risk_id}",
        correlation_id=correlation_id,
        causation_receipt_id=decision_receipt_id,
        privacy_class="CONFIDENTIAL_EVIDENCE",
        visibility_scope=visibility_scope,
    )
    outbox_record = outbox.enqueue(envelope=envelope, payload=payload)
    return WatchmanBookAttachment(
        risk=risk,
        authorization=authorization,
        payload=payload,
        envelope=envelope,
        outbox_record=outbox_record,
    )


def load_watchman_book_signer_from_env(
    env: Mapping[str, str] | None = None,
) -> WatchmanBookSigner:
    """Load Watchman's key without accepting Benjamin's signing identity."""
    source = os.environ if env is None else env
    key_id = source.get("WATCHMAN_BOOK_KEY_ID", "")
    private_key_b64 = source.get("WATCHMAN_BOOK_ED25519_PRIVATE_KEY_B64", "")
    if not key_id or not private_key_b64:
        raise BookBridgeError(
            "Watchman Book signing is unavailable: WATCHMAN_BOOK_KEY_ID and "
            "WATCHMAN_BOOK_ED25519_PRIVATE_KEY_B64 are required"
        )

    benjamin_key_id = source.get("BENJAMIN_BOOK_KEY_ID")
    benjamin_private_key_b64 = source.get("BENJAMIN_BOOK_ED25519_PRIVATE_KEY_B64")
    if benjamin_key_id and benjamin_key_id == key_id:
        raise BookBridgeError("Watchman and Benjamin must use different Book key IDs")
    if benjamin_private_key_b64 and benjamin_private_key_b64 == private_key_b64:
        raise BookBridgeError("Watchman and Benjamin must use different Book private keys")

    return WatchmanBookSigner.from_private_key_b64(
        key_id=key_id,
        private_key_b64=private_key_b64,
    )
