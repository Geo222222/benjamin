# Benjamin Operating Roles

> **Epinnox sees. The Steward decides. The Watchman guards. Benjamin authorizes. The Hand executes. The Big Book proves. The Little Book testifies. Treasury controls deployable strength. The Spoil measures realized value. The Portion divides what is lawfully distributable.**

This document is the human-readable operating model for Benjamin. It explains what each role is responsible for, the questions it asks, the artifacts it produces, and the decisions it is forbidden to make.

The governing principle is separation of authority. No component should become a monolithic brain that observes, decides, approves itself, executes, and rewrites the evidence afterward.

---

## 1. Data Plane — Observation Infrastructure

**Purpose:** collect trustworthy observations from markets, issuers, economic sources, portfolio systems, and other approved data providers.

The Data Plane asks:

- What was observed?
- From which source?
- At what source timestamp and ingestion timestamp?
- Is the observation fresh enough for the intended decision?
- Is the source healthy?
- Are multiple sources contradictory?

A useful observation looks like:

```text
Observation
instrument: AAPL
fact: closing_price
value: 229.31
source: SOURCE-X
source_timestamp: ...
ingested_at: ...
quality: VALID
staleness: 14s
raw_ref: vault://...
digest: sha256:...
```

**Produces:** normalized observations, source-health state, provenance, quality state, and references to retained source evidence.

**May not:** invent missing data, silently replace stale observations with guesses, or convert raw facts into portfolio authority.

---

## 2. The Vault — Source Evidence

**Purpose:** hold the underlying documents and sensitive source material that should not become ledger payloads.

Examples include filings, statements, API responses selected for retention, research documents, agreements, transaction files, identity documents, and other governed evidence.

The Vault answers:

> What exact source artifact did the institution rely upon?

The Big Book may retain a digest and governed reference such as:

```text
vault://sec/AAPL/10-K/2026.pdf
SHA-256: 98e13b...
```

**Produces:** durable governed evidence locations and exact cryptographic digests.

**May not:** make investment decisions or turn secret/regulated data into public evidence merely because it is useful internally.

---

## 3. Epinnox / The Eyes — Analyst and Adviser

**Purpose:** understand the field and form evidence-backed recommendations.

Epinnox asks:

> What is happening, why might it matter, and what should Benjamin consider doing?

Example:

```text
INVESTMENT CASE
Asset: XYZ

Observation:
Revenue growth accelerating.
Margins improving.
Debt declining.
Valuation below modeled normalized range.

Thesis:
The market may be pricing the company below normalized earning power.

Base case: +17%
Bull case: +31%
Bear case: -12%
Horizon: 12-24 months
Confidence: 0.71

Recommendation: ACCUMULATE
Suggested maximum allocation: 4.0%
```

**Produces:** observations, investment cases, scenarios, assumptions, risks, confidence, recommendation envelopes, and analytical provenance.

**May not:** authorize capital, bypass Watchman, place orders, or declare its own recommendation successful.

A useful phrase is:

> **Benjamin saw it, but Benjamin did not take it.**

Seeing an opportunity does not require capital deployment.

---

## 4. The Steward / The Mind — Portfolio Judgment

**Purpose:** convert recommendations into actual portfolio intent.

The Steward asks:

- Do we accept the thesis?
- Does it fit the current portfolio?
- How much capital should be committed?
- What would invalidate the decision?
- What are the entry, review, and exit conditions?

Example:

```text
InvestmentDecision
recommendation: REC-00912
status: MODIFIED
instrument: XYZ
recommended_weight: 4.0%
authorized_intent_weight: 2.5%
reason: thesis accepted; concentration reduced
review_date: ...
invalidation_conditions: [...]
```

**Produces:** `APPROVED`, `MODIFIED`, or `REJECTED` portfolio decisions with explicit reasoning and bounded intent.

**May not:** execute, erase Watchman results, fabricate evidence, or make a blocked decision executable.

---

## 5. The Watchman / The Guard — Deterministic Risk and Constraint Authority

**Purpose:** determine whether Benjamin is permitted to pursue the Steward's intent.

Watchman asks:

> Even if the thesis is good, can Benjamin lawfully and safely do this under the current mandate?

Example:

```text
Instrument allowed?        PASS
Position concentration?    PASS
Portfolio concentration?   PASS
Cash available?            PASS
Liquidity requirement?     PASS
Jurisdiction allowed?      PASS
Leverage limit?            PASS
Evidence complete?         PASS
Authority valid?           PASS

WATCHMAN: PASS
```

Or:

```text
Steward: Allocate 8%
Policy maximum: 5%

WATCHMAN: BLOCK
```

**Produces:** deterministic `PASS` or `BLOCK` decisions with policy versions and reasons.

**May not:** invent a substitute investment, resize the order on its own, or be bypassed merely because the Steward strongly prefers the trade.

Constitutional invariant:

```text
STEWARD_APPROVED + WATCHMAN_BLOCKED = NO AUTHORIZATION
```

---

## 6. Benjamin Authority — Bounded Capital Authorization

**Purpose:** convert approved portfolio intent plus Watchman PASS into the exact artifact The Hand is permitted to execute.

Example:

```text
AuthorizedExecutionRequest
fund: FIRSTFRUITS
instrument: XYZ
side: BUY
quantity: 125
decision_id: DEC-00381
risk_id: RSK-00291
expires_at: ...
idempotency_key: ...
```

**Produces:** narrow, expiring, idempotent execution authority.

**May not:** place broker orders or expand the decision after Watchman approval.

---

## 7. The Hand — Execution

**Purpose:** perform exactly the authorized action and prove what happened.

The Hand asks only:

> Is this exact instruction authentic, unexpired, independently authorized, and not already executed?

It should not know or care that Epinnox is bullish.

Example:

```text
Authorization: AUTH-7731
Instrument: XYZ
Side: BUY
Quantity: 125

Venue result:
accepted -> partial fill -> filled
```

**Produces:** execution receipts, venue identifiers, fill results, failure results, and reconciliation inputs.

**May not:** originate strategy, alter side/instrument/quantity, extend authorization, or infer intent from prose.

---

## 8. The Big Book — Private Institutional Proof

**Purpose:** preserve minimum necessary proof that material events occurred under valid authority.

The Big Book asks:

- Who produced this proof?
- Were they authorized to produce this event type?
- What exact evidence digest supports it?
- What prior event caused it?
- Who is permitted to inspect it?
- Has the history been altered?

Example lineage:

```text
EPINNOX.RECOMMENDATION
        -> BENJAMIN.DECISION
        -> BENJAMIN.RISK
        -> BENJAMIN.AUTHORIZATION
        -> HAND.EXECUTION
        -> BENJAMIN.RECONCILIATION
```

**Produces:** private, signed, append-oriented proof history with scoped visibility and cryptographic commitments.

**May not:** become a dumping ground for all raw evidence, expose private records merely to increase verifiability, or rewrite history silently.

The Big Book proves what happened. The Vault holds the underlying evidence.

---

## 9. The Little Book — Public Testimony

**Purpose:** let outsiders verify intentionally disclosed claims without exposing the institution.

The Little Book asks:

> What is the minimum public claim necessary for this external party to verify a legitimate fact?

Example:

```text
AUTHORITY CLAIM
Entity: Martin Capital LLC
Authority: Treasury Signatory
Valid: YES
Expires: ...
Evidence commitment: ...
Big Book state root: ...
Institution signature: ...
```

**Produces:** state commitments and deliberately approved public attestations.

**May not:** automatically mirror the Big Book or contain enough information to reconstruct private portfolios, wealth, distributions, strategies, family disputes, or private relationships.

---

## 10. Treasury — Deployable Strength

**Purpose:** distinguish money Benjamin has from money Benjamin is permitted to deploy.

Treasury asks:

- What cash exists?
- What cash is encumbered?
- What reserves are required?
- What liquidity must remain available?
- What is actually deployable?

Example:

```text
Fund NAV:              $1,000,000
Cash:                    $250,000
Operating reserve:        $50,000
Redemption reserve:       $30,000
Distribution reserve:     $20,000

Deployable cash:         $150,000
```

**Produces:** cash state, reserve state, liquidity state, and deployable-capital limits.

**May not:** treat reserved or restricted capital as available simply because it exists in an account.

---

## 11. Firstfruits Shadow Portfolio — Decision Proving Ground

**Purpose:** test the complete institutional process before outside capital or autonomous live execution is allowed.

Example:

```text
Date      Recommendation  Steward   Weight  Outcome
Sep 2     BUY XYZ         APPROVE   3.0%    +4.2%
Sep 3     BUY ABC         REJECT    -       +9.1%
Sep 5     HOLD DEF        HOLD      -       -3.2%
```

The shadow portfolio measures recommendation quality separately from portfolio quality.

**Produces:** simulated NAV, exposures, modeled fills, P&L, drawdown, turnover, benchmark comparison, and decision outcomes.

**May not:** be represented as live investment performance or silently use hindsight information unavailable at decision time.

---

## 12. Decision Journal — Institutional Calibration

**Purpose:** preserve what was known and why the institution acted so decisions can be reviewed without hindsight rewriting.

Example:

```text
Decision: DEC-00381
Input: REC-00912
Steward: APPROVED
Allocation: 2.5%
Known risks: [...]
Watchman: PASS
Portfolio state before: ...
Portfolio state after: ...
Evaluation date: ...
```

At the evaluation date, the institution asks:

- Was the thesis right?
- Was the sizing right?
- Did Watchman prevent a loss or block a good opportunity?
- Did the decision process use the evidence available at that time correctly?

---

## 13. Performance and Attribution — Learning What Created the Result

**Purpose:** explain why capital gained or lost value rather than merely reporting the ending number.

Example:

```text
Total return:              +14.2%
Market beta:                +8.1%
Security selection:         +4.7%
Allocation effect:          +2.3%
Transaction costs:          -0.5%
Cash drag:                  -0.4%
```

The institution should eventually distinguish:

- Epinnox recommendation quality;
- Steward decision quality;
- Watchman value added or opportunity cost;
- execution/slippage effects;
- portfolio construction effects; and
- market beta.

**Produces:** attribution, calibration, benchmark-relative performance, and evidence for improving the process.

---

## 14. The Spoil — Realized Economic Value

**Purpose:** determine what economic value has actually been earned and is potentially available for allocation.

The Spoil is calculated, not imagined.

```text
realized gains
+ dividends
+ interest
+ other realized income
- realized losses
- fees
- expenses
- obligations
- required reserves
= NET SPOIL
```

**Principal is never spoil. Unrealized appreciation is not automatically spoil.**

---

## 15. The Portion — Distribution and Allocation

**Purpose:** divide lawfully distributable value according to predetermined entitlement and policy.

Example:

```text
Net Spoil: $100,000

Reinvestment:          $50,000
Authorized distribution: $25,000
Reserve:               $15,000
Other permitted allocation: $10,000
```

The numbers above are illustrative only. Actual allocation rules come from governing fund, entity, contractual, tax, and Covenant rules.

**May not:** improvise entitlement, distribute investor assets as family property, or distribute more than the amount lawfully available.

---

## 16. The Covenant — Law of the Body

**Purpose:** define the rules that every role must obey even when doing so is inconvenient.

Examples:

```text
Epinnox cannot authorize.
Steward cannot bypass Watchman.
Watchman BLOCK means no execution authorization.
The Hand cannot originate investment intent.
The Big Book does not silently mutate history.
The Little Book does not automatically expose private state.
Treasury reserves are not deployable capital.
Principal is not spoil.
The Portion cannot exceed lawful distributable value.
```

The Covenant should increasingly become executable invariant tests rather than prose alone.

---

# Complete Morning-to-Evening Cycle

```text
MORNING — FIND AND PURSUE LAWFUL OPPORTUNITY

Data Plane
    -> Vault / provenance
    -> Epinnox sees
    -> Steward judges
    -> Watchman guards
    -> Benjamin authorizes
    -> The Hand executes
    -> Big Book proves

EVENING — ACCOUNT AND DIVIDE

Execution / holdings
    -> reconciliation
    -> portfolio valuation
    -> performance attribution
    -> realized economic value
    -> The Spoil
    -> The Portion
    -> lawful reinvestment / reserve / distribution
    -> Big Book proof
```

The institution is incomplete if it can identify and capture opportunity but cannot reconcile, account for, explain, and lawfully allocate the resulting value.

# Core Diagnostic Questions

When reviewing any new feature, ask:

1. **Who sees this?** — Data Plane / Epinnox.
2. **Who interprets it?** — Epinnox.
3. **Who decides?** — Steward.
4. **Who can block it?** — Watchman.
5. **Who authorizes capital?** — Benjamin Authority.
6. **Who performs the action?** — The Hand.
7. **Who proves what happened?** — The Big Book.
8. **Where is the sensitive source evidence?** — The Vault.
9. **What may outsiders verify?** — The Little Book, only after explicit disclosure.
10. **Was the decision actually good?** — Shadow Portfolio + Performance/Attribution.
11. **What value was actually realized?** — The Spoil.
12. **Who is lawfully entitled to what?** — The Portion.
13. **What rule prevents shortcuts?** — The Covenant.

If one component answers several incompatible questions, the architecture is beginning to collapse its authority boundaries.