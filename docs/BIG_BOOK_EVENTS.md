# Benjamin Big Book Event Classes

This file documents the **current/legacy B1 event names** emitted by the existing Benjamin foundation. It does not override the target Epinnox ownership model:

> **ZLJ sees. Benjamin decides. Watchman governs. The Hand executes. The Book remembers and proves.**

Historical event names must retain the meaning they had when issued. Future bridge schemas may introduce explicit ZLJ and Watchman namespaces rather than silently reinterpreting old records.

## `BENJAMIN.DECISION`

Proves that Benjamin produced a capital decision under a specific evidence/recommendation lineage.

The full reasoning record may remain in Benjamin's governed cognitive stores or The Vault according to retention/privacy policy.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## `BENJAMIN.RISK` — legacy B1 name

In the current foundation, this event proves that the Watchman role evaluated a Benjamin decision under a defined policy and returned a pass/block-style result.

**Target ownership:** Watchman owns governance/risk/policy truth. A future schema should use an explicit Watchman-owned event family when the cross-repository Watchman bridge is implemented.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## `BENJAMIN.AUTHORIZATION` — legacy B1 name

In the current foundation, this event proves that a bounded execution instruction reached the authorization stage after valid decision/risk lineage.

**Target ownership:** final external-action authorization belongs to Watchman, not Benjamin. This legacy event must remain interpretable for historical B1 receipts but must not be treated as the target live authority contract.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## Target event direction

Future bridge semantics should converge toward something conceptually like:

```text
ZLJ.INTELLIGENCE / ZLJ.PREDICTION
        -> BENJAMIN.DECISION
        -> WATCHMAN.AUTHORIZATION | WATCHMAN.BLOCK
        -> HAND.EXECUTION / HAND.ACTION
        -> OUTCOME / RECONCILIATION
```

Exact event names are implementation-contract concerns. The important invariant is producer ownership and preserved historical meaning.

The Hand should verify the exact governed authorization needed for its capability without receiving unrelated decision, portfolio, or model history.
