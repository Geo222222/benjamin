# Benjamin Proof Visibility Defaults

These defaults describe the intended Big Book visibility for the **current B1 event names** while preserving the target ownership model:

> **ZLJ sees. Benjamin decides. Watchman governs. The Hand executes. The Book remembers and proves.**

| Current event | Privacy class | Default readers / purpose |
| --- | --- | --- |
| `BENJAMIN.DECISION` | `CONFIDENTIAL_EVIDENCE` | Benjamin decision roles, Watchman as necessary, authorized auditor |
| `BENJAMIN.RISK` *(legacy name)* | `CONFIDENTIAL_EVIDENCE` | Watchman/governance roles, authorized auditor |
| `BENJAMIN.AUTHORIZATION` *(legacy name)* | `CONFIDENTIAL_EVIDENCE` | governed authorization verifier / Hand verifier, authorized auditor |

`BENJAMIN.RISK` and `BENJAMIN.AUTHORIZATION` are existing B1 schema names. Their continued presence does not mean Benjamin constitutionally owns final risk/governance or authorization in the target architecture.

Future bridge schemas should prefer explicit Watchman-owned governance/authorization events while preserving the historical semantics and privacy of existing receipts.

The public Little Book receives none of these private records automatically.

If an external verifier needs a legitimate fact, The Book creates a separate minimum-necessary public attestation under disclosure policy. That public claim is a new proof object, not an export of the private event.
