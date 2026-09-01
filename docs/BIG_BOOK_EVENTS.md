# Benjamin Big Book Event Classes

Current control-plane events are private Big Book proofs.

## `BENJAMIN.DECISION`

Proves that the Steward made a portfolio decision under a specific recommendation lineage. The full reasoning record may remain in Benjamin's governed store or The Vault.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## `BENJAMIN.RISK`

Proves that Watchman evaluated the decision under a defined policy and returned PASS or BLOCK. Detailed risk state may remain private.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

## `BENJAMIN.AUTHORIZATION`

Proves that a specific bounded execution instruction was authorized after valid decision and risk lineage.

Default privacy: `CONFIDENTIAL_EVIDENCE`.

The Hand may verify the authorization proof without receiving unrelated decision or portfolio evidence.
