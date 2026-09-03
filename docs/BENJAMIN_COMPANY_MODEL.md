# Benjamin Capital Management — Company Model v1

## Purpose

Benjamin is defined in two distinct layers that must never be conflated:

1. **Benjamin Capital Management** — the operating company and capital-management relationship layer.
2. **Benjamin Decision Engine** — the capital decision logic that operates inside an explicitly governed responsibility mandate.

The company owns relationships, capital structures, participants, accounts, mandates, reporting, and lifecycle administration. The decision engine receives qualified intelligence and a current capital state, evaluates permissible economic paths, and records a decision for Watchman review.

```text
OWNER / MANAGER
  defines responsibility and company policy
        ↓
BENJAMIN CAPITAL MANAGEMENT
  relationships / structures / participants / accounts
        ↓
RESPONSIBILITY MANDATE
  objective / targets / permissions / risk envelope
        ↓
BENJAMIN DECISION ENGINE
  evaluates candidate economic paths
        ↓
BENJAMIN.DECISION
        ↓
WATCHMAN
        ↓
HAND
        ↓
BOOK
```

## Canonical nouns

### Relationship
A governed association between Benjamin Capital Management and a person, household, trust, company, fund participant, or other legal/economic party.

A Relationship is not an account. One relationship may own or participate in multiple Capital Structures.

### Capital Structure
The economic container Benjamin is responsible for managing. Initial end-state structure types are:

- `INDIVIDUAL_MANAGED_ACCOUNT`
- `HOUSEHOLD_OR_JOINT_PORTFOLIO`
- `ENTITY_OR_TREASURY_ACCOUNT`
- `POOLED_PORTFOLIO`

A Capital Structure has one active Responsibility version, one or more Accounts, and one or more Participants where applicable.

### Participant
A person or entity with an economic, beneficial, governance, or reporting interest in a Capital Structure.

Participant records must distinguish:

- economic interest;
- beneficial ownership where applicable;
- contribution/redemption history;
- permissions;
- reporting rights;
- privacy boundaries.

A participant is not implicitly permitted to change the shared mandate of a pooled structure.

### Account
An externally custodied or otherwise authoritative financial account/wallet connection belonging to a Capital Structure.

Account identity is distinct from the economic Capital Structure so one structure may span multiple custodians, brokers, exchanges, or wallets without losing one governed responsibility.

### Responsibility
A versioned statement of what Benjamin is responsible for accomplishing with a Capital Structure and what authority exists to pursue it.

A Responsibility contains:

- mission and objective precedence;
- measurable targets;
- permitted horizons;
- markets Benjamin may understand;
- markets Benjamin may execute in;
- allowed economic actions;
- strategy authorities;
- liquidity requirements;
- risk envelope;
- autonomy level;
- emergency rules;
- effective-at boundary and immutable prior versions.

### Target
A measurable desired state or trajectory such as return objective, liquidity reserve, maximum drawdown, volatility range, capital utilization, or income target.

Targets are objectives, not guarantees.

### Capability Authority
A two-axis authority model separating **understanding** from **execution**.

Example:

```text
Crypto futures: UNDERSTAND = YES
Crypto futures: EXECUTE = NO
```

Benjamin may use an economic relationship as information while remaining prohibited from expressing that exposure.

### Candidate Economic Path
One feasible transformation Benjamin may consider for a Capital Structure, such as:

- hold cash;
- increase/decrease spot exposure;
- exit exposure;
- rebalance;
- hedge;
- relative-value or basis structure;
- spread/paired exposure;
- future derivative or collateral actions once authorized.

A Candidate Economic Path is not an order. It is an evaluated capital alternative.

### Path Evaluation
The durable explanation of why a Candidate Economic Path is feasible or blocked and how it compares with alternatives.

Evaluation dimensions may include expected benefit, downside, evidence quality, competence, liquidity, capital efficiency, financing, correlation, execution cost, tax sensitivity, uncertainty, mandate fit, and portfolio effects.

Hard constraints are lexicographic: a path cannot compensate for an authority or mandate violation with a higher expected return.

### Benjamin Decision
The selected capital path after evaluating the current state and permissible alternatives. It records the selected path, alternatives, reasons, expected portfolio effect, invalidation conditions, responsibility version, evidence references, and Watchman status.

### Capital Activity
Any economic change attributable to the structure or participant: contribution, redemption, fee, distribution, transfer, execution, settlement, reconciliation, realized P&L, unrealized P&L, or allocation change.

### Statement
A participant/account/structure-scoped projection of authoritative Book/accounting records over a defined reporting period.

## Relationship rules

```text
Relationship
  ├── may own or control 0..N Capital Structures
  └── may participate in 0..N Capital Structures

Capital Structure
  ├── has 1 active Responsibility version
  ├── has 1..N Accounts
  ├── has 1..N Participants where applicable
  └── has 0..N Benjamin Decisions

Responsibility
  ├── defines objectives
  ├── defines targets
  ├── defines understanding authority
  ├── defines execution authority
  ├── defines risk/liquidity boundaries
  └── is immutable once superseded

Benjamin Decision Engine
  ├── cannot rewrite Responsibility
  ├── cannot grant itself execution authority
  ├── cannot bypass Watchman
  └── cannot execute through Hand directly
```

## Economic market model

Benjamin must be designed to understand economic relationships between instruments rather than reducing markets to BUY/SELL/LONG/SHORT verbs.

For spot/futures, the end-state reasoning surface includes:

### Spot evidence
- underlying turnover;
- order-book depth and spread;
- aggressive flow;
- cross-venue agreement/dislocation;
- realized volatility;
- liquidity and venue quality.

### Futures/derivatives evidence
- notional activity;
- open interest;
- basis and term structure;
- funding/financing;
- liquidations and leverage pressure;
- mark/index divergence;
- maturity/roll behavior;
- lead/lag relationship with spot.

### Distinct weights
Benjamin/ZLJ must not use one static `futures_weight`. At minimum the architecture may distinguish:

- predictive information weight;
- regime information weight;
- risk/fragility weight;
- capital-confidence weight;
- execution suitability weight.

A derivative signal may be highly predictive while simultaneously reducing capital confidence because the move is leverage-driven or fragile.

## Owner/operator boundary

The owner/operator defines **responsibility**, not day-to-day market conclusions.

The owner controls:

1. what Benjamin is trying to achieve;
2. what Benjamin may understand and consider;
3. what Benjamin may execute;
4. how much risk/liquidity/capital authority exists;
5. which responsibility version is active.

The owner does not normally override model weights, fabricate market evidence, or issue undocumented trade instructions through the decision engine.

## Frontend contract

The manager console must make the following first-class and visible:

- Company Command;
- Relationships;
- Capital Structures;
- Participants;
- Accounts;
- Responsibility Center;
- Capital Router;
- Decision Desk;
- Portfolio / positions / cash / liquidity;
- Markets and economic relationships;
- Watchman status;
- Hand execution status;
- Book evidence;
- Client reporting and operations.

The client console must be a scoped projection of the same authoritative model, exposing a participant's/account owner's capital, performance, activity, mandate/responsibility, decisions affecting their money, Watchman protections, executions, fees, statements, and evidence without exposing other participants' private information or proprietary ZLJ internals.

## V1 frontend status

This document is a **product/domain contract**. It defines the intended end-state vocabulary and does not by itself activate live custody, derivatives execution, leverage, pooled-fund operations, or any regulated activity. Operational capability remains separately gated and must be implemented, authorized, and certified before use.
