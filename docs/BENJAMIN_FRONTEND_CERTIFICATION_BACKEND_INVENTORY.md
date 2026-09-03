# Benjamin Frontend Contract Certification + Backend Inventory v1

## Certification claim

This document certifies the **product/domain frontend contract**, not live investment operations, regulatory status, custody, execution, or profitability.

As of this contract version, Benjamin's manager and client frontends define the required human-visible concepts for:

- capital-management relationships;
- individual, household/joint, entity/treasury, and pooled capital structures;
- participant economic/reporting rights;
- externally authoritative accounts/custody connections;
- owner-defined, versioned Benjamin Responsibilities;
- economic-path routing;
- spot/futures economic-relationship interpretation;
- durable Benjamin decisions and alternatives;
- Watchman, Hand, and Book institutional handoffs;
- participant/account-scoped client reporting;
- funding, accounting, reconciliation, restriction, reporting, redemption, and closure lifecycle expectations.

All current financial figures, market values, path scores, and activity records in the new frontend contract are synthetic preview data unless backed later by authoritative services.

## Constitutional split

```text
ZLJ sees
  ↓
Benjamin Capital Management defines the governed capital relationship/container
  ↓
Owner-approved Responsibility defines Benjamin's job and authority
  ↓
Benjamin Decision Engine evaluates permissible economic paths
  ↓
Benjamin records BENJAMIN.DECISION
  ↓
Watchman authorizes or blocks
  ↓
The Hand executes an authorized external action
  ↓
The Book preserves/proves the material record
```

Benjamin cannot self-authorize capital action, cannot grant itself execution authority, and cannot convert a forecast into accounting truth.

---

# 1. Canonical backend aggregates

## Relationship

Must represent a person, household, trust, company/entity, or other lawful/economic party that has a governed relationship with Benjamin Capital Management.

Required backend capabilities:

- create/invite/onboard;
- identity and relationship status;
- contact/communication preferences;
- legal/entity type and future eligibility/compliance references;
- ownership/control relationships;
- restrictions/suspension/closure;
- document/agreement references;
- privacy and access-control projection.

A Relationship is not an Account.

## CapitalStructure

The economic container Benjamin is responsible for managing.

Initial end-state types:

- `INDIVIDUAL_MANAGED_ACCOUNT`
- `HOUSEHOLD_OR_JOINT_PORTFOLIO`
- `ENTITY_OR_TREASURY_ACCOUNT`
- `POOLED_PORTFOLIO`

Required capabilities:

- create/version/status/close;
- base currency/accounting currency;
- owners/participants;
- attached authoritative accounts/wallets;
- active Responsibility;
- valuation policy;
- liquidity/redemption policy;
- accounting ledger references;
- current NAV/equity/cash/exposure projection;
- restriction state;
- lifecycle timestamps.

## Participant

Represents an economic, beneficial, governance, or reporting interest in a CapitalStructure.

Required capabilities:

- participation lifecycle;
- economic interest or unit ownership;
- beneficial-owner/control references where applicable;
- contribution/redemption/distribution history;
- reporting rights;
- permissions;
- privacy scope;
- statement/tax-document projection.

A pooled participant cannot silently issue a separate trade mandate into a shared pool.

## AccountConnection

Represents an externally authoritative brokerage, exchange, FCM, custodian, bank, or future wallet/custody connection.

Required capabilities:

- provider-neutral identity;
- owner/structure binding;
- asset/market capabilities;
- read/trade/transfer/withdraw permission distinctions;
- credential/key reference only, never secret material in ordinary records;
- balances/positions/orders/fills/transfers retrieval;
- connection freshness/health;
- reconciliation state;
- restriction/disable lifecycle.

An AccountConnection is not the economic CapitalStructure.

## Responsibility

Versioned owner/operator definition of what Benjamin must accomplish and what authority exists to pursue it.

Must contain at minimum:

- mission;
- objective precedence;
- measurable targets;
- autonomy level;
- permitted horizons;
- market-understanding authority;
- market-execution authority;
- economic-action authority;
- strategy authority;
- risk envelope;
- liquidity requirements;
- leverage/short/derivative permissions;
- capital concentration limits;
- emergency/restriction rules;
- effective time;
- immutable superseded versions.

`UNDERSTAND` and `EXECUTE` must be independent permissions.

## CandidateEconomicPath

A possible transformation of capital, not an order.

Examples include:

- hold cash;
- increase/decrease/exit spot exposure;
- rebalance;
- hedge;
- relative-value/basis path;
- pair/spread;
- future derivative exposure;
- roll/convert/collateral action where authorized.

A path must record feasibility and reasons for block/research-only/permission.

## PathEvaluation

Must bind a CandidateEconomicPath to:

- CapitalStructure state;
- Responsibility version;
- portfolio/exposure state;
- ZLJ intelligence/evidence references;
- economic-relationship/context references;
- expected benefit and downside distributions/scenarios;
- evidence/competence quality;
- liquidity impact;
- concentration/correlation impact;
- capital efficiency;
- financing/funding/carry;
- execution costs/slippage;
- fees/tax sensitivity where applicable;
- uncertainty;
- authority/operational availability;
- deterministic reasons for any hard block.

Hard constraints are lexicographic. A higher expected return cannot compensate for an authority, survival, liquidity, or mandate violation.

## BenjaminDecision

Must bind:

- selected path;
- alternatives considered;
- Responsibility version;
- current capital/portfolio state;
- ZLJ intelligence references;
- economic-relationship references;
- expected portfolio effect;
- invalidation conditions;
- confidence/uncertainty where justified;
- creation/known-at time;
- Watchman state;
- evidence/receipt identity.

A BenjaminDecision is not an authorization or an execution.

---

# 2. Economic intelligence contracts

Benjamin must reason across economic relationships rather than instrument names alone.

## SpotState

Potential fields/families:

- provider-neutral instrument identity;
- venue;
- price/mid/reference;
- spread/depth;
- liquidity;
- aggressive/reported flow;
- volume/turnover;
- realized volatility;
- cross-venue agreement/dislocation;
- freshness/data quality;
- provenance.

## DerivativeState

Potential fields/families:

- underlying economic identity;
- contract/perpetual identity;
- maturity/expiry/settlement type;
- mark/index/reference price;
- notional volume;
- open interest;
- basis;
- annualized basis where meaningful;
- funding/financing;
- term structure;
- liquidations;
- leverage/positioning proxies;
- margin/collateral requirements where available;
- roll behavior;
- liquidity/spread/depth;
- freshness/data quality;
- provenance.

## EconomicRelationshipState

Must be point-in-time and evidence-bound.

Potential fields/families:

- spot/futures basis state;
- basis trend/dispersion;
- lead/lag relationship;
- correlation/divergence;
- spot/futures liquidity relationship;
- leverage expansion/contraction;
- liquidation/funding stress;
- price-discovery confidence;
- term-structure regime;
- cross-market contradiction;
- freshness/quality.

## Adaptive weight families

Do not implement one static `futures_weight`.

At minimum support separately governed/evidenced interpretation weights for:

1. predictive information;
2. regime information;
3. fragility/risk information;
4. capital-confidence effect;
5. execution suitability.

A futures market may carry high predictive information while simultaneously lowering capital confidence because leverage/funding/liquidation conditions are fragile.

Formula/policy changes must be versioned and cannot silently rewrite historical decisions.

---

# 3. Accounting and capital truth

This is a mandatory backend domain. The frontend is never the accounting authority.

## Authoritative capital ledger

Must support:

- contributions/deposits/subscriptions;
- withdrawals/redemptions;
- distributions;
- transfers;
- fees/expenses;
- interest/funding/financing accruals;
- realized P&L;
- unrealized P&L;
- cash;
- positions;
- liabilities;
- collateral/margin when applicable;
- settlement;
- corrections/adjustments with provenance.

## Pooled participant accounting

Before pooled capital can be operational, support unit/NAV accounting or an equivalent participant-capital-account method that prevents economic leakage among participants.

Required concepts:

- valuation cutoff;
- unit/share issuance;
- unit/share redemption;
- participant capital account;
- entry/exit NAV;
- fee allocation;
- gain/loss allocation;
- distribution allocation;
- rounding policy;
- late/stale valuation handling;
- corrections without rewriting prior evidence.

## Valuation policy

Must explicitly define:

- authoritative pricing sources;
- cutoff/as-of time;
- spot asset valuation;
- futures/derivative mark policy;
- funding/interest accrual;
- stablecoin/cash-equivalent valuation;
- multi-currency conversion;
- illiquid/stale price handling;
- disputed/missing price handling;
- liabilities/fees accrued;
- NAV/equity calculation version;
- reproducible valuation evidence.

## Performance methodology

Must distinguish:

- portfolio return vs participant return;
- cash-flow effects;
- realized vs unrealized P&L;
- gross vs net performance;
- fees/costs;
- time-weighted / money-weighted methods where appropriate;
- benchmark comparison where used;
- period/cutoff/timezone;
- corrections/restatements.

Expected-return forecasts are never booked performance.

---

# 4. Money movement and custody boundaries

Backend must distinguish:

- deposit/contribution;
- withdrawal/redemption;
- distribution;
- same-owner internal transfer;
- third-party transfer;
- trading authority;
- transfer authority;
- withdrawal authority;
- custody/possession.

No trading credential or Benjamin Responsibility may silently imply arbitrary withdrawal authority.

Every money-movement request must eventually have:

- authenticated principal;
- economic owner/participant;
- source/destination;
- amount/asset;
- authority basis;
- status lifecycle;
- external provider result;
- reconciliation;
- Book receipt.

---

# 5. Fees, expenses, and conflicts

Backend inventory includes:

- fee schedules/versioning;
- management/advisory fee accrual where applicable;
- future performance/incentive fee support only when lawfully activated;
- high-water-mark/hurdle support if later required;
- provider/trading costs;
- financing/funding costs;
- account/structure expenses;
- participant allocation;
- fee reversals/corrections;
- invoice/statement records;
- company receivable vs client asset separation.

Benjamin/company principal capital, client separate-account capital, pooled investor capital, operating cash, and fee receivables must never be represented as one undifferentiated balance.

Future co-investment/principal trading requires a separate conflict and allocation policy.

---

# 6. Reconciliation and operations

Required operational contracts:

- provider/custodian balance reconciliation;
- position reconciliation;
- order/fill reconciliation;
- cash/transfer reconciliation;
- participant accounting reconciliation;
- fee reconciliation;
- Book receipt reconciliation;
- stale/disconnected provider handling;
- duplicate/missing event detection;
- exception ownership/status;
- correction workflow;
- restart/replay/idempotency semantics;
- immutable history after restriction/closure.

Reconciliation discrepancies must be visible rather than converted into zero/healthy defaults.

---

# 7. Account and relationship lifecycle

Canonical lifecycle states must be explicitly modeled rather than inferred from UI labels.

Minimum lifecycle:

```text
INVITED
→ ONBOARDING
→ RELATIONSHIP_ESTABLISHED
→ STRUCTURE_CREATED
→ ACCOUNT_CONNECTED
→ RESPONSIBILITY_READY
→ FUNDING_PENDING
→ ACTIVE
→ RESTRICTED / SUSPENDED when necessary
→ CLOSING
→ CLOSED
```

Pooled participation additionally needs:

```text
INVITED
→ ELIGIBILITY / AGREEMENT READY (future policy/regulatory gate)
→ SUBSCRIPTION_PENDING
→ CAPITAL_PENDING
→ PARTICIPANT_ACTIVE
→ REDEMPTION_PENDING
→ REDEEMED / CLOSED
```

Future compliance/registration requirements are separate activation gates and must not be implied merely because the domain object exists.

---

# 8. Client reporting and privacy projection

The client API must never be a raw mirror of manager/domain tables.

It needs explicit authorization-aware projections for:

- current capital/economic interest;
- contributions/redemptions/distributions;
- performance;
- positions/activity where disclosure is permitted;
- fees/costs;
- active Responsibility/mandate;
- Benjamin decisions affecting the client's money;
- Watchman protections/blocks affecting the client's money;
- Hand executions/receipts affecting the client's money;
- Book evidence scoped to that relationship/participant;
- formal statements/documents/tax records;
- notices/communications.

Pooled participant projections must exclude:

- another participant's identity/PII;
- another participant's private contribution/redemption history;
- another participant's private documents/tax records;
- private company operational data;
- proprietary ZLJ model/source internals unless explicitly disclosed later.

---

# 9. Institutional bridge contracts

## ZLJ → Benjamin

Benjamin should consume stable `ZLJ.INTELLIGENCE` and economic-context contracts, not scrape ZLJ's operator UI or depend on its internal engineering representations.

Required read surfaces eventually include:

- current intelligence by economic instrument/horizon;
- intelligence by id;
- context/economic relationship references;
- competence/evidence lineage as authorized;
- known-at/valid-until/freshness/qualification state.

Benjamin must not receive ZLJ operator-command credentials.

## Benjamin → Watchman

Required:

- immutable BenjaminDecision identity/body/hash;
- CapitalStructure/Responsibility references;
- proposed economic/capital effect;
- required authority;
- evidence lineage;
- Watchman authorization/block response reference.

Benjamin cannot mutate Watchman policy through this bridge.

## Watchman → Hand

Benjamin may observe the linked result but must not become the transport for bypassing Watchman.

## Hand → Benjamin

Required read projection:

- authorized-action id;
- provider-neutral capability;
- submitted/accepted/partial/filled/failed/cancelled status;
- external refs;
- fills/settlement;
- reconciliation;
- receipt/evidence references.

Provider credentials/signing keys remain Hand-owned.

## Book → Benjamin

Required query/projection support for:

- decision evidence;
- authorization evidence;
- execution receipts;
- accounting outcomes;
- causal lineage;
- verification status.

Benjamin cannot rewrite/delete Book evidence.

---

# 10. Authorization / roles expected by frontend

At minimum distinguish:

## Company owner / system owner

May configure company-level policy, approve Responsibility templates/changes, administer relationships/structures subject to later governance/compliance policy, inspect institutional bridges, and manage operations.

Does not gain Hand/Watchman authority merely by using Benjamin.

## Portfolio/relationship manager

Scoped ability to administer assigned relationships, structures, reporting, and permitted Responsibility workflows.

## Operations

Scoped ability over onboarding status, account connectivity, funding/reconciliation/reporting workflows without market-decision authority unless separately granted.

## Client / account owner

May see only authorized own-account/structure projections and permitted requests.

## Pooled participant

May see own economic interest plus permitted shared-structure reporting, never another participant's private records.

## Benjamin service identity

Machine authority to read needed ZLJ intelligence and produce Benjamin decision artifacts. No human console superuser equivalence.

---

# 11. Indicative API inventory

Exact route naming may change during backend design, but every frontend surface implies these operations.

## Relationships

```text
POST   /relationships
GET    /relationships
GET    /relationships/{id}
PATCH  /relationships/{id}
POST   /relationships/{id}/restrict
POST   /relationships/{id}/close
GET    /relationships/{id}/documents
```

## Capital structures

```text
POST   /capital-structures
GET    /capital-structures
GET    /capital-structures/{id}
PATCH  /capital-structures/{id}
GET    /capital-structures/{id}/state
GET    /capital-structures/{id}/accounts
GET    /capital-structures/{id}/participants
POST   /capital-structures/{id}/restrict
POST   /capital-structures/{id}/close
```

## Participants

```text
POST   /capital-structures/{id}/participants
GET    /participants/{id}
GET    /participants/{id}/capital-account
GET    /participants/{id}/activity
GET    /participants/{id}/statements
POST   /participants/{id}/redemption-requests
```

## Accounts/custody connections

```text
POST   /capital-structures/{id}/accounts
GET    /accounts/{id}
GET    /accounts/{id}/state
GET    /accounts/{id}/positions
GET    /accounts/{id}/cash
GET    /accounts/{id}/activity
GET    /accounts/{id}/reconciliation
POST   /accounts/{id}/disable
```

## Responsibilities

```text
POST   /capital-structures/{id}/responsibilities
GET    /capital-structures/{id}/responsibilities
GET    /responsibilities/{id}
POST   /responsibilities/{id}/activate
POST   /responsibilities/{id}/supersede
GET    /responsibilities/{id}/diff
```

## Router / decisions

```text
GET    /capital-structures/{id}/router-state
POST   /capital-structures/{id}/path-evaluations
GET    /path-evaluations/{id}
GET    /capital-structures/{id}/candidate-paths
POST   /capital-structures/{id}/decisions
GET    /decisions/{id}
GET    /decisions/{id}/alternatives
GET    /decisions/{id}/lineage
```

The production backend may separate compute commands from read projections rather than expose unrestricted synchronous `POST` calls directly.

## Accounting / money movement

```text
GET    /capital-structures/{id}/valuation
GET    /capital-structures/{id}/ledger
GET    /capital-structures/{id}/performance
POST   /capital-structures/{id}/contribution-requests
POST   /capital-structures/{id}/redemption-requests
POST   /capital-structures/{id}/distribution-requests
GET    /capital-activities/{id}
GET    /reconciliations/{id}
```

## Reporting

```text
GET    /client/me/capital
GET    /client/me/participation
GET    /client/me/performance
GET    /client/me/activity
GET    /client/me/decisions
GET    /client/me/responsibility
GET    /client/me/protection
GET    /client/me/executions
GET    /client/me/evidence
GET    /client/me/statements
```

Client endpoints must resolve scope from authenticated identity rather than accept arbitrary participant ids from the browser.

---

# 12. Important end-state domains not yet operationally activated

These are intentionally present in the design inventory so they are not forgotten later:

- futures/derivative execution;
- leverage/margin/collateral;
- short exposure;
- futures roll/expiry/settlement;
- perpetual funding;
- basis/relative-value strategies;
- options/FX/additional asset classes;
- multi-currency accounting;
- on-chain wallets, MPC/multisig, smart-contract custody paths;
- lending/borrowing/yield/collateral systems;
- tax-lot accounting;
- corporate actions for securities;
- crypto forks/airdrops/asset migrations where applicable;
- external transfers and withdrawal policy;
- principal/client allocation and conflicts;
- disaster recovery/business continuity;
- formal regulatory/compliance reporting;
- jurisdiction/product eligibility gates;
- production identity/MFA/session/role administration;
- legal agreements/e-signatures/disclosures;
- performance-fee/high-water-mark logic if ever lawfully offered.

Being listed here does not mean enabled or legally available.

---

# 13. Frontend surface certification matrix

| Surface | Core contract defined | Synthetic/live distinction | Primary backend dependency | Authority boundary explicit |
|---|---|---|---|---|
| Company Command | YES | YES | aggregate projections | YES |
| Relationships | YES | YES | Relationship service | YES |
| Capital Structures | YES | YES | CapitalStructure service | YES |
| Participants | YES | YES | Participant accounting | YES |
| Accounts | YES | YES | custody/provider adapters | YES |
| Responsibility Center | YES | YES | versioned Responsibility service | YES |
| Capital Router | YES | YES | path evaluation engine | YES |
| Decision Desk | YES | YES | BenjaminDecision journal | YES |
| Market Relationships | YES | YES | ZLJ intelligence/context | YES |
| Watchman Bridge | YES | YES | authorization projection | YES |
| The Hand Bridge | YES | YES | execution/reconciliation projection | YES |
| The Book Bridge | YES | YES | evidence/lineage query | YES |
| Client Reporting | YES | YES | accounting + projection service | YES |
| Operations | YES | YES | lifecycle/reconciliation services | YES |
| Client My Capital | YES | YES | client-scoped accounting projection | YES |
| Client Participation | YES | YES | participant capital accounts | YES |
| Client Performance | YES | YES | accounting/performance service | YES |
| Client Activity | YES | YES | Book/account activity | YES |
| Client Benjamin | YES | YES | decision explanation projection | YES |
| Client Responsibility | YES | YES | responsibility projection | YES |
| Client Watchman | YES | YES | governance projection | YES |
| Client Executions | YES | YES | Hand receipt projection | YES |
| Client Book | YES | YES | client-scoped evidence | YES |
| Client Statements | YES | YES | report/document service | YES |

## Result

**FRONTEND_CONTRACT_DEFINED**

This result means the end-state Benjamin capital-management user experience is sufficiently defined to drive backend decomposition without treating the existing synthetic preview as operational financial software.

The next engineering milestone should be to convert this inventory into backend domain contracts and data ownership boundaries, starting with Relationship + CapitalStructure + Participant/Accounting + Responsibility before implementing the live Router.
