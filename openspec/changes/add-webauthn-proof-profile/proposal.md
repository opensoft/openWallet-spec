---
code_surface: openWallet runtime and contracts, named here and performed by nothing in this change. A verifier for the profile `openwallet.webauthn-proof.v0` beside the ratified `wallet-challenge-proof` verifier, reusing its RFC 8785 canonicalizer, with P-256 (ES256) and Ed25519 (EdDSA) verification; a proof schema in the leg Open question 8 decides; known-answer vectors made with independent tooling, including Web Authentication Level 3's own examples; and the canonical validator's recognition of the P-256 multicodec for fingerprints. No change to the ratified `wallet-challenge-proof` or to the closed custody registry. Every name here is PROPOSED (`design.md` D11), and nothing is reserved.
target_release: unallocated. The realization is expected to be an ADDITIVE MINOR; its coordinated values are allocated at realization and nothing is reserved here.
Status: proposed
Discussed: not discussed in session. Drafted on 2026-11-15 by Claude (Opus 5.5) on Brett Heap's ruling 208, as a draft for his review; ratification pending.
---

# Proposal: add-webauthn-proof-profile

## Why

Brett Heap ruled that a practitioner signs a medical decision with a passkey or a
security key, and asked for this change (ruling 208, his words in `design.md`): "A
passkey or security key. Draft that change now. A smart card cannot be used from
a phone."

openWallet's only possession profile, the ratified `wallet-challenge-proof`, is
Ed25519 over a preimage openWallet chooses. A passkey or security key signs
something else: its own authenticator data followed by the SHA-256 of the client
data (Web Authentication Level 3, §6.3.3). So no practitioner can sign under the
ratified profile with the keys ruling 208 chose. openWallet's draft practitioner
profile (`add-practitioner-profile-and-licence-verification`, openWallet-spec#10)
and openSig's draft attestation (`add-wallet-bound-attestation`, openSig-spec#4)
both rely on the proof this change defines.

## What the rulings settle, and what they leave open

**Ruled:** a practitioner signs with a passkey or a security key, and this change
is drafted now (208); for openChart, a passkey that syncs through the
practitioner's Apple or Google account counts only on a device the practitioner
has enrolled, a security key always counts, and controlled substances stay out
(209).

**Not ruled, and PROPOSED here:** everything else: the proof's form and what binds
it, every check, the algorithms, how a credential is bound to a wallet key, how a
verifier observes a key's proof of possession, what the profile records to tell a
synced passkey from a device-bound key, the custody such a key declares, the
threat model, and every name. Each is marked PROPOSED in `design.md` and listed
there for the owner.

## What Changes

One NEW capability, `wallet-webauthn-proof`, a sibling of the ratified
`wallet-challenge-proof`. Nine requirements:

- a proof is a Web Authentication assertion whose challenge is derived from the
  proof's binding fields, so it binds what the ratified profile binds and also the
  relying party; the binding comes only from the trusted registry and must be
  current, unrevoked and time valid; the challenge issuer draws the statement's
  32-byte single-use reference at random, server-side (D1, D2);
- every use is checked for its type, challenge, exact origin, relying-party
  identifier, user presence and user verification, and backup flags, with no
  repeated member in the client data; the counter and backup state are kept beside
  the binding, and a counter that does not increase is flagged once, not refused
  (D2);
- ES256 and EdDSA with Ed25519 only, one integer spelling of each in a proof (D3);
- a credential is bound from a registration and a following proof in the
  holder's own session, and works only at the relying party it is scoped to (D4);
- a party other than that relying party, such as a licence verifier, accepts a
  key's proof of possession only in a session it began with the holder's client
  itself, which the relying party neither began nor can join, and in which it
  identified the holder itself; the profile cannot tell whether that client is
  administered by the relying domain's operator; a relayed proof is never
  accepted (D5);
- the profile tells a synced passkey from a device-bound key by the backup flags,
  and says what it cannot tell, among it which device signed and who controls the
  account a passkey syncs through; the holder declares at registration that the
  device, browser and any sync account are theirs and not administered by the
  practice (D4, D6);
- a credential's custody is declared with its backup eligibility and the basis of
  the declaration, attested or the holder's word, beside it; a security key may
  declare `isolated_per_use_authorized`; no synced passkey is bound until the
  registry has a model for it (D7);
- a verified proof is possession bound to a relying party, and no more: it never
  shows that the holder saw the statement (D8);
- a relying domain checks a proof another party recorded from what is recorded
  with it (D5).

## What this change depends on, and what it composes with

- **Web Authentication Level 3**, W3C Recommendation of 25 August 2026, and the
  IANA COSE Algorithms registry (cited by section in `design.md`).
- **Ratified, not yet archived: `add-challenge-proof-runtime`**. Followed as a
  pattern and left unchanged.
- **The closed custody registry and the wallet record's closed algorithm set**,
  both unchanged; the latter already holds `ecdsa-p256` and `ed25519`.
- **Consumers, both drafts:** openWallet-spec#10, whose sign-off and licence
  verifications use this profile, and openSig-spec#4, revised alongside this
  change to attest it (D9). This change does not depend on either.

## Backward compatibility

Every existing record and the ratified `wallet-challenge-proof` stay valid and
unchanged. No finding code is renamed, repurposed or reclassified.

## Impact

- **openWallet spec leg**: this change; then its Speckit feature, number allocated
  at handoff; then the new capability's `## Purpose`.
- **openWallet code leg or spec leg contracts**: as `code_surface` names them.
- **openWallet assembly root**: a MINOR release, its number allocated at
  realization.
- **openChart**: can make a practitioner's sign-off with a passkey or security key
  once this change and the two drafts above are ratified and realized; ruling 152
  keeps every decision off until then. It evidences device enrolment itself
  (ruling 209; D6). A synced passkey can be bound only once the custody registry
  has a model for it (D7, Open question 1).
