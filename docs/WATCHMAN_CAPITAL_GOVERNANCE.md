# Watchman — Continuous Capital-State Governance

> **Status: LIVE + PROJECTED + PRE-ACTION CAPITAL CONTRACTS IMPLEMENTED / NON-LIVE / NO HAND EXECUTION AUTHORITY**
>
> This document refines the Benjamin HLDD definition of Watchman. Watchman is not a market forecaster, legal-policy engine, strategy selector, or general compliance service. Watchman is the institution's continuous capital governor: it watches the difference between the Capital State that exists, the Capital State a candidate action could create, and the Capital State permitted by the active Responsibility.

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
              candidate path
                      |
                      v
          PROJECTED CAPITAL STATE
       expected / adverse / execution stress
                      |
                      v
                  WATCHMAN
          pre-action scenario governance
                      |
               +------+------+
               |             |
          permissible     constrain
               |             |
               v             `--> Benjamin reroutes
          future governed
           authorization
               |
               v
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

The authoritative live Capital State, non-authoritative Projected Capital State, and pre-action scenario-governance contracts now exist. None of them grants live Hand execution authority.

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

## Projected Capital State

`BENJAMIN.PROJECTED_CAPITAL_STATE.v1` is a content-addressed pro-forma capital object produced from one exact authoritative Capital State plus a candidate economic path.

It answers:

> **If Benjamin attempts this path, what capital states could reasonably result under the required scenarios?**

The default required scenario set is:

- `EXPECTED` — the ordinary modeled path;
- `ADVERSE` — a downside/stress path relevant to capital survivability;
- `EXECUTION_STRESS` — a path that includes adverse execution/settlement mechanics rather than assuming ideal fills.

Each scenario independently carries its evidence references, quality state, and projected safety metrics including NAV, cash, obligations, gross exposure, derivative notional, collateral/margin, remaining risk budget, and drawdown.

Critical invariants:

- the projection binds the exact base Capital State ID/hash/as-of time;
- it binds the candidate-path and Responsibility references;
- scenario configuration is explicit rather than hidden in a reasoner prompt;
- future-known evidence is rejected;
- a `QUALIFIED` scenario cannot hide a missing required safety metric;
- an `UNAVAILABLE` scenario cannot publish misleading partial numeric state;
- post-base authoritative capital facts require a new real Capital State rather than being smuggled into a projection;
- projections expire;
- changing an adverse scenario changes projection identity;
- a projection can never advance the authoritative Capital State pointer.

The truth boundary is explicit in every projection:

```text
authoritative_capital_state       = false
may_advance_capital_state_pointer = false
requires_post_execution_reconciliation = true
```

After The Hand acts, authoritative provider/accounting evidence must be reconciled into a new real Capital State. The projection remains historical decision evidence and may later be compared with what actually happened.

## Pre-action scenario governance

`WATCHMAN.PRE_ACTION_ASSESSMENT.v1` evaluates one exact Projected Capital State against one exact Capital Envelope.

It answers:

> **Does this candidate path remain capital-safe when the expected, adverse, and execution-stress consequences are all considered?**

Every required scenario receives its own Watchman state and capital requirements. The aggregate pre-action state is the **worst justified required-scenario result**.

Example:

```text
EXPECTED          HEALTHY
ADVERSE           CORRECTION_REQUIRED
EXECUTION_STRESS  HEALTHY

OVERALL           CORRECTION_REQUIRED
RISK_INCREASE     NOT PERMITTED AS PROJECTED
```

This prevents an attractive expected case from hiding an unacceptable downside or execution path.

A required scenario that is `DEGRADED` or `UNAVAILABLE` becomes at least `CONSTRAINED`. That fails closed for `RISK_INCREASING` candidates while preserving `RISK_REDUCING` candidates as a separately governed action class.

Pre-action assessment additionally requires:

- the projection must still reference the exact current authoritative base Capital State ID/hash;
- the projection and Capital Envelope must reference the same Capital Structure and Responsibility;
- the projection must not be expired;
- scenario evidence must already satisfy the projection's point-in-time knowability rules.

A pre-action assessment is **not** execution authorization. Its truth boundary explicitly states:

```text
authoritative_capital_state = false
execution_authorization     = false
hand_instruction            = false
```

A later authorization contract must separately translate a permissible Benjamin decision into a bounded Hand authority.

## Watchman states

Watchman intentionally has five primary states:

### `HEALTHY`

Capital is comfortably inside the active envelope. Normal Benjamin autonomy may continue.

### `WATCH`

Capital is approaching a boundary or active-decision evidence has degraded. Watchman records the condition but does not yet remove ordinary action classes.

### `CONSTRAINED`

Capital truth, projection quality, or remaining risk capacity does not support increasing risk. Risk-increasing actions are removed from the permitted action-class set, but risk-neutral and risk-reducing actions remain available.

Examples include:

- Capital State is `DEFENSIVE_ONLY`;
- Capital State is blocked because authoritative truth is unavailable;
- risk budget is exhausted;
- a required pre-action projection scenario is unavailable/degraded enough that new risk cannot be justified.

### `CORRECTION_REQUIRED`

The current Capital State, active decision condition, or required projected scenario is outside the acceptable envelope and must be brought back toward an explicit required state.

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

Watchman consumes the exact content-addressed `CapitalState` produced by Benjamin's accounting/valuation layer for live surveillance and an explicitly non-authoritative `ProjectedCapitalState` for pre-action analysis.

It must never silently replace:

- stale facts with current guesses;
- missing facts with zero;
- unreconciled facts with reconciled status;
- projected capital with authoritative capital;
- market forecasts with accounting truth.

`CapitalState.routing_readiness` is an input to Watchman, not a replacement for Watchman. `FULL`, `DEFENSIVE_ONLY`, and `BLOCKED` describe how trustworthy/usable capital truth is for routing; Watchman determines the resulting capital-governance posture.

## The Book

Material Watchman state changes must be reconstructable.

Implemented Book-bound drafts are:

- `WATCHMAN.CAPITAL_ASSESSMENT` — live authoritative Capital State surveillance;
- `WATCHMAN.PRE_ACTION_ASSESSMENT` — projected candidate-path scenario governance.

The pre-action event binds:

- exact authoritative base Capital State ID/hash;
- exact Projected Capital State ID/hash;
- candidate path/action class;
- exact Capital Envelope ID/hash;
- Responsibility reference;
- each required scenario assessment;
- worst justified aggregate state;
- candidate-permitted result;
- requirements and permitted action classes;
- assessed-at time;
- explicit non-authorization truth boundary.

The Book does not need raw provider credentials, exchange payloads, or ZLJ market histories merely to prove that Watchman made an assessment.

The eventual causal chain becomes:

```text
CAPITAL STATE T0
      |
ZLJ.INTELLIGENCE
      |
BENJAMIN candidate path
      |
PROJECTED CAPITAL STATE
      |
WATCHMAN PRE-ACTION ASSESSMENT
      |
BENJAMIN.DECISION
      |
future governed authorization
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
- live Watchman Book evidence draft;
- content-addressed Projected Capital State;
- expected/adverse/execution-stress scenario contract;
- projection expiry and anti-lookahead boundaries;
- explicit non-authoritative projection truth boundary;
- pre-action scenario-by-scenario Watchman assessment;
- worst-required-scenario aggregation;
- risk-increasing fail-closed behavior for degraded/unavailable required scenarios;
- exact current-base-state binding;
- pre-action Watchman Book evidence draft.

Not yet implemented/earned:

- automatic candidate-path capital-effect/scenario projector;
- final bounded Watchman authorization contract for Hand consumption;
- event bus / continuous daemon;
- trajectory/velocity/time-to-boundary analysis;
- instrument-level and correlation concentration because Capital State does not yet expose all required normalized decomposition;
- margin/liquidation-distance modeling across provider-specific derivative rules;
- Hand emergency execution;
- live capital authority.

## Next implementation order

```text
1. Live Capital-State Watchman contract          IMPLEMENTED
2. Projected Capital State contract              IMPLEMENTED
3. Pre-action Watchman scenario assessment       IMPLEMENTED
4. Candidate-path projection/compiler            NEXT
5. Bounded Watchman -> Hand authorization
6. Event-driven surveillance + periodic reconcile
7. Decision-validity event bridge from ZLJ
8. Capital-trajectory / market-fragility context
9. Hand action-class / emergency capability binding
10. Book material-event delivery / replay
11. Shadow/replay qualification
12. Only then consider governed live authority
```
