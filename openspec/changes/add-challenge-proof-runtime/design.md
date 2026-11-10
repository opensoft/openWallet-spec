# Candidate design

Status: draft

## Context and scope

Offline Ed25519 possession proof over an authenticated challenge digest with current server-resolved key binding and opaque signing custody.

The public product owns neutral proof/evidence behavior. A relying party owns permission and explicit human consent. Wallet proof establishes possession of the registered key over a bound challenge digest. It does not attest that the referenced custody or agent composition is actually isolated. A trusted registry supplies those facts and their acceptance.

## Protocol choices

Use Ed25519 via cryptography 50.0.1 and RFC 8785 canonical bytes via rfc8785 0.1.4. These are candidate choices within the commissioned Ed25519/canonical-digest design, subject to review here. References: [Ed25519 API](https://cryptography.io/en/50.0.1/hazmat/primitives/asymmetric/ed25519/), [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), [canonicalizer 0.1.4](https://pypi.org/project/rfc8785/0.1.4/).

The exact signing message is ASCII `openWallet.challenge-proof.v0` followed by a NUL byte and JCS of all unsigned proof fields. The challenge digest is `sha256:` plus 64 lowercase hexadecimal digits of the owning issuer's canonical challenge. The owning issuer enforces freshness, caller binding and one-use. Signature encoding is strict unpadded base64url of exactly 64 bytes. References are trimmed, nonempty, at most 256 Unicode characters, without controls, DEL or surrogate code points. Binding revision and service times are nonnegative safe JSON integers. Binding validity uses zero skew and a half-open interval. Wire decoding rejects duplicate keys, constants, nonobjects and payloads over 8192 bytes.

## State and trust

The Signer interface has only `sign(message)`. No private-key serialization/export interface is required. Signer output is checked against the trusted registered public key before returning a proof. Verification requires an externally resolved current binding, exact revision and all five references, and the expected challenge digest. Inline public keys and unknown claims refuse. No persistent replay or revocation database is added here: the registry and challenge issuer own those decisions.

## Limits and acceptance

- New schemas default to spec leg; legacy wallet Q7 does not automatically cover them.
- Bindings and caller contexts are trusted adapter inputs, never a client key or client verified flag.
- Only possession is implemented; requests for MFA or human assurance refuse.
- Remote custody, composition attestor, WebAuthn/OIDC adapters and provider discovery remain dependencies.
- Remote current-binding observation is point-in-time; no distributed revocation or external-domain atomicity claim.
- Receipt retries retrieve unchanged historical evidence; fresh consumption rechecks validity and current binding.
- All repository tests and leg CI must run after merge; in-memory preparation is not source/CI/live acceptance.
- Root pins stay fixed until reviewed leg PRs merge; development package version is not an allocated release.

## Migration and rollback

Additive candidate only. Existing released files and machine keys stay fixed. Disable/remove the candidate before an assembly release if rejected; do not rewrite ratification history. No product tag, root pin or consumer dependency is advanced by the leg PRs. Future remote custody, provider discovery, workload attestation and human verification require their own governed acceptance.
