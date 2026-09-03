from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .capital_state import CapitalState, CapitalStateInput, build_capital_state


@dataclass(frozen=True)
class ProjectionReceipt:
    capital_state_id: str
    capital_structure_id: str
    content_hash: str
    created_snapshot: bool
    advanced_current: bool
    event_hash: str | None


class CapitalStateProjectionStore:
    """Durable Benjamin-side projection of immutable Capital State snapshots.

    This store is not The Book and does not become institutional proof authority.
    It gives Benjamin a deterministic local materialization/cache whose snapshot
    identities can be referenced by decisions and later proven through The Book.
    """

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.snapshot_dir = self.root / "state" / "capital_states"
        self.current_path = self.root / "state" / "capital_state_current.json"
        self.journal_path = self.root / "memory" / "capital_state_projection.jsonl"
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.current_path.parent.mkdir(parents=True, exist_ok=True)
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)

    def persist(self, state: CapitalState) -> ProjectionReceipt:
        self._validate_identity(state)
        snapshot_path = self.snapshot_dir / f"{state.capital_state_id}.json"
        snapshot_bytes = _canonical(state.to_wire())
        created_snapshot = False

        if snapshot_path.exists():
            if snapshot_path.read_bytes() != snapshot_bytes:
                raise ValueError("existing Capital State snapshot does not match immutable content")
        else:
            with snapshot_path.open("xb") as handle:
                handle.write(snapshot_bytes)
                handle.write(b"\n")
            created_snapshot = True

        current = self._read_current_index()
        previous = current.get(state.capital_structure_id)
        advanced_current = self._should_advance_current(previous, state)

        # Re-persisting the exact current state is idempotent: no duplicate event.
        if (
            not created_snapshot
            and previous is not None
            and previous.get("capital_state_id") == state.capital_state_id
            and previous.get("content_hash") == state.content_hash
        ):
            return ProjectionReceipt(
                capital_state_id=state.capital_state_id,
                capital_structure_id=state.capital_structure_id,
                content_hash=state.content_hash,
                created_snapshot=False,
                advanced_current=False,
                event_hash=None,
            )

        event_hash = self._append_event(state, advanced_current=advanced_current)

        if advanced_current:
            current[state.capital_structure_id] = {
                "capital_state_id": state.capital_state_id,
                "content_hash": state.content_hash,
                "as_of": state.as_of.isoformat(),
                "known_at": state.known_at.isoformat(),
                "routing_readiness": state.routing_readiness.value,
            }
            self._write_current_index(current)

        return ProjectionReceipt(
            capital_state_id=state.capital_state_id,
            capital_structure_id=state.capital_structure_id,
            content_hash=state.content_hash,
            created_snapshot=created_snapshot,
            advanced_current=advanced_current,
            event_hash=event_hash,
        )

    def materialize(self, source: CapitalStateInput) -> tuple[CapitalState, ProjectionReceipt]:
        state = build_capital_state(source)
        return state, self.persist(state)

    def current_ref(self, capital_structure_id: str) -> dict[str, str] | None:
        current = self._read_current_index().get(capital_structure_id)
        if current is None:
            return None
        return dict(current)

    def current_wire(self, capital_structure_id: str) -> dict[str, object] | None:
        reference = self.current_ref(capital_structure_id)
        if reference is None:
            return None
        snapshot_path = self.snapshot_dir / f"{reference['capital_state_id']}.json"
        if not snapshot_path.exists():
            raise ValueError("current Capital State pointer references a missing snapshot")
        payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
        if payload.get("content_hash") != reference["content_hash"]:
            raise ValueError("current Capital State snapshot hash does not match pointer")
        return payload

    def verify_projection_chain(self) -> tuple[bool, tuple[str, ...]]:
        if not self.journal_path.exists():
            return True, ()

        errors: list[str] = []
        previous_hash = "GENESIS"
        for index, event in enumerate(self._journal_events(), start=1):
            claimed_previous = event.get("previous_event_hash")
            claimed_hash = event.get("event_hash")
            if claimed_previous != previous_hash:
                errors.append(f"event {index} previous hash mismatch")
            body = dict(event)
            body.pop("event_hash", None)
            expected_hash = hashlib.sha256(_canonical(body)).hexdigest()
            if claimed_hash != expected_hash:
                errors.append(f"event {index} content hash mismatch")
            previous_hash = str(claimed_hash)
        return not errors, tuple(errors)

    def _append_event(self, state: CapitalState, *, advanced_current: bool) -> str:
        previous_hash = "GENESIS"
        events = list(self._journal_events())
        if events:
            previous_hash = str(events[-1]["event_hash"])

        body = {
            "schema_version": "BENJAMIN.CAPITAL_STATE.PROJECTION_EVENT.v1",
            "capital_state_id": state.capital_state_id,
            "capital_structure_id": state.capital_structure_id,
            "content_hash": state.content_hash,
            "as_of": state.as_of.isoformat(),
            "known_at": state.known_at.isoformat(),
            "routing_readiness": state.routing_readiness.value,
            "advanced_current": advanced_current,
            "previous_event_hash": previous_hash,
        }
        event_hash = hashlib.sha256(_canonical(body)).hexdigest()
        event = dict(body)
        event["event_hash"] = event_hash
        with self.journal_path.open("ab") as handle:
            handle.write(_canonical(event))
            handle.write(b"\n")
        return event_hash

    def _journal_events(self) -> Iterable[dict[str, object]]:
        if not self.journal_path.exists():
            return ()
        events: list[dict[str, object]] = []
        with self.journal_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    events.append(json.loads(line))
        return tuple(events)

    def _read_current_index(self) -> dict[str, dict[str, str]]:
        if not self.current_path.exists():
            return {}
        payload = json.loads(self.current_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Capital State current index must be an object")
        return payload

    def _write_current_index(self, current: dict[str, dict[str, str]]) -> None:
        temporary = self.current_path.with_suffix(".tmp")
        temporary.write_bytes(_canonical(current) + b"\n")
        os.replace(temporary, self.current_path)

    @staticmethod
    def _should_advance_current(previous: dict[str, str] | None, state: CapitalState) -> bool:
        if previous is None:
            return True
        previous_known = previous.get("known_at")
        if previous_known is None:
            raise ValueError("current Capital State pointer is missing known_at")
        current_known = state.known_at.isoformat()
        if current_known > previous_known:
            return True
        if current_known < previous_known:
            return False
        if previous.get("content_hash") != state.content_hash:
            raise ValueError("conflicting Capital States share the same known_at cutoff")
        return False

    @staticmethod
    def _validate_identity(state: CapitalState) -> None:
        expected_id = f"CAPSTATE-{state.content_hash[:24]}"
        if state.capital_state_id != expected_id:
            raise ValueError("Capital State identity does not match content hash")


def _canonical(value: dict[str, object]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
