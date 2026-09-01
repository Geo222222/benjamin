# Benjamin Covenant

Benjamin governs capital. It does not get to rewrite the evidence of what it governed.

## Authority invariants

1. Epinnox may recommend; it may not authorize or execute.
2. The Steward may approve or modify portfolio intent; it may not bypass Watchman.
3. Watchman `BLOCK` means no execution authorization.
4. Benjamin may authorize; it may not place broker or exchange orders.
5. The Hand may execute; it may not originate or alter investment intent.
6. Firstfruits remains design-only until explicit legal, custody, accounting, and investor-admission milestones are completed.

## Evidence invariants

7. The Book is sovereign infrastructure in `Geo222222/the-book`, not a package owned by Benjamin.
8. Benjamin signs only `BENJAMIN.*` evidence and cannot sign as Epinnox, The Hand, or The Book.
9. Material Benjamin decisions, risk results, and execution authorizations must be published to The Book before the authorization leaves Benjamin.
10. A recommendation entering the evidence-required control plane must reference an existing Epinnox Book receipt.
11. Corrections are new evidence; Benjamin never mutates historical Book entries.
12. Raw PII, credentials, private keys, and bulky evidence artifacts do not belong in blockchain payloads.
13. The Book's blockchain technology may change without changing Benjamin's authority model.
14. Principal is never reclassified as spoil merely because asset values changed.

## Failure rule

If evidence publication fails before handoff, Benjamin does not hand the authorization to The Hand. Future live execution must use a durable outbox/receipt protocol so an external execution can never be lost merely because The Book is temporarily unavailable.
