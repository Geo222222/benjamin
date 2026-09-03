from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Mapping, Optional, Tuple

from .capital_state import CapitalState, RoutingReadiness

ZERO = Decimal("0")
ONE = Decimal("1")


class WatchMode(str, Enum):
    LIVE = "LIVE"
    PRE_ACTION = "PRE_ACTION"


class WatchmanState(str, Enum):
    HEALTHY = "HEALTHY"
    WATCH = "WATCH"
    CONSTRAINED = "CONSTRAINED"
    CORRECTION_REQUIRED = "CORRECTION_REQUIRED"
    EMERGENCY = "EMERGENCY"


class ActionClass(str, Enum):
    RISK_INCREASING = "RISK_INCREASING"
    RISK_NEUTRAL = "RISK_NEUTRAL"
    RISK_REDUCING = "RISK_REDUCING"
    EMERGENCY_PROTECTIVE = "EMERGENCY_PROTECTIVE"


class DecisionValidityStatus(str, Enum):
    VALID = "VALID"
    DEGRADED = "DEGRADED"
    INVALIDATED = "INVALIDATED"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class DecisionValidityWatch:
    decision_id: str
    status: DecisionValidityStatus
    checked_at: datetime
    reason: str
    evidence_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.decision_id:
            raise ValueError("decision validity watch requires decision_id")
        if self.checked_at.tzinfo is None or self.checked_at.utcoffset() is None:
            raise ValueError("decision validity checked_at must be timezone-aware")
        if not self.reason:
            raise ValueError("decision validity watch requires a reason")


@dataclass(frozen=True)
class CapitalEnvelope:
    """Versioned deterministic boundary compiled from owner Responsibility.

    The envelope defines capital-safety thresholds. It does not decide trades,
    predict markets, or call The Hand. ZLJ may later supply trajectory/fragility
    evidence, but those observations remain separate from these hard boundaries.
    """

    capital_structure_id: str
    responsibility_ref: str
    version: str

    watch_drawdown_fraction: Decimal
    correction_drawdown_fraction: Decimal
    emergency_drawdown_fraction: Decimal

    watch_liquidity_coverage: Decimal = Decimal("1.25")
    correction_liquidity_coverage: Decimal = Decimal("1.00")
    emergency_liquidity_coverage: Decimal = Decimal("0.50")

    watch_gross_exposure_multiple: Optional[Decimal] = None
    correction_gross_exposure_multiple: Optional[Decimal] = None
    emergency_gross_exposure_multiple: Optional[Decimal] = None

    watch_derivative_notional_multiple: Optional[Decimal] = None
    correction_derivative_notional_multiple: Optional[Decimal] = None
    emergency_derivative_notional_multiple: Optional[Decimal] = None

    watch_collateral_multiple: Optional[Decimal] = None
    correction_collateral_multiple: Optional[Decimal] = None
    emergency_collateral_multiple: Optional[Decimal] = None

    def __post_init__(self) -> None:
        if not self.capital_structure_id or not self.responsibility_ref or not self.version:
            raise ValueError("capital envelope identity fields are required")
        _ordered_fraction_thresholds(
            "drawdown",
            self.watch_drawdown_fraction,
            self.correction_drawdown_fraction,
            self.emergency_drawdown_fraction,
        )
        _ordered_descending_positive_thresholds(
            "liquidity coverage",
            self.watch_liquidity_coverage,
            self.correction_liquidity_coverage,
            self.emergency_liquidity_coverage,
        )
        _ordered_optional_positive_thresholds(
            "gross exposure multiple",
            self.watch_gross_exposure_multiple,
            self.correction_gross_exposure_multiple,
            self.emergency_gross_exposure_multiple,
        )
        _ordered_optional_positive_thresholds(
            "derivative notional multiple",
            self.watch_derivative_notional_multiple,
            self.correction_derivative_notional_multiple,
            self.emergency_derivative_notional_multiple,
        )
        _ordered_optional_positive_thresholds(
            "collateral multiple",
            self.watch_collateral_multiple,
            self.correction_collateral_multiple,
            self.emergency_collateral_multiple,
        )

    def body(self) -> dict[str, object]:
        return {
            "schema_version": "WATCHMAN.CAPITAL_ENVELOPE.v1",
            "capital_structure_id": self.capital_structure_id,
            "responsibility_ref": self.responsibility_ref,
            "version": self.version,
            "drawdown": {
                "watch": _d(self.watch_drawdown_fraction),
                "correction": _d(self.correction_drawdown_fraction),
                "emergency": _d(self.emergency_drawdown_fraction),
            },
            "liquidity_coverage": {
                "watch": _d(self.watch_liquidity_coverage),
                "correction": _d(self.correction_liquidity_coverage),
                "emergency": _d(self.emergency_liquidity_coverage),
            },
            "gross_exposure_multiple": _threshold_group(
                self.watch_gross_exposure_multiple,
                self.correction_gross_exposure_multiple,
                self.emergency_gross_exposure_multiple,
            ),
            "derivative_notional_multiple": _threshold_group(
                self.watch_derivative_notional_multiple,
                self.correction_derivative_notional_multiple,
                self.emergency_derivative_notional_multiple,
            ),
            "collateral_multiple": _threshold_group(
                self.watch_collateral_multiple,
                self.correction_collateral_multiple,
                self.emergency_collateral_multiple,
            ),
        }

    def content_hash(self) -> str:
        return hashlib.sha256(_canonical(self.body())).hexdigest()

    @property
    def envelope_id(self) -> str:
        return "WATCHENV-%s" % self.content_hash()[:24]


@dataclass(frozen=True)
class CapitalRequirement:
    metric: str
    operator: str
    target: str
    current: str
    reason: str

    def __post_init__(self) -> None:
        if self.operator not in {"<=", ">="}:
            raise ValueError("capital requirement operator must be <= or >=")
        if not self.metric or not self.target or not self.current or not self.reason:
            raise ValueError("capital requirement fields must be non-empty")

    def to_wire(self) -> dict[str, str]:
        return {
            "metric": self.metric,
            "operator": self.operator,
            "target": self.target,
            "current": self.current,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class WatchmanAssessment:
    assessment_id: str
    content_hash: str
    mode: WatchMode
    capital_structure_id: str
    capital_state_id: str
    capital_state_hash: str
    capital_state_as_of: datetime
    envelope_id: str
    envelope_hash: str
    responsibility_ref: str
    state: WatchmanState
    reasons: Tuple[str, ...]
    requirements: Tuple[CapitalRequirement, ...]
    permitted_action_classes: Tuple[ActionClass, ...]
    emergency_directives: Tuple[str, ...]
    decision_validity: Optional[DecisionValidityWatch]
    assessed_at: datetime

    def to_wire(self) -> dict[str, object]:
        return {
            "schema_version": "WATCHMAN.CAPITAL_ASSESSMENT.v1",
            "assessment_id": self.assessment_id,
            "content_hash": self.content_hash,
            "mode": self.mode.value,
            "capital_structure_id": self.capital_structure_id,
            "capital_state_id": self.capital_state_id,
            "capital_state_hash": self.capital_state_hash,
            "capital_state_as_of": self.capital_state_as_of.isoformat(),
            "envelope_id": self.envelope_id,
            "envelope_hash": self.envelope_hash,
            "responsibility_ref": self.responsibility_ref,
            "state": self.state.value,
            "reasons": list(self.reasons),
            "requirements": [item.to_wire() for item in self.requirements],
            "permitted_action_classes": [item.value for item in self.permitted_action_classes],
            "emergency_directives": list(self.emergency_directives),
            "decision_validity": None
            if self.decision_validity is None
            else {
                "decision_id": self.decision_validity.decision_id,
                "status": self.decision_validity.status.value,
                "checked_at": self.decision_validity.checked_at.isoformat(),
                "reason": self.decision_validity.reason,
                "evidence_ref": self.decision_validity.evidence_ref,
            },
            "assessed_at": self.assessed_at.isoformat(),
        }


_STATE_RANK = {
    WatchmanState.HEALTHY: 0,
    WatchmanState.WATCH: 1,
    WatchmanState.CONSTRAINED: 2,
    WatchmanState.CORRECTION_REQUIRED: 3,
    WatchmanState.EMERGENCY: 4,
}


def assess_capital_state(
    capital_state: CapitalState,
    envelope: CapitalEnvelope,
    *,
    assessed_at: datetime,
    mode: WatchMode = WatchMode.LIVE,
    decision_validity: Optional[DecisionValidityWatch] = None,
) -> WatchmanAssessment:
    """Continuously evaluate actual or projected capital against its envelope.

    For `LIVE`, `capital_state` must be authoritative current capital truth.
    `PRE_ACTION` is reserved for a separately produced projected-state contract;
    callers must not relabel speculative dictionaries as CapitalState. Until a
    projected-state type is implemented, this mode is only a classification tag.
    """

    if assessed_at.tzinfo is None or assessed_at.utcoffset() is None:
        raise ValueError("watchman assessed_at must be timezone-aware")
    if capital_state.capital_structure_id != envelope.capital_structure_id:
        raise ValueError("capital envelope does not belong to this Capital Structure")
    if assessed_at < capital_state.known_at:
        raise ValueError("Watchman cannot assess before Capital State was knowable")
    if decision_validity is not None and decision_validity.checked_at > assessed_at:
        raise ValueError("Watchman cannot consume future decision-validity evidence")

    state = WatchmanState.HEALTHY
    reasons: list[str] = []
    requirements: list[CapitalRequirement] = []

    def escalate(target: WatchmanState, reason: str) -> None:
        nonlocal state
        if _STATE_RANK[target] > _STATE_RANK[state]:
            state = target
        reasons.append(reason)

    if capital_state.net_asset_value <= ZERO:
        escalate(WatchmanState.EMERGENCY, "NON_POSITIVE_NET_ASSET_VALUE")
        requirements.append(
            CapitalRequirement(
                metric="net_asset_value",
                operator=">=",
                target="POSITIVE",
                current=_d(capital_state.net_asset_value),
                reason="RESTORE_POSITIVE_EQUITY_OR_CLOSE_STRUCTURE",
            )
        )

    if capital_state.routing_readiness is RoutingReadiness.BLOCKED:
        if "NON_POSITIVE_NET_ASSET_VALUE" in capital_state.readiness_reasons:
            escalate(WatchmanState.EMERGENCY, "CAPITAL_STATE_ROUTING_BLOCKED")
        else:
            escalate(WatchmanState.CONSTRAINED, "CAPITAL_STATE_ROUTING_BLOCKED")
    elif capital_state.routing_readiness is RoutingReadiness.DEFENSIVE_ONLY:
        escalate(WatchmanState.CONSTRAINED, "CAPITAL_STATE_DEFENSIVE_ONLY")

    drawdown = capital_state.current_drawdown_fraction
    if drawdown >= envelope.emergency_drawdown_fraction:
        escalate(WatchmanState.EMERGENCY, "DRAWDOWN_EMERGENCY_BOUNDARY")
        requirements.append(
            CapitalRequirement(
                metric="current_drawdown_fraction",
                operator="<=",
                target=_d(envelope.correction_drawdown_fraction),
                current=_d(drawdown),
                reason="RESTORE_DRAWDOWN_INSIDE_CORRECTION_BOUNDARY",
            )
        )
    elif drawdown >= envelope.correction_drawdown_fraction:
        escalate(WatchmanState.CORRECTION_REQUIRED, "DRAWDOWN_CORRECTION_BOUNDARY")
        requirements.append(
            CapitalRequirement(
                metric="current_drawdown_fraction",
                operator="<=",
                target=_d(envelope.watch_drawdown_fraction),
                current=_d(drawdown),
                reason="REDUCE_CAPITAL_RISK",
            )
        )
    elif drawdown >= envelope.watch_drawdown_fraction:
        escalate(WatchmanState.WATCH, "DRAWDOWN_WATCH_BOUNDARY")

    obligations = (
        capital_state.operational_reserve
        + capital_state.minimum_liquidity_required
        + capital_state.pending_redemptions
        + capital_state.pending_withdrawals
        + capital_state.pending_distributions
    )
    liquidity_coverage = None if obligations <= ZERO else capital_state.available_cash / obligations
    if liquidity_coverage is not None:
        if liquidity_coverage <= envelope.emergency_liquidity_coverage:
            escalate(WatchmanState.EMERGENCY, "LIQUIDITY_COVERAGE_EMERGENCY")
            requirements.append(
                CapitalRequirement(
                    metric="liquidity_coverage",
                    operator=">=",
                    target=_d(envelope.correction_liquidity_coverage),
                    current=_d(liquidity_coverage),
                    reason="RESTORE_OBLIGATION_COVERAGE",
                )
            )
        elif liquidity_coverage <= envelope.correction_liquidity_coverage:
            escalate(WatchmanState.CORRECTION_REQUIRED, "LIQUIDITY_COVERAGE_CORRECTION")
            requirements.append(
                CapitalRequirement(
                    metric="liquidity_coverage",
                    operator=">=",
                    target=_d(envelope.watch_liquidity_coverage),
                    current=_d(liquidity_coverage),
                    reason="RAISE_LIQUIDITY_OR_REDUCE_COMMITMENTS",
                )
            )
        elif liquidity_coverage <= envelope.watch_liquidity_coverage:
            escalate(WatchmanState.WATCH, "LIQUIDITY_COVERAGE_WATCH")

    nav = capital_state.net_asset_value
    if nav > ZERO:
        gross_multiple = capital_state.gross_market_exposure / nav
        state = _apply_upper_multiple(
            state,
            reasons,
            requirements,
            metric="gross_market_exposure_multiple",
            current=gross_multiple,
            watch=envelope.watch_gross_exposure_multiple,
            correction=envelope.correction_gross_exposure_multiple,
            emergency=envelope.emergency_gross_exposure_multiple,
        )
        derivative_multiple = capital_state.derivative_gross_notional / nav
        state = _apply_upper_multiple(
            state,
            reasons,
            requirements,
            metric="derivative_notional_multiple",
            current=derivative_multiple,
            watch=envelope.watch_derivative_notional_multiple,
            correction=envelope.correction_derivative_notional_multiple,
            emergency=envelope.emergency_derivative_notional_multiple,
        )
        collateral_multiple = capital_state.collateral_committed / nav
        state = _apply_upper_multiple(
            state,
            reasons,
            requirements,
            metric="collateral_multiple",
            current=collateral_multiple,
            watch=envelope.watch_collateral_multiple,
            correction=envelope.correction_collateral_multiple,
            emergency=envelope.emergency_collateral_multiple,
        )

    if capital_state.risk_budget_remaining <= ZERO:
        escalate(WatchmanState.CONSTRAINED, "NO_RISK_BUDGET_REMAINING")

    if decision_validity is not None:
        if decision_validity.status is DecisionValidityStatus.INVALIDATED:
            escalate(WatchmanState.CORRECTION_REQUIRED, "ACTIVE_DECISION_INVALIDATED")
            requirements.append(
                CapitalRequirement(
                    metric="active_decision_validity",
                    operator=">=",
                    target="REASSESSED_OR_CLOSED",
                    current="INVALIDATED",
                    reason="BENJAMIN_MUST_REASSESS_POSITION_PATH",
                )
            )
        elif decision_validity.status in {DecisionValidityStatus.DEGRADED, DecisionValidityStatus.UNAVAILABLE}:
            escalate(WatchmanState.WATCH, "ACTIVE_DECISION_VALIDITY_%s" % decision_validity.status.value)

    reasons = list(dict.fromkeys(reasons)) or ["CAPITAL_INSIDE_ENVELOPE"]
    requirements = _unique_requirements(requirements)
    permitted = _permitted_actions(state)
    emergency = _emergency_directives(state)

    body = {
        "schema_version": "WATCHMAN.CAPITAL_ASSESSMENT.v1",
        "mode": mode.value,
        "capital_structure_id": capital_state.capital_structure_id,
        "capital_state_id": capital_state.capital_state_id,
        "capital_state_hash": capital_state.content_hash,
        "capital_state_as_of": capital_state.as_of.isoformat(),
        "envelope_id": envelope.envelope_id,
        "envelope_hash": envelope.content_hash(),
        "responsibility_ref": envelope.responsibility_ref,
        "state": state.value,
        "reasons": reasons,
        "requirements": [item.to_wire() for item in requirements],
        "permitted_action_classes": [item.value for item in permitted],
        "emergency_directives": list(emergency),
        "decision_validity": None
        if decision_validity is None
        else {
            "decision_id": decision_validity.decision_id,
            "status": decision_validity.status.value,
            "checked_at": decision_validity.checked_at.isoformat(),
            "reason": decision_validity.reason,
            "evidence_ref": decision_validity.evidence_ref,
        },
        "assessed_at": assessed_at.isoformat(),
    }
    content_hash = hashlib.sha256(_canonical(body)).hexdigest()
    return WatchmanAssessment(
        assessment_id="WATCH-%s" % content_hash[:24],
        content_hash=content_hash,
        mode=mode,
        capital_structure_id=capital_state.capital_structure_id,
        capital_state_id=capital_state.capital_state_id,
        capital_state_hash=capital_state.content_hash,
        capital_state_as_of=capital_state.as_of,
        envelope_id=envelope.envelope_id,
        envelope_hash=envelope.content_hash(),
        responsibility_ref=envelope.responsibility_ref,
        state=state,
        reasons=tuple(reasons),
        requirements=tuple(requirements),
        permitted_action_classes=permitted,
        emergency_directives=emergency,
        decision_validity=decision_validity,
        assessed_at=assessed_at,
    )


def _apply_upper_multiple(
    current_state: WatchmanState,
    reasons: list[str],
    requirements: list[CapitalRequirement],
    *,
    metric: str,
    current: Decimal,
    watch: Optional[Decimal],
    correction: Optional[Decimal],
    emergency: Optional[Decimal],
) -> WatchmanState:
    state = current_state

    def escalate(target: WatchmanState, reason: str) -> None:
        nonlocal state
        if _STATE_RANK[target] > _STATE_RANK[state]:
            state = target
        reasons.append(reason)

    token = metric.upper()
    if emergency is not None and current >= emergency:
        escalate(WatchmanState.EMERGENCY, "%s_EMERGENCY" % token)
        requirements.append(
            CapitalRequirement(
                metric=metric,
                operator="<=",
                target=_d(correction if correction is not None else emergency),
                current=_d(current),
                reason="RESTORE_%s" % token,
            )
        )
    elif correction is not None and current >= correction:
        escalate(WatchmanState.CORRECTION_REQUIRED, "%s_CORRECTION" % token)
        requirements.append(
            CapitalRequirement(
                metric=metric,
                operator="<=",
                target=_d(watch if watch is not None else correction),
                current=_d(current),
                reason="REDUCE_%s" % token,
            )
        )
    elif watch is not None and current >= watch:
        escalate(WatchmanState.WATCH, "%s_WATCH" % token)
    return state


def _permitted_actions(state: WatchmanState) -> Tuple[ActionClass, ...]:
    if state in {WatchmanState.HEALTHY, WatchmanState.WATCH}:
        return (
            ActionClass.RISK_INCREASING,
            ActionClass.RISK_NEUTRAL,
            ActionClass.RISK_REDUCING,
        )
    if state is WatchmanState.CONSTRAINED:
        return (ActionClass.RISK_NEUTRAL, ActionClass.RISK_REDUCING)
    if state is WatchmanState.CORRECTION_REQUIRED:
        return (ActionClass.RISK_NEUTRAL, ActionClass.RISK_REDUCING)
    return (ActionClass.RISK_REDUCING, ActionClass.EMERGENCY_PROTECTIVE)


def _emergency_directives(state: WatchmanState) -> Tuple[str, ...]:
    if state is not WatchmanState.EMERGENCY:
        return ()
    return (
        "FREEZE_NEW_RISK",
        "CANCEL_RISK_INCREASING_ORDERS",
        "REDUCE_TO_SAFE_EXPOSURE",
        "CLOSE_LIQUIDATION_THREATENED_POSITION",
        "RESTORE_MINIMUM_COLLATERAL_BUFFER",
    )


def _unique_requirements(values: list[CapitalRequirement]) -> list[CapitalRequirement]:
    output: list[CapitalRequirement] = []
    seen: set[tuple[str, str, str, str, str]] = set()
    for item in values:
        key = (item.metric, item.operator, item.target, item.current, item.reason)
        if key not in seen:
            seen.add(key)
            output.append(item)
    return output


def _threshold_group(
    watch: Optional[Decimal],
    correction: Optional[Decimal],
    emergency: Optional[Decimal],
) -> Mapping[str, Optional[str]]:
    return {
        "watch": None if watch is None else _d(watch),
        "correction": None if correction is None else _d(correction),
        "emergency": None if emergency is None else _d(emergency),
    }


def _ordered_fraction_thresholds(name: str, watch: Decimal, correction: Decimal, emergency: Decimal) -> None:
    if not (ZERO <= watch <= correction <= emergency <= ONE):
        raise ValueError("%s thresholds must satisfy 0 <= watch <= correction <= emergency <= 1" % name)


def _ordered_descending_positive_thresholds(
    name: str,
    watch: Decimal,
    correction: Decimal,
    emergency: Decimal,
) -> None:
    if not (watch > ZERO and correction > ZERO and emergency > ZERO):
        raise ValueError("%s thresholds must be positive" % name)
    if not (watch >= correction >= emergency):
        raise ValueError("%s thresholds must satisfy watch >= correction >= emergency" % name)


def _ordered_optional_positive_thresholds(
    name: str,
    watch: Optional[Decimal],
    correction: Optional[Decimal],
    emergency: Optional[Decimal],
) -> None:
    values = (watch, correction, emergency)
    if all(value is None for value in values):
        return
    if any(value is None for value in values):
        raise ValueError("%s thresholds must be all configured or all omitted" % name)
    assert watch is not None and correction is not None and emergency is not None
    if not (watch > ZERO and correction > ZERO and emergency > ZERO):
        raise ValueError("%s thresholds must be positive" % name)
    if not (watch <= correction <= emergency):
        raise ValueError("%s thresholds must satisfy watch <= correction <= emergency" % name)


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _d(value: Decimal) -> str:
    return format(value, "f")
