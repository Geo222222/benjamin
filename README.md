# Benjamin

> **ZLJ sees. Benjamin decides. Watchman governs. The Hand executes. The Book remembers and proves.**

Benjamin is **Epinnox's capital decision intelligence**. Benjamin serves Epinnox as the money mind: it consumes qualified market intelligence and authoritative financial context, reasons about what Epinnox should do, and emits bounded decision intent.

Benjamin does **not** own market perception, final governance/authorization, external execution, custody, or institutional proof infrastructure.

## V1 mandate

Benjamin v1 is deliberately narrow:

> **Master short-horizon trading decisions first: scalping / micro trades -> intraday -> short swing trading.**

Long-horizon investment planning, strategic portfolio construction, capital allocation across external portfolios, and broader treasury intelligence come later.

For v1 Benjamin must answer questions such as:

- Is there a real trade here or should we abstain?
- What evidence matters for this horizon?
- Is the expected edge still positive after fees, spread, slippage, and latency?
- Which models are competent in this instrument/regime/horizon?
- Are apparently independent signals actually derived from the same evidence?
- What is the thesis and what invalidates it?
- What size is justified by the current capital/position context?
- Should an open trade be held, reduced, or closed?
- How confident should Benjamin be, given its own measured competence?

`NO TRADE` is a first-class decision.

## Epinnox organs

### ZLJ — seeing

`Geo222222/z-look-jamaican` owns market perception and intelligence production: observations, features, market state, microstructure, regimes, forecasts, model predictions, calibration, drift, and model-competence evidence.

ZLJ output is evidence. It is not capital authority.

### Benjamin — deciding

Benjamin owns capital judgment: decision context, evidence qualification, thesis, alternatives, trade/no-trade, sizing judgment, invalidation, trade-management intent, confidence, and decision learning.

Benjamin may use deterministic services, statistical/ML models, local models, frontier models, and other qualified cognitive operators. Those models are organs inside the cognition system; **Benjamin is not reducible to one model**.

### Watchman — governing

Watchman is downstream of Benjamin and owns policy, mandate, limits, compliance, exposure rules, jurisdiction, authority, and the final permission or block required before an external financial action.

Benjamin does not authorize itself.

### The Hand — executing

`Geo222222/the-hand` is the authorized external-action capability plane. It owns the tools/adapters that can change external financial state: exchange/broker orders, wallet/custody signing, transfers, settlement, banking/payment/treasury rails, and future approved financial integrations.

The Hand may implement many capabilities, but it may not originate or materially alter Benjamin's economic intent.

### The Book — remembering and proving

`Geo222222/the-book` owns authoritative cross-system evidence, memory lineage, private proof history, and public testimony policy. It preserves the material chain from ZLJ evidence through Benjamin decision, Watchman governance, Hand execution, and later outcome.

The Book is not Benjamin's brain and Benjamin is not The Book's writer of all truth.

## Target lifecycle

```text
MARKET / WORLD
      |
      v
     ZLJ
qualified observations / state / predictions
      |
      +--------------------------+
      |                          |
      v                          v
  THE BOOK -----------------> BENJAMIN
 evidence/history             decision cognition
                                 |
                                 v
                         BENJAMIN.DECISION
                                 |
                                 v
                             WATCHMAN
                         authorize / block
                                 |
                       authorized action
                                 |
                                 v
                            THE HAND
                    external capability/adaptor
                                 |
                                 v
                              WORLD
                                 |
                                 v
                            THE BOOK
                      outcome / proof lineage
                                 |
                       learning feedback
                                 |
                 +---------------+---------------+
                 v                               v
                ZLJ                           BENJAMIN
```

## Benjamin cognitive architecture

Benjamin's intended intelligence is a composable, evidence-driven cognitive system rather than a monolithic trading model or unconstrained LLM.

For v1, cognition is organized at different speeds:

```text
                    BENJAMIN
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
     Reflex         Tactical       Reflective
 deterministic     decision        learning /
 fast truth        cognition       metacognition
```

### Reflex

Deterministic/canonical values that should not depend on generated reasoning: spread, position state, fees, slippage bounds, freshness, order constraints, hard limits supplied by authoritative services, and other machine-checkable facts.

### Tactical

The core v1 decision intelligence: evidence qualification, model disagreement, regime fit, expected edge, thesis/invalidation, trade/no-trade, sizing judgment, hold/reduce/exit intent, and uncertainty.

### Reflective

Slower self-evaluation: model/source degradation, calibration, recurring reasoning errors, regime-specific weakness, timing/slippage problems, and whether a model/procedure should be demoted or replaced.

See [`docs/FUTURE_COGNITIVE_ARCHITECTURE.md`](docs/FUTURE_COGNITIVE_ARCHITECTURE.md).

## Three forms of cognitive memory

Benjamin requires three distinct forms of memory:

- **Semantic memory** — durable knowledge, validated lessons, strategy definitions, market concepts, model capabilities/limitations, and policy knowledge.
- **Episodic memory** — what happened in specific market cases: evidence, predictions, decisions, outcomes, errors, and reasoning trajectories.
- **Procedural memory** — governed methods for how Benjamin reasons, qualifies evidence, handles disagreement, abstains, and constructs decisions.

Benjamin owns the meaning and use of these cognitive memories. The Book owns authoritative evidence/proof lineage and may preserve or reference the material records needed to reconstruct them. The two responsibilities must not be collapsed.

## Learning without uncontrolled self-modification

Benjamin should learn continuously through outcome comparison, calibration, contextual model competence, memory updates, and explicit model succession.

A production model should not silently rewrite its own neural weights while controlling capital. Candidate model changes should be replayed, evaluated, shadowed, qualified, and explicitly promoted.

## The benchmark

The primary v1 qualification question is not simply:

> Did Benjamin make money?

It is:

> **Does Benjamin demonstrate repeatable positive decision quality under controlled conditions after realistic costs, with calibrated confidence and bounded drawdown?**

Qualification should separate ZLJ prediction quality from Benjamin decision quality and Hand execution quality.

Relevant evidence includes expected versus realized edge, fees, slippage, net P&L, win/loss distribution, profit factor, drawdown, MFE/MAE, holding period, calibration, and performance by instrument, horizon, regime, model, and strategy family.

## Privacy principle

> **Everything material must be provable. Benjamin does not publish everything it knows.**

Portfolio state, strategies, opportunities, model competence, internal deliberation, counterparties, credentials, tax/banking information, and private reasoning are private by default.

The Big Book preserves minimum-necessary private proof/evidence. The Little Book is a separate disclosure surface and is never an automatic export of Benjamin cognition or portfolio history.

## ACM-07 consoles

Benjamin has separately built Manager and Client console shells:

```text
apps/manager-console
apps/client-console
```

The Manager Console is the internal operating surface. The Client Console is participant-scoped and must never become a browser-filtered copy of manager-only state.

The current ACM-07.0 implementation uses synthetic shadow fixtures and does not represent accepted subscriptions, live client assets, live performance, or production investor records.

See [`docs/ACM-07_CONSOLES.md`](docs/ACM-07_CONSOLES.md).

## Transitional implementation note

Existing code/contracts may still contain earlier terms such as **Steward**, `BENJAMIN.RISK`, or `BENJAMIN.AUTHORIZATION`. Those names describe the current foundation and are not constitutional ownership claims for the target bridge architecture.

The target semantics are:

- Benjamin decides;
- Watchman governs/authorizes or blocks;
- The Hand executes.

Future bridge work should migrate schemas without erasing historical evidence or silently changing already-issued proof semantics.

## Current status

**FOUNDATION / SHADOW — NO LIVE MONEY OR EXECUTION.**

The current repository does not yet contain the complete live Benjamin v1 reasoner, the production ZLJ bridge, production Watchman bridge, live Hand capability routing, or autonomous capital deployment.
