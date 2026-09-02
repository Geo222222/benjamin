import hashlib
from pathlib import Path

import pytest

from benjamin.book_outbox import ACKNOWLEDGED, PENDING, BookOutbox, OutboxConflict


class FailingTransport:
    def append_idempotent(self, *, envelope, payload):
        raise ConnectionError("Book unavailable")


class AcceptingTransport:
    def append_idempotent(self, *, envelope, payload):
        return {
            "receipt_id": envelope["receipt_id"],
            "sequence": 11,
            "entry_hash": "b" * 64,
            "recorded_at": "2026-09-02T19:00:00Z",
            "accepted": True,
            "duplicate_replay": False,
        }


def envelope(payload: bytes) -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "receipt_id": "BEN-R1",
        "producer": "Benjamin",
        "producer_key_id": "benjamin-k1",
        "event_type": "BENJAMIN.DECISION",
        "privacy_class": "CONFIDENTIAL_EVIDENCE",
        "payload_digest": hashlib.sha256(payload).hexdigest(),
        "signature": "signed",
    }


def test_transient_failure_is_not_silently_dropped(tmp_path: Path) -> None:
    outbox = BookOutbox(tmp_path)
    payload = b"decision"
    original = outbox.enqueue(envelope=envelope(payload), payload=payload)

    failed = outbox.deliver_one("BEN-R1", FailingTransport())
    assert failed["state"] == PENDING
    assert failed["attempt_count"] == 1
    assert failed["envelope_digest"] == original["envelope_digest"]
    assert outbox.pending_receipt_ids() == ("BEN-R1",)

    accepted = outbox.deliver_one("BEN-R1", AcceptingTransport())
    assert accepted["state"] == ACKNOWLEDGED
    assert accepted["attempt_count"] == 2
    assert accepted["book_receipt"]["sequence"] == 11
    assert outbox.pending_receipt_ids() == ()


def test_receipt_id_cannot_change_meaning(tmp_path: Path) -> None:
    outbox = BookOutbox(tmp_path)
    first = b"one"
    outbox.enqueue(envelope=envelope(first), payload=first)
    second = b"two"
    with pytest.raises(OutboxConflict):
        outbox.enqueue(envelope=envelope(second), payload=second)
