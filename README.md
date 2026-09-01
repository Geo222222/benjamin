# Benjamin

> **Epinnox sees. Benjamin decides. The Watchman guards. The Hand executes. The Book remembers. The spoil is accounted for before it is divided.**

Benjamin is the capital-management control plane. It is deliberately separate from market intelligence and from execution.

## Vocabulary

- **Epinnox / The Eyes** — observes markets, produces evidence-backed recommendations. It has no capital authority.
- **The Steward / The Mind** — accepts, modifies, or rejects recommendations and sets portfolio intent.
- **The Watchman / The Guard** — deterministic risk, mandate, compliance, and jurisdiction controls. A Watchman block means no execution.
- **The Hand** — separate execution system. It may execute only a valid, unexpired authorization created by Benjamin.
- **The Book / Memory** — append-only evidence of recommendations, decisions, risk results, authorizations, executions, ownership, and corrections.
- **Treasury** — determines deployable capital after reserves and obligations.
- **The Spoil** — realized economic value after losses, fees, expenses, and required reserves. Investor principal is never spoil.
- **The Portion** — applies predetermined entitlement and distribution policy to distributable spoil.
- **The Covenant** — invariants that every component must obey.
- **Firstfruits** — the first fund configuration; a fund instance, not a separate software system.

## Hard boundaries

1. Epinnox may recommend; it may not authorize or execute.
2. The Steward may approve portfolio intent; it may not bypass Watchman.
3. Watchman may block an otherwise approved decision.
4. Benjamin may authorize; it may not place broker or exchange orders.
5. The Hand may execute; it may not originate or modify investment intent.
6. The Book is append-only. Corrections are new records, never destructive edits.
7. No live execution exists in this foundation.

## Foundation lifecycle

```text
Epinnox Recommendation
        |
        v
Steward Decision
        |
        v
Watchman Evaluation
        |
   PASS | BLOCK
        |
        v
Benjamin Authorization
        |
        v
AuthorizedExecutionRequest
        |
        v
The Hand (separate repository)
        |
        v
ExecutionReceipt
        |
        v
The Book
```

## Repository layout

```text
src/benjamin/
  domain.py       # immutable domain contracts
  steward.py      # decision authority
  watchman.py     # deterministic guard rails
  authority.py    # creates execution authorizations
  book.py         # append-only evidence ledger
contracts/        # cross-repository JSON contracts
funds/firstfruits # fund policy/configuration
rules/            # machine-readable covenant defaults
tests/            # constitutional invariants
```

## Current milestone: B0 — Constitutional Kernel

B0 proves the authority boundaries before any brokerage integration, investor onboarding, blockchain anchoring, or autonomous trading is added.

The next phase may add persistent storage, signed receipts, portfolio state, Treasury, investor capital accounting, and Epinnox adapters without changing these authority rules.

## Status

**FOUNDATION ONLY — NO LIVE MONEY, NO LIVE BROKER, NO EXCHANGE EXECUTION.**
