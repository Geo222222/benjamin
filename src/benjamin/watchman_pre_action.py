from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple

from .capital_state import CapitalState
from .projected_capital_state import (
    ProjectedCapitalScenario,
    ProjectedCapitalState,
    ProjectionScenarioKind,
    ProjectionStatus,
)
from .watchman_capital import ActionClass, CapitalEnvelope, CapitalRequirement, WatchmanState

ZERO = Decimal("0")

_STATE_RANK = {
    WatchmanState.HEALTHY: 0,
    WatchmanState.WATCH: 1,
    WatchmanState.CONSTRAINED: 2,
    WatchmanState.CORRECTION_REQUIRED: 3,
    WatchmanState.EMERGENCY: 4,
}


@dataclass(frozen=True)
class ProjectedScenarioAssessment:
    scenario_kind: ProjectionScenarioKind
    projection_status: ProjectionStatus
    state: WatchmanState
    reasons: Tuple[str, ...]
    requirements: Tuple[CapitalRequirement, ...]

    def to_wire(self) -> dict[str, object]:
        return {
            "scenario_kind": self.scenario_kind.value,
            "projection_status": self.projection_status.value,
            "state": self.state.value,
            "reasons": list(self.reasons),
            "requirements": [item.to_wire() for item in self.requirements],
        }


@dataclass(frozen=True)
class PreActionWatchmanAssessment:
    assessment_id: str
    content_hash: str
    capital_structure_id: str
    base_capital_state_id: str
    base_capital_state_hash: str
    projection_id: str
    projection_hash: str
    candidate_path_ref: str
    candidate_action_class: ActionClass
    envelope_id: str
    envelope_hash: str
    responsibility_ref: str
    state: WatchmanState
    candidate_permitted: bool
    permitted_action_classes: Tuple[ActionClass, ...]
    reasons: Tuple[str, ...]
    requirements: Tuple[CapitalRequirement, ...]
    scenario_assessments: Tuple[ProjectedScenarioAssessment, ...]
    assessed_at: datetime

    def to_wire(self) -> dict[str, object]:
        return {
            "schema_version": "WATCHMAN.PRE_ACTION_ASSESSMENT.v1",
            "assessment_id": self.assessment_id,
            "content_hash": self.content_hash,
            "capital_structure_id": self.capital_structure_id,
            "base_capital_state_id": self.base_capital_state_id,
            "base_capital_state_hash": self.base_capital_state_hash,
            "projection_id": self.projection_id,
            "projection_hash": self.projection_hash,
            "candidate_path_ref": self.candidate_path_ref,
            "candidate_action_class": self.candidate_action_class.value,
            "envelope_id": self.envelope_id,
            "envelope_hash": self.envelope_hash,
            "responsibility_ref": self.responsibility_ref,
            "state": self.state.value,
            "candidate_permitted": self.candidate_permitted,
            "permitted_action_classes": [item.value for item in self.permitted_action_classes],
            "reasons": list(self.reasons),
            "requirements": [item.to_wire() for item in self.requirements],
            "scenario_assessments": [
                item.to_wire() for item in sorted(self.scenario_assessments, key=lambda item: item.scenario_kind.value)
            ],
            "assessed_at": self.assessed_at.isoformat(),
            "truth_boundary": {
                "authoritative_capital_state": False,
                "execution_authorization": False,
                "hand_instruction": False,
            },
        }


def assess_projected_capital_state(
    base_state: CapitalState,
    projection: ProjectedCapitalState,
    envelope: CapitalEnvelope,
    *,
    candidate_action_class: ActionClass,
    assessed_at: datetime,
) -> PreActionWatchmanAssessment:
    """Evaluate every required projected scenario against one Capital Envelope.

    The worst justified required-scenario result governs the candidate path.
    This is a capital-safety assessment, not execution authorization. Missing or
    degraded required scenarios fail closed against new risk while preserving
    separately classified risk-reducing paths.
    """

    _aware("pre-action assessed_at", assessed_at)
    if assessed_at < projection.known_at:
        raise ValueError("Watchman cannot assess a projection before it was knowable")
    if assessed_at >= projection.valid_until:
        raise ValueError("Projected Capital State is expired")
    if base_state.capital_structure_id != projection.capital_structure_id:
        raise ValueError("projection Capital Structure differs from base Capital State")
    if envelope.capital_structure_id != projection.capital_structure_id:
        raise ValueError("Capital Envelope differs from projected Capital Structure")
    if envelope.responsibility_ref != projection.responsibility_ref:
        raise ValueError("projection Responsibility differs from Capital Envelope")
    if base_state.capital_state_id != projection.base_capital_state_id:
        raise ValueError("projection base Capital State id is no longer current")
    if base_state.content_hash != projection.base_capital_state_hash:
        raise ValueError("projection base Capital State hash is no longer current")

    required = tuple(projection.required_scenarios)
    if not required:
        raise ValueError("pre-action assessment requires projected scenarios")

    scenario_results = tuple(
        _assess_scenario(projection.scenario(kind), envelope)
        for kind in required
    )
    overall_state = max(
        (item.state for item in scenario_results),
        key=lambda item: _STATE_RANK[item],
    )
    permitted = _permitted_actions(overall_state)
    candidate_permitted = candidate_action_class in permitted

    reasons: list[str] = []
    requirements: list[CapitalRequirement] = []
    for item in scenario_results:
        for reason in item.reasons:
            reasons.append("%s:%s" % (item.scenario_kind.value, reason))
        requirements.extend(item.requirements)
    if not candidate_permitted:
        reasons.append("CANDIDATE_ACTION_CLASS_NOT_PERMITTED")
    reasons = list(dict.fromkeys(reasons)) or ["ALL_REQUIRED_SCENARIOS_INSIDE_CAPITAL_ENVELOPE"]
    requirements = _unique_requirements(requirements)

    body = {
        "schema_version": "WATCHMAN.PRE_ACTION_ASSESSMENT.v1",
        "capital_structure_id": projection.capital_structure_id,
        "base_capital_state_id": base_state.capital_state_id,
        "base_capital_state_hash": base_state.content_hash,
        "projection_id": projection.projection_id,
        "projection_hash": projection.content_hash,
        "candidate_path_ref": projection.candidate_path_ref,
        "candidate_action_class": candidate_action_class.value,
        "envelope_id": envelope.envelope_id,
        "envelope_hash": envelope.content_hash(),
        "responsibility_ref": envelope.responsibility_ref,
        "state": overall_state.value,
        "candidate_permitted": candidate_permitted,
        "permitted_action_classes": [item.value for item in permitted],
        "reasons": reasons,
        "requirements": [item.to_wire() for item in requirements],
        "scenario_assessments": [
            item.to_wire() for item in sorted(scenario_results, key=lambda item: item.scenario_kind.value)
        ],
        "assessed_at": assessed_at.isoformat(),
        "truth_boundary": {
            "authoritative_capital_state": False,
            "execution_authorization": False,
            "hand_instruction": False,
        },
    }
    content_hash = hashlib.sha256(_canonical(body)).hexdigest()
    return PreActionWatchmanAssessment(
        assessment_id="WATCHPRE-%s" % content_hash[:24],
        content_hash=content_hash,
        capital_structure_id=projection.capital_structure_id,
        base_capital_state_id=base_state.capital_state_id,
        base_capital_state_hash=base_state.content_hash,
        projection_id=projection.projection_id,
        projection_hash=projection.content_hash,
        candidate_path_ref=projection.candidate_path_ref,
        candidate_action_class=candidate_action_class,
        envelope_id=envelope.envelope_id,
        envelope_hash=envelope.content_hash(),
        responsibility_ref=envelope.responsibility_ref,
        state=overall_state,
        candidate_permitted=candidate_permitted,
        permitted_action_classes=permitted,
        reasons=tuple(reasons),
        requirements=tuple(requirements),
        scenario_assessments=scenario_results,
        assessed_at=assessed_at,
    )


def _assess_scenario(
    scenario: ProjectedCapitalScenario,
    envelope: CapitalEnvelope,
) -> ProjectedScenarioAssessment:
    state = WatchmanState.HEALTHY
    reasons: list[str] = []
    requirements: list[CapitalRequirement] = []

    def escalate(target: WatchmanState, reason: str) -> None:
        nonlocal state
        if _STATE_RANK[target] > _STATE_RANK[state]:
            state = target
        reasons.append(reason)

    if scenario.status is ProjectionStatus.UNAVAILABLE:
        escalate(WatchmanState.CONSTRAINED, "REQUIRED_SCENARIO_UNAVAILABLE")
        return ProjectedScenarioAssessment(
            scenario_kind=scenario.kind,
            projection_status=scenario.status,
            state=state,
            reasons=tuple(reasons),
            requirements=(),
        )
    if scenario.status is ProjectionStatus.DEGRADED:
        escalate(WatchmanState.CONSTRAINED, "REQUIRED_SCENARIO_DEGRADED")
    if scenario.missing_metrics:
        escalate(WatchmanState.CONSTRAINED, "REQUIRED_SAFETY_METRICS_MISSING")

    nav = scenario.net_asset_value
    if nav is not None and nav <= ZERO:
        escalate(WatchmanState.EMERGENCY, "NON_POSITIVE_PROJECTED_NET_ASSET_VALUE")
        requirements.append(
            CapitalRequirement(
                metric="net_asset_value",
                operator=">=",
                target="POSITIVE",
                current=_d(nav),
                reason="PROJECTED_STATE_MUST_PRESERVE_POSITIVE_EQUITY",
            )
        )

    drawdown = scenario.drawdown_fraction
    if drawdown is not None:
        if drawdown >= envelope.emergency_drawdown_fraction:
            escalate(WatchmanState.EMERGENCY, "PROJECTED_DRAWDOWN_EMERGENCY")
            requirements.append(
                CapitalRequirement(
                    metric="drawdown_fraction",
                    operator="<=",
                    target=_d(envelope.correction_drawdown_fraction),
                    current=_d(drawdown),
                    reason="PROJECTED_DRAWDOWN_MUST_RETURN_INSIDE_CORRECTION_BOUNDARY",
                )
            )
        elif drawdown >= envelope.correction_drawdown_fraction:
            escalate(WatchmanState.CORRECTION_REQUIRED, "PROJECTED_DRAWDOWN_CORRECTION")
            requirements.append(
                CapitalRequirement(
                    metric="drawdown_fraction",
                    operator="<=",
                    target=_d(envelope.watch_drawdown_fraction),
                    current=_d(drawdown),
                    reason="PROJECTED_DRAWDOWN_EXCEEDS_ACCEPTABLE_PATH",
                )
            )
        elif drawdown >= envelope.watch_drawdown_fraction:
            escalate(WatchmanState.WATCH, "PROJECTED_DRAWDOWN_WATCH")

    obligations = scenario.obligations_total
    cash = scenario.available_cash
    if obligations is not None and cash is not None and obligations > ZERO:
        coverage = cash / obligations
        if coverage <= envelope.emergency_liquidity_coverage:
            escalate(WatchmanState.EMERGENCY, "PROJECTED_LIQUIDITY_EMERGENCY")
            requirements.append(
                CapitalRequirement(
                    metric="liquidity_coverage",
                    operator=">=",
                    target=_d(envelope.correction_liquidity_coverage),
                    current=_d(coverage),
                    reason="PROJECTED_PATH_MUST_RESTORE_OBLIGATION_COVERAGE",
                )
            )
        elif coverage <= envelope.correction_liquidity_coverage:
            escalate(WatchmanState.CORRECTION_REQUIRED, "PROJECTED_LIQUIDITY_CORRECTION")
            requirements.append(
                CapitalRequirement(
                    metric="liquidity_coverage",
                    operator=">=",
                    target=_d(envelope.watch_liquidity_coverage),
                    current=_d(coverage),
                    reason="PROJECTED_PATH_DOES_NOT_PRESERVE_LIQUIDITY",
                )
            )
        elif coverage <= envelope.watch_liquidity_coverage:
            escalate(WatchmanState.WATCH, "PROJECTED_LIQUIDITY_WATCH")

    if nav is not None and nav > ZERO:
        state = _upper_multiple(
            state,
            reasons,
            requirements,
            metric="gross_market_exposure_multiple",
            current=None if scenario.gross_market_exposure is None else scenario.gross_market_exposure / nav,
            watch=envelope.watch_gross_exposure_multiple,
            correction=envelope.correction_gross_exposure_multiple,
            emergency=envelope.emergency_gross_exposure_multiple,
        )
        state = _upper_multiple(
            state,
            reasons,
            requirements,
            metric="derivative_notional_multiple",
            current=None if scenario.derivative_gross_notional is None else scenario.derivative_gross_notional / nav,
            watch=envelope.watch_derivative_notional_multiple,
            correction=envelope.correction_derivative_notional_multiple,
            emergency=envelope.emergency_derivative_notional_multiple,
        )
        state = _upper_multiple(
            state,
            reasons,
            requirements,
            metric="collateral_multiple",
            current=None if scenario.collateral_committed is None else scenario.collateral_committed / nav,
            watch=envelope.watch_collateral_multiple,
            correction=envelope.correction_collateral_multiple,
            emergency=envelope.emergency_collateral_multiple,
        )

    if scenario.risk_budget_remaining is not None and scenario.risk_budget_remaining <= ZERO:
        escalate(WatchmanState.CONSTRAINED, "PROJECTED_NO_RISK_BUDGET_REMAINING")

    return ProjectedScenarioAssessment(
        scenario_kind=scenario.kind,
        projection_status=scenario.status,
        state=state,
        reasons=tuple(dict.fromkeys(reasons)) or ("SCENARIO_INSIDE_CAPITAL_ENVELOPE",),
        requirements=tuple(_unique_requirements(requirements)),
    )


def _upper_multiple(
    current_state: WatchmanState,
    reasons: list[str],
    requirements: list[CapitalRequirement],
    *,
    metric: str,
    current: Optional[Decimal],
    watch: Optional[Decimal],
    correction: Optional[Decimal],
    emergency: Optional[Decimal],
) -> WatchmanState:
    state = current_state
    if current is None or watch is None or correction is None or emergency is None:
        return state
    token = metric.upper()
    if current >= emergency:
        state = _max_state(state, WatchmanState.EMERGENCY)
        reasons.append("PROJECTED_%s_EMERGENCY" % token)
        requirements.append(
            CapitalRequirement(
                metric=metric,
                operator="<=",
                target=_d(correction),
                current=_d(current),
                reason="PROJECTED_PATH_MUST_RESTORE_%s" % token,
            )
        )
    elif current >= correction:
        state = _max_state(state, WatchmanState.CORRECTION_REQUIRED)
        reasons.append("PROJECTED_%s_CORRECTION" % token)
        requirements.append(
            CapitalRequirement(
                metric=metric,
                operator="<=",
                target=_d(watch),
                current=_d(current),
                reason="PROJECTED_PATH_EXCEEDS_%s" % token,
            )
        )
    elif current >= watch:
        state = _max_state(state, WatchmanState.WATCH)
        reasons.append("PROJECTED_%s_WATCH" % token)
    return state


def _permitted_actions(state: WatchmanState) -> Tuple[ActionClass, ...]:
    if state in {WatchmanState.HEALTHY, WatchmanState.WATCH}:
        return (
            ActionClass.RISK_INCREASING,
            ActionClass.RISK_NEUTRAL,
            ActionClass.RISK_REDUCING,
        )
    if state in {WatchmanState.CONSTRAINED, WatchmanState.CORRECTION_REQUIRED}:
        return (ActionClass.RISK_NEUTRAL, ActionClass.RISK_REDUCING)
    return (ActionClass.RISK_REDUCING, ActionClass.EMERGENCY_PROTECTIVE)


def _max_state(left: WatchmanState, right: WatchmanState) -> WatchmanState:
    return left if _STATE_RANK[left] >= _STATE_RANK[right] else right


def _unique_requirements(values: list[CapitalRequirement]) -> list[CapitalRequirement]:
    result: list[CapitalRequirement] = []
    seen: set[tuple[str, str, str, str, str]] = set()
    for item in values:
        key = (item.metric, item.operator, item.target, item.current, item.reason)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _d(value: Decimal) -> str:
    return format(value, "f")


def _aware(name: str, value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("%s must be timezone-aware" % name)
