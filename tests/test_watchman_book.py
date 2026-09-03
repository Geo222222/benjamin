import base64
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from benjamin import DecisionStatus, OrderSide, Recommendation, RiskPolicy, decide
from benjamin.book_bridge import BookBridgeError
from benjamin.book_outbox import ACKNOWLEDGED, PENDING, BookOutboxError
from benjamin.watchman_book import (
    WatchmanBookOutbox,
    WatchmanBookSigner,
    load_watchman_book_signer_from_env,
    prepare_watchman_book_attachment,
)


NOW = datetime(2026, 9, 2, 23, 45, tzinfo=timezone.utc)


def recommendation(quantity: str = "3") -> Recommendation:
    return Recommendation(
        recommendation_id="REC-WATCH-001",
        fund_id="FIRSTFRUITS",
        instrument="BTC-USD",
        side=OrderSide.BUY,
        quantity=Decimal(quantity),
        thesis_ref="BOOK-ZLJ-001",
        created_at=NOW,
    )


def approved_decision(quantity: str = "3"):
    return decide(
        recommendation(quantity),
        status=DecisionStatus.APPROVED,
        reason="within mandate",
        now=NOW,
    )


def private_key_b64(key: Ed25519PrivateKey) -> str:
    raw = key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return base64.b64encode(raw).decode("ascii")


class FailingTransport:
    def append_idempotent(self, *, envelope, payload):
        raise ConnectionError("Book unavailable")


class AcceptingTransport:
    def append_idempotent(self, *, envelope, payload):
        return {
            "receipt_id": envelope["receipt_id"],
            "sequence": 7,
            "entry_hash": "a" * 64,
            "recorded_at": "2026-09-02T23:46:00Z",
            "accepted": True,
            "duplicate_replay": False,
        }


def test_watchman_identity_owns_only_watchman_namespace() -> None:
    signer = WatchmanBookSigner(key_id="watchman-k1", private_key=Ed25519PrivateKey.generate())
    identity = signer.public_identity
    assert identity.producer == "Watchman"
    assert identity.allowed_event_prefixes == ("WATCHMAN.",)

    with pytest.raises(BookBridgeError):
        signer.sign_v2_envelope(
            receipt_id="FORGED-1",
            event_type="BENJAMIN.DECISION",
            evidence_class="ECONOMIC",
            subject_id="DEC-1",
            occurred_at=NOW,
            known_at=NOW,
            produced_at=NOW,
            payload_digest="0" * 64,
        )


@pytest.mark.parametrize("event_type", ["ZLJ.INTELLIGENCE", "HAND.EXECUTION"])
def test_watchman_cannot_impersonate_other_organs(event_type: str) -> None:
    signer = WatchmanBookSigner(key_id="watchman-k1", private_key=Ed25519PrivateKey.generate())
    with pytest.raises(BookBridgeError):
        signer.sign_v2_envelope(
            receipt_id="FORGED-2",
            event_type=event_type,
            evidence_class="CONSTITUTIONAL",
            subject_id="GOV-1",
            occurred_at=NOW,
            known_at=NOW,
            produced_at=NOW,
            payload_digest="0" * 64,
        )


def test_watchman_loader_requires_its_own_runtime_key() -> None:
    benjamin_key = Ed25519PrivateKey.generate()
    with pytest.raises(BookBridgeError, match="WATCHMAN_BOOK_KEY_ID"):
        load_watchman_book_signer_from_env(
            {
                "BENJAMIN_BOOK_KEY_ID": "benjamin-k1",
                "BENJAMIN_BOOK_ED25519_PRIVATE_KEY_B64": private_key_b64(benjamin_key),
            }
        )


def test_watchman_loader_rejects_benjamin_key_reuse() -> None:
    shared = private_key_b64(Ed25519PrivateKey.generate())
    with pytest.raises(BookBridgeError, match="different Book private keys"):
        load_watchman_book_signer_from_env(
            {
                "BENJAMIN_BOOK_KEY_ID": "benjamin-k1",
                "BENJAMIN_BOOK_ED25519_PRIVATE_KEY_B64": shared,
                "WATCHMAN_BOOK_KEY_ID": "watchman-k1",
                "WATCHMAN_BOOK_ED25519_PRIVATE_KEY_B64": shared,
            }
        )


def test_pass_creates_watchman_authorization_with_exact_constraints(tmp_path: Path) -> None:
    signer = WatchmanBookSigner(key_id="watchman-k1", private_key=Ed25519PrivateKey.generate())
    outbox = WatchmanBookOutbox(tmp_path)
    decision = approved_decision("3")
    attachment = prepare_watchman_book_attachment(
        decision,
        decision_receipt_id="BOOK-BEN-001",
        risk_policy=RiskPolicy(
            allowed_instruments=frozenset({"BTC-USD"}),
            max_order_quantity=Decimal("10"),
        ),
        policy_version="watchman-b0-v1",
        signer=signer,
        outbox=outbox,
        correlation_id="LIFE-001",
        now=NOW,
    )

    payload = json.loads(attachment.payload)
    assert attachment.risk.status.value == "PASS"
    assert attachment.authorization is not None
    assert attachment.envelope["producer"] == "Watchman"
    assert attachment.envelope["event_type"] == "WATCHMAN.AUTHORIZATION"
    assert attachment.envelope["causation_receipt_id"] == "BOOK-BEN-001"
    assert attachment.envelope["subject_id"] == attachment.risk.risk_id
    assert attachment.envelope["valid_until"] == attachment.authorization.expires_at.isoformat()
    assert payload["decision_receipt_id"] == "BOOK-BEN-001"
    assert payload["decision_id"] == decision.decision_id
    assert payload["result"] == "AUTHORIZE"
    assert payload["capability_constraints"] == {
        "capability": "ORDER_EXECUTION",
        "instrument": "BTC-USD",
        "side": "BUY",
        "quantity": "3",
        "idempotency_key": attachment.authorization.idempotency_key,
    }
    assert all(check["status"] == "PASS" for check in payload["checks"])
    assert attachment.outbox_record["state"] == PENDING
    assert attachment.outbox_record["producer"] == "Watchman"


def test_block_creates_no_executable_capability(tmp_path: Path) -> None:
    signer = WatchmanBookSigner(key_id="watchman-k1", private_key=Ed25519PrivateKey.generate())
    decision = approved_decision("11")
    attachment = prepare_watchman_book_attachment(
        decision,
        decision_receipt_id="BOOK-BEN-002",
        risk_policy=RiskPolicy(
            allowed_instruments=frozenset({"BTC-USD"}),
            max_order_quantity=Decimal("10"),
        ),
        policy_version="watchman-b0-v1",
        signer=signer,
        outbox=WatchmanBookOutbox(tmp_path),
        now=NOW,
    )

    payload = json.loads(attachment.payload)
    assert attachment.risk.status.value == "BLOCK"
    assert attachment.authorization is None
    assert attachment.envelope["event_type"] == "WATCHMAN.BLOCK"
    assert attachment.envelope["causation_receipt_id"] == "BOOK-BEN-002"
    assert attachment.envelope["valid_until"] is None
    assert payload["result"] == "BLOCK"
    assert payload["capability_constraints"] is None
    assert payload["expires_at"] is None
    assert any(check["status"] == "BLOCK" for check in payload["checks"])


def test_watchman_outbox_rejects_benjamin_envelope(tmp_path: Path) -> None:
    payload = b"decision"
    with pytest.raises(BookOutboxError):
        WatchmanBookOutbox(tmp_path).enqueue(
            envelope={
                "receipt_id": "BEN-1",
                "producer": "Benjamin",
                "event_type": "BENJAMIN.DECISION",
                "privacy_class": "CONFIDENTIAL_EVIDENCE",
                "payload_digest": __import__("hashlib").sha256(payload).hexdigest(),
            },
            payload=payload,
        )


def test_watchman_outbox_retries_exact_signed_evidence(tmp_path: Path) -> None:
    signer = WatchmanBookSigner(key_id="watchman-k1", private_key=Ed25519PrivateKey.generate())
    outbox = WatchmanBookOutbox(tmp_path)
    attachment = prepare_watchman_book_attachment(
        approved_decision("2"),
        decision_receipt_id="BOOK-BEN-003",
        risk_policy=RiskPolicy(allowed_instruments=frozenset({"BTC-USD"})),
        policy_version="watchman-b0-v1",
        signer=signer,
        outbox=outbox,
        now=NOW,
    )
    receipt_id = str(attachment.envelope["receipt_id"])
    original_digest = attachment.outbox_record["envelope_digest"]

    failed = outbox.deliver_one(receipt_id, FailingTransport())
    assert failed["state"] == PENDING
    assert failed["envelope_digest"] == original_digest
    assert failed["attempt_count"] == 1

    accepted = outbox.deliver_one(receipt_id, AcceptingTransport())
    assert accepted["state"] == ACKNOWLEDGED
    assert accepted["envelope_digest"] == original_digest
    assert accepted["attempt_count"] == 2
    assert accepted["book_receipt"]["sequence"] == 7
