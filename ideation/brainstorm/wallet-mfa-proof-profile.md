# Wallet Possession and Subject Binding — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Propose a runtime challenge proof over existing wallet keys, issuer attestations, and grants.
Topics: wallet-mfa, openwallet, proof-of-possession, subject-attestation
Repository context: opensoft/openWallet-spec with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Define a neutral wallet authentication proof and negative corpus.
- Bind the presented key to an independently resolved domain subject.

## Baseline and proposal

The current core defines held keys, custody, grant exercise, subject attestation, retirement, and revocation. The agent profile binds authority to composition. This proposal adds the runtime broker presentation seam.

The wallet authenticates the verifier and signs a challenge covering tenant, audience, nonce, expiry, and applicable operation digest. It presents declared key and issuer-attestation references. The verifier checks trusted binding, key membership/state, signature, custody ceiling, and current grant chain.

## Composition and domain identity

The declared composition includes its component set and digest. A trusted runtime or independent attestor must bind actual execution and key to that declaration. Agent self-report is insufficient.

Domain subjects remain independently resolvable through wallet replacement and recovery. Explicit subject linking requires proof of both sides and collision handling.

## Boundaries and open decisions

Public records hold references and public verification material. Secrets stay in declared custody. Choose canonicalization, issuer discovery, revocation, and broker adapter during governance.

## Relationships

[Verification references](wallet-mfa-verification-references.md) adds assurance. [Wallet synthesis](wallet-mfa-synthesis-wallet-profile.md) joins them. [Shared contracts](https://github.com/opensoft/openxFactory/blob/docs/wallet-mfa-design/ideation/brainstorm/wallet-mfa-shared-contracts.md) describes the cross-product envelope.
