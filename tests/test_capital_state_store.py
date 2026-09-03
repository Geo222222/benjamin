from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json

import pytest

from benjamin import (
    CapitalSourceRef,
    CapitalStateInput,
    CapitalStateProjectionStore,
    ReconciliationStatus,
    SourceQuality,
    ValuationPolicyRef,
)

BASE = datetime(2026, 9, 3, 21, 0, tzinfo=timezone.utc)


def make_input(*, seconds=0, cash="100", known_seconds=None, risk_budget="50") -> CapitalStateInput:
    as_of = BASE + timedelta(seconds=seconds)
    known_at = BASE + timedelta(seconds=seconds if known_seconds is None else known_seconds)
    src = CapitalSourceRef(
        source_id=f"SRC-{seconds}",
        source_kind="CUSTODIAN_ACCOUNT_SNAPSHOT",
        account_id="ACC-001",
        observed_at=as_of,
        known_at=known_at,
        content_hash=(f"{seconds:064d}")[-64:],
        quality=SourceQuality.VALID,
    )
    return CapitalStateInput(
        capital_structure_id="CAP-001",
        base_currency="USD",
        as_of=as_of,
        known_at=known_at,
        valuation_policy=ValuationPolicyRef("VAL-001", "1", "v" * 64),
        account_ids=("ACC-001",),
        source_refs=(src,),
        reconciliation_status=ReconciliationStatus.RECONCILED,
        cash_balance=Decimal(cash),
        available_cash=Decimal(cash),
        participant_equity=Decimal(cash),
        risk_budget_remaining=Decimal(risk_budget),
    )


def test_materialize_persists_immutable_snapshot_and_current_pointer(tmp_path) -> None:
    store = CapitalStateProjectionStore(tmp_path)
    state, receipt = store.materialize(make_input())

    assert receipt.created_snapshot is True
    assert receipt.advanced_current is True
    assert receipt.event_hash is not None
    assert (store.snapshot_dir / f"{state.capital_state_id}.json").exists()
    assert store.current_ref("CAP-001")["capital_state_id"] == state.capital_state_id
    assert store.current_wire("CAP-001")["content_hash"] == state.content_hash
    assert store.verify_projection_chain() == (True, ())


def test_duplicate_materialization_is_idempotent(tmp_path) -> None:
    store = CapitalStateProjectionStore(tmp_path)
    first_state, first = store.materialize(make_input())
    second_state, second = store.materialize(make_input())

    assert first_state == second_state
    assert first.event_hash is not None
    assert second.created_snapshot is False
    assert second.advanced_current is False
    assert second.event_hash is None
    lines = store.journal_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1


def test_newer_state_advances_current_pointer(tmp_path) -> None:
    store = CapitalStateProjectionStore(tmp_path)
    older, _ = store.materialize(make_input(seconds=0, cash="100"))
    newer, receipt = store.materialize(make_input(seconds=5, cash="125"))

    assert receipt.advanced_current is True
    assert store.current_ref("CAP-001")["capital_state_id"] == newer.capital_state_id
    assert older.capital_state_id != newer.capital_state_id
    assert store.verify_projection_chain() == (True, ())


def test_historical_state_is_preserved_without_rewinding_current(tmp_path) -> None:
    store = CapitalStateProjectionStore(tmp_path)
    newer, _ = store.materialize(make_input(seconds=5, cash="125"))
    older, receipt = store.materialize(make_input(seconds=0, cash="100"))

    assert receipt.created_snapshot is True
    assert receipt.advanced_current is False
    assert (store.snapshot_dir / f"{older.capital_state_id}.json").exists()
    assert store.current_ref("CAP-001")["capital_state_id"] == newer.capital_state_id
    assert store.verify_projection_chain() == (True, ())


def test_conflicting_states_at_same_known_at_fail_closed(tmp_path) -> None:
    store = CapitalStateProjectionStore(tmp_path)
    store.materialize(make_input(seconds=0, cash="100"))
    with pytest.raises(ValueError, match="conflicting Capital States"):
        store.materialize(make_input(seconds=0, cash="101"))


def test_snapshot_tamper_is_detected_on_replay(tmp_path) -> None:
    store = CapitalStateProjectionStore(tmp_path)
    state, _ = store.materialize(make_input())
    path = store.snapshot_dir / f"{state.capital_state_id}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["cash_balance"] = "999999"
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")), encoding="utf-8")

    with pytest.raises(ValueError, match="immutable content"):
        store.persist(state)


def test_current_pointer_missing_snapshot_fails_closed(tmp_path) -> None:
    store = CapitalStateProjectionStore(tmp_path)
    state, _ = store.materialize(make_input())
    (store.snapshot_dir / f"{state.capital_state_id}.json").unlink()
    with pytest.raises(ValueError, match="missing snapshot"):
        store.current_wire("CAP-001")


def test_projection_journal_tamper_is_detected(tmp_path) -> None:
    store = CapitalStateProjectionStore(tmp_path)
    store.materialize(make_input(seconds=0))
    store.materialize(make_input(seconds=2, cash="120"))

    lines = store.journal_path.read_text(encoding="utf-8").splitlines()
    event = json.loads(lines[0])
    event["routing_readiness"] = "BLOCKED"
    lines[0] = json.dumps(event, sort_keys=True, separators=(",", ":"))
    store.journal_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    valid, errors = store.verify_projection_chain()
    assert valid is False
    assert any("content hash mismatch" in error for error in errors)
    assert any("previous hash mismatch" in error for error in errors)
