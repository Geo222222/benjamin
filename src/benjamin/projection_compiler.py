from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple

from .candidate_path import CandidateEconomicPath
from .capital_state import CapitalState
from .projected_capital_state import (
    ProjectedCapitalScenario,
    ProjectedCapitalState,
    ProjectionEvidenceRef,
    ProjectionScenarioKind,
    ProjectionStatus,
    build_projected_capital_state,
)

ZERO = Decimal("0")
ONE = Decimal("1")


class ProjectionCompilerError(ValueError):
    pass


@dataclass(frozen=True)
class ScenarioCapitalEffect:
    schema_version: str
    effect_id: str
    content_hash: str
    candidate_path_id: str
    candidate_path_hash: str
    scenario_kind: ProjectionScenarioKind
    status: ProjectionStatus
    base_currency: str
    estimator_version: str
    known_at: datetime
    evidence_refs: Tuple[ProjectionEvidenceRef, ...]
    market_pnl_change_base: Optional[Decimal]
    execution_cost_base: Optional[Decimal]
    financing_cost_base: Optional[Decimal]
    available_cash_delta_before_costs_base: Optional[Decimal]
    obligations_delta_base: Optional[Decimal]
    gross_market_exposure_delta_base: Optional[Decimal]
    derivative_notional_delta_base: Optional[Decimal]
    collateral_delta_base: Optional[Decimal]
    initial_margin_delta_base: Optional[Decimal]
    maintenance_margin_delta_base: Optional[Decimal]
    risk_budget_remaining_delta_base: Optional[Decimal]
    projected_drawdown_fraction: Optional[Decimal]
    projected_notional_change_base: Optional[Decimal]
    capital_commitment_base: Optional[Decimal]
    missing_effects: Tuple[str, ...] = ()

    def to_wire(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "effect_id": self.effect_id,
            "content_hash": self.content_hash,
            "candidate_path_id": self.candidate_path_id,
            "candidate_path_hash": self.candidate_path_hash,
            "scenario_kind": self.scenario_kind.value,
            "status": self.status.value,
            "base_currency": self.base_currency,
            "estimator_version": self.estimator_version,
            "known_at": self.known_at.isoformat(),
            "evidence_refs": [item.to_wire() for item in sorted(self.evidence_refs, key=lambda item: item.evidence_id)],
            "effects": {
                "market_pnl_change_base": _optional_d(self.market_pnl_change_base),
                "execution_cost_base": _optional_d(self.execution_cost_base),
                "financing_cost_base": _optional_d(self.financing_cost_base),
                "available_cash_delta_before_costs_base": _optional_d(self.available_cash_delta_before_costs_base),
                "obligations_delta_base": _optional_d(self.obligations_delta_base),
                "gross_market_exposure_delta_base": _optional_d(self.gross_market_exposure_delta_base),
                "derivative_notional_delta_base": _optional_d(self.derivative_notional_delta_base),
                "collateral_delta_base": _optional_d(self.collateral_delta_base),
                "initial_margin_delta_base": _optional_d(self.initial_margin_delta_base),
                "maintenance_margin_delta_base": _optional_d(self.maintenance_margin_delta_base),
                "risk_budget_remaining_delta_base": _optional_d(self.risk_budget_remaining_delta_base),
                "projected_drawdown_fraction": _optional_d(self.projected_drawdown_fraction),
                "projected_notional_change_base": _optional_d(self.projected_notional_change_base),
                "capital_commitment_base": _optional_d(self.capital_commitment_base),
            },
            "missing_effects": list(sorted(set(self.missing_effects))),
            "unit_boundary": {
                "economic_amount_unit": "BASE_CURRENCY_VALUE_OR_NOTIONAL",
                "provider_native_quantity": False,
                "contract_count": False,
                "lot_size": False,
            },
        }


def build_scenario_capital_effect(
    path: CandidateEconomicPath,
    *,
    scenario_kind: ProjectionScenarioKind,
    status: ProjectionStatus,
    estimator_version: str,
    known_at: datetime,
    evidence_refs: Tuple[ProjectionEvidenceRef, ...],
    market_pnl_change_base: Optional[Decimal],
    execution_cost_base: Optional[Decimal],
    financing_cost_base: Optional[Decimal],
    available_cash_delta_before_costs_base: Optional[Decimal],
    obligations_delta_base: Optional[Decimal],
    gross_market_exposure_delta_base: Optional[Decimal],
    derivative_notional_delta_base: Optional[Decimal],
    collateral_delta_base: Optional[Decimal],
    initial_margin_delta_base: Optional[Decimal],
    maintenance_margin_delta_base: Optional[Decimal],
    risk_budget_remaining_delta_base: Optional[Decimal],
    projected_drawdown_fraction: Optional[Decimal],
    projected_notional_change_base: Optional[Decimal],
    capital_commitment_base: Optional[Decimal],
    missing_effects: Tuple[str, ...] = (),
) -> ScenarioCapitalEffect:
    if not estimator_version:
        raise ProjectionCompilerError("scenario effect estimator_version is required")
    _aware("scenario effect known_at", known_at)
    if known_at < path.created_at:
        raise ProjectionCompilerError("scenario effect cannot predate candidate path")
    if any(item.known_at > known_at for item in evidence_refs):
        raise ProjectionCompilerError("scenario effect cannot consume future-known evidence")
    if len({item.evidence_id for item in evidence_refs}) != len(evidence_refs):
        raise ProjectionCompilerError("scenario effect evidence refs must be unique")
    _unique_strings(missing_effects, "missing_effects")

    values = {
        "market_pnl_change_base": market_pnl_change_base,
        "execution_cost_base": execution_cost_base,
        "financing_cost_base": financing_cost_base,
        "available_cash_delta_before_costs_base": available_cash_delta_before_costs_base,
        "obligations_delta_base": obligations_delta_base,
        "gross_market_exposure_delta_base": gross_market_exposure_delta_base,
        "derivative_notional_delta_base": derivative_notional_delta_base,
        "collateral_delta_base": collateral_delta_base,
        "initial_margin_delta_base": initial_margin_delta_base,
        "maintenance_margin_delta_base": maintenance_margin_delta_base,
        "risk_budget_remaining_delta_base": risk_budget_remaining_delta_base,
        "projected_drawdown_fraction": projected_drawdown_fraction,
        "projected_notional_change_base": projected_notional_change_base,
        "capital_commitment_base": capital_commitment_base,
    }
    if status is ProjectionStatus.QUALIFIED:
        missing = [name for name, value in values.items() if value is None]
        if missing:
            raise ProjectionCompilerError("qualified scenario effect is missing: %s" % ", ".join(sorted(missing)))
        if missing_effects:
            raise ProjectionCompilerError("qualified scenario effect cannot declare missing_effects")
        if not evidence_refs:
            raise ProjectionCompilerError("qualified scenario effect requires evidence")
        if any(item.quality is not ProjectionStatus.QUALIFIED for item in evidence_refs):
            raise ProjectionCompilerError("qualified scenario effect requires qualified evidence")
    if status is ProjectionStatus.UNAVAILABLE and any(value is not None for value in values.values()):
        raise ProjectionCompilerError("unavailable scenario effect must not publish partial numeric effects")
    if status is not ProjectionStatus.UNAVAILABLE and not evidence_refs:
        raise ProjectionCompilerError("available scenario effect requires evidence")

    for name, value in {
        "execution_cost_base": execution_cost_base,
        "financing_cost_base": financing_cost_base,
        "projected_notional_change_base": projected_notional_change_base,
        "capital_commitment_base": capital_commitment_base,
    }.items():
        if value is not None and value < ZERO:
            raise ProjectionCompilerError("%s cannot be negative" % name)
    if projected_drawdown_fraction is not None and not (ZERO <= projected_drawdown_fraction <= ONE):
        raise ProjectionCompilerError("projected_drawdown_fraction must be between 0 and 1")

    body = {
        "schema_version": "BENJAMIN.SCENARIO_CAPITAL_EFFECT.v1",
        "candidate_path_id": path.path_id,
        "candidate_path_hash": path.content_hash,
        "scenario_kind": scenario_kind.value,
        "status": status.value,
        "base_currency": path.base_currency,
        "estimator_version": estimator_version,
        "known_at": known_at.isoformat(),
        "evidence_refs": [item.to_wire() for item in sorted(evidence_refs, key=lambda item: item.evidence_id)],
        "effects": {name: _optional_d(value) for name, value in sorted(values.items())},
        "missing_effects": list(sorted(set(missing_effects))),
        "unit_boundary": {
            "economic_amount_unit": "BASE_CURRENCY_VALUE_OR_NOTIONAL",
            "provider_native_quantity": False,
            "contract_count": False,
            "lot_size": False,
        },
    }
    content_hash = hashlib.sha256(_canonical(body)).hexdigest()
    return ScenarioCapitalEffect(
        schema_version="BENJAMIN.SCENARIO_CAPITAL_EFFECT.v1",
        effect_id="EFFECT-%s" % content_hash[:24],
        content_hash=content_hash,
        candidate_path_id=path.path_id,
        candidate_path_hash=path.content_hash,
        scenario_kind=scenario_kind,
        status=status,
        base_currency=path.base_currency,
        estimator_version=estimator_version,
        known_at=known_at,
        evidence_refs=tuple(sorted(evidence_refs, key=lambda item: item.evidence_id)),
        market_pnl_change_base=market_pnl_change_base,
        execution_cost_base=execution_cost_base,
        financing_cost_base=financing_cost_base,
        available_cash_delta_before_costs_base=available_cash_delta_before_costs_base,
        obligations_delta_base=obligations_delta_base,
        gross_market_exposure_delta_base=gross_market_exposure_delta_base,
        derivative_notional_delta_base=derivative_notional_delta_base,
        collateral_delta_base=collateral_delta_base,
        initial_margin_delta_base=initial_margin_delta_base,
        maintenance_margin_delta_base=maintenance_margin_delta_base,
        risk_budget_remaining_delta_base=risk_budget_remaining_delta_base,
        projected_drawdown_fraction=projected_drawdown_fraction,
        projected_notional_change_base=projected_notional_change_base,
        capital_commitment_base=capital_commitment_base,
        missing_effects=tuple(sorted(missing_effects)),
    )


def compile_projected_capital_state(
    base_state: CapitalState,
    path: CandidateEconomicPath,
    *,
    effects: Tuple[ScenarioCapitalEffect, ...],
    projector_version: str,
    known_at: datetime,
    valid_until: datetime,
    required_scenarios: Tuple[ProjectionScenarioKind, ...] = (
        ProjectionScenarioKind.EXPECTED,
        ProjectionScenarioKind.ADVERSE,
        ProjectionScenarioKind.EXECUTION_STRESS,
    ),
) -> ProjectedCapitalState:
    """Compile evidence-bound scenario effects into a Projected Capital State.

    The compiler performs deterministic capital arithmetic only. It does not
    predict market returns, execution cost, financing, margin, or fragility.
    Those values must arrive as versioned evidence-bound ScenarioCapitalEffects
    from qualified expert/model processes.
    """

    _aware("projection compiler known_at", known_at)
    _aware("projection compiler valid_until", valid_until)
    if base_state.capital_structure_id != path.capital_structure_id:
        raise ProjectionCompilerError("candidate path Capital Structure differs from base Capital State")
    if base_state.capital_state_id != path.base_capital_state_id or base_state.content_hash != path.base_capital_state_hash:
        raise ProjectionCompilerError("candidate path base Capital State is no longer current")
    if known_at < path.created_at:
        raise ProjectionCompilerError("projection cannot predate candidate path")
    if known_at >= path.valid_until:
        raise ProjectionCompilerError("candidate path is expired")
    if valid_until <= known_at or valid_until > path.valid_until:
        raise ProjectionCompilerError("projection validity must remain inside candidate-path validity")
    if not projector_version:
        raise ProjectionCompilerError("projector_version is required")
    if len({item.scenario_kind for item in effects}) != len(effects):
        raise ProjectionCompilerError("scenario effects must have unique scenario kinds")
    by_kind = {item.scenario_kind: item for item in effects}
    missing = [kind.value for kind in required_scenarios if kind not in by_kind]
    if missing:
        raise ProjectionCompilerError("missing required scenario effects: %s" % ", ".join(sorted(missing)))

    base_obligations = (
        base_state.operational_reserve
        + base_state.minimum_liquidity_required
        + base_state.pending_redemptions
        + base_state.pending_withdrawals
        + base_state.pending_distributions
    )
    scenarios = []
    for kind in required_scenarios:
        effect = by_kind[kind]
        if effect.candidate_path_id != path.path_id or effect.candidate_path_hash != path.content_hash:
            raise ProjectionCompilerError("scenario effect is bound to a different candidate path")
        if effect.base_currency != base_state.base_currency:
            raise ProjectionCompilerError("scenario effect base currency differs from Capital State")
        if effect.known_at > known_at:
            raise ProjectionCompilerError("projection cannot consume future-known scenario effect")
        if effect.status is ProjectionStatus.UNAVAILABLE:
            scenarios.append(
                ProjectedCapitalScenario(
                    kind=kind,
                    status=ProjectionStatus.UNAVAILABLE,
                    net_asset_value=None,
                    available_cash=None,
                    obligations_total=None,
                    gross_market_exposure=None,
                    derivative_gross_notional=None,
                    collateral_committed=None,
                    initial_margin=None,
                    maintenance_margin=None,
                    risk_budget_remaining=None,
                    drawdown_fraction=None,
                    evidence_refs=effect.evidence_refs,
                    missing_metrics=effect.missing_effects or ("SCENARIO_CAPITAL_EFFECTS",),
                )
            )
            continue

        assert effect.market_pnl_change_base is not None
        assert effect.execution_cost_base is not None
        assert effect.financing_cost_base is not None
        assert effect.available_cash_delta_before_costs_base is not None
        assert effect.obligations_delta_base is not None
        assert effect.gross_market_exposure_delta_base is not None
        assert effect.derivative_notional_delta_base is not None
        assert effect.collateral_delta_base is not None
        assert effect.initial_margin_delta_base is not None
        assert effect.maintenance_margin_delta_base is not None
        assert effect.risk_budget_remaining_delta_base is not None
        assert effect.projected_drawdown_fraction is not None
        assert effect.projected_notional_change_base is not None
        assert effect.capital_commitment_base is not None

        nav = base_state.net_asset_value + effect.market_pnl_change_base - effect.execution_cost_base - effect.financing_cost_base
        cash = base_state.available_cash + effect.available_cash_delta_before_costs_base - effect.execution_cost_base - effect.financing_cost_base
        obligations = base_obligations + effect.obligations_delta_base
        gross = base_state.gross_market_exposure + effect.gross_market_exposure_delta_base
        derivative = base_state.derivative_gross_notional + effect.derivative_notional_delta_base
        collateral = base_state.collateral_committed + effect.collateral_delta_base
        initial_margin = base_state.initial_margin + effect.initial_margin_delta_base
        maintenance_margin = base_state.maintenance_margin + effect.maintenance_margin_delta_base
        risk_budget = base_state.risk_budget_remaining + effect.risk_budget_remaining_delta_base

        for name, value in {
            "available_cash": cash,
            "obligations_total": obligations,
            "gross_market_exposure": gross,
            "derivative_gross_notional": derivative,
            "collateral_committed": collateral,
            "initial_margin": initial_margin,
            "maintenance_margin": maintenance_margin,
            "risk_budget_remaining": risk_budget,
        }.items():
            if value < ZERO:
                raise ProjectionCompilerError("compiled %s cannot be negative" % name)

        breaches = []
        if effect.capital_commitment_base > path.max_capital_commitment_base:
            breaches.append("MAX_CAPITAL_COMMITMENT_EXCEEDED")
        if effect.projected_notional_change_base > path.target_notional_change_base:
            breaches.append("TARGET_NOTIONAL_CHANGE_EXCEEDED")

        scenarios.append(
            ProjectedCapitalScenario(
                kind=kind,
                status=effect.status,
                net_asset_value=nav,
                available_cash=cash,
                obligations_total=obligations,
                gross_market_exposure=gross,
                derivative_gross_notional=derivative,
                collateral_committed=collateral,
                initial_margin=initial_margin,
                maintenance_margin=maintenance_margin,
                risk_budget_remaining=risk_budget,
                drawdown_fraction=effect.projected_drawdown_fraction,
                evidence_refs=effect.evidence_refs,
                missing_metrics=effect.missing_effects,
                path_constraint_breaches=tuple(breaches),
            )
        )

    return build_projected_capital_state(
        base_state,
        candidate_path_ref=path.path_id,
        responsibility_ref=path.responsibility_ref,
        projector_version=projector_version,
        known_at=known_at,
        valid_until=valid_until,
        scenarios=tuple(scenarios),
        required_scenarios=required_scenarios,
    )


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _optional_d(value: Optional[Decimal]) -> Optional[str]:
    return None if value is None else format(value, "f")


def _aware(name: str, value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ProjectionCompilerError("%s must be timezone-aware" % name)


def _unique_strings(values: Tuple[str, ...], name: str) -> None:
    if any(not item for item in values) or len(set(values)) != len(values):
        raise ProjectionCompilerError("%s must contain unique non-empty values" % name)
