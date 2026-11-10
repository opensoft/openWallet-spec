# Synthesis: Wallet Proof with External Verification — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Combine subject-bound key proofs and external assurance with current grant and custody constraints.
Topics: wallet-mfa, openwallet, identity-brokering, synthesis
Repository context: opensoft/openWallet-spec with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Qualify one broker adapter against wallet proof and additional verification evidence.

## Members and joints

[Possession proof](wallet-mfa-proof-profile.md) establishes the presenting key and trusted subject binding. [Verification references](wallet-mfa-verification-references.md) adds bound assurance. The broker checks both and issues application-scoped tokens. The application evaluates current authority and domain permission.

A separate human approval uses a distinct domain subject and separate session. It binds the exact request digest. The agent remains the actor exercising its grant.

## Lifecycle

Retired keys, revoked standing or grant chains, and changed agent composition refuse exercise. Runtime adapters must preserve immediate revocation requirements. Token expiry alone is insufficient.

The [integration envelope](https://github.com/opensoft/openxFactory/blob/docs/wallet-mfa-design/ideation/brainstorm/wallet-mfa-shared-contracts.md) requires coordinated ownership and versioning across products. The wallet owns proof production. openMFA owns additional verification.

## Open decisions

Choose adapter, issuer discovery, canonicalization, workload attestation, and revocation availability. [Wallet overview](wallet-mfa-overview.md) maps the proposal.
