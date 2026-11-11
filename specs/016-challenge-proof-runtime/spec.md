# Feature Specification: openWallet challenge-proof-runtime

**Feature Branch**: `016-challenge-proof-runtime`
**Created**: 2026-11-10
**Status**: Possession-only wire contract ratified; candidate realization pending
**Input**: Commissioned upstream prerequisite following codeXfactory PR #577; separately ratified by Brett Heap on 2026-11-10 at `778cedb30406e753fee5b4a95d96ac2c18b78ae4`. See the governing proposal's owner record; operational acceptance remains separate.

## User Scenarios & Testing

### User Story 1 - Verify bounded authentication evidence (Priority: P1)

A relying party needs cryptographic possession evidence tied to its exact challenge and a current registered key.

**Independent Test**: Generate an ephemeral registered key; a correct proof verifies, while a changed challenge, binding or signature refuses.

**Acceptance Scenarios**:
1. Given valid trusted context, when the declared method succeeds, then only bounded verified facts are returned.
2. Given altered evidence or an unavailable trust dependency, when verification is attempted, then no new evidence or use is created.
3. Given a request for stronger assurance or domain permission, when this candidate is used, then it cannot supply that claim.

### Edge Cases

Unknown/missing fields, invalid signatures, wrong algorithm/profile, expired or revoked keys, wrong subject/caller/tenant/audience, conflicting retries, and unavailable signer/backend must refuse. Cross-protocol signatures, duplicate JSON keys and noncanonical base64url must refuse.

## Requirements

- **FR-001**: openWallet SHALL sign and verify only the fixed Ed25519 profile over the domain separator `openWallet.challenge-proof.v0\0` followed by RFC 8785 canonical UTF-8 bytes of every unsigned proof field. It SHALL compare the expected challenge digest, trusted binding references and binding revision before returning verified facts.
- **FR-002**: openWallet SHALL accept binding metadata only from a trusted server registry; client proof data SHALL NOT supply a public key. The binding SHALL be current, unrevoked and time valid. The signing interface SHALL expose signing only, without requiring raw key export.
- **FR-003**: openWallet SHALL reject duplicate JSON keys, unknown fields, noncanonical signatures and unsupported algorithms. Verified possession SHALL NOT imply MFA, human presence, composition attestation, delegation or domain permission.

## Key Entities

proof, TrustedKeyBinding, VerifiedPossession and opaque Signer.

## Success Criteria

- Every scoped positive and adversarial case passes in the code leg's offline suite.
- Structural contracts pass their own spec-leg checks; these checks make no signature claim.
- Existing product gates retain their declared behavior and limitations.
- No receipt/proof is described as human approval, MFA, workload composition or domain permission.

## Assumptions and exclusions

Trusted service clock, caller adapter, registry, signing adapter and operator-controlled file storage are explicit trust inputs. Real remote custody, human/provider adapters, public service transport, live QA, accepted assembly pins and release qualification remain outside this first candidate.
