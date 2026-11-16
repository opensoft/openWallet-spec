# Tasks: add-webauthn-proof-profile

Speckit builds these; OpenSpec ratifies them. The realization feature is TO BE
ALLOCATED at handoff (§6). No feature number is reserved here. Every box is open,
because the change is `Status: proposed`.

`[OPERATOR]` = only Brett Heap can perform it. `[GOVERNANCE]` = it needs a ruling
first.

## 1. Governance

- [ ] 1.1 One adversarial review of this revision at `Status: proposed` (an
      independent review of the first draft at `4d32fa1` has run; its findings
      and their dispositions are in `design.md`), reading it against Web
      Authentication Level 3 (Recommendation of 25 August 2026), the
      IANA COSE Algorithms registry, the ratified `wallet-challenge-proof` and its
      ratification record, the closed custody registry, openWallet-spec#10 and
      openSig-spec#4. The verdicts go into `design.md` with their dispositions.
- [ ] 1.2 **[OPERATOR] [GOVERNANCE]** Rule on the open questions in `design.md`, the
      first two first, and dispose of the design calls WP-1 to WP-11.
- [ ] 1.3 **[OPERATOR] [GOVERNANCE]** Ratify or return. Brett Heap (openWallet
      operator authority).
- [ ] 1.4 On ratification: `Status: ratified` and a `Ratified:` line carrying the
      ruling's words verbatim in `proposal.md`, and a ratification record under
      `review/`. Then re-run the pinned gate green.

## 2. Contracts

- [ ] 2.1 A proof schema for `openwallet.webauthn-proof.v0`: closed, at most 8192
      bytes, the ten binding fields (`alg` a JSON integer, `-7` or `-8`) and the
      three byte fields of D1, in the leg Open question 8 decides.
- [ ] 2.2 The binding's added fields (D4), the basis of custody among them, as a
      schema or as the registry's record, with the signature counter, the
      current backup state and each proof's counter flag kept beside the
      binding, outside its revisioned record (D2).
- [ ] 2.3 Synthetic examples only: no real credential, key, origin or person.

## 3. Runtime and validator

- [ ] 3.1 A verifier making every check of D2, the binding's state among them, with
      no network call and no state of its own, returning the verified facts, both
      backup flags and the counter flag, which it compares only at a proof's first
      verification.
- [ ] 3.2 P-256 (ES256, strict DER, on-curve check) and Ed25519 (canonical S)
      verification; the
      canonical validator recognizes the P-256 multicodec and recomputes its
      fingerprint over the 33-byte compressed point (D3).
- [ ] 3.3 Known-answer vectors from independent tooling over derived challenges,
      and negative vectors for each refusal of D2 and D3; Level 3's own examples
      (its §16) only as signature-level vectors and as negative vectors for user
      verification and cross-origin use (D11).
- [ ] 3.4 Registration (D4): `-8` and `-7` offered; a binding only after a
      registration and a proof in the same session; a credential identifier
      bound once; no multi-device credential bound while no model of the
      registry describes it (D7).
- [ ] 3.5 A party other than the relying party accepts a proof only in a session
      in which it identified the holder, never a relayed one; and the check of a
      recorded proof (D5).

## 4. Composition

- [ ] 4.1 openWallet-spec#10 cites this change for its sign-off and its verifiers'
      proofs of possession; keep the two consistent until both archive.
- [ ] 4.2 openSig-spec#4 attests proofs under this profile (D9); keep the two
      consistent.
- [ ] 4.3 If Open question 1 is answered with a new custody model, that change
      archives before this one, or this one is revised to name it.

## 5. Release (assembly root)

- [ ] 5.1 Allocate the coordinated values at realization. Nothing is reserved
      before then.

## 6. Handoff and archive

- [ ] 6.1 Hand off to exactly one Speckit feature, its number allocated then.
- [ ] 6.2 Archive only after the realization lands and the assembly root's pin
      moves; at archive, write the new capability's `## Purpose`.
