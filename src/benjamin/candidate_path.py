from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Tuple

from .capital_state import CapitalState
from .watchman_capital import ActionClass

ZERO = Decimal("0")


class EconomicPathType(str, Enum):
    HOLD = "HOLD"
    INCREASE_SPOT = "INCREASE_SPOT"
    REDUCE_SPOT = "REDUCE_SPOT"
    EXIT_SPOT = "EXIT_SPOT"
    INCREASE_DERIVATIVE = "INCREASE_DERIVATIVE"
    REDUCE_DERIVATIVE = "REDUCE_DERIVATIVE"
    EXIT_DERIVATIVE = "EXIT_DERIVATIVE"
    HEDGE = "HEDGE"
    REBALANCE = "REBALANCE"
    BASIS_RELATIVE_VALUE = "BASIS_RELATIVE_VALUE"
    RAISE_LIQUIDITY = "RAISE_LIQUIDITY"


@dataclass(frozen=True)
class CandidateEconomicPath:
    schema_version: str
    path_id: str
    content_hash: str
    capital_structure_id: str
    base_capital_state_id: str
    base_capital_state_hash: str
    responsibility_ref: str
    path_type: EconomicPathType
    action_class: ActionClass
    economic_root_id: str
    expression_refs: Tuple[str, ...]
    target_notional_change_base: Decimal
    max_capital_commitment_base: Decimal
    base_currency: str
    target_horizon_seconds: int
    purpose: str
    intelligence_refs: Tuple[str, ...]
    relationship_state_refs: Tuple[str, ...]
    classification_evidence_refs: Tuple[str, ...]
    created_at: datetime
    valid_until: datetime

    def to_wire(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "path_id": self.path_id,
            "content_hash": self.content_hash,
            "capital_structure_id": self.capital_structure_id,
            "base_capital_state_id": self.base_capital_state_id,
            "base_capital_state_hash": self.base_capital_state_hash,
            "responsibility_ref": self.responsibility_ref,
            "path_type": self.path_type.value,
            "action_class": self.action_class.value,
            "economic_root_id": self.economic_root_id,
            "expression_refs": list(self.expression_refs),
            "target_notional_change": {
                "value": _d(self.target_notional_change_base),
                "unit": "BASE_CURRENCY_NOTIONAL",
                "currency": self.base_currency,
            },
            "max_capital_commitment": {
                "value": _d(self.max_capital_commitment_base),
                "unit": "BASE_CURRENCY_VALUE",
                "currency": self.base_currency,
            },
            "target_horizon_seconds": self.target_horizon_seconds,
            "purpose": self.purpose,
            "intelligence_refs": list(self.intelligence_refs),
            "relationship_state_refs": list(self.relationship_state_refs),
            "classification_evidence_refs": list(self.classification_evidence_refs),
            "created_at": self.created_at.isoformat(),
            "valid_until": self.valid_until.isoformat(),
            "truth_boundary": {
                "provider_order": False,
                "provider_native_quantity": False,
                "execution_authorization": False,
                "capital_projection": False,
            },
        }


def build_candidate_economic_path(
    base_state: CapitalState,
    *,
    responsibility_ref: str,
    path_type: EconomicPathType,
    action_class: ActionClass,
    economic_root_id: str,
    expression_refs: Tuple[str, ...],
    target_notional_change_base: Decimal,
    max_capital_commitment_base: Decimal,
    target_horizon_seconds: int,
    purpose: str,
    intelligence_refs: Tuple[str, ...],
    relationship_state_refs: Tuple[str, ...] = (),
    classification_evidence_refs: Tuple[str, ...] = (),
    created_at: datetime,
    valid_until: datetime,
) -> CandidateEconomicPath:
    """Create Benjamin's provider-neutral candidate economic transformation.

    V1 expresses economic size only in the Capital Structure base currency. It
    deliberately contains no exchange contract counts, lots, base-asset units,
    provider symbols, order IDs, leverage settings, or provider-native quantity.
    Those mechanics belong downstream in qualified Hand capabilities.
    """

    if not responsibility_ref or not economic_root_id or not purpose:
        raise ValueError("candidate path identity/purpose fields are required")
    _aware("candidate path created_at", created_at)
    _aware("candidate path valid_until", valid_until)
    if created_at < base_state.known_at:
        raise ValueError("candidate path cannot exist before base Capital State was knowable")
    if valid_until <= created_at:
        raise ValueError("candidate path valid_until must be after created_at")
    if target_horizon_seconds <= 0:
        raise ValueError("candidate path target_horizon_seconds must be positive")
    if target_notional_change_base < ZERO or max_capital_commitment_base < ZERO:
        raise ValueError("candidate path economic amounts cannot be negative")
    _unique(expression_refs, "expression_refs")
    _unique(intelligence_refs, "intelligence_refs")
    _unique(relationship_state_refs, "relationship_state_refs")
    _unique(classification_evidence_refs, "classification_evidence_refs")

    if path_type is EconomicPathType.HOLD:
        if target_notional_change_base != ZERO or max_capital_commitment_base != ZERO:
            raise ValueError("HOLD path must have zero economic change/commitment")
        if action_class is not ActionClass.RISK_NEUTRAL:
            raise ValueError("HOLD path must be RISK_NEUTRAL")
    else:
        if not expression_refs:
            raise ValueError("market-transforming path requires expression_refs")
        if target_notional_change_base <= ZERO:
            raise ValueError("market-transforming path requires positive target notional change")

    increasing_types = {
        EconomicPathType.INCREASE_SPOT,
        EconomicPathType.INCREASE_DERIVATIVE,
    }
    reducing_types = {
        EconomicPathType.REDUCE_SPOT,
        EconomicPathType.EXIT_SPOT,
        EconomicPathType.REDUCE_DERIVATIVE,
        EconomicPathType.EXIT_DERIVATIVE,
        EconomicPathType.RAISE_LIQUIDITY,
    }
    context_dependent = {
        EconomicPathType.HEDGE,
        EconomicPathType.REBALANCE,
        EconomicPathType.BASIS_RELATIVE_VALUE,
    }
    if path_type in increasing_types and action_class is not ActionClass.RISK_INCREASING:
        raise ValueError("increase path must be classified RISK_INCREASING")
    if path_type in reducing_types and action_class is not ActionClass.RISK_REDUCING:
        raise ValueError("reduce/exit/liquidity path must be classified RISK_REDUCING")
    if path_type in context_dependent and not classification_evidence_refs:
        raise ValueError("context-dependent path requires action-class classification evidence")
    if action_class is ActionClass.EMERGENCY_PROTECTIVE:
        raise ValueError("Benjamin candidate paths cannot self-classify as EMERGENCY_PROTECTIVE")

    body = {
        "schema_version": "BENJAMIN.CANDIDATE_ECONOMIC_PATH.v1",
        "capital_structure_id": base_state.capital_structure_id,
        "base_capital_state_id": base_state.capital_state_id,
        "base_capital_state_hash": base_state.content_hash,
        "responsibility_ref": responsibility_ref,
        "path_type": path_type.value,
        "action_class": action_class.value,
        "economic_root_id": economic_root_id,
        "expression_refs": list(sorted(expression_refs)),
        "target_notional_change": {
            "value": _d(target_notional_change_base),
            "unit": "BASE_CURRENCY_NOTIONAL",
            "currency": base_state.base_currency,
        },
        "max_capital_commitment": {
            "value": _d(max_capital_commitment_base),
            "unit": "BASE_CURRENCY_VALUE",
            "currency": base_state.base_currency,
        },
        "target_horizon_seconds": target_horizon_seconds,
        "purpose": purpose,
        "intelligence_refs": list(sorted(intelligence_refs)),
        "relationship_state_refs": list(sorted(relationship_state_refs)),
        "classification_evidence_refs": list(sorted(classification_evidence_refs)),
        "created_at": created_at.isoformat(),
        "valid_until": valid_until.isoformat(),
        "truth_boundary": {
            "provider_order": False,
            "provider_native_quantity": False,
            "execution_authorization": False,
            "capital_projection": False,
        },
    }
    content_hash = hashlib.sha256(_canonical(body)).hexdigest()
    return CandidateEconomicPath(
        schema_version="BENJAMIN.CANDIDATE_ECONOMIC_PATH.v1",
        path_id="PATH-%s" % content_hash[:24],
        content_hash=content_hash,
        capital_structure_id=base_state.capital_structure_id,
        base_capital_state_id=base_state.capital_state_id,
        base_capital_state_hash=base_state.content_hash,
        responsibility_ref=responsibility_ref,
        path_type=path_type,
        action_class=action_class,
        economic_root_id=economic_root_id,
        expression_refs=tuple(sorted(expression_refs)),
        target_notional_change_base=target_notional_change_base,
        max_capital_commitment_base=max_capital_commitment_base,
        base_currency=base_state.base_currency,
        target_horizon_seconds=target_horizon_seconds,
        purpose=purpose,
        intelligence_refs=tuple(sorted(intelligence_refs)),
        relationship_state_refs=tuple(sorted(relationship_state_refs)),
        classification_evidence_refs=tuple(sorted(classification_evidence_refs)),
        created_at=created_at,
        valid_until=valid_until,
    )


def _unique(values: Tuple[str, ...], name: str) -> None:
    if any(not item for item in values) or len(set(values)) != len(values):
        raise ValueError("%s must contain unique non-empty refs" % name)


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _d(value: Decimal) -> str:
    return format(value, "f")


def _aware(name: str, value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("%s must be timezone-aware" % name)
