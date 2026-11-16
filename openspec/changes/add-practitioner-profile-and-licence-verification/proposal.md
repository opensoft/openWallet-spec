---
code_surface: openWallet code leg (`opensoft/openWallet-code`), named here and performed by nothing in this change. A NEW contract family directory `contracts/openxwallet-practitioner-profile/` (its leg is Open question 7) holding a licence verification schema (kind `xfactory_wallet_licence_verification`), a verifier revocation list schema (kind `xfactory_wallet_licence_revocation_list`) and a relying domain's held verifier key schema (kind `xfactory_wallet_held_verifier_key`), with its README and synthetic positive and negative examples; `scripts/validate-openxwallet.py` (three new kinds, new ERROR codes in a `licence-verification-*` family, new requirement rows, no rename, no new WARNING); and one description sentence in `contracts/openxwallet/openxwallet-subject-attestation.schema.yaml`, which quotes the non-substrate rule and would otherwise omit its exception. No new proof profile: a sign-off uses the ratified `wallet-challenge-proof`. At the assembly root, the bookkeeping of a release. Every name here is PROPOSED (`design.md` D14), and nothing is reserved.
target_release: unallocated. The realization is expected to be an ADDITIVE MINOR in which three owned members are added and one digested contract byte moves. Per the root AGENTS.md rule 5 the five coordinated values are allocated at realization and nothing is reserved here.
Status: proposed
Discussed: not discussed in session. Drafted on 2026-11-15 by Claude (Opus 5.5) on Brett Heap's ruling 153, as a draft for his review, and revised the same day after an independent review, a confirmation review and a final check, and again after his rulings 208 to 214; ratification pending.
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
- a sign-off is checkable inside the practice's own deployment, so the chart
  never waits on an outside service to accept a decision (156);
- the practice's own licence record and the wallet's both hold (160);
- openChart decides whether a sign-off counts (155);
- a practitioner signs with a passkey or a security key, and the openWallet
  change giving them a proof format is drafted now (208), as
  `add-webauthn-proof-profile`;
- for openChart, a passkey that syncs through the practitioner's Apple or Google
  account counts only on a device the practitioner has enrolled, a security key
  always counts, and controlled substances stay out (209);
- a practice may not issue the licence verification for its own practitioners:
  the verifier must be independent (210);
- for the first practice the verifier is a verification service the owner runs,
  checking each licence against the state board's own record, with its key
  shipped in openChart (211);
- a relying domain that cannot fetch the newest revocation list does not stop
  accepting sign-offs; it uses the newest list it holds and records how old that
  was (212);
- a verification may be relied on until the licence expires, and at most 12
  months, and the verifier re-checks the board's record monthly and revokes on a
  change (213);
- a sign-off holds up against forgery even against whoever runs the practice's
  server, and does not stop that person deleting records or back-dating (214).

**Not ruled, and PROPOSED here:** everything else. What a licence verification
states, who may issue it and how a relying domain comes to hold the verifier's
key, how it is checked and ended, the threat model, what custody a sign-off key
declares, every name, and the wording of both deltas. Each is marked PROPOSED in
`design.md` and listed there for the owner, with the open questions still open.

## What Changes

One NEW capability and one `## MODIFIED Requirements` block on the existing
capability `openxwallet`. No change to `openxwallet-agent-profile`.

1. **ADDED capability `openxwallet-practitioner-profile`**, the second profile
   over the neutral core, on the agent profile's pattern: a sibling family that
   adds what is practitioner-specific and changes nothing in the core. Eight
   requirements:
   - a practitioner holder carries licence verifications, one per licence, each
     naming the keys it covers, with a reliance bound no later than the licence's
     expiry or twelve months after the check; no other class carries one
     (`design.md` D2);
   - a verification is issued by a named verifier, in a signing domain of its
     own, over a recorded proof of possession from each key it names (D3);
   - a relying domain holds verifier keys as records of its own, with a
     recorded provenance (a release of the relying system, or two named
     people), each delivered with its verifier's newest revocation list, and a
     compromise time; only a key delivered with a release supports the threat
     model's aim (D4);
   - a verification is checked inside the relying domain and never waits on an
     outside service: the domain keeps every verification it receives and a
     supersession index of them; an old revocation list flags a reliance and
     never blocks it, and a raised item never goes to the signer alone (D5,
     D6);
   - how it ends, checked at reliance, and which revocations reach a human (D6);
   - it is evidence about a licence, never identity or authority (D7);
   - a relying domain binds each sign-off key to its account itself, and takes
     its copy of the wallet record only from the practitioner (D8);
   - a practitioner's sign-off is a proof of possession over the relying
     domain's statement digest, under the passkey and security-key profile
     `wallet-webauthn-proof` (ruling 208) or the ratified
     `wallet-challenge-proof`, as the relying domain states; it is not consent,
     the key's custody says what the registry says it evidences, and the
     relying domain states which custody it accepts as its own acceptance rule
     (D9).
2. **MODIFIED "The capability is an authority control, never an identity
   substrate"**: the one named exception of ruling 154, named by the act (a
   practitioner's sign-off of a medical decision, and the binding of that wallet
   to the practitioner's account that the sign-off needs, and nothing else), and
   the sentence of ruling 183, marked as a clarification of the identifier rule
   and not a second exception. Every word and both scenarios of the canonical
   text are kept; four scenarios are added (D10).

## What this change depends on, and what it composes with

- **Ratified, not yet archived: `add-challenge-proof-runtime`** (the
  possession-only wire profile `wallet-challenge-proof`, ratified 2026-11-10).
  Unchanged, and binding the same things a passkey proof binds; it is not how a
  practitioner signs in openChart's version 1 (ruling 208; D9, D13).
- **Proposed, a separate draft: `add-webauthn-proof-profile`** (capability
  `wallet-webauthn-proof`), drafted under ruling 208. A practitioner's sign-off
  is made in it, with a passkey or a security key, and it says how a verifier
  observes such a key's proof of possession (D3, D9).
- **Proposed, not ratified: `add-trust-anchors-and-machine-holders`**, with its
  open amendment in pull request #6. It MODIFIES the same requirement this
  change modifies; whichever archives second regenerates at the union (D11).
  This change does not otherwise depend on it (D12).
- **Ratified, not yet archived: `add-composition-drift-cascade`**. It modifies
  "Revocation propagates through the chain", which this change leaves alone and
  relies on (D6, D13).
- **Commissioned, not ratified as a contract: `add-reference-registry-custody`**.
  Its registry is one way to run the key binding registry that the ratified
  proof profile requires (D8, D13).

## Backward compatibility

**Every existing record remains valid, unchanged.** `practitioner` is already in
the closed `holder_class` set. The licence verification, its revocation list and
the held verifier key are NEW kinds that no record uses. The custody registry,
the grant, the exercise, the distinct-holder constraint, the subject
attestation's shape and the agent composition do not change. No finding code is
renamed, repurposed or reclassified, and no new WARNING is added, because
LedgerxFactory runs the validator with `--strict`.

**A domain that adopts no wallets stays conformant.** The exception lets a
domain require a wallet for one act; it obliges no domain to.

**One digested byte is expected to move.** The subject attestation schema's
description quotes the rule this change amends. Left alone it would state the
rule without its exception (D14).

## Impact

- **openWallet spec leg**: this change; then its Speckit feature, number
  allocated at handoff; then the new capability's `## Purpose`, which no delta
  form reaches.
- **openWallet code leg**: the new contract family, the validator extension, the
  corpus and one description sentence, as `code_surface` names them.
- **openWallet assembly root**: a MINOR release, its number allocated at
  realization.
- **A separate change**: the passkey and security-key profile is drafted as
  `add-webauthn-proof-profile` (ruling 208), not in this change (D9).
- **openSig**: `add-wallet-bound-attestation` relies on the seam that both
  designs state in the same words.
- **openChart**: can make the two checks of its sign-off that it cannot make
  today, once both drafts are ratified and realized. Its draft would need the
  changes this change's pull request lists; this change does not restate or
  change openChart's rules.
- **Other pinning consumers** (openXwallet, openxFactory, LedgerxFactory,
  MedxFactory): a pin bump when they next re-sync. Nothing they declare becomes
  invalid.
