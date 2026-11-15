---
code_surface: openWallet code leg (`opensoft/openWallet-code`), named here and performed by nothing in this change. A NEW contract family directory `contracts/openxwallet-practitioner-profile/` (its leg is Open question 1) holding a licence verification schema (kind `xfactory_wallet_licence_verification`) and a verifier revocation list schema (kind `xfactory_wallet_licence_revocation_list`), with its README and synthetic positive and negative examples; `scripts/validate-openxwallet.py` (two new kinds, new ERROR codes in a `licence-verification-*` family, new requirement rows, no rename, no new WARNING); and one description sentence in `contracts/openxwallet/openxwallet-subject-attestation.schema.yaml`, which quotes the non-substrate rule and would otherwise omit its exception. No new proof profile: a sign-off uses the ratified `wallet-challenge-proof`. At the assembly root, the bookkeeping of a release. Every name here is PROPOSED (`design.md` D12), and nothing is reserved.
target_release: unallocated. The realization is expected to be an ADDITIVE MINOR in which two owned members are added and one digested contract byte moves. Per the root AGENTS.md rule 5 the five coordinated values are allocated at realization and nothing is reserved here.
Status: proposed
Discussed: not discussed in session. Drafted on 2026-11-15 by Claude (Opus 5.5) on Brett Heap's ruling 153, as a draft for his review; ratification pending.
---

# Proposal: add-practitioner-profile-and-licence-verification

## Why

openChart is the clinical chart of a small medical practice. Its owner, Brett
Heap, ruled that every medical decision entered in the chart needs the
practitioner's own sign-off, made by a logged-in user with their openWallet and
openSig (ruling 151, his words quoted in `design.md`): "the openWallet will
have the verification of license and the openSig will attest that it is from
that wallet."

openWallet cannot do its part today, for three reasons:

1. **There is no licence verification.** The closed `holder_class` set has had
   `practitioner` since the birth change, and the birth change named a
   practitioner profile as a successor, "each gated on a consumer". No profile
   was written, because no consumer had asked. openChart's draft
   `define-clinical-acts-foundation` (openChart-spec#5) is that consumer.
2. **The canonical rule forbids what ruling 151 needs.** "The capability is an
   authority control, never an identity substrate" says a wallet SHALL NOT
   become a prerequisite for operating a domain. Ruling 151 makes a wallet a
   prerequisite for one act of the chart.
3. **The chart names an AI by its wallet identifier,** and the same rule says a
   wallet identifier never becomes a subject identifier.

So openChart's draft fails closed: until openWallet and openSig can do their
part, no real decision is recorded (ruling 152). On 2026-11-15 the owner
accepted the recommendations that answer all three (rulings 153, 154 and 183).
This change is the openWallet half of ruling 153. Its openSig half is the draft
change `add-wallet-bound-attestation` in `opensoft/openSig-spec`.

## What the rulings settle, and what they leave open

**Ruled** (the words are in `design.md`, "The owner's rulings"):

- the wallet holds the verification of licence, and openSig attests that the
  signature is from that wallet (151);
- this repository's rule gains ONE named exception, a practitioner's sign-off of
  a medical decision, and the rest of the chart still works without a wallet
  (154);
- a wallet ID may name an AI as the author of a record, still never identifies a
  patient or a person, and nothing needs the wallet to be reachable to read the
  chart (183);
- a sign-off is checkable inside the practice's own deployment (156);
- the practice's own licence record and the wallet's both hold (160);
- openChart decides whether a sign-off counts (155).

**Not ruled, and PROPOSED here:** everything else. What a licence verification
states, who may issue it, how it is checked and ended, what custody a sign-off
key declares, every name, and the wording of both deltas. Each is marked
PROPOSED in `design.md` and listed there for the owner.

## What Changes

One NEW capability and one `## MODIFIED Requirements` block on the existing
capability `openxwallet`. No change to `openxwallet-agent-profile`.

1. **ADDED capability `openxwallet-practitioner-profile`**, the second profile
   over the neutral core, on the agent profile's pattern: a sibling family that
   adds what is practitioner-specific and changes nothing in the core. Six
   requirements:
   - a practitioner holder carries licence verifications, one per licence, and
     no other class carries one (`design.md` D2);
   - a verification is issued by a named verifier, signed in a signing domain of
     its own, over a proof of possession from the bound wallet (D3);
   - it is checked inside the relying domain with no outside call, and what it
     must refuse (D4);
   - how it ends: reliance bound, supersession, revocation, wallet revocation,
     checked at reliance (D5);
   - it is evidence about a licence, never identity or authority, and the
     relying domain binds its own account (D6);
   - a practitioner's sign-off is a proof of possession, under the ratified
     possession-only profile, over the relying domain's statement, and the
     signing key's custody says what it evidences (D7).
2. **MODIFIED "The capability is an authority control, never an identity
   substrate"**: the one named exception of ruling 154, and the sentence of
   ruling 183. Every word and both scenarios of the canonical text are kept;
   four scenarios are added (D8).

## What this change depends on

- **Ratified, not yet archived: `add-challenge-proof-runtime`** (the
  possession-only wire profile `wallet-challenge-proof`, ratified 2026-11-10).
  A sign-off's proof is that profile, unchanged (D7, D11).
- **Proposed, not ratified: `add-trust-anchors-and-machine-holders`**, with its
  open amendment in pull request #6. The relying domain's held verifier key is
  naturally one of its `issuer` trust anchors, and it MODIFIES the same
  requirement this change modifies. This change's text does not depend on it,
  and `design.md` D9 and D10 say what happens if it is ratified, changed or
  returned.
- **Ratified, not yet archived: `add-composition-drift-cascade`**. It modifies
  "Revocation propagates through the chain", which this change leaves alone and
  relies on (D5, D11).
- **Commissioned, not ratified as a contract: `add-reference-registry-custody`**.
  Its registry is one way to run the key binding registry that the ratified
  proof profile requires (D7, D11).

## Backward compatibility

**Every existing record remains valid, unchanged.** `practitioner` is already in
the closed `holder_class` set. The licence verification and its revocation list
are NEW kinds that no record uses. The custody registry, the grant, the
exercise, the distinct-holder constraint, the subject attestation's shape and
the agent composition do not change. No finding code is renamed, repurposed or
reclassified, and no new WARNING is added, because LedgerxFactory runs the
validator with `--strict`.

**A domain that adopts no wallets stays conformant.** The exception lets a
domain require a wallet for one act; it obliges no domain to.

**One digested byte is expected to move.** The subject attestation schema's
description quotes the rule this change amends. Left alone it would state the
rule without its exception (D12).

## Impact

- **openWallet spec leg**: this change; then its Speckit feature, number
  allocated at handoff; then the new capability's `## Purpose`, which no delta
  form reaches.
- **openWallet code leg**: the new contract family, the validator extension, the
  corpus and one description sentence, as `code_surface` names them.
- **openWallet assembly root**: a MINOR release, its number allocated at
  realization.
- **openSig**: `add-wallet-bound-attestation` relies on the seam that both
  designs state in the same words.
- **openChart**: can make the two checks of its sign-off that it cannot make
  today, once both drafts are ratified and realized. Its draft would need the
  changes this change's pull request lists; this change does not restate or
  change openChart's rules.
- **Other pinning consumers** (openXwallet, openxFactory, LedgerxFactory,
  MedxFactory): a pin bump when they next re-sync. Nothing they declare becomes
  invalid.
