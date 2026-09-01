# Benjamin

> **Epinnox sees. Benjamin decides. The Watchman guards. The Hand executes. The Book remembers. The spoil is accounted for before it is divided.**

Benjamin is the capital-management control plane. It owns investment authority, portfolio intent, deterministic risk gates, Treasury policy, and future fund operations. It does **not** own market intelligence, execution, or the sovereign evidence ledger.

## The body

- **Epinnox / The Eyes** — observes and analyzes; publishes its own analytical evidence to The Book.
- **The Steward / The Mind** — accepts, modifies, or rejects recommendations.
- **The Watchman / The Guard** — deterministic risk, mandate, compliance, and jurisdiction controls.
- **Benjamin Authority** — creates a bounded execution authorization only after Steward approval and Watchman PASS.
- **The Hand** — separate repository; executes exact authorized instructions.
- **The Book / Memory** — separate repository `Geo222222/the-book`; verifies signed evidence from every organ and anchors proofs to blockchain infrastructure.
- **Treasury** — future deployable-capital and reserve authority.
- **The Spoil** — future realized-value accounting domain. Principal is never spoil.
- **The Portion** — future entitlement and distribution policy.
- **The Covenant** — rules every Benjamin component must obey.
- **Firstfruits** — first fund configuration; not a separate software system.

## Evidence-required lifecycle

```text
Epinnox analysis
      |
      v
EPINNOX.RECOMMENDATION -----> The Book receipt
      |
      v
Benjamin Steward Decision --> BENJAMIN.DECISION ------> The Book
      |
      v
Watchman Evaluation --------> BENJAMIN.RISK ----------> The Book
      |
 PASS | BLOCK
      |
      v
Benjamin Authorization -----> BENJAMIN.AUTHORIZATION -> The Book
      |
      v
AuthorizedExecutionRequest
      |
      v
The Hand
      |
      v
HAND.EXECUTION --------------> The Book
```

A recommendation without an Epinnox Book receipt is not eligible for the evidence-required control-plane path. An authorization is not handed to The Hand until Benjamin's decision, risk result, and authorization have each produced Book evidence lineage.

## Repository boundary

Benjamin no longer contains an internal `Book` ledger. `src/benjamin/evidence.py` defines only the producer-side gateway contract to the sovereign Book repository. The Book owns signature verification, append-only history, lineage, Merkle roots, and blockchain anchoring.

## Current milestone: B1 — Evidence-aware Control Plane

B1 adds an evidence-required orchestration path while preserving the B0 pure domain functions for deterministic testing. No live broker, investor onboarding, fund token, or public blockchain writer exists here.

## Status

**FOUNDATION — NO LIVE MONEY OR EXECUTION.**
