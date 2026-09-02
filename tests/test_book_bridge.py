import base64
from datetime import datetime, timezone

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from benjamin.book_bridge import BenjaminBookSigner, BookBridgeError, canonical_json


NOW = datetime(2026, 9, 2, 18, 50, tzinfo=timezone.utc)


def test_public_identity_reserves_only_benjamin_namespace() -> None:
    signer = BenjaminBookSigner(key_id="benjamin-k1", private_key=Ed25519PrivateKey.generate())
    identity = signer.public_identity
    assert identity.producer == "Benjamin"
    assert identity.key_id == "benjamin-k1"
    assert identity.allowed_event_prefixes == ("BENJAMIN.",)
    assert identity.public_key_b64


def test_v2_decision_signature_verifies_with_public_identity() -> None:
    signer = BenjaminBookSigner(key_id="benjamin-k1", private_key=Ed25519PrivateKey.generate())
    envelope = signer.sign_v2_envelope(
        receipt_id="BEN-R1",
        event_type="BENJAMIN.DECISION",
        evidence_class="ECONOMIC",
        subject_id="DEC-001",
        occurred_at=NOW,
        known_at=NOW,
        produced_at=NOW,
        valid_until=NOW,
        payload_digest="0" * 64,
        payload_ref="vault://benjamin/decisions/DEC-001",
        causation_receipt_id="ZLJ-R1",
    )
    signature = base64.b64decode(str(envelope.pop("signature")), validate=True)
    public_bytes = base64.b64decode(signer.public_identity.public_key_b64, validate=True)
    Ed25519PublicKey.from_public_bytes(public_bytes).verify(signature, canonical_json(envelope))


@pytest.mark.parametrize("event_type", ["ZLJ.INTELLIGENCE", "WATCHMAN.AUTHORIZATION", "HAND.EXECUTION"])
def test_benjamin_signer_cannot_impersonate_other_organs(event_type: str) -> None:
    signer = BenjaminBookSigner(key_id="benjamin-k1", private_key=Ed25519PrivateKey.generate())
    with pytest.raises(BookBridgeError):
        signer.sign_v2_envelope(
            receipt_id="FORGED-R1",
            event_type=event_type,
            evidence_class="ECONOMIC",
            subject_id="FORGED-001",
            occurred_at=NOW,
            known_at=NOW,
            produced_at=NOW,
            payload_digest="0" * 64,
        )


def test_private_key_material_is_not_exposed() -> None:
    signer = BenjaminBookSigner(key_id="benjamin-k1", private_key=Ed25519PrivateKey.generate())
    identity = signer.public_identity.wire()
    assert "private_key" not in identity
    assert "private_key_b64" not in identity
