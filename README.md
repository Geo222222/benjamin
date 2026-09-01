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

See `PRIVACY.md`, `docs/EVIDENCE_BOUNDARY.md`, `docs/OPERATING_ROLES.md`, and `contracts/privacy-defaults.json`.

## Current milestone

**B1.1 — Privacy-scoped evidence-aware control plane.**

No live broker, investor onboarding, tokenized fund ownership, production private chain, or public-chain writer exists here yet.

## Status

**FOUNDATION — NO LIVE MONEY OR EXECUTION.**
