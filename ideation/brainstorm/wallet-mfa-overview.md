# openWallet Authentication Profile Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Propose runtime wallet authentication that composes with openMFA and factory-owned authorization.
Topics: wallet-mfa, openwallet, openmfa, proof-of-possession
Repository context: opensoft/openWallet-spec with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Release a neutral possession-proof profile after governed implementation and qualification.

## Motivation and delivery

Agents and humans need attributable access through wallet keys with trusted subject binding, truthful custody, and bounded grants. Independent human approval remains a separate domain decision.

The current core contracts and validator are the baseline. Runtime integration is proposed here.

## Document map

- [Wallet synthesis](wallet-mfa-synthesis-wallet-profile.md)
  - [Proof profile](wallet-mfa-proof-profile.md)
  - [Verification references](wallet-mfa-verification-references.md)

## Ownership and fit

openWallet owns proof and existing authority/custody contracts. openMFA owns additional verification. The broker issues tokens. openXwallet would bind factory trust anchors and approval vocabulary. Domains resolve subjects and enforce permissions.

Existing [core](../../openspec/specs/openxwallet/spec.md) and [agent profile](../../openspec/specs/openxwallet-agent-profile/spec.md) remain authoritative. Implementation and releases follow existing leg/root governance.

## Boundaries and open decisions

Use credential references and protected custody. Select broker support, canonicalization, issuer trust, and revocation before implementation. Domain subject reconstruction remains wallet neutral.

## Cross-system navigation

- [Shared architecture](https://github.com/opensoft/openxFactory/blob/docs/wallet-mfa-design/ideation/brainstorm/wallet-mfa-overview.md)
- [openMFA service](https://github.com/opensoft/openMFA-spec/blob/docs/wallet-mfa-design/ideation/brainstorm/wallet-mfa-overview.md)
- [codeXfactory pilot](https://github.com/codeXfactory/codexFactory/blob/docs/wallet-mfa-design/ideation/brainstorm/wallet-mfa-overview.md)
