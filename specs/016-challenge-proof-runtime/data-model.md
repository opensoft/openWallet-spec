# Data model

Status: draft

Entities: proof, TrustedKeyBinding, VerifiedPossession and opaque Signer.

Proof fields bind profile/algorithm, challenge digest, binding revision, binding/wallet/key/subject/custody references and signature. TrustedKeyBinding additionally carries the resolved public key, service validity and revocation. VerifiedPossession returns references and digest only.

Exact field schemas live under `contracts/` in this spec leg. Runtime cross-field, trusted-resolution, signature and current-state checks remain mandatory beyond schema structure.
