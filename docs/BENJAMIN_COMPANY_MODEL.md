# Benjamin Capital Management — High-Level Design (HLDD)

> **Status: ARCHITECTURAL TARGET / FRONTEND-CONTRACT DEFINED / NON-LIVE**
>
> This document is the authoritative high-level design for Benjamin Capital Management and the Benjamin Decision Engine. It defines intended behavior, ownership boundaries, capital-state semantics, routing behavior, institutional handoffs, and the frontend-to-backend contract direction. It does **not** activate live custody, live execution, leverage, derivatives execution, pooled-fund operations, regulatory status, or guaranteed profitability.

## 1. Executive definition

Benjamin exists in two distinct but connected forms:

1. **Benjamin Capital Management** — the business and capital-operating layer. It manages the relationship between people/entities and the capital structures entrusted to Benjamin.
2. **Benjamin Decision Engine** — the governed money logic. It evaluates what a specific body of capital should do next, given its current economic state, its owner-defined Responsibility, qualified ZLJ intelligence, and available economic paths.

The company answers:

> **Whose money is this, how is it structured, what obligations exist, what authority has been granted, and what must be reported?**

The decision engine answers:

> **Given what this capital is responsible for becoming, what is the best permissible transformation from its current state?**

Benjamin is therefore not fundamentally a trading bot. It is a **capital operating system with a governed capital decision engine inside it**.

## 2. Constitutional position

```text
MARKET / WORLD
      |
      v
     ZLJ
  sees / models / qualifies
      |
      v
ZLJ.INTELLIGENCE
      |
      v
BENJAMIN CAPITAL MANAGEMENT
  knows the governed capital container
      |
      +-------------------------+
      |                         |
      v                         v
CAPITAL STATE             RESPONSIBILITY
what the money is         what the money must do
      |                         |
      +------------+------------+
                   |
                   v
          BENJAMIN ROUTER
     candidate economic paths
                   |
                   v
       BENJAMIN DECISION ENGINE
                   |
                   v
          BENJAMIN.DECISION
                   |
                   v
               WATCHMAN
          authorize / block
                   |
                   v
                THE HAND
         execute authorized action
                   |
                   v
                 WORLD
                   |
                   v
              ACCOUNTING
                   |
                   v
          NEW CAPITAL STATE
                   |
                   v
                THE BOOK
       remembers / proves lineage
                   |
          learning feedback
          /              \
         v                v
        ZLJ            BENJAMIN
```

Constitutional ownership remains:

- **ZLJ sees.** It owns market perception, market-state intelligence, prediction, calibration, competence, and economic market relationships.
- **Benjamin decides.** It owns capital judgment and the selection of the best permissible economic path for a governed Capital Structure.
- **Watchman governs.** It owns mandate enforcement, risk/policy/compliance constraints, and final authorization or block.
- **The Hand executes.** It owns authenticated external-action capabilities and provider integrations.
- **The Book remembers and proves.** It owns authoritative cross-organ evidence and reconstructable lineage.

Benjamin cannot self-authorize, cannot grant itself execution authority, cannot invent accounting truth, and cannot bypass Watchman or The Hand.

## 3. The two Benjamins

### 3.1 Benjamin Capital Management — the Money Man

The operating company owns or administers the capital-management relationship and its lifecycle:

- Relationships;
- Capital Structures;
- Participants and beneficial/economic interests;
- Account Connections;
- Responsibility versions;
- capital/accounting projections;
- contributions, subscriptions, redemptions, withdrawals, distributions, and fees;
- client reporting;
- operational restrictions and closure;
- institutional bridge visibility to ZLJ, Watchman, Hand, and Book.

Benjamin Capital Management does not imply custody. Assets may remain externally custodied while Benjamin receives only the narrowly granted authority required by the Responsibility and downstream governance.

### 3.2 Benjamin Decision Engine — the Money Logic

The Decision Engine operates **inside** a governed Capital Structure. It receives:

- authoritative point-in-time Capital State;
- active Responsibility version;
- qualified ZLJ intelligence;
- economic relationship state;
- portfolio/exposure context;
- costs, liquidity, and operational availability;
- relevant semantic, episodic, and procedural memory.

It then:

1. constructs candidate economic paths;
2. rejects paths that are impossible or outside authority;
3. evaluates surviving paths economically;
4. compares their effects on the entire Capital Structure;
5. selects the best justified permissible path, including `HOLD` / `ABSTAIN` when appropriate;
6. records a durable `BENJAMIN.DECISION` for Watchman.

The Decision Engine does not execute the decision.

## 4. Canonical economic unit: Capital Structure

Benjamin reasons economically at the **Capital Structure** level, not at the brokerage/exchange-account level.

A Capital Structure is the governed economic container whose capital Benjamin is responsible for managing.

Initial end-state types:

- `INDIVIDUAL_MANAGED_ACCOUNT`
- `HOUSEHOLD_OR_JOINT_PORTFOLIO`
- `ENTITY_OR_TREASURY_ACCOUNT`
- `POOLED_PORTFOLIO`

A single Capital Structure may span multiple implementation surfaces:

```text
FAMILY GROWTH I
      |
      +-- Coinbase account
      +-- Kraken account
      +-- Alpaca account
      +-- bank cash account
      +-- client-controlled wallet
      `-- future futures / collateral account
```

Those are not six independent portfolios. They are account/custody/execution surfaces belonging to one governed economic responsibility.

**Rule:** `AccountConnection != CapitalStructure`.

## 5. First-class Capital State

### 5.1 Definition

`CapitalState` is Benjamin's authoritative, point-in-time economic representation of a Capital Structure.

It answers:

> **What is the complete economic state of the capital Benjamin is responsible for, as knowable at time T?**

Capital State must be derived from authoritative accounting/custody/provider evidence and must never be fabricated by the decision reasoner or frontend.

Conceptually:

```text
ZLJ
  Market State
      |
      v
  Intelligence

BENJAMIN
  Capital State
      |
      v
  Decision
```

This symmetry is intentional: ZLJ represents the world; Benjamin represents the money.

### 5.2 Minimum Capital State families

A Capital State may include, where applicable:

- Capital Structure identity;
- as-of / known-at timestamp;
- accounting/base currency;
- gross assets;
- net asset value / equity;
- available cash;
- cash reserved for obligations;
- spot assets and current valuation;
- derivative exposure and marked value;
- long/short/net/gross exposure;
- liabilities;
- receivables/payables;
- collateral committed;
- initial/maintenance margin;
- unsettled trades/capital;
- accrued fees;
- accrued funding/financing/interest;
- realized P&L;
- unrealized P&L;
- concentration and correlation exposure;
- current drawdown;
- risk budget used/remaining;
- minimum liquidity requirement;
- pending contribution/subscription amounts;
- pending redemption/withdrawal/distribution obligations;
- participant equity/capital-account totals;
- stale/missing/reconciliation state;
- exact source/account/valuation-policy lineage.

A useful projection may look like:

```text
CAPITAL STATE

Structure                 Family Growth I
Gross assets              $184,000
Cash                       $42,000
Spot assets                $97,000
Derivative exposure        $35,000
Receivables                 $4,000
Liabilities                 $8,000
Collateral committed       $18,000
Unsettled capital            $2,000
Participant equity         $176,000
Required liquidity          $26,400
Available deployable        $31,700
Current drawdown                4.2%
Risk budget remaining        $9,100
```

### 5.3 Capital State invariants

Capital State must:

- be point-in-time and reproducible;
- preserve valuation-policy version;
- preserve authoritative account/source lineage;
- expose stale, missing, contradictory, or unreconciled conditions;
- distinguish accounting truth from forecast/expected return;
- distinguish settled from unsettled value;
- distinguish available capital from capital reserved for obligations;
- distinguish economic exposure from cash paid;
- include participant/redemption liabilities that constrain deployable capital;
- never silently coerce unknown data to zero or healthy status.

### 5.4 Accounting is part of cognition

The decision loop is not:

```text
forecast -> trade -> calculate P&L later
```

It is:

```text
CAPITAL STATE T0
      |
      v
BENJAMIN DECISION
      |
      v
WATCHMAN AUTHORIZATION
      |
      v
HAND EXECUTION
      |
      v
ACCOUNTING EVENTS
      |
      v
RECONCILIATION
      |
      v
CAPITAL STATE T1
```

Therefore accounting is not back-office decoration. It is an authoritative input to the next decision.

## 6. Canonical company/domain nouns

### Relationship

A governed association between Benjamin Capital Management and a person, household, trust, company/entity, participant, or other lawful/economic party.

A Relationship may own, control, or participate in multiple Capital Structures.

### Participant

A person/entity with an economic, beneficial, governance, or reporting interest in a Capital Structure.

Participant state must distinguish:

- economic interest / units / capital account;
- beneficial ownership/control where applicable;
- contribution/subscription history;
- redemption/withdrawal history;
- distributions;
- allocated fees/expenses;
- reporting rights;
- permissions;
- privacy scope.

A participant does not silently receive authority to alter a pooled structure's Responsibility.

### AccountConnection

An externally authoritative brokerage, exchange, FCM, custodian, bank, or future wallet/custody connection attached to a Capital Structure.

It must keep separate permissions for:

- read balances/activity;
- trade;
- transfer;
- withdraw;
- sign;
- other provider-specific capabilities.

Trading authority never silently implies unrestricted withdrawal authority.

### Responsibility

A versioned owner/operator definition of **Benjamin's job** for a Capital Structure.

Responsibility is split into three distinct categories:

#### Objectives — what Benjamin should seek

Examples:

- preserve capital;
- compound capital;
- aggressive growth;
- absolute return;
- income;
- liquidity preservation;
- tax efficiency;
- target return/volatility/utilization ranges.

Targets are aspirations/optimization objectives, never guaranteed outcomes.

#### Obligations — what Benjamin must preserve or satisfy

Examples:

- remain solvent;
- maintain minimum liquidity;
- satisfy a pending redemption/distribution;
- stay inside maximum drawdown;
- preserve required reserves;
- respect time-horizon or concentration limits;
- honor account/structure restrictions.

Obligations constrain the feasible economic path set.

#### Authorities — what Benjamin may understand, consider, and execute

Authorities must distinguish:

- market-understanding authority;
- market-execution authority;
- economic-action authority;
- strategy authority;
- leverage/short/derivative authority;
- autonomy level;
- emergency/restriction rules.

Example:

```text
Crypto futures     UNDERSTAND = YES
Crypto futures     EXECUTE    = NO
```

Benjamin may learn from futures while remaining prohibited from expressing futures exposure.

### Target

A measurable desired trajectory/state used by the Router as an objective, not as a promise.

### EconomicRelationshipState

A point-in-time representation of relationships between economically linked instruments/markets, supplied or grounded by qualified ZLJ intelligence.

### CandidateEconomicPath

A possible transformation of the Capital Structure. It is **not an order**.

Examples:

- hold cash / abstain;
- increase spot exposure;
- reduce exposure;
- exit;
- rebalance;
- hedge;
- short where authorized;
- future derivative exposure;
- basis / relative-value structure;
- pair/spread;
- roll;
- convert exposure;
- move/resize collateral;
- raise liquidity for a redemption;
- preserve cash because no qualified path is superior.

### PathEvaluation

The durable evaluation of a candidate path against Capital State, Responsibility, ZLJ intelligence, economic relationships, expected outcomes, costs, risk, liquidity, and authority.

### BenjaminDecision

The selected economic path after comparing feasible alternatives. A Benjamin Decision is neither Watchman authorization nor Hand execution.

### CapitalActivity

Any economic change attributable to the structure or participant, including contribution, redemption, fee, distribution, transfer, execution, settlement, financing/funding accrual, reconciliation, P&L, or accounting correction.

### Statement

A participant/account/structure-scoped reporting projection of authoritative accounting/Book records over a defined period.

## 7. Relationship and ownership graph

```text
Relationship
  |- may own/control 0..N Capital Structures
  `- may participate in 0..N Capital Structures

Capital Structure
  |- has 1 active Responsibility version
  |- has 1..N AccountConnections where applicable
  |- has 1..N Participants where applicable
  |- has a point-in-time Capital State
  `- has 0..N Benjamin Decisions

Participant
  |- has economic/capital-account interest
  |- has reporting/privacy scope
  |- has lifecycle and capital activity
  `- does not independently override shared Responsibility

Responsibility
  |- Objectives
  |- Obligations
  |- Authorities
  `- immutable once superseded

Benjamin Decision Engine
  |- cannot rewrite Responsibility
  |- cannot fabricate Capital State
  |- cannot grant itself authority
  |- cannot bypass Watchman
  `- cannot execute directly through The Hand
```

## 8. The Capital Router

### 8.1 Purpose

The Router is an **economic-path router**, not merely a strategy selector and not an order router.

It answers:

> **Given this capital, its obligations, its targets, its current state, and what ZLJ knows about the world, which permissible capital transformation best advances the Responsibility?**

The same market intelligence may produce different paths for different Capital Structures because their Capital States and Responsibilities differ.

Example:

```text
SAME BTC INTELLIGENCE
        |
        +-- Aggressive individual / unused risk budget
        |      -> limited spot increase
        |
        +-- Moderate portfolio / crypto already concentrated
        |      -> no new exposure
        |
        +-- Large structure / hedge authority enabled
        |      -> hedge or relative-value path
        |
        `-- Drawdown near hard boundary
               -> hold cash / reduce risk
```

### 8.2 Router input contract

The Router should eventually consume only versioned/qualified objects, including:

- `CapitalState`;
- active `Responsibility`;
- `ZLJ.INTELLIGENCE` objects;
- `EconomicRelationshipState`;
- relevant portfolio/correlation/risk projections;
- operational/account capability state;
- cost/liquidity/financing projections;
- relevant cognitive memory/procedure versions.

### 8.3 Candidate generation

The Router may generate many candidate economic paths, including paths that are ultimately blocked. Preserving blocked/high-scoring alternatives is useful evidence because it explains the effect of owner authority and governance.

### 8.4 Hard gate order

Path selection must be lexicographically constrained. The conceptual order is:

1. **Operationally possible?** Required account/capability/data exists and is usable.
2. **Responsibility-authorized?** The active authority permits the path.
3. **Survivable?** Plausible downside does not violate hard capital/risk obligations.
4. **Liquidity-safe?** Reserves, redemptions, settlement, and liquidity obligations remain satisfiable.
5. **Evidence sufficient?** Market intelligence and model competence meet the required threshold.
6. **Then optimize economic outcome.** Compare expected benefit after costs, uncertainty, and portfolio effects.

A high expected return can never compensate for a hard authority, solvency, liquidity, or mandate violation.

### 8.5 Evaluation dimensions

For feasible paths, evaluation may consider:

- expected return/distribution;
- downside/tail scenarios;
- evidence quality;
- ZLJ competence/calibration;
- uncertainty;
- liquidity impact;
- drawdown impact;
- correlation/concentration impact;
- capital efficiency;
- financing/funding/carry;
- execution/slippage/fees;
- tax sensitivity where appropriate;
- expected holding horizon;
- reversibility;
- opportunity cost;
- effect on pending obligations;
- execution suitability.

The final implementation must preserve enough decomposition to explain why one path outranked another.

## 9. Spot, futures, and economic relationships

Benjamin must understand economic relationships rather than reducing markets to `BUY / SELL / LONG / SHORT` verbs.

### 9.1 Spot evidence

Potential evidence families include:

- underlying turnover;
- spread/depth;
- aggressive/reported flow;
- liquidity;
- realized volatility;
- venue quality;
- cross-venue agreement/dislocation;
- inventory/settlement evidence where legitimately observable.

### 9.2 Futures / derivatives evidence

Potential evidence families include:

- notional activity;
- open interest;
- basis;
- annualized basis where meaningful;
- funding/financing;
- term structure;
- liquidation pressure;
- mark/index divergence;
- margin/collateral state where available;
- maturity/roll behavior;
- positioning/leverage proxies;
- spread/depth/liquidity;
- lead/lag relationship with spot.

Futures are not hard-coded as false/inflated information and spot is not hard-coded as universally unlevered truth. The architecture must measure market structure and let qualified evidence determine relevance.

### 9.3 Multiple adaptive weight families

There is no single static `futures_weight`.

At minimum, ZLJ/Benjamin should distinguish context-dependent influence on:

1. **predictive information** — how much this market helps forecast future state;
2. **regime information** — how much it identifies the current environment;
3. **fragility/risk information** — how much it reveals leverage/liquidation/instability;
4. **capital-confidence effect** — whether the information should increase or reduce Benjamin's willingness to deploy capital;
5. **execution suitability** — whether the market is an appropriate implementation venue/instrument.

Thus futures can simultaneously be:

```text
Predictive information       HIGH
Regime information           HIGH
Fragility                     VERY HIGH
Capital confidence            MODERATE / LOWERED
Execution suitability         LOW / DISABLED BY AUTHORITY
```

This is intentional. `Informational value != capital authority != execution suitability`.

### 9.4 Economic behaviors beyond direction

End-state Benjamin should be capable of understanding, evaluating, and later—only when authorized—expressing relationships such as:

- basis expansion/compression;
- cash-and-carry / reverse cash-and-carry;
- funding divergence;
- term-structure changes;
- hedging;
- synthetic exposure;
- relative value;
- cross-venue dislocation;
- cross-instrument spreads;
- liquidation cascades;
- margin pressure;
- collateral efficiency;
- carry/roll cost;
- convergence/divergence.

Understanding a behavior does not activate execution authority for it.

## 10. Participant economics are Capital State inputs

For pooled/joint structures, participants are not merely percentages on a dashboard.

Their activity creates real economic claims and obligations:

- subscriptions/contributions;
- effective-date ownership;
- units or participant capital accounts;
- distributions;
- allocated fees/expenses;
- pending redemptions;
- withdrawal obligations;
- gain/loss allocations;
- high-water-mark/hurdle state where a future lawful product requires it.

Example:

```text
Portfolio NAV              $200,000
Cash                        $20,000
Pending redemption          $30,000
```

Benjamin must not treat the $20,000 cash or remaining portfolio as freely deployable without accounting for the redemption obligation. That obligation belongs inside Capital State and Responsibility feasibility.

Before pooled capital can become operational, the backend must support unit/NAV accounting or an equivalent participant-capital-account method that prevents economic leakage between participants.

## 11. Decision contract

A future `BENJAMIN.DECISION` should bind at minimum:

- decision identity/schema/version;
- Capital Structure;
- exact Capital State reference/hash/as-of time;
- exact Responsibility version;
- selected Candidate Economic Path;
- alternatives considered;
- reasons alternatives were blocked/rejected;
- relevant ZLJ intelligence references;
- Economic Relationship State references;
- expected benefit/downside;
- expected portfolio/capital effect;
- liquidity/risk/cost impact;
- invalidation conditions;
- uncertainty/confidence decomposition where justified;
- reasoner/router/procedure versions;
- known-at/valid-until/expiration semantics;
- Watchman state/reference;
- Book evidence identity.

A decision must be reconstructable from what Benjamin knew at the time.

## 12. Owner/operator control model

The owner/operator defines **Benjamin's Responsibility**, not day-to-day market conclusions.

The owner controls:

1. **Objectives** — what the capital should seek;
2. **Obligations** — what must be preserved/satisfied;
3. **Understanding authority** — what markets/economic relationships Benjamin may use as evidence;
4. **Execution authority** — what markets/actions may ever be proposed for execution;
5. **Risk/liquidity envelope**;
6. **Autonomy level**;
7. **effective Responsibility version**.

The owner should not normally:

- manually set transient model weights to force a desired market conclusion;
- rewrite ZLJ evidence;
- bypass the Router with undocumented trade intent;
- bypass Watchman;
- directly grant The Hand capital intent outside the institutional chain.

Responsibility changes are versioned and prospective. Historical decisions remain bound to the version that actually governed them.

## 13. Cognitive architecture

Benjamin is not one model. It is a composable system of deterministic services, statistical/ML models, retrieval systems, and qualified reasoning operators.

Potential internal operators include:

```text
Benjamin
  |- CapitalStateCompiler / validator
  |- ResponsibilityCompiler
  |- EvidenceQualifier
  |- ContradictionDetector
  |- EconomicRelationshipInterpreter
  |- ForecastComparator
  |- CostAndEdgeReasoner
  |- CandidatePathGenerator
  |- Scenario / counterfactual reasoner
  |- Portfolio / capital-effect reasoner
  |- CapitalRouter
  |- DecisionReasoner
  |- ConfidenceCalibrator
  |- SelfModel / metacognition
  `- OutcomeLearner
```

No single model is sovereign.

### Three cognitive speeds

#### Reflex

Fast deterministic/canonical truth:

- Capital State validity;
- current positions/cash/exposure;
- fees and known costs;
- data freshness;
- account/capability availability;
- hard Responsibility constraints;
- immediate invalidation conditions.

#### Tactical

The core money logic:

- compare qualified intelligence;
- construct candidate paths;
- reason about spot/futures/economic relationships;
- evaluate expected benefit/downside after costs;
- compare portfolio effects;
- select the best permissible path;
- build a bounded decision and invalidation.

#### Reflective

Slower learning/metacognition:

- identify recurring decision errors;
- distinguish ZLJ forecast error from Benjamin routing error from Hand execution error;
- update competence/calibration/self-model evidence;
- propose model/procedure succession;
- identify regime-specific weakness.

## 14. Three forms of memory

Benjamin requires distinct memory systems:

### Semantic memory — what Benjamin knows

- capital/market mechanisms;
- validated strategy/economic relationship knowledge;
- model capabilities/limitations;
- Responsibility concepts;
- accounting/risk concepts;
- validated lessons.

### Episodic memory — what happened

A case may bind:

- Capital State T0;
- Responsibility version;
- ZLJ intelligence and economic relationship state;
- candidate paths;
- selected decision;
- Watchman result;
- Hand execution quality;
- accounting changes;
- Capital State T1;
- outcome/evaluation;
- lessons.

### Procedural memory — how Benjamin reasons

- how Capital State is compiled/validated;
- how candidate paths are generated;
- how hard gates are applied;
- how path scores/decompositions are calculated;
- how disagreement is preserved;
- how decisions are constructed;
- how abstention occurs;
- how decisions route to Watchman.

Procedures are versioned and cannot silently rewrite themselves while controlling capital.

## 15. The Book as the state-transition spine

The Book is more than a receipt viewer. It should preserve or reference enough material evidence to reconstruct the causal state transition:

```text
CAPITAL STATE T0
      |
ZLJ.INTELLIGENCE
      |
CANDIDATE PATHS
      |
BENJAMIN.DECISION
      |
WATCHMAN AUTHORIZATION / BLOCK
      |
HAND EXECUTION
      |
ACCOUNTING EVENTS
      |
RECONCILIATION
      |
CAPITAL STATE T1
      |
OUTCOME / LEARNING
```

This supports questions such as:

- Why is this client's/pool's money worth what Benjamin reports?
- What did Benjamin know when it decided?
- Which Responsibility governed the decision?
- Which alternatives were considered?
- What did Watchman authorize or block?
- What did The Hand actually do?
- What accounting events changed capital truth?
- How did the resulting Capital State differ from the expected outcome?

The Book owns proof lineage; Benjamin owns the meaning/use of its cognitive memory.

## 16. Accounting, valuation, and reconciliation

Backend implementation must treat these as core decision dependencies.

### Accounting ledger

Must eventually support:

- contributions/subscriptions;
- withdrawals/redemptions;
- distributions;
- transfers;
- fees/expenses;
- funding/financing/interest accruals;
- realized/unrealized P&L;
- positions/cash/liabilities;
- collateral/margin;
- settlement;
- corrections with provenance.

### Valuation

Must version and evidence:

- authoritative price sources;
- valuation cutoff;
- spot valuation;
- futures/derivative marks;
- stablecoin/cash-equivalent rules;
- funding/interest accrual;
- multi-currency conversion;
- stale/illiquid/missing-price handling;
- liabilities/accruals;
- NAV/equity calculation.

### Reconciliation

Must compare internal projections with external authoritative providers and expose discrepancies explicitly. Unknown/external-unavailable truth is not a zero discrepancy.

## 17. Frontend contract

### Manager Console

The manager surface is capital-first, not market-first:

- Company Command;
- Relationships;
- Capital Structures;
- Participants;
- Accounts;
- Responsibility Center;
- Capital Router;
- Decision Desk;
- Market Relationships;
- Watchman Bridge;
- The Hand Bridge;
- The Book Bridge;
- Client Reporting;
- Operations.

The frontend answers:

> **What capital exists, who owns it, what is Benjamin responsible for, what is available/committed/at risk, what paths Benjamin considered, what it decided, why, what happened, and what was actually earned?**

### Client Console

The client frontend is an authorization-aware projection of the same authoritative company model.

An individual owner may see their complete allowed account/structure economics. A pooled participant sees their own economic interest plus permitted structure activity, not another participant's private identity, contribution/redemption history, tax documents, or company/ZLJ proprietary internals.

## 18. Institutional API boundaries

### ZLJ -> Benjamin

Benjamin consumes stable qualified intelligence/economic-context objects. Benjamin does not scrape the ZLJ UI and does not receive ZLJ operator credentials.

### Benjamin -> Watchman

Benjamin submits a durable decision with Capital State, Responsibility, expected economic effect, and evidence references. Benjamin cannot mutate Watchman policy through this bridge.

### Watchman -> Hand

Only governed authorization becomes executable authority.

### Hand -> Benjamin

Benjamin receives read projections of execution, settlement, and reconciliation status. Provider credentials/signing keys remain Hand-owned.

### Book -> Benjamin

Benjamin can query authorized evidence/lineage but cannot rewrite/delete Book truth.

## 19. Front-to-back backend build order

The frontend exercise establishes the preferred backend sequence:

```text
1. Relationship
      |
2. Capital Structure
      |
3. Participant / ownership accounting
      |
4. Account / custody connections
      |
5. Authoritative accounting ledger
      |
6. Valuation + Capital State
      |
7. Responsibility
      |
8. ZLJ intelligence / economic-relationship bridge
      |
9. Candidate Path Generator + Capital Router
      |
10. Benjamin Decision
      |
11. Watchman bridge
      |
12. Hand bridge
      |
13. Book / reporting / outcome loop
```

This order teaches Benjamin **what money it is responsible for before teaching it how to transform that money**.

## 20. Certification / activation ladder

The architecture separates design knowledge from operational authority.

A concept may progress through states such as:

```text
DEFINED
  -> FRONTEND_CONTRACT_DEFINED
  -> BACKEND_CONTRACT_DEFINED
  -> IMPLEMENTED
  -> TESTED
  -> REPLAY / SHADOW QUALIFIED
  -> GOVERNED OPERATIONAL AUTHORITY
```

Different capabilities progress independently.

Example:

```text
Futures understanding       may become QUALIFIED
Futures execution           may remain DISABLED
Leverage execution          may remain DISABLED
Pooled participant model    may be DEFINED
Pooled live operations      may remain NOT ACTIVATED
```

No UI element, model capability, or research result silently grants operational authority.

## 21. Core invariants

1. **Capital Structure is the economic unit; AccountConnection is an implementation surface.**
2. **Capital State is authoritative point-in-time capital truth, not generated reasoning.**
3. **Accounting and reconciliation feed the next decision; they are part of cognition.**
4. **Responsibility = Objectives + Obligations + Authorities.**
5. **Understanding authority and execution authority are independent.**
6. **The Router selects economic transformations, not merely trading strategies.**
7. **Hard authority/solvency/liquidity constraints outrank expected return.**
8. **Spot/futures influence is multidimensional and adaptive, never one static scalar.**
9. **Participant obligations affect deployable capital and therefore Capital State.**
10. **Benjamin Decision is not Watchman authorization and is not Hand execution.**
11. **The Book must make material state transitions reconstructable.**
12. **Historical Responsibility/model/procedure/valuation versions remain reproducible.**
13. **Unknown, stale, missing, or unreconciled state is explicit; it is never silently healthy.**
14. **`HOLD` / `ABSTAIN` is a valid economic path when no qualified alternative is better.**
15. **Targeted multiplication is an objective, never a guaranteed transformation of capital.**

## 22. Current status

The manager/client frontend contracts and backend inventory are defined on the frontend-contract branch and remain synthetic/non-live. The architecture above is the target high-level system design.

Current claims do **not** include:

- accepted/live managed client capital;
- live custody authority;
- live derivatives execution;
- live leverage;
- live pooled-fund operations;
- regulatory activation/certification;
- proven router economic edge;
- guaranteed profit or capital multiplication.

The next backend milestone should begin with authoritative company/capital primitives and Capital State, not with a live trade router.
