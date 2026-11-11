## ADDED Requirements

### Requirement: Context-bound possession
openWallet SHALL sign and verify only the fixed Ed25519 profile over the domain separator `openWallet.challenge-proof.v0\0` followed by RFC 8785 canonical UTF-8 bytes of every unsigned proof field. It SHALL compare the expected challenge digest, trusted binding references and binding revision before returning verified facts.

#### Scenario: Proof tampering
- WHEN the challenge digest, binding, signature or profile changes
- THEN verification refuses.

### Requirement: Trusted binding and custody boundary
openWallet SHALL accept binding metadata only from a trusted server registry; client proof data SHALL NOT supply a public key. The binding SHALL be current, unrevoked and time valid. The signing interface SHALL expose signing only, without requiring raw key export.

#### Scenario: Revoked key
- WHEN the binding is revoked, expired or revised
- THEN an old proof refuses.

### Requirement: Strict profile and limited meaning
openWallet SHALL reject duplicate JSON keys, unknown fields, noncanonical signatures and unsupported algorithms. Verified possession SHALL NOT imply MFA, human presence, composition attestation, delegation or domain permission.

#### Scenario: Claim escalation
- WHEN a caller adds an MFA or authority claim
- THEN the proof refuses.
