# Watchman — Continuous Capital-State Governance

> **Status: BACKEND CONTRACT IMPLEMENTED / NON-LIVE / NO HAND EXECUTION AUTHORITY**
>
> This document refines the Benjamin HLDD definition of Watchman. Watchman is not a market forecaster, legal-policy engine, strategy selector, or general compliance service. Watchman is the institution's continuous capital governor: it watches the difference between the Capital State that exists and the Capital State permitted by the active Responsibility.

## Constitutional question

```text
ZLJ
What is happening in the market?

Benjamin
What should this capital do?

Watchman
Can this capital safely remain in its current or proposed state?

The Hand
How do I perform the authorized capital action?

The Book
What happened and what proves it?
```

Watchman watches the money before, during, and after Benjamin acts.

## Core loop

```text
                     ZLJ
             market intelligence
                      |
                      v
                  BENJAMIN
              capital decision
                      |
                      v
           projected capital effect
                      |
                      v
                  WATCHMAN
               pre-action watch
                      |
               +------+------+
               |             |
          acceptable      constrain
               |             |
               v             `--> Benjamin reroutes
             HAND
               |
            execution
               |
               v
          CAPITAL STATE
               |
       +-------+--------+
       |                |
       v                v
   WATCHMAN             ZLJ
live capital watch   live market watch
       |                |
       +-------+--------+
               |
               v
           BENJAMIN
        next decision
```

The first implemented slice covers **authoritative live Capital State surveillance**. A separate Projected Capital State contract must be implemented before Watchman may treat a pre-action simulation as anything other than a projection. Projected state must never masquerade as accounting truth.

## Capital Envelope

Owner/operator Responsibility compiles into a versioned `CapitalEnvelope`.

The envelope is not a trade strategy. It defines the measurable capital boundaries Watchman must defend, including currently implemented families such as:

- drawdown boundaries;
- liquidity-obligation coverage;
- gross market exposure relative to NAV;
- derivative notional relative to NAV;
- collateral commitment relative to NAV.

Future envelopes may add instrument concentration, correlated exposure, margin/liquidation distance, participant-specific obligations, scenario stress, and other capital-safety metrics after their authoritative state inputs exist.

Envelope identity is content-addressed and binds the exact Responsibility reference/version used to govern the capital.

## Watchman states

Watchman intentionally has five primary states:

### `HEALTHY`

Capital is comfortably inside the active envelope. Normal Benjamin autonomy may continue.

### `WATCH`

Capital is approaching a boundary or active-decision evidence has degraded. Watchman records the condition but does not yet remove ordinary action classes.

### `CONSTRAINED`

Capital truth or remaining risk capacity does not support increasing risk. Risk-increasing actions are removed from the permitted action-class set, but risk-neutral and risk-reducing actions remain available.

Examples include:

- Capital State is `DEFENSIVE_ONLY`;
- Capital State is blocked because authoritative truth is unavailable;
- risk budget is exhausted.

### `CORRECTION_REQUIRED`

The current Capital State or active decision condition is outside the acceptable envelope and must be brought back toward an explicit required state.

Watchman does **not** select the economic path. It emits requirements such as:

```text
current_drawdown_fraction <= 0.05
liquidity_coverage >= 1.50
active_decision_validity >= REASSESSED_OR_CLOSED
```

Benjamin receives the requirement and determines the best permissible corrective path.

### `EMERGENCY`

Capital survival is threatened or an emergency envelope boundary has been crossed. Only risk-reducing or narrowly preauthorized emergency-protective capability classes may remain available.

## Action classes

Watchman governs action classes rather than provider APIs:

- `RISK_INCREASING`
- `RISK_NEUTRAL`
- `RISK_REDUCING`
- `EMERGENCY_PROTECTIVE`

This lets The Hand later classify qualified capabilities independently of provider implementation.

Example:

```text
position.increase     -> RISK_INCREASING
position.reduce       -> RISK_REDUCING
position.close        -> RISK_REDUCING
cancel risk order     -> EMERGENCY_PROTECTIVE / context-bound neutral
```

Watchman never calls Coinbase, Kraken, Alpaca, a bank, or a wallet directly.

## Decision-validity watch

Benjamin decisions should eventually publish explicit invalidation conditions. ZLJ watches the market evidence necessary to determine whether those conditions remain true. Watchman consumes only the resulting qualified validity state.

```text
ZLJ evidence
    |
    v
DecisionValidityWatch
    |
    +-- VALID
    +-- DEGRADED
    +-- INVALIDATED
    `-- UNAVAILABLE
```

`INVALIDATED` forces `CORRECTION_REQUIRED` and tells Benjamin to reassess or close the governed path. Watchman does not invent the replacement trade.

Future-known validity evidence is rejected.

## Emergency path

Normal correction:

```text
Watchman
   |
required safe state
   |
   v
Benjamin
   |
select corrective path
   |
   v
Hand
```

Emergency protection may later support a much narrower path:

```text
WATCHMAN.EMERGENCY
        |
        v
PREAUTHORIZED RISK-REDUCING HAND CAPABILITY
        |
        v
NEW CAPITAL STATE
        |
        v
BENJAMIN REASSESSES
```

The first contract publishes the only emergency directive vocabulary currently contemplated:

- `FREEZE_NEW_RISK`
- `CANCEL_RISK_INCREASING_ORDERS`
- `REDUCE_TO_SAFE_EXPOSURE`
- `CLOSE_LIQUIDATION_THREATENED_POSITION`
- `RESTORE_MINIMUM_COLLATERAL_BUFFER`

These are **directives, not live execution authority**. The Hand must later independently qualify capability semantics, idempotency, units, provider behavior, and postcondition verification before any such path can become operational.

## Market intelligence boundary

Watchman is not a second ZLJ.

ZLJ may publish market facts such as:

- liquidity deterioration;
- volatility expansion;
- leverage/funding stress;
- liquidation fragility;
- basis/term-structure change;
- correlation/concentration regime;
- decision invalidation evidence.

Watchman interprets those facts only through their **capital consequence**.

```text
ZLJ understands danger in the market.
Watchman understands danger to this money.
```

Trajectory-aware Watchman logic (distance/velocity/time-to-boundary) is a future phase and must consume qualified, point-in-time ZLJ intelligence rather than recalculate market state itself.

## Capital State truth boundary

Watchman consumes the exact content-addressed `CapitalState` produced by Benjamin's accounting/valuation layer.

It must never silently replace:

- stale facts with current guesses;
- missing facts with zero;
- unreconciled facts with reconciled status;
- projected capital with authoritative capital;
- market forecasts with accounting truth.

`CapitalState.routing_readiness` is an input to Watchman, not a replacement for Watchman. `FULL`, `DEFENSIVE_ONLY`, and `BLOCKED` describe how trustworthy/usable capital truth is for routing; Watchman determines the resulting capital-governance posture.

## The Book

Material Watchman state changes must be reconstructable.

The first Book-bound draft is:

`WATCHMAN.CAPITAL_ASSESSMENT`

It binds minimum-necessary evidence including:

- assessment/content hash;
- Capital Structure;
- exact Capital State ID/hash/as-of time;
- exact Capital Envelope ID/hash;
- Responsibility reference;
- Watchman state;
- reasons;
- required capital conditions;
- permitted action classes;
- emergency directives where present;
- decision-validity reference/state where present;
- assessed-at time.

The Book does not need raw provider credentials, exchange payloads, or ZLJ market histories merely to prove that Watchman made an assessment.

The eventual causal chain becomes:

```text
CAPITAL STATE T0
      |
ZLJ.INTELLIGENCE
      |
BENJAMIN.DECISION
      |
WATCHMAN PRE-ACTION ASSESSMENT
      |
HAND EXECUTION
      |
CAPITAL STATE T1
      |
WATCHMAN LIVE ASSESSMENT
      |
WARNING / CONSTRAINT / CORRECTION / EMERGENCY
      |
BENJAMIN corrective decision
      |
HAND corrective execution
      |
CAPITAL STATE T2
```

## Current implementation boundary

Implemented now:

- content-addressed Capital Envelope;
- deterministic live Capital State assessment;
- five Watchman states;
- action-class restriction;
- explicit required-state conditions;
- decision-validity intake;
- future-evidence rejection;
- emergency directive vocabulary;
- Book evidence draft.

Not yet implemented/earned:

- Projected Capital State;
- automatic pre-action capital-effect simulation;
- event bus / continuous daemon;
- trajectory/velocity/time-to-boundary analysis;
- instrument-level and correlation concentration because Capital State does not yet expose all required normalized decomposition;
- margin/liquidation-distance modeling across provider-specific derivative rules;
- Hand emergency execution;
- live capital authority.

## Next implementation order

```text
1. Live Capital-State Watchman contract          IMPLEMENTED
2. Projected Capital State contract              NEXT
3. Pre-action Watchman assessment                after projection
4. Event-driven surveillance + periodic reconcile
5. Decision-validity event bridge from ZLJ
6. Capital-trajectory / market-fragility context
7. Hand action-class / emergency capability binding
8. Book material-event delivery / replay
9. Shadow/replay qualification
10. Only then consider governed live authority
```
