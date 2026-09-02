# Benjamin

> **Epinnox sees. Benjamin decides. The Watchman guards. The Hand executes. The Big Book proves. The Little Book testifies. The spoil is accounted for before it is divided.**

Benjamin is the capital-management control plane. It owns capital truth: investment authority, portfolio intent, deterministic risk gates, Treasury policy, fund operations, and eventually the accounting of spoil and portion.

Benjamin does **not** own market intelligence, execution, stewardship truth, or public disclosure infrastructure.

## The body

- **Epinnox / The Eyes** — observes markets, researches, and recommends.
- **The Steward / The Mind** — accepts, modifies, or rejects recommendations.
- **The Watchman / The Guard** — deterministic risk, mandate, compliance, and jurisdiction controls.
- **Benjamin Authority** — creates a bounded execution authorization only after Steward approval and Watchman PASS.
- **The Hand** — separate repository; performs exact authorized execution.
- **The Big Book** — private authoritative proof history in `Geo222222/the-book`.
- **The Little Book** — public verification surface operated by The Book; never an automatic export of Benjamin state.
- **The Vault** — governed storage for source evidence that should not become ledger payloads.
- **Treasury** — deployable capital, cash, liquidity, and reserves.
- **The Spoil** — realized economic value after losses, fees, obligations, and required reserves. Principal is never spoil.
- **The Portion** — entitlement and distribution policy.
- **The Covenant** — rules every Benjamin component must obey.
- **Firstfruits** — first fund configuration; not a separate software system.

For the concrete operating questions, example inputs/outputs, prohibitions, and the complete morning-to-evening lifecycle for each role, see **[`docs/OPERATING_ROLES.md`](docs/OPERATING_ROLES.md)**. That document is the canonical human-readable role guide.

## Future cognitive architecture

Benjamin's long-term decision intelligence is explicitly planned as a **composable, evidence-driven cognitive system**, not a monolithic trading model and not an unconstrained LLM.

The future design allows Benjamin to consume typed market, research, machine-learning, portfolio, risk, cost, and historical-memory objects; qualify their provenance and competence; reason over disagreements and competing hypotheses; and emit a typed decision proposal. Existing Watchman/Governor and authorization boundaries remain downstream.

The architecture requires three distinct forms of memory:

- **Semantic memory** — what Benjamin knows: durable strategy, market, research, policy, capability, and validated lesson knowledge.
- **Episodic memory** — what happened: timestamped market cases, predictions, decisions, outcomes, errors, and reasoning trajectories.
- **Procedural memory** — how Benjamin reasons: governed decision methods, evidence-handling procedures, abstention rules, and escalation logic.

Z Look Jamaican may later provide structured market-intelligence, state, story, model, prediction, and opportunity objects to Benjamin, but those objects remain evidence inputs rather than capital authority.

The plan also defines model objects, multi-outcome prediction objects, a contextual model-competence router, calibration and drift tracking, an empirical self-model, explicit disagreement records, and controlled model succession so Benjamin can learn continuously without silently mutating a qualified production brain.

See **[`docs/FUTURE_COGNITIVE_ARCHITECTURE.md`](docs/FUTURE_COGNITIVE_ARCHITECTURE.md)**. This is a future architectural contract only; it does not activate live reasoning, model promotion, or execution.

## ACM-07 consoles

Benjamin now has two deliberately separate frontend applications:

```text
apps/manager-console
apps/client-console
```

The **Manager Console** is the internal operating surface for research, portfolio state, Steward decisions, Watchman results, authorization/execution status, evidence health, reporting, and Covenant health.

The **Client Console** is a participant-scoped surface for that participant's own capital account, authorized performance view, activity, documents, notices, and proofs.

The Client Console is **not** a filtered Manager Console. It has a separate build and must eventually receive a separate server-side participant read model so manager-only information never enters the client payload merely to be hidden in the browser.

The current ACM-07.0 implementation uses synthetic shadow fixtures only and displays that status prominently. It does not represent accepted subscriptions, live client assets, live performance, or production investor records.

See **[`docs/ACM-07_CONSOLES.md`](docs/ACM-07_CONSOLES.md)** and **[`contracts/console-view-policy.json`](contracts/console-view-policy.json)** for the information architecture and privacy invariants.

Run locally after installing Node dependencies:

```bash
npm install
npm run dev:manager
```

or in a second terminal:

```bash
npm run dev:client
```

Build both independently with:

```bash
npm run build:consoles
```

Console builds are part of Constitutional CI alongside the Python kernel tests.

## Privacy principle

> **Everything material must be provable. Benjamin does not publish everything it knows.**

Portfolio positions, strategies, opportunities, acquisition targets, valuations, counterparties, tax information, banking information, risk state, and internal deliberations are private by default.

Current decision, risk, and authorization evidence is classified `CONFIDENTIAL_EVIDENCE` and is published only to the **Big Book** with scoped readers. There is no automatic path to the Little Book.

## Private evidence-required lifecycle

```text
Epinnox analysis
      |
      v
EPINNOX.RECOMMENDATION -----> private Big Book receipt
      |
      v
Benjamin Steward Decision --> BENJAMIN.DECISION ------> Big Book
      |
      v
Watchman Evaluation --------> BENJAMIN.RISK ----------> Big Book
      |
 PASS | BLOCK
      |
      v
Benjamin Authorization -----> BENJAMIN.AUTHORIZATION -> Big Book
      |
      v
AuthorizedExecutionRequest
      |
      v
The Hand
      |
      v
HAND.EXECUTION --------------> Big Book
```

A recommendation without required Epinnox provenance is not eligible for the evidence-required control-plane path. An authorization is not handed to The Hand until Benjamin's decision, risk result, and authorization have each produced private Big Book lineage.

## Public verification is separate

When the outside world needs to verify a legitimate claim, Benjamin does not expose its private records. A separate disclosure decision may produce a minimum-necessary Little Book attestation derived from a Big Book commitment.

Examples include a public authority credential, intentionally disclosed asset claim, or institutional state commitment.

The Little Book must never become sufficient to reconstruct Benjamin's private portfolio or institutional wealth.

## Repository boundary

`src/benjamin/evidence.py` defines the producer-side **Big Book** gateway contract. It classifies proof drafts and visibility before publication. The Book owns proof verification, private append-only history, least-privilege reads, Merkle/state commitments, and the public Little Book disclosure surface.

See `PRIVACY.md`, `docs/EVIDENCE_BOUNDARY.md`, `docs/OPERATING_ROLES.md`, `docs/FUTURE_COGNITIVE_ARCHITECTURE.md`, `docs/ACM-07_CONSOLES.md`, `contracts/privacy-defaults.json`, and `contracts/console-view-policy.json`.

## Current milestone

**B1.1 + ACM-07.0 — Privacy-scoped evidence-aware control plane with separately built Manager and Client console shells.**

No live broker, investor onboarding, tokenized fund ownership, production private chain, public-chain writer, live cognitive reasoner, continuously adapting production model, or live client capital exists here yet.

## Status

**FOUNDATION / SHADOW UI — NO LIVE MONEY OR EXECUTION.**
