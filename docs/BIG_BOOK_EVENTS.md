# Benjamin Big Book Event Classes

This file documents the **current/legacy B1 event names** emitted by the existing Benjamin foundation plus newly introduced explicit organ-owned event families. It does not override the target Epinnox ownership model:

> **ZLJ sees. Benjamin decides. Watchman watches/governs the capital. The Hand executes. The Book remembers and proves.**

Historical event names must retain the meaning they had when issued. New schemas should use explicit organ-owned namespaces rather than silently reinterpreting old records.

## `BENJAMIN.DECISION`

Proves that Benjamin produced a capital decision under a specific evidence/recommendation lineage.

The full reasoning record may remain in Benjamin's governed cognitive stores or The Vault according to retention/privacy policy.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## `BENJAMIN.RISK` — legacy B1 name

In the current foundation, this event proves that the original Watchman role evaluated a Benjamin decision under a simple pass/block policy.

This legacy event remains historical evidence. It does **not** define the target continuous Watchman behavior.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## `WATCHMAN.CAPITAL_ASSESSMENT`

Proves that Watchman evaluated one exact content-addressed authoritative Capital State against one exact content-addressed Capital Envelope/Responsibility boundary.

The minimum-necessary payload binds:

- Capital State ID/hash/as-of time;
- Capital Envelope ID/hash;
- Responsibility reference;
- assessment mode;
- Watchman state (`HEALTHY`, `WATCH`, `CONSTRAINED`, `CORRECTION_REQUIRED`, `EMERGENCY`);
- reasons and explicit required capital conditions;
- permitted action classes;
- emergency directives where applicable;
- active-decision validity reference/state where applicable;
- assessed-at time.

Raw account credentials, provider payloads, or ZLJ market histories are not copied merely to prove the Watchman assessment.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## `WATCHMAN.PRE_ACTION_ASSESSMENT`

Proves that Watchman evaluated a candidate economic path against one exact `ProjectedCapitalState` before execution.

The payload binds:

- exact authoritative base Capital State ID/hash;
- exact Projected Capital State ID/hash;
- candidate-path reference and action class;
- exact Capital Envelope ID/hash and Responsibility reference;
- per-scenario results for required `EXPECTED`, `ADVERSE`, and `EXECUTION_STRESS` projections;
- the worst justified aggregate Watchman state;
- candidate-permitted result;
- required capital conditions and permitted action classes;
- assessed-at time.

This event is **capital-safety evidence, not execution authority**. Its truth boundary explicitly states:

```text
authoritative_capital_state = false
execution_authorization     = false
hand_instruction            = false
```

The Hand must never accept this evidence event as an executable request.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## `BENJAMIN.AUTHORIZATION` — legacy B1 name

In the current foundation, this event proves that a bounded execution instruction reached the authorization stage after valid decision/risk lineage.

**Target ownership:** capital-safety authorization belongs to Watchman. This legacy event must remain interpretable for historical B1 receipts but must not be treated as the target live authority contract.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## Target event direction

Future bridge semantics should converge toward something conceptually like:

```text
ZLJ.INTELLIGENCE / ZLJ.PREDICTION
        -> BENJAMIN candidate path / projection
        -> WATCHMAN.PRE_ACTION_ASSESSMENT
        -> BENJAMIN.DECISION
        -> future WATCHMAN.AUTHORIZATION | WATCHMAN.CONSTRAINT
        -> HAND.EXECUTION / HAND.ACTION
        -> CAPITAL_STATE / RECONCILIATION
        -> WATCHMAN.CAPITAL_ASSESSMENT
        -> WATCHMAN.CORRECTION_REQUIRED | WATCHMAN.EMERGENCY where needed
        -> BENJAMIN corrective decision
        -> OUTCOME / LEARNING
```

Exact event names beyond implemented assessment events remain implementation-contract concerns. The important invariant is producer ownership and preserved historical meaning.

The Hand should verify the exact governed authorization needed for its capability without receiving unrelated decision, portfolio, or model history.
