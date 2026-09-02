# Benjamin Operating Roles

> **ZLJ sees. Benjamin decides. Watchman governs. The Hand executes. The Big Book remembers and proves. The Little Book testifies.**

This document is the human-readable operating model for Benjamin inside Epinnox. It explains what each organ is responsible for, what it produces, and what it is forbidden to absorb from the others.

The governing principle is separation of authority. No component should become a monolithic brain that observes, decides, approves itself, executes, and rewrites evidence afterward.

---

## 1. ZLJ — Market Perception and Intelligence Production

**Repository:** `Geo222222/z-look-jamaican`

**Purpose:** establish what is happening in the market and produce qualified intelligence objects for Benjamin.

ZLJ asks:

- What was observed?
- From which source and at what time?
- Is the observation fresh and sequence-valid?
- What deterministic features describe the current market?
- What market state/regime appears to be present?
- What do qualified models predict over explicit horizons?
- How calibrated and competent are those models in comparable conditions?
- Where do models or hypotheses disagree?

Example output:

```text
ForecastObject
instrument: BTC-USD
horizon: 30s
proposition: price_up >= 8bps
probability: 0.71
expected_move: +11.4bps
model: microstructure_model_04
market_regime: directional_liquid
confidence: 0.78
valid_until: ...
evidence_refs: [...]
qualification: QUALIFIED
```

**Produces:** observations, measurements, market-state objects, regimes, model predictions, opportunity evidence, calibration/drift/competence records, and provenance.

**May not:** decide `TRADE / NO TRADE`, originate capital intent, size the final position, authorize capital, place orders, custody funds, or declare its own prediction economically successful merely because price later moved.

---

## 2. The Vault / Source Evidence

**Purpose:** hold underlying source artifacts and sensitive evidence that should not become raw immutable ledger payloads.

Examples include retained API payloads, research documents, statements, agreements, model artifacts, datasets, identity material, and other governed source evidence.

The Vault answers:

> What exact source artifact did the institution rely upon?

**Produces:** governed evidence locations and cryptographic digests.

**May not:** make market predictions, capital decisions, governance decisions, or external financial actions.

---

## 3. Benjamin — Capital Decision Intelligence

**Purpose:** convert qualified evidence plus authoritative capital/position context into bounded decisions.

Benjamin v1 focuses on:

1. scalping / micro trades;
2. intraday trades;
3. short swing trades.

Benjamin asks:

- Is there actually a trade here?
- Which evidence matters for this exact horizon?
- Which models are qualified and independent enough to matter?
- What evidence contradicts the trade?
- What is the expected move and downside?
- Does the edge survive spread, fees, slippage, latency, and uncertainty?
- What is the thesis?
- What invalidates it?
- What size is justified by current capital/position state?
- Should we enter, hold, reduce, exit, or abstain?
- How confident should Benjamin be given its measured competence?

Example:

```text
TradeDecision
instrument: BTC-USD
decision: ENTER
side: BUY
horizon: 2m
intended_size: bounded-size-request
expected_edge_after_costs: +6.2bps
confidence: 0.67
thesis: short-horizon directional continuation
invalidation: order-flow reversal + liquidity deterioration
expires_at: ...
evidence_refs: [...]
```

**Produces:** `ENTER`, `HOLD`, `REDUCE`, `EXIT`, or `NO_TRADE` decisions with explicit evidence, assumptions, confidence, expected edge, sizing judgment, and invalidation.

**May not:** authorize itself, bypass Watchman, place external orders, hold production signing keys, rewrite ZLJ observations, or fabricate Book history.

`NO_TRADE` is a valid decision.

---

## 4. Watchman — Governance and Authorization

**Purpose:** determine whether Benjamin's proposed external financial action is permitted under current law, policy, mandate, risk, authority, and operating state.

Watchman asks:

> Even if Benjamin's trade thesis is good, is Epinnox permitted to perform this action now?

Example:

```text
Instrument allowed?          PASS
Account/venue allowed?       PASS
Position concentration?      PASS
Capital available?           PASS
Daily loss limit?            PASS
Leverage rule?               PASS
Jurisdiction/compliance?     PASS
Decision unexpired?          PASS
Evidence requirement?        PASS

WATCHMAN: AUTHORIZE
```

Or:

```text
Benjamin intended size: 8%
Policy maximum: 5%

WATCHMAN: BLOCK
```

**Produces:** `AUTHORIZE` or `BLOCK` with exact governing rules, limits, expiry, and capability constraints.

**May not:** invent a substitute investment thesis, become the market reasoner, silently resize the economic intent unless policy explicitly defines a bounded transformation, or be bypassed because Benjamin is highly confident.

Constitutional invariant:

```text
BENJAMIN_DECISION + WATCHMAN_BLOCK = NO HAND ACTION
```

---

## 5. The Hand — Authorized External Capability Plane

**Repository:** `Geo222222/the-hand`

**Purpose:** perform the exact external financial action authorized by Watchman and report what actually happened.

The Hand is broader than one broker adapter. It is the home for Epinnox tools/abilities that can change external financial state.

Potential capability families include:

- exchange adapters;
- broker adapters;
- wallet/custody signing;
- blockchain transaction submission;
- bank/ACH/wire rails;
- payment processors;
- treasury transfers/sweeps;
- settlement providers;
- other future authenticated money-place integrations.

The Hand asks:

> Is this action authentically authorized, unexpired, supported by an allowed capability, and not already executed?

Example:

```text
WatchmanAuthorization: AUTH-7731
Capability: exchange.order.submit
Instrument: BTC-USD
Side: BUY
Quantity: ...
Constraints: ...
IdempotencyKey: ...
```

**Produces:** capability invocation receipts, provider/venue identifiers, acceptance/rejection, fills, transfer/settlement results, failures, and reconciliation inputs.

**May not:** originate strategy, change economic purpose, change side/instrument/destination/size outside authorization, extend authorization, infer intent from prose, or choose a different financial action merely because another adapter exists.

The Hand may route among technically equivalent adapters only when Watchman authorization permits that routing.

---

## 6. The Big Book — Private Institutional Memory and Proof

**Repository:** `Geo222222/the-book`

**Purpose:** preserve minimum-necessary authoritative evidence that material events occurred under valid lineage and authority.

The Big Book asks:

- Who produced this record?
- What domain truth does that producer own?
- What evidence digest/reference supports it?
- What prior event caused it?
- Who may inspect it?
- Has history been altered?

Target lineage:

```text
ZLJ.INTELLIGENCE
      -> BENJAMIN.DECISION
      -> WATCHMAN.AUTHORIZATION | WATCHMAN.BLOCK
      -> HAND.EXECUTION
      -> OUTCOME / RECONCILIATION
      -> LEARNING EVIDENCE
```

**Produces:** private signed/append-oriented evidence history, scoped visibility, causal lineage, and cryptographic commitments.

**May not:** become the market reasoner, capital decision-maker, Watchman, executioner, or a dumping ground for every raw feature/prompt/private artifact.

The Big Book proves and remembers. The Vault holds underlying governed source evidence where appropriate.

---

## 7. The Little Book — Public Testimony

**Purpose:** let outsiders verify intentionally disclosed claims without exposing private institutional history.

The Little Book is not a second copy of the Big Book.

**Produces:** deliberately approved public attestations and state commitments.

**May not:** automatically expose private portfolio composition, strategies, model stack, wealth, exact trades, internal reasoning, private relationships, or confidential agreements.

---

## 8. Treasury / Authoritative Capital State

**Purpose:** distinguish money that exists from money currently available for a Benjamin decision and from money Watchman permits to be used.

Relevant questions include:

- What cash exists?
- What is settled?
- What is encumbered?
- What positions are open?
- What capital is reserved?
- What obligations exist?
- What exposure already exists?
- What amount is actually available for this decision?

Benjamin consumes authoritative capital state; it must not hallucinate it.

Watchman applies governing limits to that state.

The Hand executes against the appropriate external account/capability only after authorization.

---

## 9. Benjamin V1 Shadow Decision Proving Ground

**Purpose:** test the complete short-horizon decision process before autonomous live capital is allowed.

A shadow record should separate:

```text
ZLJ prediction quality
Benjamin decision quality
Watchman governance effect
Hand modeled/actual execution quality
```

Measure where relevant:

- opportunities considered;
- trade/no-trade decisions;
- expected edge;
- realized edge;
- fees/slippage;
- net P&L;
- drawdown;
- win/loss distribution;
- MFE/MAE;
- holding period;
- calibration;
- performance by instrument/horizon/regime/model/procedure.

**May not:** be represented as live investment performance or use hindsight information unavailable at decision time.

---

## 10. Cognitive Memory — Learning What Benjamin Knew and Did

Benjamin requires:

### Semantic memory
Durable knowledge, definitions, validated research, model capabilities/limitations, and graduated lessons.

### Episodic memory
Specific market cases: what was known, predictions, decision, outcome, errors, and later lessons.

### Procedural memory
How Benjamin reasons: evidence qualification, conflict handling, abstention, decision construction, and escalation to Watchman.

The Book provides authoritative evidence/proof lineage. Benjamin owns how cognitive memory is organized, retrieved, and used.

---

## 11. Decision and Performance Attribution

The institution should not learn from raw ending P&L alone.

It should eventually distinguish:

- ZLJ perception/prediction contribution;
- Benjamin decision contribution;
- Watchman value added or opportunity cost;
- Hand execution/slippage contribution;
- market beta/randomness;
- cost effects.

A profitable outcome does not automatically prove every upstream component was correct. A losing outcome does not automatically prove every upstream decision was irrational.

---

## 12. The Spoil — Realized Economic Value

**Purpose:** determine what economic value has actually been earned and may become available for lawful allocation.

```text
realized gains
+ dividends / interest / other realized income where applicable
- realized losses
- fees
- expenses
- obligations
- required reserves
= NET SPOIL
```

**Principal is never spoil. Unrealized appreciation is not automatically spoil.**

This is later-stage capital/accounting logic; it is not part of the v1 scalp decision loop except where current realized state affects available capital.

---

## 13. The Portion — Distribution and Allocation

**Purpose:** divide lawfully distributable value according to predetermined entitlement and policy.

The Portion is downstream institutional accounting/governance. It is not a reason for Benjamin v1 to broaden itself into long-term portfolio or distribution intelligence prematurely.

---

## 14. The Covenant — Law of the Body

Examples:

```text
ZLJ cannot decide capital.
Benjamin cannot authorize itself.
Watchman BLOCK means no external financial action.
The Hand cannot originate economic intent.
The Book cannot invent another organ's truth.
The Little Book does not automatically expose private state.
A model's confidence does not create authority.
Historical proof is not silently rewritten.
```

The Covenant should increasingly become executable invariant tests rather than prose alone.

---

# Complete V1 Trading Cycle

```text
MARKET
   |
   v
ZLJ
observe / derive / model / qualify
   |
   +---------------------> Big Book provenance
   |
   v
BENJAMIN
enter / hold / reduce / exit / no-trade
   |
   +---------------------> Big Book decision evidence
   |
   v
WATCHMAN
authorize / block
   |
   +---------------------> Big Book governance evidence
   |
   v
THE HAND
capability adapter / external action
   |
   +---------------------> Big Book execution evidence
   |
   v
REALITY / OUTCOME
   |
   v
THE BOOK
outcome lineage
   |
   +-------------> ZLJ calibration
   |
   +-------------> Benjamin learning
```

# Core Diagnostic Questions

When reviewing any new feature, ask:

1. **Who sees this?** — ZLJ.
2. **Who decides what it means for capital?** — Benjamin.
3. **Who can permit or block the external financial action?** — Watchman.
4. **Who performs the authenticated external action?** — The Hand.
5. **Who preserves authoritative lineage?** — The Book.
6. **Where is underlying sensitive source evidence?** — The Vault/governed storage.
7. **What may outsiders verify?** — The Little Book, only after explicit disclosure.
8. **Was the market prediction good?** — ZLJ evaluation.
9. **Was the capital decision good?** — Benjamin evaluation.
10. **Did governance improve or constrain the result?** — Watchman attribution.
11. **Was execution faithful and economical?** — The Hand attribution.
12. **What value was actually realized?** — accounting / Spoil.
13. **What rule prevents shortcuts?** — The Covenant.

If a feature cannot answer which organ owns its truth and authority, its boundary is not yet well-defined.
