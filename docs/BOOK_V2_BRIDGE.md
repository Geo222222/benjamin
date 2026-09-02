# Benjamin -> The Book v2 Bridge

Benjamin owns capital-decision truth and may sign only `BENJAMIN.*` Book Evidence Protocol v2 events.

## Producer identity

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

## Privacy

Capital decision evidence is `CONFIDENTIAL_EVIDENCE` by default. A public Little Book claim requires a separate disclosure decision; it is never an automatic projection of Benjamin's Book evidence.

## Timing and lineage

A v2 decision envelope binds the exact decision payload digest, primary causal receipt, additional evidence dependencies, `known_at`, `produced_at`, expiry/validity, privacy, and visibility.

This lets The Book prove what evidence Benjamin depended upon without requiring The Book to store Benjamin's full private reasoning trace.

## Failure posture

If signing or Book delivery is unavailable, Benjamin must not claim that material decision evidence was durably recorded. The durable producer outbox provides the next bridge layer so Book outages cannot silently erase decision history.
