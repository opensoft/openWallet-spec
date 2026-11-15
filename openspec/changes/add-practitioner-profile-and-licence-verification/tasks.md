# Tasks: add-practitioner-profile-and-licence-verification

Speckit builds these; OpenSpec ratifies them. The realization feature is TO BE
ALLOCATED at handoff (§7). No feature number is reserved here. Every box is
open, because the change is `Status: proposed`.

`[OPERATOR]` = only Brett Heap can perform it. `[GOVERNANCE]` = it needs a
ruling first.

## 1. Governance

- [ ] 1.1 Alignment pass: ONE adversarial reviewer over this revision at
      `Status: proposed`. It reads against the canonical `openxwallet` and
      `openxwallet-agent-profile`, the ratified and unarchived
      `add-challenge-proof-runtime` (with its ratification record) and
      `add-composition-drift-cascade`, the core contracts, the validator,
      openChart-spec#5's sign-off (CA-04, AU-03, AU-07, EN-06) and openSig's
      draft `add-wallet-bound-attestation`. The verdicts go into `design.md` as
      returned, each with its disposition. One independent review has already
      run, on the first draft at `8aa0364`.
- [ ] 1.2 **[OPERATOR] [GOVERNANCE]** Rule on the nineteen open questions in
      `design.md` ("Open questions for ratification"), by number, the first five
      first, and dispose of the design calls PP-1 to PP-16.
- [ ] 1.3 **[OPERATOR] [GOVERNANCE]** Ratify or return. Brett Heap (openWallet
      operator authority).
- [ ] 1.4 On ratification: `Status: ratified` and a `Ratified:` line carrying the
      ruling's words verbatim in `proposal.md`, plus a ratification record in
      `design.md`. Then re-run the pinned gate (this leg's `AGENTS.md` rule 4)
      green. If any delta byte changed after the ruling, re-rule it.
- [ ] 1.5 Before ratifying, compare `design.md`'s section "The seam between
      openWallet and openSig" with the same section of openSig's
      `add-wallet-bound-attestation` at the head being ratified there. They must
      be identical; a difference is resolved in both drafts first.

## 2. Contracts — a NEW family, in the leg Open question 7 decides

- [ ] 2.1 `contracts/openxwallet-practitioner-profile/README.md`: what the
      profile is, that it is a sibling of the agent profile, that a verification
      states no clinical scope, and the threat model's aim and limits.
- [ ] 2.2 NEW `openxwallet-licence-verification.schema.yaml`, kind
      `xfactory_wallet_licence_verification`, with the fields of `design.md` D2,
      `subject.keys[]` included: closed shapes, `additionalProperties: false` at
      every depth, no property that could hold key material or list acts,
      decisions or scopes, and the closed `status_found` and `source.kind` sets.
- [ ] 2.3 NEW `openxwallet-licence-revocation-list.schema.yaml`, kind
      `xfactory_wallet_licence_revocation_list`: the verifier, a sequence that
      only rises, `issued_at`, the time by which the next list is published, and
      entries of verification id, revocation time and reason class (D6).
- [ ] 2.4 NEW `openxwallet-held-verifier-key.schema.yaml`, kind
      `xfactory_wallet_held_verifier_key`: the verifier, the key and its
      fingerprint, the licensing authorities it is held for, provenance
      (`release` with the release named, or `two_person` with two named people
      and the announcement referenced), state and `compromised_since` (D4).
- [ ] 2.5 `contracts/openxwallet/openxwallet-subject-attestation.schema.yaml`:
      one description sentence naming the exception (D14). Its `sha256:` moves.
- [ ] 2.6 Synthetic examples: valid ones, and one negative example per new
      finding code. No real person, licence identifier, authority record or key.

## 3. Validator

- [ ] 3.1 `KIND_TO_SCHEMA` gains the three kinds.
- [ ] 3.2 New ERROR codes in a `licence-verification-*` family, each a
      computation: the bound wallet resolves and its holder class is
      `practitioner`; every key in `subject.keys[]` is one the bound wallet
      declares, its fingerprint recomputes from its public key, and its proof is
      present; the verifier's key is declared by the verifier's wallet;
      `supersedes` resolves to a verification of the same licence, wallet and
      verifier; `issued_at` is not earlier than `source.checked_at`;
      `rely_until` is later than `issued_at`, no later than `licence.expires_on`
      where given, and no later than twelve months after `source.checked_at`;
      `conditions_ref` is present exactly with `active_with_conditions`; a held
      verifier key carries a provenance from the closed set, with two distinct
      named people for `two_person`; one id per record.
- [ ] 3.3 One requirement row per ADDED requirement (proposed `OXWP-R1` to
      `OXWP-R8`), each with at least one negative confirmation.
- [ ] 3.4 No code renamed, repurposed or reclassified; no new WARNING; facts the
      validator cannot check, such as a verifier's signature or a recorded
      proof's signature, reported as NOTES.

## 4. Runtime (code leg)

- [ ] 4.1 Sign and verify a licence verification and a revocation list under
      their signing domains, reusing the RFC 8785 canonicalizer and the Ed25519
      primitive the possession profile already uses; independently generated
      known-answer vectors, on feature 016's T007 precedent.
- [ ] 4.2 A relying-domain check that returns `relied_on` (with the list used,
      its age and any freshness flag), `refused` or `not_checkable` with its
      reason, from the five held inputs of D5 alone, that makes no network call
      and never waits, and that refuses to replace a held list with a lower
      sequence.

## 5. Release (assembly root)

- [ ] 5.1 Allocate the five coordinated values at realization: the three new
      owned rows, the moved subject attestation digest, the CHANGELOG entry and
      the release record. Nothing is reserved before then.

## 6. Composition

- [ ] 6.1 If `add-trust-anchors-and-machine-holders` archives first, regenerate
      this change's MODIFIED block at the union `design.md` D11 states, and
      re-run the pinned gate before archiving this change. If this change
      archives first, that change carries the same obligation. In either case,
      check the regenerated block line by line: every line of both changes'
      blocks, body text as well as scenarios, must be present, because the CLI
      checks scenarios and not body text.
- [ ] 6.2 If `add-trust-anchors-and-machine-holders` is ratified, decide whether
      the held verifier key reuses its per-key state machinery (D12). No
      requirement here changes either way.
- [ ] 6.3 If `add-challenge-proof-runtime`'s archive renames
      `wallet-challenge-proof`, update this change's reference to it.

## 7. Handoff and archive

- [ ] 7.1 Hand off to exactly one Speckit feature, its number allocated then.
- [ ] 7.2 Archive only after the realization lands and the assembly root's pin
      moves; at archive, write the new capability's `## Purpose`, which no delta
      form reaches.
