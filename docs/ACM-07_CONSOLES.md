# ACM-07 — Manager Console and Client Console

## Objective

ACM-07 makes Benjamin observable and usable through two deliberately separate frontend surfaces:

1. **Manager Console** — institutional operating surface for Benjamin decision operations, Watchman governance state, Hand execution state, evidence health, and authorized auditors/operators.
2. **Client Console** — participant-facing surface for one participant's lawful capital-account truth, documents, notices, and proofs.

The two consoles are not role-switched views of the same application. They are separate build artifacts with separate view models so manager-only information cannot leak into a client bundle and merely be hidden by client-side permissions.

## Constitutional rule

> **A client receives no more information than is necessary to exercise their rights, understand their own participation, and verify legitimate claims.**

The Manager Console may inspect private institutional state according to role and authority. The Client Console receives only participant-scoped or intentionally public data.

The console must preserve the Epinnox organ boundary:

> **ZLJ sees. Benjamin decides. Watchman governs. The Hand executes. The Book remembers and proves.**

A UI workflow may connect these organs. It does not transfer ownership among them.

## Current phase

Both consoles currently render **demo/shadow snapshots only**. They do not represent live client assets, accepted subscriptions, live performance, or production investor records.

The first goal is to qualify information architecture, privacy boundaries, and operator workflows before ACM-01 through ACM-06 replace demo snapshots with authoritative read models.

---

# Manager Console

## Primary question

> **What does the manager need to know or decide right now?**

## Initial navigation

- **Overview** — capital, risk, data/evidence health, active work, recent decisions.
- **Research** — ZLJ intelligence, market cases, model/prediction context, and opportunities awaiting Benjamin consideration.
- **Portfolio** — positions, exposure, cash, reserves, benchmark and shadow NAV.
- **Decisions** — Benjamin decisions, abstentions, pending/revised decision work, invalidation/review conditions.
- **Watchman** — policy checks, authorizations, blocks, exposure limits, mandate health.
- **Execution** — Watchman authorization state and Hand receipts; never a strategy-authoring or self-authorizing surface.
- **Evidence** — Big Book proof health, missing lineage, reconciliation state.
- **Participants** — participant administration only for roles entitled to see it.
- **Reports** — attribution, calibration, statements, audit exports.
- **Covenant** — active mandate/policy versions and constitutional health.

## Overview read model

The first Manager Console snapshot should answer:

```text
Capital
Shadow NAV
Cash
Deployable cash
Required reserves

Risk / Governance
Current drawdown
Largest position
Gross/net exposure
Watchman authorizations / blocks

Market Intelligence
ZLJ data/model health
Active market cases
Qualified opportunities awaiting Benjamin decision

Decisions
Recent Benjamin decisions
No-trade / abstention decisions
Invalidation/review state

Operations
Pending Watchman authorizations
Hand execution failures
Reconciliation breaks

Evidence
Big Book integrity
Missing proofs / lineage
Unreviewed outcomes
```

## Manager-only information

Examples include:

- private ZLJ market intelligence, model competence, and opportunity evidence;
- private Benjamin theses and decision rationale;
- opportunity and acquisition targets;
- portfolio positions and exact exposures;
- cash/reserve state;
- Watchman reasoning and internal limits;
- pending Watchman authorizations;
- Hand execution and reconciliation detail;
- participant administration where authorized;
- internal performance attribution;
- private Big Book lineage.

None of these fields are eligible for the Client Console merely because they exist in the Manager Console.

---

# Client Console

## Primary question

> **What is true about my participation, what changed, what am I entitled to, and how can I verify it?**

## Initial navigation

- **Overview** — participant-specific account summary and status.
- **Capital Account** — contributions, withdrawals/redemptions when applicable, units/interests, participant NAV/equity.
- **Performance** — participant-authorized performance presentation and period returns.
- **Activity** — participant-scoped capital events and distributions.
- **Documents** — agreements, statements, tax documents, notices and disclosures the participant is entitled to receive.
- **Proof Center** — participant proofs and intentionally public Little Book attestations.
- **Profile & Access** — contact/security settings; secret/regulated identity material remains in restricted identity systems rather than the frontend payload.
- **Support** — governed communication channel.

## Client Console must never expose

- other participants' balances, identities, contributions or distributions;
- private ZLJ research, model stack, predictions, or opportunity queue;
- private Benjamin theses or decision reasoning;
- unreleased acquisition targets or unrealized opportunities;
- exact portfolio holdings unless a deliberate reporting policy authorizes them;
- internal Watchman thresholds or private governance/risk deliberations;
- Hand authorization/action payloads;
- unrestricted Big Book browsing;
- banking credentials, SSNs, identity documents, private keys or other `SECRET_REGULATED` data.

## Participant proof example

```text
Contribution accepted:      $25,000
Effective date:             2026-09-01
Agreement reference:        AG-229
Participant entitlement:    250.000 units
Big Book proof:             RCP-...
Document digest:            sha256:...
```

The participant may be able to verify that event without learning anything about another participant.

---

# Separate read contracts

The backend must eventually publish two independent DTO families:

```text
ManagerConsoleSnapshot
ClientConsoleSnapshot
```

A `ClientConsoleSnapshot` is **not** created by serializing a manager object and removing fields in the browser. The server/read-model boundary constructs the participant view from authorized participant-scoped sources.

This is a security invariant.

---

# Data-source progression

## ACM-07.0 — UI qualification

- static demo/shadow snapshots;
- responsive navigation and information hierarchy;
- explicit `SHADOW / DEMO` status;
- no mutation paths;
- no live money claims.

## ACM-07.1 — authoritative read models

After ACM-01 through ACM-06 mature, replace demo snapshots with read models sourced from:

- ZLJ market-intelligence/data/model APIs;
- Benjamin decision/context services;
- Watchman governance/authorization state;
- Treasury and portfolio accounting;
- The Hand execution/capability receipts;
- Big Book proof/index services;
- participant-accounting services.

Each source remains authoritative only for the truth it owns.

## ACM-07.2 — governed actions

Only after read models are qualified should the Manager Console gain mutation workflows.

Examples include:

- ask Benjamin to create/revise/reject a capital decision;
- submit a Benjamin decision to Watchman;
- display/request actions around a Watchman authorization or block without bypassing it;
- invoke an authorized Hand capability through the proper server-side bridge;
- reconcile an outcome;
- request an explicit disclosure from The Book.

Every mutation routes through the owning domain; the UI never mutates capital truth directly and never treats one organ's action as another organ's authority.

Client mutations remain narrow: profile/access requests, document acknowledgements, subscription/redemption requests when legally and operationally enabled, and support workflows. Requests do not become effective state until the governing domain accepts them.

---

# UI laws

1. Manager and client apps are separate build artifacts.
2. Client access is participant-scoped at the server/read-model boundary, not by browser hiding.
3. Every screen must identify whether data is `DEMO`, `SHADOW`, or authoritative.
4. No performance display may imply live audited performance when it is simulated.
5. No console may invent missing financial facts.
6. Stale/degraded/unavailable data must be visibly represented as such.
7. Manager actions must preserve ZLJ, Benjamin, Watchman, Hand, and Book ownership boundaries.
8. A Benjamin decision is not a Watchman authorization; a Watchman authorization is not a Hand execution.
9. Client views may expose participant proofs without exposing institution-wide private history.
10. Secret/regulated data is never embedded in ordinary frontend state.
11. Public Little Book information is explicit testimony, never an automatic projection of the Manager Console.

# Definition of done for the first slice

The first slice is complete when both frontend applications build independently and demonstrate their intended information boundaries using synthetic/shadow fixtures. No backend integration or live financial operation is required for ACM-07.0.
