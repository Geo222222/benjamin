from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

ZERO = Decimal("0")
ONE = Decimal("1")


class SourceQuality(str, Enum):
    VALID = "VALID"
    DEGRADED = "DEGRADED"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class ReconciliationStatus(str, Enum):
    RECONCILED = "RECONCILED"
    PARTIAL = "PARTIAL"
    DISCREPANCY = "DISCREPANCY"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class RoutingReadiness(str, Enum):
    """How Capital State quality constrains Benjamin's candidate-path search.

    This is not capital authorization. It only tells the Router which *classes*
    of paths may be considered before Responsibility and Watchman apply.
    """

    FULL = "FULL"
    DEFENSIVE_ONLY = "DEFENSIVE_ONLY"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class CapitalSourceRef:
    source_id: str
    source_kind: str
    account_id: str
    observed_at: datetime
    known_at: datetime
    content_hash: str
    quality: SourceQuality = SourceQuality.VALID

    def __post_init__(self) -> None:
        _require_non_empty("source_id", self.source_id)
        _require_non_empty("source_kind", self.source_kind)
        _require_non_empty("account_id", self.account_id)
        _require_non_empty("content_hash", self.content_hash)
        _require_aware("observed_at", self.observed_at)
        _require_aware("known_at", self.known_at)
        if self.known_at < self.observed_at:
            raise ValueError("source known_at cannot precede observed_at")


@dataclass(frozen=True)
class ValuationPolicyRef:
    policy_id: str
    version: str
    content_hash: str

    def __post_init__(self) -> None:
        _require_non_empty("valuation policy id", self.policy_id)
        _require_non_empty("valuation policy version", self.version)
        _require_non_empty("valuation policy content hash", self.content_hash)


@dataclass(frozen=True)
class CapitalStateInput:
    """Authoritative facts used to construct one point-in-time Capital State.

    Monetary fields are expressed in `base_currency` unless their name denotes
    exposure/notional rather than booked value. Positive liability fields
    represent amounts owed. `derivative_mark_value` and P&L/net exposure fields
    may be signed.

    `available_cash` means provider/accounting cash available before Benjamin's
    internal liquidity/operational/reserve obligations below. Provider-locked
    collateral should not be counted as available cash.
    """

    capital_structure_id: str
    base_currency: str
    as_of: datetime
    known_at: datetime
    valuation_policy: ValuationPolicyRef
    account_ids: tuple[str, ...]
    source_refs: tuple[CapitalSourceRef, ...]
    reconciliation_status: ReconciliationStatus

    cash_balance: Decimal = ZERO
    available_cash: Decimal = ZERO
    spot_asset_value: Decimal = ZERO
    derivative_mark_value: Decimal = ZERO
    other_asset_value: Decimal = ZERO
    receivables: Decimal = ZERO
    unsettled_receivables: Decimal = ZERO

    liabilities: Decimal = ZERO
    unsettled_payables: Decimal = ZERO
    accrued_fees: Decimal = ZERO
    accrued_financing: Decimal = ZERO

    operational_reserve: Decimal = ZERO
    minimum_liquidity_required: Decimal = ZERO
    pending_redemptions: Decimal = ZERO
    pending_withdrawals: Decimal = ZERO
    pending_distributions: Decimal = ZERO
    pending_inflows: Decimal = ZERO

    collateral_committed: Decimal = ZERO
    initial_margin: Decimal = ZERO
    maintenance_margin: Decimal = ZERO

    spot_gross_exposure: Decimal = ZERO
    derivative_gross_notional: Decimal = ZERO
    gross_market_exposure: Decimal = ZERO
    net_market_exposure: Decimal = ZERO

    realized_pnl: Decimal = ZERO
    unrealized_pnl: Decimal = ZERO
    participant_equity: Decimal = ZERO
    risk_budget_remaining: Decimal = ZERO
    current_drawdown_fraction: Decimal = ZERO

    stale_fields: tuple[str, ...] = ()
    missing_fields: tuple[str, ...] = ()
    discrepancy_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty("capital_structure_id", self.capital_structure_id)
        _require_non_empty("base_currency", self.base_currency)
        _require_aware("as_of", self.as_of)
        _require_aware("known_at", self.known_at)
        if self.known_at < self.as_of:
            raise ValueError("capital state known_at cannot precede as_of")
        if not self.account_ids:
            raise ValueError("capital state requires at least one authoritative account")
        if any(not account_id for account_id in self.account_ids):
            raise ValueError("capital state account identifiers must be non-empty")
        if len(set(self.account_ids)) != len(self.account_ids):
            raise ValueError("capital state account identifiers must be unique")
        if not self.source_refs:
            raise ValueError("capital state requires authoritative source references")

        for source in self.source_refs:
            if source.account_id not in self.account_ids:
                raise ValueError("source account must belong to Capital State account_ids")
            if source.observed_at > self.as_of:
                raise ValueError("capital state cannot include source observations after as_of")
            if source.known_at > self.known_at:
                raise ValueError("capital state cannot include information known after state known_at")

        non_negative = {
            "cash_balance": self.cash_balance,
            "available_cash": self.available_cash,
            "spot_asset_value": self.spot_asset_value,
            "other_asset_value": self.other_asset_value,
            "receivables": self.receivables,
            "unsettled_receivables": self.unsettled_receivables,
            "liabilities": self.liabilities,
            "unsettled_payables": self.unsettled_payables,
            "accrued_fees": self.accrued_fees,
            "accrued_financing": self.accrued_financing,
            "operational_reserve": self.operational_reserve,
            "minimum_liquidity_required": self.minimum_liquidity_required,
            "pending_redemptions": self.pending_redemptions,
            "pending_withdrawals": self.pending_withdrawals,
            "pending_distributions": self.pending_distributions,
            "pending_inflows": self.pending_inflows,
            "collateral_committed": self.collateral_committed,
            "initial_margin": self.initial_margin,
            "maintenance_margin": self.maintenance_margin,
            "spot_gross_exposure": self.spot_gross_exposure,
            "derivative_gross_notional": self.derivative_gross_notional,
            "gross_market_exposure": self.gross_market_exposure,
            "participant_equity": self.participant_equity,
            "risk_budget_remaining": self.risk_budget_remaining,
        }
        for name, value in non_negative.items():
            if value < ZERO:
                raise ValueError(f"{name} cannot be negative")

        if self.available_cash > self.cash_balance:
            raise ValueError("available_cash cannot exceed cash_balance")
        if self.maintenance_margin > self.initial_margin and self.initial_margin > ZERO:
            raise ValueError("maintenance_margin cannot exceed initial_margin")
        if not (ZERO <= self.current_drawdown_fraction <= ONE):
            raise ValueError("current_drawdown_fraction must be between 0 and 1")


@dataclass(frozen=True)
class CapitalState:
    schema_version: str
    capital_state_id: str
    content_hash: str
    capital_structure_id: str
    base_currency: str
    as_of: datetime
    known_at: datetime
    valuation_policy: ValuationPolicyRef
    account_ids: tuple[str, ...]
    source_refs: tuple[CapitalSourceRef, ...]
    reconciliation_status: ReconciliationStatus

    gross_assets: Decimal
    gross_liabilities: Decimal
    net_asset_value: Decimal
    cash_balance: Decimal
    available_cash: Decimal
    liquidity_available_for_deployment: Decimal
    risk_capital_available: Decimal

    spot_asset_value: Decimal
    derivative_mark_value: Decimal
    other_asset_value: Decimal
    receivables: Decimal
    unsettled_receivables: Decimal
    liabilities: Decimal
    unsettled_payables: Decimal
    accrued_fees: Decimal
    accrued_financing: Decimal

    operational_reserve: Decimal
    minimum_liquidity_required: Decimal
    pending_redemptions: Decimal
    pending_withdrawals: Decimal
    pending_distributions: Decimal
    pending_inflows: Decimal

    collateral_committed: Decimal
    initial_margin: Decimal
    maintenance_margin: Decimal
    spot_gross_exposure: Decimal
    derivative_gross_notional: Decimal
    gross_market_exposure: Decimal
    net_market_exposure: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    participant_equity: Decimal
    risk_budget_remaining: Decimal
    current_drawdown_fraction: Decimal

    routing_readiness: RoutingReadiness
    readiness_reasons: tuple[str, ...]
    stale_fields: tuple[str, ...]
    missing_fields: tuple[str, ...]
    discrepancy_refs: tuple[str, ...]

    def to_wire(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "capital_state_id": self.capital_state_id,
            "content_hash": self.content_hash,
            "capital_structure_id": self.capital_structure_id,
            "base_currency": self.base_currency,
            "as_of": self.as_of.isoformat(),
            "known_at": self.known_at.isoformat(),
            "valuation_policy": {
                "policy_id": self.valuation_policy.policy_id,
                "version": self.valuation_policy.version,
                "content_hash": self.valuation_policy.content_hash,
            },
            "account_ids": list(self.account_ids),
            "source_refs": [_source_to_wire(source) for source in self.source_refs],
            "reconciliation_status": self.reconciliation_status.value,
            "gross_assets": _money(self.gross_assets),
            "gross_liabilities": _money(self.gross_liabilities),
            "net_asset_value": _money(self.net_asset_value),
            "cash_balance": _money(self.cash_balance),
            "available_cash": _money(self.available_cash),
            "liquidity_available_for_deployment": _money(self.liquidity_available_for_deployment),
            "risk_capital_available": _money(self.risk_capital_available),
            "spot_asset_value": _money(self.spot_asset_value),
            "derivative_mark_value": _money(self.derivative_mark_value),
            "other_asset_value": _money(self.other_asset_value),
            "receivables": _money(self.receivables),
            "unsettled_receivables": _money(self.unsettled_receivables),
            "liabilities": _money(self.liabilities),
            "unsettled_payables": _money(self.unsettled_payables),
            "accrued_fees": _money(self.accrued_fees),
            "accrued_financing": _money(self.accrued_financing),
            "operational_reserve": _money(self.operational_reserve),
            "minimum_liquidity_required": _money(self.minimum_liquidity_required),
            "pending_redemptions": _money(self.pending_redemptions),
            "pending_withdrawals": _money(self.pending_withdrawals),
            "pending_distributions": _money(self.pending_distributions),
            "pending_inflows": _money(self.pending_inflows),
            "collateral_committed": _money(self.collateral_committed),
            "initial_margin": _money(self.initial_margin),
            "maintenance_margin": _money(self.maintenance_margin),
            "spot_gross_exposure": _money(self.spot_gross_exposure),
            "derivative_gross_notional": _money(self.derivative_gross_notional),
            "gross_market_exposure": _money(self.gross_market_exposure),
            "net_market_exposure": _money(self.net_market_exposure),
            "realized_pnl": _money(self.realized_pnl),
            "unrealized_pnl": _money(self.unrealized_pnl),
            "participant_equity": _money(self.participant_equity),
            "risk_budget_remaining": _money(self.risk_budget_remaining),
            "current_drawdown_fraction": _money(self.current_drawdown_fraction),
            "routing_readiness": self.routing_readiness.value,
            "readiness_reasons": list(self.readiness_reasons),
            "stale_fields": list(self.stale_fields),
            "missing_fields": list(self.missing_fields),
            "discrepancy_refs": list(self.discrepancy_refs),
        }


def build_capital_state(source: CapitalStateInput) -> CapitalState:
    """Construct a reproducible Capital State without looking past `known_at`.

    Pending inflows never increase deployable capital until they become settled,
    authoritative cash. Pending outflows and liquidity obligations reduce the
    amount the Router may treat as available for new risk.
    """

    derivative_asset = max(source.derivative_mark_value, ZERO)
    derivative_liability = max(-source.derivative_mark_value, ZERO)

    gross_assets = (
        source.cash_balance
        + source.spot_asset_value
        + derivative_asset
        + source.other_asset_value
        + source.receivables
        + source.unsettled_receivables
    )
    gross_liabilities = (
        derivative_liability
        + source.liabilities
        + source.unsettled_payables
        + source.accrued_fees
        + source.accrued_financing
    )
    net_asset_value = gross_assets - gross_liabilities

    immediate_obligations = (
        source.operational_reserve
        + source.minimum_liquidity_required
        + source.pending_redemptions
        + source.pending_withdrawals
        + source.pending_distributions
    )
    liquidity_available = max(source.available_cash - immediate_obligations, ZERO)
    risk_capital_available = min(liquidity_available, source.risk_budget_remaining)

    readiness, readiness_reasons = _routing_readiness(
        source=source,
        net_asset_value=net_asset_value,
        risk_capital_available=risk_capital_available,
    )

    body = {
        "schema_version": "BENJAMIN.CAPITAL_STATE.v1",
        "capital_structure_id": source.capital_structure_id,
        "base_currency": source.base_currency,
        "as_of": source.as_of.isoformat(),
        "known_at": source.known_at.isoformat(),
        "valuation_policy": {
            "policy_id": source.valuation_policy.policy_id,
            "version": source.valuation_policy.version,
            "content_hash": source.valuation_policy.content_hash,
        },
        "account_ids": list(source.account_ids),
        "source_refs": [_source_to_wire(item) for item in source.source_refs],
        "reconciliation_status": source.reconciliation_status.value,
        "gross_assets": _money(gross_assets),
        "gross_liabilities": _money(gross_liabilities),
        "net_asset_value": _money(net_asset_value),
        "cash_balance": _money(source.cash_balance),
        "available_cash": _money(source.available_cash),
        "liquidity_available_for_deployment": _money(liquidity_available),
        "risk_capital_available": _money(risk_capital_available),
        "spot_asset_value": _money(source.spot_asset_value),
        "derivative_mark_value": _money(source.derivative_mark_value),
        "other_asset_value": _money(source.other_asset_value),
        "receivables": _money(source.receivables),
        "unsettled_receivables": _money(source.unsettled_receivables),
        "liabilities": _money(source.liabilities),
        "unsettled_payables": _money(source.unsettled_payables),
        "accrued_fees": _money(source.accrued_fees),
        "accrued_financing": _money(source.accrued_financing),
        "operational_reserve": _money(source.operational_reserve),
        "minimum_liquidity_required": _money(source.minimum_liquidity_required),
        "pending_redemptions": _money(source.pending_redemptions),
        "pending_withdrawals": _money(source.pending_withdrawals),
        "pending_distributions": _money(source.pending_distributions),
        "pending_inflows": _money(source.pending_inflows),
        "collateral_committed": _money(source.collateral_committed),
        "initial_margin": _money(source.initial_margin),
        "maintenance_margin": _money(source.maintenance_margin),
        "spot_gross_exposure": _money(source.spot_gross_exposure),
        "derivative_gross_notional": _money(source.derivative_gross_notional),
        "gross_market_exposure": _money(source.gross_market_exposure),
        "net_market_exposure": _money(source.net_market_exposure),
        "realized_pnl": _money(source.realized_pnl),
        "unrealized_pnl": _money(source.unrealized_pnl),
        "participant_equity": _money(source.participant_equity),
        "risk_budget_remaining": _money(source.risk_budget_remaining),
        "current_drawdown_fraction": _money(source.current_drawdown_fraction),
        "routing_readiness": readiness.value,
        "readiness_reasons": list(readiness_reasons),
        "stale_fields": list(source.stale_fields),
        "missing_fields": list(source.missing_fields),
        "discrepancy_refs": list(source.discrepancy_refs),
    }
    content_hash = hashlib.sha256(_canonical(body)).hexdigest()
    capital_state_id = f"CAPSTATE-{content_hash[:24]}"

    return CapitalState(
        schema_version="BENJAMIN.CAPITAL_STATE.v1",
        capital_state_id=capital_state_id,
        content_hash=content_hash,
        capital_structure_id=source.capital_structure_id,
        base_currency=source.base_currency,
        as_of=source.as_of,
        known_at=source.known_at,
        valuation_policy=source.valuation_policy,
        account_ids=source.account_ids,
        source_refs=source.source_refs,
        reconciliation_status=source.reconciliation_status,
        gross_assets=gross_assets,
        gross_liabilities=gross_liabilities,
        net_asset_value=net_asset_value,
        cash_balance=source.cash_balance,
        available_cash=source.available_cash,
        liquidity_available_for_deployment=liquidity_available,
        risk_capital_available=risk_capital_available,
        spot_asset_value=source.spot_asset_value,
        derivative_mark_value=source.derivative_mark_value,
        other_asset_value=source.other_asset_value,
        receivables=source.receivables,
        unsettled_receivables=source.unsettled_receivables,
        liabilities=source.liabilities,
        unsettled_payables=source.unsettled_payables,
        accrued_fees=source.accrued_fees,
        accrued_financing=source.accrued_financing,
        operational_reserve=source.operational_reserve,
        minimum_liquidity_required=source.minimum_liquidity_required,
        pending_redemptions=source.pending_redemptions,
        pending_withdrawals=source.pending_withdrawals,
        pending_distributions=source.pending_distributions,
        pending_inflows=source.pending_inflows,
        collateral_committed=source.collateral_committed,
        initial_margin=source.initial_margin,
        maintenance_margin=source.maintenance_margin,
        spot_gross_exposure=source.spot_gross_exposure,
        derivative_gross_notional=source.derivative_gross_notional,
        gross_market_exposure=source.gross_market_exposure,
        net_market_exposure=source.net_market_exposure,
        realized_pnl=source.realized_pnl,
        unrealized_pnl=source.unrealized_pnl,
        participant_equity=source.participant_equity,
        risk_budget_remaining=source.risk_budget_remaining,
        current_drawdown_fraction=source.current_drawdown_fraction,
        routing_readiness=readiness,
        readiness_reasons=readiness_reasons,
        stale_fields=source.stale_fields,
        missing_fields=source.missing_fields,
        discrepancy_refs=source.discrepancy_refs,
    )


def _routing_readiness(
    *,
    source: CapitalStateInput,
    net_asset_value: Decimal,
    risk_capital_available: Decimal,
) -> tuple[RoutingReadiness, tuple[str, ...]]:
    reasons: list[str] = []

    if net_asset_value <= ZERO:
        return RoutingReadiness.BLOCKED, ("NON_POSITIVE_NET_ASSET_VALUE",)

    if source.reconciliation_status is ReconciliationStatus.UNAVAILABLE:
        return RoutingReadiness.BLOCKED, ("RECONCILIATION_UNAVAILABLE",)

    if all(item.quality is SourceQuality.UNAVAILABLE for item in source.source_refs):
        return RoutingReadiness.BLOCKED, ("ALL_CAPITAL_SOURCES_UNAVAILABLE",)

    if source.reconciliation_status is not ReconciliationStatus.RECONCILED:
        reasons.append(f"RECONCILIATION_{source.reconciliation_status.value}")
    if source.discrepancy_refs:
        reasons.append("OPEN_RECONCILIATION_DISCREPANCY")
    if source.missing_fields:
        reasons.append("MISSING_CAPITAL_FIELDS")
    if source.stale_fields:
        reasons.append("STALE_CAPITAL_FIELDS")

    if any(item.quality is SourceQuality.UNAVAILABLE for item in source.source_refs):
        reasons.append("CAPITAL_SOURCE_UNAVAILABLE")
    if any(item.quality is SourceQuality.STALE for item in source.source_refs):
        reasons.append("CAPITAL_SOURCE_STALE")
    if any(item.quality is SourceQuality.DEGRADED for item in source.source_refs):
        reasons.append("CAPITAL_SOURCE_DEGRADED")

    if risk_capital_available <= ZERO:
        reasons.append("NO_RISK_CAPITAL_AVAILABLE")

    if reasons:
        return RoutingReadiness.DEFENSIVE_ONLY, tuple(dict.fromkeys(reasons))
    return RoutingReadiness.FULL, ("CAPITAL_STATE_FULLY_ROUTABLE",)


def _source_to_wire(source: CapitalSourceRef) -> dict[str, str]:
    return {
        "source_id": source.source_id,
        "source_kind": source.source_kind,
        "account_id": source.account_id,
        "observed_at": source.observed_at.isoformat(),
        "known_at": source.known_at.isoformat(),
        "content_hash": source.content_hash,
        "quality": source.quality.value,
    }


def _money(value: Decimal) -> str:
    return format(value, "f")


def _canonical(value: dict[str, object]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _require_non_empty(name: str, value: str) -> None:
    if not value:
        raise ValueError(f"{name} must be non-empty")


def _require_aware(name: str, value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
