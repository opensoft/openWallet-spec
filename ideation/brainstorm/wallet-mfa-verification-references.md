# Wallet Verification References and Custody — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Reference external verification while preserving the presenting key's declared custody ceiling.
Topics: wallet-mfa, openwallet, custody, openmfa, assurance
Repository context: opensoft/openWallet-spec with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Define credential-binding references and trusted verification receipt consumption.
- Prove added factors cannot silently raise custody or authority.

## Proposed model

A wallet client invokes an authenticator or requests verification. A future governed profile may reference credential binding, verifier, permitted method, and custody. Wallet records carry no TOTP seeds, private keys, recovery codes, provider passwords, or factor responses.

Receipts bind subject, method, freshness, audience, challenge, and verified custody evidence. Consumers validate issuer and policy. Client-supplied assurance cannot confer permission.

## Independence and recovery

Two freely invocable credentials share an execution compromise boundary. Stronger per-use attribution requires authorization outside that environment. Recovery replaces or retires bindings under policy and invalidates dependent uses while preserving the domain subject.

## Governance and relationships

This brainstorm leaves published schemas and the closed custody registry at their current baseline. Contract changes need an OpenSpec proposal in this leg, code-leg implementation, and coordinated assembly release. Factory approval keys continue to come from their declared vocabulary binding.

[Proof profile](wallet-mfa-proof-profile.md) and [synthesis](wallet-mfa-synthesis-wallet-profile.md) connect verification to use.
