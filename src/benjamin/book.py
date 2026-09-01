from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class BookEntry:
    index: int
    event_type: str
    subject_id: str
    payload: dict[str, Any]
    recorded_at: str
    previous_hash: str
    entry_hash: str


class Book:
    """Small in-memory hash chain proving append-only semantics for B0."""

    def __init__(self) -> None:
        self._entries: list[BookEntry] = []

    @property
    def entries(self) -> tuple[BookEntry, ...]:
        return tuple(self._entries)

    def append(self, event_type: str, subject_id: str, payload: dict[str, Any]) -> BookEntry:
        if not event_type or not subject_id:
            raise ValueError("event_type and subject_id are required")

        previous_hash = self._entries[-1].entry_hash if self._entries else "GENESIS"
        recorded_at = datetime.now(timezone.utc).isoformat()
        material = {
            "index": len(self._entries),
            "event_type": event_type,
            "subject_id": subject_id,
            "payload": payload,
            "recorded_at": recorded_at,
            "previous_hash": previous_hash,
        }
        canonical = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
        entry_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        entry = BookEntry(entry_hash=entry_hash, **material)
        self._entries.append(entry)
        return entry

    def correct(self, prior: BookEntry, reason: str, replacement: dict[str, Any]) -> BookEntry:
        if prior not in self._entries:
            raise ValueError("correction target must already exist in The Book")
        return self.append(
            "CORRECTION",
            prior.subject_id,
            {
                "corrects_entry_hash": prior.entry_hash,
                "reason": reason,
                "replacement": replacement,
            },
        )

    def verify(self) -> bool:
        for i, entry in enumerate(self._entries):
            expected_previous = self._entries[i - 1].entry_hash if i else "GENESIS"
            if entry.previous_hash != expected_previous:
                return False
            material = asdict(entry)
            material.pop("entry_hash")
            canonical = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
            if hashlib.sha256(canonical.encode("utf-8")).hexdigest() != entry.entry_hash:
                return False
        return True
