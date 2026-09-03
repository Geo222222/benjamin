from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple

from .capital_state import CapitalState

ZERO = Decimal("0")
ONE = Decimal("1")


class ProjectionScenarioKind(str, Enum):
    EXPECTED = "EXPECTED"
    ADVERSE = "ADVERSE"
    EXECUTION_STRESS = "EXECUTION_STRESS"


class ProjectionStatus(str, Enum):
    QUALIFIED = "QUALIFIED"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class ProjectionEvidenceRef:
    evidence_id: str
    evidence_kind: str
    observed_at: datetime
    known_at: datetime
    content_hash: str
    quality: ProjectionStatus = ProjectionStatus.QUALIFIED

    def __post_init__(self) -> None:
        if not self.evidence_id or not self.evidence_kind or not self.content_hash:
            raise ValueError("projection evidence identity is required")
        _aware("projection evidence observed_at", self.observed_at)
        _aware("projection evidence known_at", self.known_at)
        if self.known_at < self.observed_at:
            raise ValueError("projection evidence known_at cannot precede observed_at")
        _digest(self.content_hash, "projection evidence content_hash")

    def to_wire(self) -> dict[str, object]:
        return {
            "evidence_id": self.evidence_id,
            "evidence_kind": self.evidence_kind,
            "observed_at": self.observed_at.isoformat(),
            "known_at": self.known_at.isoformat(),
            "content_hash": self.content_hash,
            "quality": self.quality.value,
        }


@dataclass(frozen=True)
class ProjectedCapitalScenario:
    kind: ProjectionScenarioKind
    status: ProjectionStatus
    net_asset_value: Optional[Decimal]
    available_cash: Optional[Decimal]
    obligations_total: Optional[Decimal]
    gross_market_exposure: Optional[Decimal]
    derivative_gross_notional: Optional[Decimal]
    collateral_committed: Optional[Decimal]
    initial_margin: Optional[Decimal]
    maintenance_margin: Optional[Decimal]
    risk_budget_remaining: Optional[Decimal]
    drawdown_fraction: Optional[Decimal]
    evidence_refs: Tuple[ProjectionEvidenceRef, ...]
    missing_metrics: Tuple[str, ...] = ()
    path_constraint_breaches: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        metrics = self.metrics()
        if self.status is ProjectionStatus.QUALIFIED:
            missing = [name for name, value in metrics.items() if value is None]
            if missing:
                raise ValueError("qualified projected scenario is missing metrics: %s" % ", ".join(sorted(missing)))
            if self.missing_metrics:
                raise ValueError("qualified projected scenario cannot declare missing_metrics")
        if self.status is ProjectionStatus.UNAVAILABLE and any(value is not None for value in metrics.values()):
            raise ValueError("unavailable projected scenario must not publish partial numeric state")
        if len({item.evidence_id for item in self.evidence_refs}) != len(self.evidence_refs):
            raise ValueError("projection scenario evidence refs must be unique")
        if self.status is not ProjectionStatus.UNAVAILABLE and not self.evidence_refs:
            raise ValueError("available projected scenario requires evidence refs")
        _unique_strings(self.missing_metrics, "missing_metrics")
        _unique_strings(self.path_constraint_breaches, "path_constraint_breaches")

        non_negative = {
            "available_cash": self.available_cash,
            "obligations_total": self.obligations_total,
            "gross_market_exposure": self.gross_market_exposure,
            "derivative_gross_notional": self.derivative_gross_notional,
            "collateral_committed": self.collateral_committed,
            "initial_margin": self.initial_margin,
            "maintenance_margin": self.maintenance_margin,
            "risk_budget_remaining": self.risk_budget_remaining,
        }
        for name, value in non_negative.items():
            if value is not None and value < ZERO:
                raise ValueError("%s cannot be negative" % name)
        if self.drawdown_fraction is not None and not (ZERO <= self.drawdown_fraction <= ONE):
            raise ValueError("projected drawdown_fraction must be between 0 and 1")
        if (
            self.initial_margin is not None
            and self.maintenance_margin is not None
            and self.initial_margin > ZERO
            and self.maintenance_margin > self.initial_margin
        ):
            raise ValueError("projected maintenance_margin cannot exceed initial_margin")

    def metrics(self) -> dict[str, Optional[Decimal]]:
        return {
            "net_asset_value": self.net_asset_value,
            "available_cash": self.available_cash,
            "obligations_total": self.obligations_total,
            "gross_market_exposure": self.gross_market_exposure,
            "derivative_gross_notional": self.derivative_gross_notional,
            "collateral_committed": self.collateral_committed,
            "initial_margin": self.initial_margin,
            "maintenance_margin": self.maintenance_margin,
            "risk_budget_remaining": self.risk_budget_remaining,
            "drawdown_fraction": self.drawdown_fraction,
        }

    def to_wire(self) -> dict[str, object]:
        return {
            "kind": self.kind.value,
            "status": self.status.value,
            "metrics": {
                name: None if value is None else _d(value)
                for name, value in sorted(self.metrics().items())
            },
            "evidence_refs": [item.to_wire() for item in sorted(self.evidence_refs, key=lambda item: item.evidence_id)],
            "missing_metrics": list(sorted(set(self.missing_metrics))),
            "path_constraint_breaches": list(sorted(set(self.path_constraint_breaches))),
        }


@dataclass(frozen=True)
class ProjectedCapitalState:
    schema_version: str
    projection_id: str
    content_hash: str
    capital_structure_id: str
    base_capital_state_id: str
    base_capital_state_hash: str
    base_capital_state_as_of: datetime
    candidate_path_ref: str
    responsibility_ref: str
    projector_version: str
    known_at: datetime
    valid_until: datetime
    required_scenarios: Tuple[ProjectionScenarioKind, ...]
    scenarios: Tuple[ProjectedCapitalScenario, ...]

    def scenario(self, kind: ProjectionScenarioKind) -> ProjectedCapitalScenario:
        for item in self.scenarios:
            if item.kind is kind:
                return item
        raise KeyError(kind.value)

    def to_wire(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "projection_id": self.projection_id,
            "content_hash": self.content_hash,
            "capital_structure_id": self.capital_structure_id,
            "base_capital_state_id": self.base_capital_state_id,
            "base_capital_state_hash": self.base_capital_state_hash,
            "base_capital_state_as_of": self.base_capital_state_as_of.isoformat(),
            "candidate_path_ref": self.candidate_path_ref,
            "responsibility_ref": self.responsibility_ref,
            "projector_version": self.projector_version,
            "known_at": self.known_at.isoformat(),
            "valid_until": self.valid_until.isoformat(),
            "required_scenarios": [item.value for item in self.required_scenarios],
            "scenarios": [item.to_wire() for item in sorted(self.scenarios, key=lambda item: item.kind.value)],
            "truth_boundary": {
                "authoritative_capital_state": False,
                "may_advance_capital_state_pointer": False,
                "requires_post_execution_reconciliation": True,
            },
        }


def build_projected_capital_state(
    base_state: CapitalState,
    *,
    candidate_path_ref: str,
    responsibility_ref: str,
    projector_version: str,
    known_at: datetime,
    valid_until: datetime,
    scenarios: Tuple[ProjectedCapitalScenario, ...],
    required_scenarios: Tuple[ProjectionScenarioKind, ...] = (
        ProjectionScenarioKind.EXPECTED,
        ProjectionScenarioKind.ADVERSE,
        ProjectionScenarioKind.EXECUTION_STRESS,
    ),
) -> ProjectedCapitalState:
    """Create a content-addressed pro-forma capital projection.

    This object is explicitly not accounting truth. It may be used by Benjamin
    and Watchman for pre-action reasoning, but only a later reconciled Capital
    State may become authoritative after external execution.
    """

    if not candidate_path_ref or not responsibility_ref or not projector_version:
        raise ValueError("projection identity fields are required")
    _aware("projection known_at", known_at)
    _aware("projection valid_until", valid_until)
    if known_at < base_state.known_at:
        raise ValueError("projection cannot be known before its base Capital State")
    if valid_until <= known_at:
        raise ValueError("projection valid_until must be after known_at")
    if not scenarios:
        raise ValueError("Projected Capital State requires scenarios")
    if len({item.kind for item in scenarios}) != len(scenarios):
        raise ValueError("projected scenario kinds must be unique")
    if len(set(required_scenarios)) != len(required_scenarios):
        raise ValueError("required_scenarios must be unique")
    present = {item.kind for item in scenarios}
    missing_required = [item.value for item in required_scenarios if item not in present]
    if missing_required:
        raise ValueError("missing required projection scenarios: %s" % ", ".join(sorted(missing_required)))

    for scenario in scenarios:
        for evidence in scenario.evidence_refs:
            if evidence.observed_at > base_state.as_of and evidence.evidence_kind == "AUTHORITATIVE_CAPITAL_FACT":
                raise ValueError("projection cannot relabel post-base capital facts as known base truth")
            if evidence.known_at > known_at:
                raise ValueError("projection cannot consume evidence known after projection known_at")

    body = {
        "schema_version": "BENJAMIN.PROJECTED_CAPITAL_STATE.v1",
        "capital_structure_id": base_state.capital_structure_id,
        "base_capital_state_id": base_state.capital_state_id,
        "base_capital_state_hash": base_state.content_hash,
        "base_capital_state_as_of": base_state.as_of.isoformat(),
        "candidate_path_ref": candidate_path_ref,
        "responsibility_ref": responsibility_ref,
        "projector_version": projector_version,
        "known_at": known_at.isoformat(),
        "valid_until": valid_until.isoformat(),
        "required_scenarios": [item.value for item in required_scenarios],
        "scenarios": [item.to_wire() for item in sorted(scenarios, key=lambda item: item.kind.value)],
        "truth_boundary": {
            "authoritative_capital_state": False,
            "may_advance_capital_state_pointer": False,
            "requires_post_execution_reconciliation": True,
        },
    }
    content_hash = hashlib.sha256(_canonical(body)).hexdigest()
    projection_id = "PROJCAP-%s" % content_hash[:24]
    return ProjectedCapitalState(
        schema_version="BENJAMIN.PROJECTED_CAPITAL_STATE.v1",
        projection_id=projection_id,
        content_hash=content_hash,
        capital_structure_id=base_state.capital_structure_id,
        base_capital_state_id=base_state.capital_state_id,
        base_capital_state_hash=base_state.content_hash,
        base_capital_state_as_of=base_state.as_of,
        candidate_path_ref=candidate_path_ref,
        responsibility_ref=responsibility_ref,
        projector_version=projector_version,
        known_at=known_at,
        valid_until=valid_until,
        required_scenarios=required_scenarios,
        scenarios=scenarios,
    )


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _d(value: Decimal) -> str:
    return format(value, "f")


def _aware(name: str, value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("%s must be timezone-aware" % name)


def _digest(value: str, name: str) -> None:
    if len(value) != 64:
        raise ValueError("%s must be SHA-256 hex" % name)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError("%s must be SHA-256 hex" % name) from exc


def _unique_strings(values: Tuple[str, ...], name: str) -> None:
    if any(not item for item in values) or len(set(values)) != len(values):
        raise ValueError("%s must contain unique non-empty values" % name)
