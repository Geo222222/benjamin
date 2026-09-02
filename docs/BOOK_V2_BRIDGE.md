# Benjamin -> The Book v2 Bridge

Benjamin owns capital-decision truth and may sign only `BENJAMIN.*` Book Evidence Protocol v2 events.

## Benjamin producer identity

Runtime signing uses an Ed25519 key held inside Benjamin's secret boundary.

Required runtime secret inputs:

- `BENJAMIN_BOOK_KEY_ID`
- `BENJAMIN_BOOK_ED25519_PRIVATE_KEY_B64`

The private key must never be committed to Git, persisted in ordinary cognitive memory, included in reports, or sent to The Book.

The public identity contains only:

```text
producer: Benjamin
key_id: <runtime key id>
allowed_event_prefixes: [BENJAMIN.]
public_key_b64: <public key only>
```

## Constitutional boundary

Benjamin may emit target events such as:

- `BENJAMIN.DECISION`
- `BENJAMIN.DECISION_SUPERSEDED`
- `BENJAMIN.DECISION_EVALUATION`
- `BENJAMIN.COMPETENCE_CHANGE`
- `BENJAMIN.PROCEDURE_VERSION`
- `BENJAMIN.JOURNAL_COMMITMENT`

Benjamin may not sign `ZLJ.*`, `WATCHMAN.*`, `HAND.*`, `MARTIANS.*`, or Book-owned proof records. In particular, a Benjamin signing key cannot convert a capital decision into final external-action authorization.

## Transitional Watchman attachment

The deterministic Watchman implementation still physically lives inside the Benjamin repository during the B1 transition. Physical location does not confer Benjamin authority over Watchman.

Watchman therefore has a separate Ed25519 identity and a separate durable outbox:

```text
producer: Watchman
allowed_event_prefixes: [WATCHMAN.]
```

Required Watchman runtime secret inputs are:

- `WATCHMAN_BOOK_KEY_ID`
- `WATCHMAN_BOOK_ED25519_PRIVATE_KEY_B64`

The runtime loader rejects reuse of Benjamin's key id or private key when both identities are present. The Book additionally rejects registration of the same public key under different constitutional producers.

The resulting authority chain is:

```text
ZLJ.INTELLIGENCE
       ↓
BENJAMIN.DECISION
       ↓
WATCHMAN.AUTHORIZATION | WATCHMAN.BLOCK
```

A Watchman governance payload must identify the actual `BENJAMIN.DECISION` Book receipt as its primary cause. The Book verifies that the referenced ledger entry is in fact a `BENJAMIN.DECISION`; pointing Watchman at a ZLJ receipt or an unrelated record is rejected.

`WATCHMAN.AUTHORIZATION` contains the exact bounded capability constraints that passed deterministic policy: capability, instrument, side, quantity, idempotency key, and expiry. `WATCHMAN.BLOCK` contains no executable capability constraints and no authorization artifact.

During this transition, the existing B1 `AuthorizedExecutionRequest` is still generated on a passing Watchman result and is used to derive those exact v2 capability constraints. Existing `BENJAMIN.RISK` and `BENJAMIN.AUTHORIZATION` tests remain unchanged as historical compatibility coverage. They do not grant the Benjamin Book key authority to emit `WATCHMAN.*` events.

The Hand is not changed by this attachment. Item 12 must explicitly migrate downstream verification from the legacy Benjamin authorization model to the Watchman-signed authorization model only after its architecture is explained and reviewed.

## Privacy

Capital decision and Watchman governance evidence are `CONFIDENTIAL_EVIDENCE` by default. A public Little Book claim requires a separate disclosure decision; it is never an automatic projection of private Book evidence.

## Timing and lineage

A v2 decision envelope binds the exact decision payload digest, primary causal receipt, additional evidence dependencies, `known_at`, `produced_at`, expiry/validity, privacy, and visibility.

A Watchman authorization binds its evaluation time as both `occurred_at` and `known_at`, the Benjamin decision receipt as primary causation, and its authorization expiry as `valid_until`. A block records the governance result without inventing executable validity.

This lets The Book prove what evidence Benjamin depended upon and what deterministic governance result followed without requiring The Book to store Benjamin's full private reasoning trace.

## Failure posture

If signing or Book delivery is unavailable, the originating organ must not claim that material evidence was durably recorded. The durable producer outboxes persist the exact signed evidence before delivery so Book outages cannot silently erase or regenerate decision/governance history.
