# Benjamin Proof Visibility Defaults

These defaults describe the intended Big Book visibility for the current B1 events.

| Event | Privacy class | Default readers |
| --- | --- | --- |
| `BENJAMIN.DECISION` | `CONFIDENTIAL_EVIDENCE` | Steward, Watchman, authorized auditor |
| `BENJAMIN.RISK` | `CONFIDENTIAL_EVIDENCE` | Watchman, Authority, authorized auditor |
| `BENJAMIN.AUTHORIZATION` | `CONFIDENTIAL_EVIDENCE` | Authority, Hand verifier, authorized auditor |

The public Little Book receives none of these records automatically.

If an external verifier needs a fact, Benjamin requests a separate minimum-necessary public attestation from The Book. That public claim is a new proof object, not an export of the private event.
