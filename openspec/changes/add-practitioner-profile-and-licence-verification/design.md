# Design: add-practitioner-profile-and-licence-verification

## Context

Drafted on 2026-11-15 by Claude (Opus 5.5), on Brett Heap's ruling 153, as a
draft for his review, and revised the same day after an independent review, a
confirmation review, a final check with an automated review, and his rulings 208
to 214.
**Nothing here is ratified.** The owner's rulings quoted below are his
decisions; every other choice in this change is a design call, marked PROPOSED
where it is made and listed in "Design calls" below, so that it can be
confirmed or overturned one by one.

The consumer is openChart's draft `define-clinical-acts-foundation`
(openChart-spec#5, read at `d9a9c63`). Its practitioner's sign-off makes four
checks at the moment of signing; two of them read things that do not exist yet:
a licence verification held in the practitioner's openWallet, and an openSig
attestation that the signature came from that wallet. Until both exist, every
sign-off fails closed and drafts stay drafts (its CA-04 and AN-14; ruling 152).
This change specifies the first. The openSig draft `add-wallet-bound-attestation`
specifies the second. The two share one seam, stated in the same words in both
designs.

What this change says openWallet provides, it says in openWallet's terms. It
does not restate or change openChart's rules. Where it uses openChart's needs as
a check on its own design, it cites them.

**Read for this change**, at these heads:

- `opensoft/openWallet-spec` `main` at `a2d554d`: the canonical `openxwallet` and
  `openxwallet-agent-profile`, the four open changes and the ratification record
  of `add-challenge-proof-runtime`, the three archives, the plan of Speckit
  feature 006 and all of feature 016; and pull request #6 at `4d83535`;
- `opensoft/openWallet-code` at `bb0e9da`, read only: the record schema, the
  closed custody registry, the subject attestation and the validator's kinds;
- `opensoft/openSig-spec`: `main` at `23ebbfe`, pull request #1 at `8668f30` and
  pull request #2 at `a05fcee`;
- openChart-spec#5 at `d9a9c63`: Decision 4, Decision 19, Open Questions 9 and
  11 (10, 16, 17 and 24 are closed there by rulings 156, 160, 186 and 183), the
  requirements AU-03, AU-07, AN-02, AN-08, AN-14, CA-04, CA-08, CA-14 and EN-06,
  and the content schema's sign-off evidence.

## The owner's rulings

Every row is a ruling by **Brett Heap**. **Rulings are not ratification.** This
change stays `Status: proposed` until he ratifies it.

**Ruling 151**, 2026-11-15, his words, verbatim:

> "for 12, and any medical decision we need the practitioner to sign off. so we
> need a logged in user that we use their openWallet and openSig to sign and
> validate that entry. the openWallet will have the verification of license and
> the openSig will attest that it is from that wallet."

"12" is clause 12 of the approved wording of his ruling 80, which openChart-spec#5
records in its public form. Where ruling 151 and a clause of ruling 80 differ,
ruling 151 is the later ruling and governs.

**Rulings 152 to 156, 160, 183 and 186.** On 2026-11-15 he answered the decisions
numbered 152 to 194 with the words "accept your recs for 152-194". Each became a
ruling in the words of the recommendation as last presented to him. The rows
that bind this change, question and ruling verbatim:

| No. | Question | Ruling |
|---|---|---|
| 152 | Until openWallet and openSig can do their part, does openChart record any decision? | No real decision until both exist. It can still be built and tested against stand-ins. |
| 153 | Draft the missing pieces as changes in those two repos? | Yes: a practitioner profile carrying a licence verification in openWallet, and a wallet-bound attestation in openSig, each as a draft for your review. |
| 154 | openWallet's rule says a wallet is never a prerequisite for operating a domain. Ruling 151 makes one a prerequisite for signing a medical decision. | Amend openWallet's rule with one named exception: a practitioner's sign-off of a medical decision. The rest of the chart still works without a wallet. |
| 155 | openSig keeps clinical attestation in openChart. | Leave that as is. openChart decides whether a sign-off counts; openSig only attests that the signature came from that wallet. |
| 156 | openChart promises the clinical record works with no outside system. Where must a sign-off be checkable? | Inside the practice's own deployment, so the chart never waits on an outside service to accept a decision. |
| 160 | Which licence record counts: the practice's own, or the wallet's? | Both must hold, and ruling 98's check stays. |
| 183 | Ruling 80 names an AI by its openWallet ID. openWallet's own specification says a wallet is "never an identity substrate". Clarify openWallet so the two agree? | Yes: a wallet ID may name an AI as the author of a record. It still never identifies a patient or a person, and nothing needs the wallet to be reachable to read the chart. |
| 186 | Ruling 151 has the practitioner sign as a logged-in user. Logged in where: must it be openChart itself, or may the sign-off be made in another system and checked by the chart? | In openChart only, in version 1, as ruling 35 has physicians working there. A sign-off made in another system counts later, once openWallet and openSig can prove it to the chart. |

**Rulings 208 to 214.** On 2026-11-15 he answered the decisions numbered 195 to
214 with the words "accept your recs for 195-214". Each became a ruling in the
words of the recommendation as last presented to him. The rows that bind this
change, question and ruling verbatim:

| No. | Question | Ruling |
|---|---|---|
| 208 | How does a practitioner sign: with a smart-card style key, or with a passkey or security key? The second needs one more openWallet change, a proof format for them. | A passkey or security key. Draft that change now. A smart card cannot be used from a phone. |
| 209 | May it be a passkey that syncs through the practitioner's Apple or Google account? | Yes, but only on a device the practitioner has enrolled, as ruling 134 allows for approvals. A security key always counts. Controlled substances stay out (ruling 83) and would need stronger keys. |
| 210 | May a practice issue the licence verification for its own practitioners? | No. Ruling 160 wants the practice's record and the wallet's to both hold, which means little if the practice issues both. The verifier must be independent. |
| 211 | No independent verifier exists yet. Who verifies licences for the first practice? | A verification service you run, checking each licence against the state board's own record, with its key shipped in openChart. Until one exists, ruling 152 keeps every decision off. |
| 212 | If the chart cannot fetch the verifier's latest revocation list, should it stop accepting sign-offs? | No, per ruling 156. It uses the newest list it holds, records how old that was, and alerts the medical director once it is over 72 hours old. A verification still expires on its own date. |
| 213 | How long may a licence verification be relied on before renewal? | Until the licence itself expires, and at most 12 months. The verifier re-checks the board's record monthly and revokes on a change, so the practitioner renews once a year at most. |
| 214 | Should a sign-off hold up even against whoever runs the practice's server? | Yes, against forgery: the verification names the practitioner's own signing keys and is signed by the independent verifier. It does not stop that person deleting records or back-dating; outside timestamps can close that later. |

**What each of them rules here, and what stays PROPOSED.** Only a ruling's words
are ruled. Every detail beyond them is a design call, marked where it is made.

- **208** rules that a practitioner signs with a passkey or a security key, and
  that the openWallet change giving them a proof format is drafted now. It is
  the separate draft change `add-webauthn-proof-profile` (capability
  `wallet-webauthn-proof`); this change relies on it and does not contain it
  (D9). The ratified `wallet-challenge-proof` stays as ratified and is not how a
  practitioner signs in openChart's version 1. Open question 2 is closed.
- **209** rules, for openChart, which keys count: a passkey that syncs through
  the practitioner's Apple or Google account, only on a device the practitioner
  has enrolled; a security key always; controlled substances stay out. Enrolling
  a device is the relying domain's matter. What openWallet owes the domain is the
  means to tell a synced passkey from a device-bound key, which the new profile
  records (D9).
- **210** rules that a practice may not issue the licence verification for its
  own practitioners: the verifier must be independent. Open question 3's first
  question is closed; D4 says how a relying domain holds the rule, and what the
  standard cannot enforce.
- **211** rules who verifies for the first practice: a verification service the
  owner runs, checking each licence against the state board's own record, with
  its key shipped in openChart; until one exists, ruling 152 keeps every decision
  off. Open question 3's second question is closed. The service has no
  specification here, and nothing is drafted for it (Open question 20).
- **212** rules that freshness never blocks: the relying domain uses the newest
  list it holds and records how old that was, and a verification still expires
  on its own date (D5). The 72 hours and the alert to the medical director are
  openChart's. Open question 4 is closed, and tension T1 with it.
- **213** rules the reliance bound, until the licence itself expires and at most
  12 months, and the verifier's monthly re-check of the board's record, with a
  revocation on a change, which this change states as a duty on the verifier
  (D6). Measuring the twelve months from when the licence was checked stays
  PROPOSED. Open question 9 is closed.
- **214** rules the threat model's aim in its own words (D8 and the seam). Open
  question 1 is closed. Reading it for this profile, and its limits beyond the
  ruling's words, stay PROPOSED.

Ruling 98, cited by ruling 160, is recorded in openChart-spec#5: "A second named
person confirms; a one-administrator practice records licence verification
against the board's public record." That is the practice's own check, and it
stays the practice's (D7). Ruling 35, cited by ruling 186, is recorded there
too: "For now the physician uses openChart, on mobile or workstation." It bears
on which devices can sign (D9).

Ruling 157, accepted in the same words, is not this change's to encode but
bears on it: "151. An AI only ever makes recommendations until a practitioner
signs. Limited and full practice as designed would need a new ruling." Nothing
here can make an agent's signature a practitioner's sign-off (D1).

## What this change stands on

Checked on 2026-11-15 at the heads above.

| Change or record | Standing | How this change uses it |
|---|---|---|
| `openxwallet`, `openxwallet-agent-profile` | canonical, ratified, archived | The core this profile sits over; the agent profile is its pattern (D1). |
| `add-challenge-proof-runtime` (capability `wallet-challenge-proof`) | **ratified** 2026-11-10 for its possession-only wire profile ("Ratify both possession-only profiles"), not yet archived; runtime acceptance pending | A sign-off's proof is that profile, unchanged, within the limits its ratification record states (D9, D13). |
| `add-composition-drift-cascade` | ratified 2026-08-28, not yet archived | Its restatement of "Revocation propagates through the chain" is the revocation rule D6 relies on. Not modified here. |
| `add-reference-registry-custody` | commissioned implementation and isolated qualification; not a ratified contract | Its registry is one way to run the key binding registry the ratified profile requires (D8, D13). |
| `add-trust-anchors-and-machine-holders`, and its amendment in pull request #6 | proposed, not ratified | It MODIFIES the same requirement as this change (D11). This change no longer depends on it (D12). Not edited here. |
| The closed custody registry, version 1 (`openWallet-code` `bb0e9da`) | ratified with the birth change | What a sign-off key's custody evidences (D9). |
| The closed `holder_class` set | ratified; already includes `practitioner` | No schema change is needed for the class (D1). |
| `add-webauthn-proof-profile` (capability `wallet-webauthn-proof`) | proposed, a separate draft drafted under ruling 208 | The proof a practitioner's sign-off is made in, with a passkey or a security key, and how a verifier observes such a key's proof of possession (D3, D9). |

## D1 — A practitioner profile: a sibling capability over the core (PROPOSED, PP-1)

The birth change `add-openxwallet` made the core/profile split "the substance of
this proposal": "Patient and practitioner profiles are named successors, each
gated on a consumer, and each a NEW capability over the same core rather than a
modification of it". Feature 006's plan said the same of the contracts: "a
patient or practitioner profile arrives as a third directory, never as an edit to
the first", and the agent profile's own purpose says it is a sibling family "so
patient and practitioner profiles arrive the same way". openChart is now the
consumer. So this change adds `openxwallet-practitioner-profile`, a sibling of
the agent profile, and changes the core only where ruling 154 says the core's
rule must change.

**What the profile carries.** The licence verification and its revocation list;
the verifier keys a relying domain holds; what a relying domain checks and
refuses; how a verification ends; what it never is; how a relying domain binds
each sign-off key; and what openWallet provides for a practitioner's sign-off.
Nothing else: no composition (that is the agent profile's), no clinical
vocabulary, no grant semantics, and no rule about which decisions a licence
permits.

**The holder-class rule is first a record rule.** A licence verification bound
to a wallet whose holder is not a `practitioner` is refused, in the way the agent
profile's composition is refused for a non-agent wallet (validator code
`composition-on-non-agent`). A relying domain relies on the verifier-signed
verification, never on a wallet's own statement of its class, which keeps faith
with the proposed rule "A verifier is blind to holder class"
(`add-trust-anchors-and-machine-holders` D4), whose reason is that a class read
from the presenter's own record is a self-declaration. A relying domain MAY also
refuse when its held record of the bound wallet declares another class: refusing
on a self-declared class only makes the domain stricter, so it is safe.

**An agent never carries one.** So nothing in this profile can make an agent's
signature a practitioner's sign-off, which is what ruling 157 needs.

REJECTED:

- **The verification as a field of the wallet record.** It would put the
  verifier's statement on the subject's own record, so the subject would carry
  its own vetting, the fault `add-trust-anchors-and-machine-holders` D6 names
  for enrolment evidence. Verifications also churn at a different rate from the
  record, which is the governed declaration of the holder's authority.
- **The verification as a grant.** A licence is not authority the wallet
  confers. A grant whose scope said "licensed physician" would be a second
  authority vocabulary beside the grant scope, which "Agent authority is grant
  scope, not a parallel vocabulary" forbids in spirit for agents and this
  profile forbids for practitioners.
- **The verification as a subject attestation.** That kind is a subject's
  optional wallet reference, closed to the role `attestation`. A licence is a
  different fact, about the holder rather than about a subject that names the
  wallet.
- **A core change instead of a profile.** The core is holder-class agnostic by
  its own scenario; everything practitioner-specific belongs in the profile.

## D2 — What a licence verification states (PROPOSED, PP-2)

The fields, at the level the requirement binds. The schema is realization work
(`tasks.md` §2).

| Field | What it carries |
|---|---|
| `verification_id` | The record's identity, a random value, so that a published revocation list cannot be linked to a person. A duplicate is refused under the existing `record-id-duplicate`. |
| `subject.wallet_ref`, `subject.did` | The bound wallet: its `wallet_id`, and the DID of its primary key reference. |
| `subject.keys[]` | Every key the verification covers: its reference (`<did>#<key_id>`), its `key_fingerprint`, its public key, the proof of possession it made over the verifier's challenge, and when (D3). |
| `licence.authority` | The licensing authority, by an identifier the relying domain's held verifier key is scoped to (D4). |
| `licence.jurisdiction` | Where the authority licenses: an ISO 3166-1 alpha-2 country code, or an ISO 3166-2 subdivision code. |
| `licence.licence_id` | The authority's own identifier for the licence, as issued (see "The licence identifier is carried in clear" below). |
| `licence.licence_class` | The licence class or profession, in the authority's own designation. |
| `licence.licence_class_label` | OPTIONAL, for display only. No rule reads it. |
| `licence.expires_on` | OPTIONAL: the licence's own expiry, where the source states one. |
| `status_found` | Closed: `active`, `active_with_conditions`, `inactive`, `expired`, `suspended`, `revoked`. `conditions_ref` is REQUIRED with `active_with_conditions` and refused otherwise. |
| `source.kind` | Closed: `authority_record` (the authority's own record, read directly), `authority_publication` (a register the authority publishes), `designated_source` (a source the authority designates as primary for this fact). |
| `source.ref`, `source.checked_at` | What was consulted, and when. |
| `verifier.wallet_ref`, `verifier.did`, `verifier.key_id` | The verifier's wallet and the declared key that signed. |
| `issued_at`, `rely_until` | When the verification was issued, and its reliance bound. `issued_at` is not earlier than `source.checked_at`; `rely_until` is later than `issued_at`, no later than `licence.expires_on` where one is given, and no later than twelve months after `source.checked_at`. |
| `supersedes` | OPTIONAL: the `verification_id` this one supersedes, from the same verifier, for the same licence and wallet. |
| `identity_evidence_ref` | An opaque reference to the verifier's own record of how it satisfied itself that the licensee is the wallet's holder (D3). |
| `signature` | `alg` and `value`, over the canonical form of every other field (D3). |

**No clinical scope.** The record has no property that could list acts,
decisions or scopes, and closes `additionalProperties` at every depth, so the
wrong reading cannot be represented. Which decisions a licence class may make
is the relying domain's own configuration (D7). openChart's sign-off evidence
records what a verification "covers"; under this profile that is openChart's
own mapping from the verification's authority, jurisdiction and class, never a
field of the verification.

**The licence identifier is carried in clear.** The relying domain needs it to
compare the wallet's verification with its own record of the practitioner's
licence, which ruling 160 requires to hold beside it (D7). Licensing
authorities commonly publish licence identifiers. It identifies a licence, never
a patient, and it never becomes a subject identifier (D7). Open question 11.

**The reliance bound has two ceilings.** Ruling 213 rules them: "Until the
licence itself expires, and at most 12 months." The verifier sets it, and it is
never later than the licence's own expiry nor more than twelve months after the
licence was checked; measuring the twelve months from the check is PROPOSED. Twelve months, not a month, because the verifier also
re-checks the source on its own schedule and revokes on a change (D6), so the
bound is the backstop, not the main defence; and because each renewal asks the
practitioner for a fresh proof of possession to the verifier (D3).

**One verification per licence.** A practitioner with licences from two
authorities carries two. A change to one licence then supersedes or revokes one
verification and leaves the other alone.

**The status set.** A verifier records what it found. Only some statuses can
support anything, and which ones a relying domain accepts is its own decision
(Open question 15).

REJECTED:

- **A verification bound to the wallet and not to keys.** A wallet record
  carries no signature, and its key set is held by the relying domain. A
  verification that followed any key the held record declares would follow a
  key someone added to that record later (D8).
- **A profession taxonomy across jurisdictions.** Whether one authority's class
  is equivalent to another's is a legal judgment for the relying domain, not a
  fact a neutral standard can own (Open question 13).
- **One verification listing every licence a holder has.** A change to one
  licence would reissue all of them, and supersession would stop being per
  licence.
- **A digest of the licence identifier instead of the identifier.** A digest of
  a small, structured number space can be reversed by trying them all; a salted
  commitment needs its salt shared with the very party that already holds the
  number.

## D3 — Who issues a licence verification, and how (PROPOSED, PP-3)

**A verifier is a holder with a wallet of its own,** typically of class
`organisation`, and signs with a key that wallet declares. The verifier is a
party in the wallet ecosystem; its wallet is no prerequisite for operating the
relying domain, which holds only the verifier's key (D4).

**The signature.** Ed25519 over a domain separator and the RFC 8785 canonical
UTF-8 bytes of every field but `signature`: `openWallet.licence-verification.v1`
and a NUL byte for a verification, `openWallet.licence-revocation-list.v1` and a
NUL byte for a revocation list. That is the construction of the ratified
possession-only profile (domain separator `openWallet.challenge-proof.v0` and a
NUL byte, then RFC 8785), with separators of its own, so no record of one kind
verifies as another. It reuses one canonicalizer, one algorithm and the
known-answer vector practice of feature 016 (its T007).

**A proof of possession from each key it names.** Before it issues, the verifier
issues a challenge and obtains a proof of possession from each key the
verification will name, in the proof profile that key makes proofs in: for a
passkey or a security key, `wallet-webauthn-proof` (ruling 208). Such a key is a
WebAuthn credential scoped to one relying party (Web Authentication Level 3,
§6.1, `rpIdHash`), so it signs only for the deployment it was registered at, and
a verifier is a different party. How the verifier then observes the proof
itself is settled in `add-webauthn-proof-profile`; its recommendation is a
related-origin ceremony (Level 3, §5.11), in which the verifier's own page asks
the practitioner's key, under the deployment's relying-party identifier, to sign
the verifier's challenge.

**The verifier identifies the licensee itself, in the session in which each key
proves possession** (PROPOSED). A proof at the verifier's page shows only that a
client holding a credential scoped to the deployment signed there. The
deployment is that relying party: it can register a credential of its own and
present it at the verifier's page with a wallet record it supplies, and a native
client writes whatever origin it likes into the client data. So the verifier
obtains each proof within the session in which it identified the licensee by its
own means, independently of the deployment, and names a key only on such a
proof. A proof relayed through the deployment would show the verifier only what
the deployment chose to relay, so the link between the key and the person would
then rest on the deployment; it can never meet the condition, and no
verification names a key on one (D8).

The verification records, for each key, the key's reference, fingerprint and
public key, the proof itself and when it was made, and, for a proof under
`wallet-webauthn-proof`, what checking it needs: the relying-party identifier,
the origin at which the verifier obtained it, the credential identifier, the
backup flags it carries, and the verifier's statement that it obtained it within
the session in which it identified the licensee. Anyone holding the verification
can then check that the proof verifies under that public key and that its
fingerprint is the one named. A verification
covers exactly the keys it names. The binding to keys is the verifier's claim,
and possession of each key is the one fact about it the verifier can check for
itself. Issuance happens outside the relying domain and ahead of time; nothing
in it is on the path of a sign-off, so ruling 156 is not engaged by it.

**Who checks the recorded proofs.** The relying domain does, whenever it checks
the verification: each proof verifies, under its own profile, under the
recorded public key, and a proof under `wallet-webauthn-proof` passes that
profile's check of a recorded proof, made from what is recorded with it and,
where the domain bound that key itself, against its own relying-party identifier
and the credential it bound (`add-webauthn-proof-profile`, D5); the proof names
the recorded key reference and the wallet the verification is bound to (its
`wallet_ref` equals `subject.wallet_ref`); and the recorded fingerprint is that
key's. A verification with a proof that fails any of these, or a passkey proof
recorded without the verifier's statement of an identified session, is refused
as `signature_invalid` (D5); the validator can check the two references
statically (`tasks.md` 3.2). The domain cannot check the verifier's challenge,
its identification of the licensee or its binding of the key, which are the
verifier's own, and a recorded proof never binds a key to an account in the
domain (D8). The validator does not
verify signatures, so it reports the recorded proofs as NOTES (`tasks.md` 3.4).

**What the recorded proofs disclose.** Each carries the verifier's own
`subject_ref` and `binding_ref` to every relying domain that holds the
verification, so the verifier uses opaque references there that name no person.

**Identity proofing is the verifier's own record.** openWallet defines no
identity-proofing standard. How the verifier satisfied itself that the licensee
it checked and the wallet's holder are the same person is its own record,
referenced by `identity_evidence_ref`, in the way
`add-trust-anchors-and-machine-holders` D6 keeps enrolment evidence the issuer's
record. A relying domain does not depend on that record alone: it binds each key
to its own account itself and compares the licence with its own record (D7, D8).

**Who may be a verifier is not narrowed by the standard,** beyond holding a
declared key. What the standard does narrow is how a relying domain comes to
hold a verifier's key (D4). Ruling 160 asks for two records that both hold,
which is worth little if one party issues both; ruling 210 requires the verifier
to be independent (D4).

REJECTED:

- **Only the licensing authority may verify.** No authority issues such records
  today, so the consumer would wait indefinitely; the standard can admit an
  authority as a verifier when one does.
- **The holder's own statement of its licence.** A holder asserting its own
  licence is the `asserted_identity` the closed custody registry excludes in
  spirit: proof replaced by assertion.
- **openSig as the verifier.** Ruling 155: openSig only attests that the
  signature came from that wallet.

## D4 — The verifier keys a relying domain holds (PROPOSED, PP-4)

A relying domain checks a verification only against a verifier key it already
holds. It holds each one as a record of its own, never in a wallet of its own,
because ruling 154's exception does not reach the domain's own configuration
(D10). It never takes a verifier's key from the practitioner, and never from the
verification it is checking.

**A recorded provenance, from a closed set of two.** Each held verifier key
records how it arrived:

- `release`: it was delivered with a release of the relying system, which names
  the release; or
- `two_person`: it was added by two named people, and the addition was announced
  to the domain's declared audience, which the record references. No
  administrator acting through the domain can supply that record alone.

The provenance is recorded, not proof against whoever runs the deployment: in a
small practice the administrator and the operator are often one person, and an
operator can alter the domain's records. No administrator acting through the
domain can make it hold a verifier key alone.

**An independent verifier (ruling 210).** "No. Ruling 160 wants the practice's
record and the wallet's to both hold, which means little if the practice issues
both. The verifier must be independent." How the profile lets a relying domain
hold that (PROPOSED): a verification names its verifier; a relying domain may
require the verifier to be a holder other than itself; and a domain that admits
`release` keys only holds no verifier key the practice supplied, since every
one arrives with a release of the relying system. For openChart's first
practice, ruling 211 makes that key the owner's own verification service,
shipped in openChart. What the profile cannot enforce: it cannot see who
controls a verifier key, so independence rests on who ships the release; where
`two_person` keys are admitted, two people at the same practice can add the
practice's own key, which the provenance makes visible but does not prevent;
and whoever runs a deployment's software can forge the two-person record or
skip the check altogether (D8's limits). So ruling 210 holds in openChart with
release-only keys, and is visible, not enforced, wherever `two_person` keys are
admitted (tension T7).

**Held for named licensing authorities.** A held verifier key records, as
`held_for`, the licensing authorities it is held for, each by the identifier a
verification carries in `licence.authority`, and is relied on for those alone: a
verification naming another authority is refused as
`verifier_not_held_for_authority` (D5), however correctly it is signed. Holding
a key for one authority never trusts it for every authority.

**Only a key that ships with a release supports the aim (D8).** An honest check
runs on a copy of the records with the verifier keys from a release of the
relying system. A `release` key is one such a check holds. A `two_person` key is
evidenced only by the domain's own records, so an honest check does not hold it:
a genuine sign-off resting on it fails that check, and inside the deployment a
forged two-person record looks the same as a genuine one. The standard keeps
both provenances, because a relying domain with no release channel of its own
still needs a way to hold a verifier's key. Each reliance records the
provenance of the key it rested on, and a reliance resting on a `two_person` key
is recorded as such and falls outside the aim. A relying domain may admit
`release` keys only; the recommendation for openChart version 1 is that it does
(Open question 3).

**The first revocation list arrives with the key.** A verifier key is
delivered, with a release or by two people, together with that verifier's
newest revocation list, so a new deployment can check the verifier's
verifications from its first sign-off, and `not_checkable` with
`revocation_list_missing` does not hold that sign-off up (D5).

**State, and a compromise time.** A held verifier key is `active`, `suspended`
or `revoked`. A key known to be compromised also records the time from which it
is treated as compromised. From the moment the compromise is recorded, no
verification it signed is relied on, and every reliance on a verification it
signed, made since that time, is raised to the responsible human through the
domain's declared escalation path. A compromised key can sign a verification
with any `issued_at` it likes, so its verifications are not sorted into good and
bad by their own dates; genuine ones are reissued under a new key.

**The held record** (PROPOSED kind `xfactory_wallet_held_verifier_key`): the
verifier's DID and wallet, the key and its fingerprint, the licensing
authorities it is held for, its provenance, the sequence of the revocation list
delivered with it, its state, and `compromised_since` where it applies.

REJECTED:

- **The domain's verifier keys as trust anchors of a wallet the domain holds.**
  The first draft did this, through `add-trust-anchors-and-machine-holders`. A
  trust anchor is owned by a wallet, so the domain would need a wallet of its
  own, which is outside ruling 154's exception.
- **Any administrator may add a verifier key.** The practice could then mint
  verifications for its own practitioners.

## D5 — Checking a verification, and never waiting (ruling 156) (PROPOSED, PP-5)

Ruling 156: "Inside the practice's own deployment, so the chart never waits on an
outside service to accept a decision." A relying domain decides from six things
it already holds: the verification, as the holder presented it; the held
verifier key (D4); every revocation it has received from that verifier, the
newest list included (below); the held record of the bound wallet (D8); the
supersession index it keeps (below); and its own clock. It contacts no
verifier, licensing authority, directory, wallet or holder device, and waits on
none.

**Revocation freshness never blocks** (ruling 212: "No, per ruling 156. It uses
the newest list it holds, records how old that was, and alerts the medical
director once it is over 72 hours old. A verification still expires on its own
date."). Ruled here: freshness never blocks, the newest list held is used, and
its age is recorded. The 72 hours and the alert are openChart's. The rest is
PROPOSED. The deployment fetches each verifier's revocation list when it can. At reliance it uses the newest list it holds and
never waits for a newer one. It records on the reliance which list it used (the
verifier, the list's sequence and issue time) and how old that list was. Past
the domain's freshness bound the reliance still stands, is flagged, and is
raised to a human in the relying domain, never to the signer alone (D6, "Who
receives a raised item"). A held list is never replaced by one with a lower
sequence, so nobody can roll a revocation back by replaying an older list.

**A revocation once received is permanent.** A newer list that left out an
earlier revocation would otherwise make a revoked verification pass again,
whatever its sequence. So a verifier keeps every revocation in every list it
publishes until the revoked verification's reliance bound has passed (D6), and
a relying domain keeps every revocation it has received and treats it as
permanent: a later list that omits one restores nothing. An omission before the
revoked verification's reliance bound is a fault in the verifier's list, and
the domain raises it to a human.

**The worst case, stated plainly.** If no newer list arrives, because the
verifier stops publishing or because whoever runs the deployment withholds its
lists (D8's limits), no revocation reaches the domain either. Each reliance on
that verifier's verifications then stands, flagged and raised, and the only hard
stop is each verification's reliance bound, up to twelve months after the
licence was checked (D2).

**What expires does so on a date the deployment already holds.** A verification's
reliance bound is in the verification. Past it the verification is not relied
on, which needs no outside call; the practitioner renews ahead of time (D6).

**Three outcomes** (PROPOSED names): `relied_on`, carrying the list used and its
age, the provenance of the verifier key (D4) and, past the freshness bound, a
flag; `refused`, with a reason from a closed list (`reliance_bound_passed`,
`superseded`, `revoked`, `wallet_mismatch`, `key_not_covered`,
`verifier_not_held`, `verifier_not_held_for_authority`, `verifier_not_active`,
`verifier_compromised`, `signature_invalid`, `wallet_not_active`,
`status_not_accepted`), where `verifier_not_held_for_authority` means the domain
holds the verifier key, but not for the licensing authority the verification
names (D4), and where
`signature_invalid` means that the verifier's signature does not verify, or
that a proof of possession the verification records does not verify or does not
name the key and the wallet it is recorded for (D3); and `not_checkable`,
with a reason (`revocation_list_missing`, `wallet_record_missing`), only where
the deployment holds nothing to check with. `not_checkable` is cured by the
deployment obtaining what it lacks, never by the signer. Because a verifier key
arrives with its verifier's newest list (D4), `revocation_list_missing` arises
only when that delivery failed.

**Supersession is decided from what the domain holds, and the domain keeps it.**
Supersession needs no revocation: a verifier that re-verifies issues a later
verification naming the earlier one in `supersedes`, and may publish nothing
about the earlier one. So the verification presented, its verifier key, the
revocation list, the wallet record and the clock can all be unchanged while the
verification has been replaced, and a check limited to those five cannot tell.
The domain therefore keeps every licence verification it receives, and keeps a
supersession index of them: for each one another names in `supersedes`, the one
that supersedes it. A later verification enters the index only once its
signature verifies under a held verifier key and it is from the same verifier,
for the same licence and wallet. The index is derived from the kept
verifications, so it can be rebuilt from them; an entry is never removed, even
when the later verification is revoked or passes its reliance bound, because a
superseded verification never returns to force (D6). Presented after the domain
received its successor, an earlier verification is refused as `superseded`. One
exception keeps a compromised verifier key from superseding genuine
verifications for good: an entry made by a verification signed with a verifier
key later recorded as compromised stops applying from the moment the compromise
is recorded, and is kept for audit. A compromised key can sign any `issued_at`
(D4), so its entries are not sorted by date; the effect of a forged entry was
only a refusal, and reissuing the genuine verification recovers from it.
What someone who can alter the domain's records can do to the index is in D8.

**The freshness bound is the domain's.** The verifier states, in each list, the
time by which it will publish the next; the domain declares how old a list may
be before a reliance on it is flagged. Neither number is openWallet's. For
openChart, ruling 212 sets it at 72 hours, with an alert to the medical
director.

**The alternative, which ruling 212 declines:** refusing a reliance once the
newest list held is older than the freshness bound. It would give a sharper
guarantee against a revocation that has not arrived, and it would make accepting
a decision wait on the verifier's next publication.

REJECTED:

- **Asking the authority or the verifier at the moment of reliance.** It puts an
  outside service in the path of every sign-off, which ruling 156 forbids, and
  tells a third party who relied on whose licence and when, the leak
  `add-trust-anchors-and-machine-holders` D3 names for online certificate checks.
- **A stale list making sign-offs "not checkable" until the verifier publishes
  again.** The first draft did this. It waits on an outside service.

## D6 — How a verification ends, and what the practitioner must do (PROPOSED, PP-6)

A verification stops being relied on at its reliance bound, with no grace
period; when the domain holds a later verification that supersedes it; when its
verifier revokes it; when the bound wallet is revoked, and while it is
suspended; and from the moment the domain stops holding the verifier's key as
active.

**The verifier re-checks the source every month, and revokes on a change.**
Ruling 213: "The verifier re-checks the board's record monthly and revokes on a
change, so the practitioner renews once a year at most." This change states the
re-check as a duty on the verifier (requirement on how a verification ends); a
verifier MAY re-check more often (PROPOSED). That is what keeps the gap between an authority's action and the
relying domain short, not the reliance bound. If an authority suspends a licence
after a verification was issued, the verification is relied on until the
verifier's revocation reaches the domain or its reliance bound passes, whichever
comes first. The gap is bounded by how fast the verifier learns of the change
and publishes, and by how often the domain fetches; a reliance made on an old
list is flagged and raised (D5). In the worst case no newer list arrives at all,
because the verifier stops publishing or because whoever runs the deployment
withholds its lists; then the only hard stop is the verification's reliance
bound, up to twelve months after the licence was checked, and every sign-off
resting on it until then stands, flagged and raised.

**What the practitioner must do, and how often:**

1. Sign with a passkey or a security key (ruling 208), declared in their wallet
   and able to make `wallet-webauthn-proof` proofs; for openChart, a passkey that
   syncs through their Apple or Google account counts only on a device they have
   enrolled, and a security key always counts (ruling 209). Which custody model
   such a key declares is settled in `add-webauthn-proof-profile`, where it is
   still open for a synced passkey (D9).
2. For each licence, prove possession of each sign-off key to a verifier the
   practice holds, once, so that it issues a verification naming those keys.
3. Bind each sign-off key to their account in their own session (D8).
4. Renew each verification before its reliance bound: once a year at most, as
   ruling 213 says, sooner if the licence expires sooner. Renewal is a new verification
   and a fresh proof of possession to the verifier.
5. Obtain a new verification whenever they add or replace a sign-off key.

No monthly ceremony is asked of them. The verifier's monitoring does the rest.

**A revocation is terminal.** A revoked verification never returns to force;
re-verification is a new verification that names the one it supersedes. That is
the rule the ratified `add-composition-drift-cascade` states for grants ("A
revoked grant SHALL NEVER return to the active state"), applied to a record that
is not a grant.

**"Revocation propagates through the chain", read for a record that is not a
grant.** A verification confers no authority and has no derivations, so the
requirement's propagation through derived grants does not reach it. Its other
principles do: revocation is checked at use, never trusted from issuance, and
revoking the holder's standing (here, the wallet) ends what rests on it. This
change does not modify that requirement, which the ratified drift cascade
already restates (D13).

**Retiring a key.** A verification names keys. Retiring one stops it making a
sign-off the verification supports; the verification still supports the other
keys it names.

**Reason classes** (PROPOSED, closed): `licence_status_changed`, `issued_in_error`,
`binding_lost`, `wallet_revoked`, `verifier_withdrawn`. A revocation never
rewrites a reliance made while the verification was in force. A revocation of
class `issued_in_error`, which says the verification was never true, or of class
`verifier_withdrawn`, which gives no reason the domain can weigh, is raised for
every reliance it affects to the responsible human through the relying domain's
declared escalation path; so is every reliance on a compromised verifier key
since its compromise time (D4). The drift cascade records a reason class that is
never consulted to narrow propagation; these classes are consulted only to widen
who is told, never to spare anything.

**Who receives a raised item.** Never the signer alone. Every item this profile
raises (a reliance on an old list, on a compromised verifier key since its
compromise time, or on a verification revoked as `issued_in_error` or
`verifier_withdrawn`) reaches a human other than the practitioner whose sign-off
it concerns. Where that practitioner is the human who would receive it, as when
the medical director of a one-practitioner practice signs, the relying domain
names a second recipient, such as its administrative role or a named outside
reviewer. For openChart, the recommendation is that a practice names one when it
configures its escalation path (Open question 4).

REJECTED:

- **A grace period after the reliance bound.** It turns the bound into a
  suggestion.
- **A thirty-day reliance bound.** The first draft recommended it. It asks every
  practitioner for a proof-of-possession ceremony with an outside verifier every
  month, for protection the verifier's monitoring already gives.
- **Rewriting past reliances on revocation.** The record of what a decision
  rested on at the time is the audit; what to do about it is a human's decision.

## D7 — What a verification never is, and how it meets the relying domain's own licence record (rulings 151 and 160) (PROPOSED, PP-7)

A licence verification is evidence that a named verifier found a licence in a
stated status and bound it to a wallet and to named keys. It is not proof of who
a person is, not a patient or subject identifier, and not authority.

**The match openChart's Open Question 9 asks for has three legs,** and no single
party supplies all of them:

1. **The verifier's leg.** The verifier states that the licensee it checked is
   the holder of the keys it names (`identity_evidence_ref`), and each key proved
   possession to it (`subject.keys[]`).
2. **The relying domain's binding.** The domain binds each key to its own account
   by that key's proof of possession, over a challenge the domain issued, in that
   account's own session (D8). openChart's AU-07 is this leg.
3. **The relying domain's own licence record.** The domain compares the licensing
   authority, the jurisdiction, the licence identifier and the licence class in
   the verification with its own record of that account's licence. That needs
   the domain's own record to hold those same four facts. openChart's AU-03
   attestations are this record, and they hold none of the four today; that is
   openChart's to change. Ruling 98's check is this record for a first
   designation.

So: the account's person holds the key (leg 2), the key's holder holds the
licence according to the verifier (leg 1), and the practice's own record says
the account's person holds that licence (leg 3). Legs 2 and 3 are the domain's
own records, which whoever runs the deployment can alter; the signer an honest
check reports comes from leg 1 (D8, "Who the signer is"). Ruling 160's "both must hold"
is legs 1 and 3 together, and it is worth most when the verifier is not the
practice (D4, Open question 3).

**The wallet identifier still never becomes a person's identifier.** The domain
resolves the person by its own account identifier. The wallet identifier on a
sign-off is evidence of which wallet signed.

REJECTED:

- **Carrying the holder's name or date of birth in the verification so that a
  domain can match it.** It would make the wallet a carrier of personal identity,
  and the domain already knows who its account belongs to.

## D8 — The threat model, per-key binding and the held wallet record (PROPOSED, PP-8)

**The aim, ruled.** Asked "Should a sign-off hold up even against whoever runs
the practice's server?", the owner ruled (214): "Yes, against forgery: the
verification names the practitioner's own signing keys and is signed by the
independent verifier. It does not stop that person deleting records or
back-dating; outside timestamps can close that later."

**How this change reads it** (PROPOSED). A forgery is a sign-off in a
practitioner's name made without that practitioner's key. The practitioner is
the licence holder that the relied-on verification names, for the keys it
names. An honest check is one run on a copy of the records with the verifier
keys from a release of the relying system. So the aim holds only for a sign-off
whose licence verification is signed by a verifier key that ships with a
release; a reliance on a key that two people added is recorded as such and falls
outside it (D4). It holds, too, only where the verifier identified the licensee
itself, by its own means and independently of the deployment, in the session in
which each named key proved possession (D3); a proof relayed through the
deployment cannot show that, so no verification names a key on one. Every
sentence below was checked against the ruling's words.

**Who the signer is.** A sign-off shows which licence holder's key signed, as the
verification names that licence holder. Which account the domain shows the
decision under is the domain's own record, which whoever runs the deployment can
alter. An operator who is also a practitioner can rebind another practitioner's
account to their own key and verification and sign under that account, and the
three legs of D7 still hold, because none of them authenticates which person an
account belongs to against whoever runs the deployment. That is not a forgery in
ruling 214's words: the key and the verification are the operator's own, and the
verification names the operator's licence. So an honest check reports the signer
from the licence fields of the verification relied on, never from the account,
and a relying domain raises any difference between that licence and its own
licence record for the account (requirement on evidence about a licence). The
profile binds a key to a licence holder; it does not bind an account to a
person, and does not claim to. Ruling 214's words hold as written under this
reading, on the conditions this section states, and short of a synced passkey's
account, a limit below.

**What reaches it:**

- **A verification names key fingerprints** (D2, D3), signed by a verifier whose
  key arrived with a release of the relying system, so an honest check holds it
  (D4). A key that two people at the practice added is held too, but a reliance
  on it falls outside the aim. A key someone adds to the held wallet record
  later is covered by nothing.
- **The verifier identified the licensee itself,** by its own means and
  independently of the deployment, in the session in which each named key
  proved possession (D3). A related-origin proof shows only that a client holding
  a credential scoped to the deployment signed at the verifier's page; the
  deployment is that relying party and can register a credential of its own, and
  a native client writes whatever origin it likes, so only the verifier's own
  identification ties the key to the licensee. That identification is the
  verifier's record, which a relying domain cannot check, and a relayed proof
  never meets it.
- **Each sign-off key is bound individually,** by that key's own proof of
  possession, over the domain's challenge, in the practitioner's own session.
- **The held wallet record comes only from the practitioner.** The domain takes it
  from the practitioner, in their own session, and accepts a key added to it only
  with a proof from the added key made in that session. No administrator adds a
  key; an administrator may suspend the domain's reliance on it. A change to the
  record's state reaches the domain from the practitioner, in their own session,
  or from a verifier's revocation list (`binding_lost`, `wallet_revoked`).
- **At acceptance the relying domain checks the proof itself** under the public
  key it bound, which a verification names, over its own recomputed statement
  digest. openSig's attestation is checked too, but a forged attestation cannot
  stand in for the proof (the seam, "Who verifies what").

**Its limits, stated as plainly.** The ruling names two: deleting records and
back-dating. Beyond its words (PROPOSED), whoever runs the deployment can also
hide records, withhold revocation lists, run altered software that skips the
checks, refuse service, and show the practitioner one statement while the key
signs another. Back-dating is possible within what the deployment's own clock
allows, because the statement's signing time and the single-use challenge both
come from the deployment. Substitution is possible because no key in either
profile shows its holder what it signs: a passkey or security key shows at most
the relying party and the account, and the page that shows the statement is the
deployment's own. A substituted sign-off uses the practitioner's key and
gesture, so it is not a sign-off made without the key, and an honest check
accepts it; whether it counts as a forgery under ruling 214 is put to the owner
(Open question 21). Withholding lists forges no sign-off, but it keeps a revoked licence
relied on, every reliance flagged, until the verification's reliance bound (D5,
D6). A practitioner who colludes with the operator can back-date too. Outside
evidence of time, such as anchoring the digests of openSig's attestations, is a
successor (D15).

**A relayed proof.** A proof that reaches the verifier through the deployment
shows the verifier only what the deployment chose to forward, possibly a proof
from a key of its own. The aim does not hold for it, so no verification names a
key on one (D3).

**A synced passkey's account.** Whoever controls or can recover the account a
synced passkey syncs through, such as a managed work account the practice
administers, can obtain the passkey on a device of their own and sign with the
practitioner's own key without the practitioner. Under this reading that is not
a forgery, because the key is the practitioner's, yet it is what the ruling asks
about. Neither profile can see which account holds a passkey; the passkey
profile records the practitioner's declaration that the account is theirs alone
and is not administered by the practice, and puts the limit to the owner
(`add-webauthn-proof-profile`, its Open question 12). No synced passkey can be
bound there until the custody registry has a model for it (its Open question
1).

**The supersession index under the same threat** (D5). The index is one of the
domain's records, so whoever can alter them can add an entry, which refuses a
verification still in force, or delete one, which lets a superseded verification
be relied on again. Adding is refusing service, among the limits. Deleting
forges no sign-off by itself, because a sign-off still needs a key the domain
bound and the verification names, made by its holder; it matters where the
later verification dropped a key, for instance one the practitioner lost. An
honest check does not trust the index: it rebuilds it from the verifications in
its copy of the records, each of which names what it supersedes and is signed
by the verifier, so a deleted entry shows unless the later verification itself
is deleted, which is deleting records, among the limits. A practitioner who
loses a key also retires it in their wallet, which stops that key making a
sign-off whatever happens to the index (D6). An entry made by a verification
whose verifier key is later recorded as compromised stops applying from that
record, and is kept for audit (D5).

**Revocations under the same threat.** A relying domain keeps every revocation it
has received and treats it as permanent (D5), so a newer list that omits an entry
restores nothing. Whoever can alter the domain's records can still delete a kept
revocation, which is deleting records; an honest check finds it again in any list
in its copy that carried it, since a verifier keeps every revocation in every
list until the revoked verification's bound has passed.

**Per-key bindings and the registry.** The ratified profile checks a proof against
a binding from a trusted registry, and `add-reference-registry-custody` keeps one
current binding per subject. Each bound key therefore has its own binding, whose
subject is the domain's reference for that account's binding of that key. Only a
bound key can sign; replacing a key is a new binding, and a sign-off with the new
key needs a verification that names it (D6, item 5).

REJECTED:

- **One binding per wallet.** The first draft bound the wallet, so every key the
  held record declared could sign under it, including one an operator added.
- **Requiring `did:key` so that the DID is the key.** It would also stop a key
  following an added record entry, but it constrains every practitioner's wallet
  layout to solve what naming fingerprints already solves.

## D9 — The sign-off: a proof over the relying domain's statement; custody; consent; devices (PROPOSED, PP-9)

**The proof: a passkey or a security key, under `wallet-webauthn-proof`** (ruling
208). A practitioner's sign-off is a proof under the profile drafted in
`add-webauthn-proof-profile`, whose `challenge_digest` is `sha256:` and the
SHA-256 of the relying domain's RFC 8785 canonical statement for that sign-off.
The statement carries the domain's single-use challenge, so the proof binds that
challenge. The profile's WebAuthn challenge is derived from the proof's binding
fields, so the proof binds the wallet, the key, the subject, the custody
reference, the binding and its revision, as the ratified profile does, and also
the relying domain, by its relying-party identifier hash and origin. The domain
is the challenge's owning issuer, which, in the ratified profile's words,
"enforces freshness, caller binding and one-use". The ratified
`wallet-challenge-proof` stays as ratified and binds the same things in its own
form; a relying domain states which profile it accepts, and openChart's version
1 accepts the passkey and security-key profile (ruling 208). For openChart the statement is its sign-off statement and the
digest is its `statement_sha256` (its CD-53).

**The custody reference** (closes the gap between an opaque reference and the
closed registry). The ratified profile treats `custody_ref` as an opaque
reference. In a binding used for a sign-off it is
`openxwallet-custody:<registry_version>:<model>`, for example
`openxwallet-custody:1:isolated_per_use_authorized`, and it equals the custody
the held wallet record declares for that key. A proof whose custody reference
differs from its binding's is already refused by the profile, which compares the
proof's references with the binding's. openSig's `custody_reference_mismatch`
compares the binding's custody reference with the held record's declaration.

**What the signing key's custody evidences** is already stated by the closed
custody registry. A key whose declared custody is `isolated_per_use_authorized`
evidences that the HOLDER acted; `holder_readable` and `isolated_invocable`
evidence only the holder's environment. The registry defines the per-use
authorization as one the holder's execution context "cannot itself supply", so a
PIN typed into the workstation that asks for the signature does not supply it.
This change leaves the registry's statement as it is.

**What a relying domain accepts for a sign-off is its own acceptance rule** (not a
change to the registry). The profile requires only that a relying domain states
which custody it accepts for a practitioner's sign-off. It may ask more of the
signing key than its declared custody: the registry's per-use authorization may
be "a hardware presence check, an external policy approval, a separate
custodian", and a relying domain may accept only the first, each use authorized
by the practitioner on the device that holds the key. The registry's statement,
and every other consumer's reading of it, are unchanged, so no MODIFIED delta of
the registry or of the core's custody requirement is needed. Under
`wallet-webauthn-proof`, the user-verification flag the authenticator sets on
each use (Level 3, §6.1) shows that verification happened on the authenticator,
as far as the authenticator is trusted; under the ratified profile nothing
shows it, and for a key a custody-acceptance record would show it (Open question
6).

For openChart, ruling 209 is that rule: a passkey that syncs through the
practitioner's Apple or Google account counts only on a device the practitioner
has enrolled; a security key always counts; controlled substances stay out.
openChart's draft also proposes accepting only `isolated_per_use_authorized`
(its CD-48), which a synced passkey may not honestly be able to declare (D6, item
1; tension T4).

**A wallet whose sign-off key is per-use authorized must itself be.** The core
refuses a declared key whose custody ceiling outranks its wallet's, and the
wallet's own custody is its primary key's. So a practitioner's wallet that declares
an `isolated_per_use_authorized` sign-off key must declare its primary key with the
same custody. That changes what hardware a practitioner needs.

**A declaration is not proof.** The ratified profile's design says it "does not
attest that the referenced custody or agent composition is actually isolated. A
trusted registry supplies those facts and their acceptance." So the evidence on
which the registry accepted a key's custody matters, and openWallet defines no
standard for it yet (Open question 6, tension T3).

**Possession is neither authority nor consent.** The ratification record of
`add-challenge-proof-runtime` states the limit in full: "They do not assert MFA,
human presence, explicit human consent, workload composition, delegation or domain
permission. The relying party continues to own permission and separate
exact-request human consent." The change's own ratification entry, in its
`.openspec.yaml`, adds: "Real custody, factor adapters, human approval and live
qualification remain separate gates." A sign-off is consent to
an exact request. So the relying domain owns it: what the signer was shown (openChart
already refuses a signature over a digest that differs from the content shown),
re-authentication at signing (openChart's CD-10), and per-use authorization at the
key, through the custody it accepts. The proof is evidence that a key signed a
digest, and no more (tension T2).

**Devices, settled by ruling 208.** "A passkey or security key. Draft that change
now. A smart card cannot be used from a phone." The ratified profile is Ed25519
over an exact, domain-separated preimage, and a WebAuthn authenticator signs only
its own authenticator data followed by the SHA-256 of the client data (Web
Authentication Level 3, §6.3.3), so no passkey or security key can make the
ratified proof. The profile they can make is drafted as its own change,
`add-webauthn-proof-profile` (capability `wallet-webauthn-proof`), and states what
this section used to list as owed: how its challenge binds the statement digest,
the binding references, the revision and the custody reference; what binds the
proof to the deployment (the relying-party identifier hash and the origin); the
user-presence and user-verification flags on every use; the backup flags that
tell a synced passkey from a device-bound key; what registration attestation
evidences; and that openSig can attest it. This change relies on it and does not
restate it. Which custody model a synced passkey declares is open there, because
the registry's text may not honestly cover a key that a provider copies to every
device in an account, and until it is answered no synced passkey can be bound
under that profile (tension T4).

REJECTED:

- **Version 1 on smart-card class keys only.** The first draft recommended it. It
  contradicts ruling 35 and EN-06 for phones, and would hide a buildability gap
  behind a device rule.
- **Widening the ratified profile in this change.** It is ratified as it stands;
  a new proof form is a new change.
- **A profile rule that every key of a practitioner's wallet must be
  `isolated_per_use_authorized`.** A practitioner's wallet may declare keys for
  other uses, within its own ceiling; the relying domain decides what it accepts
  for a sign-off.

## D10 — The exception of ruling 154 and the sentence of ruling 183 (the exception RULED; its wording PROPOSED, PP-10)

The MODIFIED block keeps every word of the canonical requirement and both of its
scenarios, and adds two paragraphs and four scenarios.

**The exception is named by the act, as the ruling names it.** Ruling 154: "Amend
openWallet's rule with one named exception: a practitioner's sign-off of a medical
decision." A consuming domain MAY make a practitioner's wallet a prerequisite for
that practitioner's sign-off of a medical decision, and for the binding of that
wallet to the practitioner's account that the sign-off needs, and for nothing
else. The binding is named because a sign-off cannot be checked without it: it is
part of the act, not a second act. The scenario "the exception admits no second
act" makes "one" testable. A domain that requires a wallet to sign in, to read a
record, to enter information, to configure itself, or to hold the keys it checks a
sign-off with is outside the exception.

**The relying domain needs no wallet of its own.** The first draft gave it one, to
hold verifier keys as trust anchors. Under the act-named exception the domain
holds verifier keys as records of its own (D4), and openSig's attestation key is a
key of the deployment, not a key declared in a wallet. A verifier holding a wallet
of its own is a party in the wallet ecosystem, and its wallet is no prerequisite
for operating the relying domain.

**Why the exception is in the core.** Ruling 154 amends the core's rule. A generic
hook, such as "a profile may name an act that needs a wallet", would let any later
profile add an exception without amending the core, which is not one named
exception. The core names the act and points to the profile for what that
sign-off is.

**"Medical decision" is the consuming domain's term.** openChart keeps the list of
what counts as a decision. openWallet does not define it, and the exception says
so.

**The rest still works without a wallet.** Ruling 154: "The rest of the chart still
works without a wallet." Ruling 183: "nothing needs the wallet to be reachable to
read the chart." So reconstructing a record and resolving a subject need no
wallet, a signed-off record included, and reading a signed-off record contacts no
wallet. What a domain does with a sign-off attempted without a wallet is the
domain's to decide.

**Ruling 183 clarifies the identifier rule; it is not a second exception to the
prerequisite rule,** and the delta says so. The ruling's "AI" is a holder of class
`agent`. The ruling's words are kept. PROPOSED: naming an agent holder as a
record's author includes naming it as the party on whose behalf a relay wrote the
record, which is how openChart names an AI that a registered relay delivers (its
AN-02, CD-61 and CD-67). "Never identifies a person" covers practitioners too: a
practitioner's wallet identifier on a sign-off is evidence of which wallet signed,
and the person is the domain's own account.

**No validator or schema behaviour changes for the core.** The subject attestation
still refuses `reconstructable_without_wallet: false` and still resolves only by
`subject_ref`; the exception concerns making and binding a sign-off, not
reconstructing a record. Only that schema's description, which quotes the rule,
gains a sentence (D14).

REJECTED:

- **The exception for "the sign-off and nothing else".** The first draft's wording.
  It left openChart's own account binding, which the sign-off needs, outside the
  exception.
- **The exception for "the acts that make a sign-off checkable".** Broader than the
  ruling: it would have covered a domain holding keys in a wallet of its own.
- **The exception in the profile alone.** A profile cannot override the core's rule;
  the core would still forbid it.
- **Letting a wallet identifier name any holder as an author.** The ruling names an
  AI.

## D11 — The collision with `add-trust-anchors-and-machine-holders` (PROPOSED, PP-11)

That change, `Status: proposed`, also MODIFIES "The capability is an authority
control, never an identity substrate". It appends one sentence to the
requirement's paragraph, on trust anchors, and adds the scenario "an anchor is a
trust fact about a key, never an identity". Its open amendment, pull request #6 at
`4d83535`, does not touch this requirement: it adds a MODIFIED "Authority travels as
attenuated grants, never as keys", which this change does not modify.

**How the two compose.** A MODIFIED block replaces the whole requirement when it
archives, and the pinned CLI refuses an archive whose MODIFIED block omits a
scenario the current spec still has. This leg measured that refusal at
`add-multi-key-wallets`' archive. Both deltas are written against the canonical
text at `a2d554d`, so both validate today. **Whichever of the two archives second
SHALL first regenerate its MODIFIED block at the union** and re-run the pinned
gate. The CLI guards scenarios but not the requirement's body text: an archive
whose block keeps the other change's scenario and drops its sentence passes, and
the sentence is lost. So the regeneration is checked against both blocks
sentence by sentence and scenario by scenario, ignoring line breaks, and not by
the CLI alone (`tasks.md` 6.1). A literal line-by-line check is not enough
either way: it flags a lossless union, because that change appends its sentence
to a line of the canonical paragraph.

**The union**, for whichever regenerates:

1. the canonical first paragraph, with that change's appended sentence on anchors,
   unchanged;
2. this change's two paragraphs, unchanged;
3. the scenarios: the two canonical ones, that change's "an anchor is a trust fact
   about a key, never an identity", and this change's four.

**No sentence widens the exception.** That change says this capability "SHALL NOT
make holding anchors a prerequisite for operating a domain, any more than holding a
wallet". It stays as written. The relying domain holds its verifier keys as records
of its own and never as anchors of a wallet (D4), so holding anchors is no
prerequisite for checking a sign-off, and the exception covers no anchor. The first
draft proposed a harmonizing sentence that would have widened the exception to "the
anchors a domain holds"; it is withdrawn.

This change does not edit that change, and does not comment on its pull request.

## D12 — Relation to the trust anchors proposed in `add-trust-anchors-and-machine-holders` (PROPOSED, PP-12)

This change no longer depends on that one. The relying domain's held verifier key
(D4) resembles an `issuer` anchor: a root that vouches for a population, verified
offline. It differs in the one way ruling 154 makes decisive: an anchor is owned by
a wallet, and the relying domain has none. Its provenance set (`release`,
`two_person`) is also different from that change's provenance methods, because its
question is different: not "how did this holder come to trust this key" but "can
one administrator, acting through the domain, make it trust a verifier alone, and
can a check from outside the domain see how the key arrived".

If that change is ratified, the realization may reuse its machinery where the two
agree, such as the per-key state and its rule that a revoked key never returns. That
change names, among its successors, "Anchor sets shared across wallets, such as an
organisation-level anchor set distributed to every host"; a verifier key set
delivered with a release of the relying system is close to that, and the two could
converge there. Either way the two can be ratified in either order.

## D13 — Composition with the other changes this change touches

- **`add-challenge-proof-runtime`** (ratified wire profile, not archived). Used
  unchanged; no byte of it moves. Its capability `wallet-challenge-proof` is not yet
  canonical. If its archive renames it, this change's reference to it moves
  editorially. Its limits are kept in full: possession only, and no claim of MFA,
  human presence, explicit human consent, delegation or permission (D9).
- **`add-composition-drift-cascade`** (ratified, not archived). It MODIFIES
  "Revocation propagates through the chain". This change does not, so the two
  cannot collide; D6 relies on its principles.
- **`add-reference-registry-custody`** (commissioned). Its registry is the kind of
  trusted registry D9 needs inside a deployment; one current binding per subject is
  why each key gets its own binding (D8). Its reference custody is
  `isolated_invocable`, which evidences the environment, so it is never a
  practitioner's custody for a sign-off openChart accepts.
- **`add-trust-anchors-and-machine-holders`** and pull request #6: D11 and D12.

## D14 — Placement, names, code surface and release class (PROPOSED, PP-13 and PP-14)

**Which leg holds the new contract family is open (Open question 7).** The declared
Q7 override places `contracts/openxwallet/` and `contracts/openxwallet-agent-profile/`
in the code leg, beside the validator that resolves every contract path from its own
location, and covers those two families only. The ratified challenge-proof change
says "New schemas default to spec leg; legacy wallet Q7 does not automatically cover
them", and put its own schema in this leg's `contracts/`. Feature 006's plan expects a
profile to arrive as "a third directory" beside the two. The recommendation is the
code leg, by an explicit extension of the Q7 override, because Q7's reason holds for a
family validated by the same validator: "The schemas, the corpus and the validator are
one release unit."

**Names that become machine keys once released** (root AGENTS.md rule 3), all PROPOSED
and cheapest to change now:

- the capability `openxwallet-practitioner-profile`, and the directory
  `contracts/openxwallet-practitioner-profile/`;
- the kinds `xfactory_wallet_licence_verification`,
  `xfactory_wallet_licence_revocation_list` and `xfactory_wallet_held_verifier_key`,
  keeping the `xfactory_wallet_*` prefix the family keeps;
- the contract ids `openxwallet-licence-verification`,
  `openxwallet-licence-revocation-list` and `openxwallet-held-verifier-key`;
- the signing domains `openWallet.licence-verification.v1` and
  `openWallet.licence-revocation-list.v1`;
- the custody reference form `openxwallet-custody:<registry_version>:<model>`;
- the closed values of `status_found`, `source.kind`, the held key's provenance and
  state, the reason classes, and the check outcomes and reasons;
- the finding-code family `licence-verification-*`.

The spelling is "licence", the noun as openChart's drafts spell it.

**The validator** gains three kinds in `KIND_TO_SCHEMA`, ERROR codes in the new
family, and one requirement row per ADDED requirement (proposed `OXWP-R1` to
`OXWP-R8`), each with at least one negative confirmation. No code is renamed,
repurposed or reclassified, and there is no new WARNING, because LedgerxFactory runs
the validator with `--strict`. Facts the validator cannot check, such as a verifier's
signature, are reported as NOTES, as the canonical validator "does not verify
signatures, resolve DIDs, or contact a key store".

**One description sentence moves one digest.** The subject attestation schema's
description quotes the rule this change amends. Left alone it would state the rule
without its exception, a description false on arrival.

**Release class: an ADDITIVE MINOR.** Three owned members are added and one digested
byte moves. Nothing a consumer declares becomes invalid. The five coordinated values
are allocated at realization and nothing is reserved here.

## D15 — Non-goals and named successors (PROPOSED, PP-15)

Each is out for a reason, not by omission, and each is a scope choice the owner may
overturn:

1. **The proof profile for passkeys and security keys,** and openSig's attestation
   of it: drafted now as its own change, `add-webauthn-proof-profile`, under
   ruling 208 (D9), and not part of this change.
2. **A custody-acceptance record**: the evidence on which a registry accepts a key's
   declared custody, such as registration attestation (Open question 6).
3. **Outside evidence of time**, such as anchoring the digests of openSig's
   attestations, or a trusted timestamp (D8).
4. **An identity-proofing standard.** The verifier's record (D3).
5. **Equivalence of licence classes across jurisdictions.** The relying domain's
   judgment (D2).
6. **A sign-off made in another system.** Ruling 186: openChart only, in version 1;
   it counts later, once openWallet and openSig can prove it to the chart. A proof
   over a statement whose challenge the chart did not issue needs its own change.
7. **A patient profile.** Still a named successor gated on a consumer of its own.
8. **Practitioner credentials other than a licence**: a controlled-substance
   registration, a board certification, hospital privileges. openChart keeps
   prescriber facts as practice attestations.
9. **A scheme accrediting verifiers.** Each relying domain decides which verifier
   keys it holds, within D4's provenance rule.
10. **A use-time reliance record kind**, which would make reliance statically
    checkable, like the verification-event record that
    `add-trust-anchors-and-machine-holders` names as a successor.

## The seam between openWallet and openSig

This section is written in the same words in openWallet's
`add-practitioner-profile-and-licence-verification` and in openSig's
`add-wallet-bound-attestation`. A change to it in one draft is a change to it
in both. Every line of it is PROPOSED.

**The split.** openWallet owns the keys, the proof of possession and the
licence verification. openSig owns a sealed record that a given proof over a
given digest verified, or did not, against a given key binding at a given time.
The relying party (openChart, for a practitioner's sign-off of a medical
decision) issues the single-use challenge, writes the statement, owns
exact-request consent, binds each sign-off key to its account, checks the
proof, the attestation and the licence verification, and alone decides whether
the sign-off counts. Neither openWallet nor openSig decides clinical meaning.
openWallet's draft calls the relying party the relying domain, after its
core's "consuming domain"; the two words name one party.

**The aim, ruled (ruling 214).** "Yes, against forgery: the verification names
the practitioner's own signing keys and is signed by the independent verifier.
It does not stop that person deleting records or back-dating; outside
timestamps can close that later." That person is whoever runs the practice's
server. Read for this seam (PROPOSED): a forgery is a sign-off in a
practitioner's name made without that practitioner's key; the practitioner is
the licence holder the relied-on verification names; and an honest check is
one run on a copy of the records with the verifier keys from a release of the
relying system. The aim holds only where the verifier identified the licensee
itself, by its own means and independently of the deployment, in the session in
which each key the verification names proved possession; a proof relayed through
the deployment cannot show that, so no verification names a key on one. Limits
beyond the ruling's words (PROPOSED): whoever runs the deployment can also hide
records, withhold revocation lists, run altered software that skips the checks,
refuse service, show the account a decision is filed under as someone else's,
and show the practitioner one statement while the key signs another, because no
key in either proof profile shows its holder what it signs; and whoever controls
or can recover the account a synced passkey syncs through, such as a managed
work account the practice administers, can sign with the practitioner's own key
without the practitioner, which neither profile can see.

| Question | The answer both drafts give |
|---|---|
| What identifies a wallet | The `wallet_id` of its openWallet wallet record. It is `wallet_ref` in a proof and in an attestation, and `openwallet_id` in openChart's sign-off evidence. It is attestation, never the identifier of a person or a patient. |
| Who the signer is | The licence holder whose licence the relied-on verification names, for a key it names. Which account the relying party shows a decision under is its own record, which whoever runs the deployment can alter. An honest check reports the signer from the verification's licence fields, never from the account, and the relying party raises any difference between that licence and its own record of the account's licence. |
| What identifies a key | The pair (`did`, `key_id`) under which the wallet declares it, and its `key_fingerprint`: `sha256:` and the lowercase hex SHA-256 of the raw public key, openWallet's one spelling; for a passkey's P-256 key, openWallet's draft passkey profile fixes the raw form. It is `key_ref` in a proof, written as the DID URL `<did>#<key_id>`. An attestation records the reference as the proof gave it and, where openSig found a binding, the fingerprint recomputed from the public key that binding named; it never fills from the proof a value it did not resolve. |
| Which keys may make a sign-off | Only a key that the relying party bound to the practitioner's account individually, by that key's own proof of possession in the practitioner's own session, and whose fingerprint a licence verification in force names. The relying party takes its held copy of the wallet record only from the practitioner, and no administrator adds a key to it. Each bound key has its own binding; with a registry that keeps one current binding per subject, the subject is that account's binding of that key. Replacing a key is a new binding and needs a verification that names the new key. |
| What custody a key declares | One model of openWallet's closed custody registry (`openxwallet-custody`, registry version 1), declared for that key in its wallet record: `holder_readable`, `isolated_invocable` or `isolated_per_use_authorized`. In a binding used for a sign-off, the custody reference is `openxwallet-custody:<registry_version>:<model>` and equals the model the held wallet record declares for that key; openSig's `custody_reference_mismatch` compares those two. Under the registry, as ratified, only `isolated_per_use_authorized` evidences that the holder acted: each use needs an authorization the holder's execution context cannot itself supply, for which the registry names "a hardware presence check, an external policy approval, a separate custodian". A wallet may declare such a key only if its own custody is the same model, because no declared key may outrank its wallet. A declaration is not proof: neither openWallet's proof nor openSig's attestation shows that a key's custody is what the wallet declares; a custody-acceptance record could show that for a key, and openWallet's draft passkey profile records whether a declaration rests on attestation evidence or on the holder's word. How each use was authorized is shown only under `wallet-webauthn-proof`, whose user-verification flag shows that verification happened on the authenticator, as far as the authenticator is trusted; under the ratified profile nothing shows it. |
| Which custody a sign-off needs | The relying party decides, and states which custody it accepts for a practitioner's sign-off. What more it asks of a key, such as each use authorized by the practitioner on the device that holds the key and never by a code typed into the computer that asks for the signature, is an acceptance rule of its own, which leaves the registry's statement as it is. For openChart, ruling 209: "Yes, but only on a device the practitioner has enrolled, as ruling 134 allows for approvals. A security key always counts. Controlled substances stay out (ruling 83) and would need stronger keys." Enrolling a device is the relying party's. No model of the registry as written describes a synced passkey, so openWallet's draft passkey profile binds none until one does, and the yes for a synced passkey waits on that (its Open question 1). openSig records the model the key declares, and for a passkey proof the authenticator's flags as signed, and never raises either. |
| What the proof is made over | In openChart's version 1, a passkey or a security key (ruling 208), under openWallet's draft profile `wallet-webauthn-proof` (change `add-webauthn-proof-profile`): the authenticator signs its authenticator data followed by the SHA-256 of the client data, and the client data's challenge is derived from the proof's unsigned binding fields, so the proof binds what the ratified profile binds and also the relying party, by its relying-party identifier hash and origin. openWallet's ratified possession-only profile `wallet-challenge-proof` stays as ratified: profile constant `openwallet.challenge-proof.v0`; Ed25519 over the domain separator `openWallet.challenge-proof.v0` and a NUL byte, then the RFC 8785 canonical form of every unsigned proof field. In either profile the `challenge_digest` is `sha256:` and the SHA-256 of the relying party's RFC 8785 canonical statement, which carries the relying party's single-use challenge. For openChart that statement is the sign-off statement, and the digest is its `statement_sha256`. The challenge reference is an opaque random value, 32 bytes drawn at random by the relying party's own server and used once, in unpadded base64url, that carries no meaning. The proof also binds the wallet, the key, the subject, the custody reference, the binding and its revision. openSig is given the digest and the challenge reference, never the statement. |
| Who owns consent | The relying party. A sign-off is consent to an exact request, and openWallet's ratified profile does "not assert MFA, human presence, explicit human consent, workload composition, delegation or domain permission". The relying party evidences what the signer was shown, refusing a signature over a digest that differs from it; re-authentication at signing; and, through the custody it accepts, per-use authorization at the key. Neither the proof nor the attestation is consent. |
| Who verifies what | openWallet's verification, in the proof's own profile, checks a proof against the key's binding, which must be current, unrevoked and time valid. openSig runs that verification, never a second implementation of it, and seals the result with what it was given, what it resolved (the binding the proof rested on, where it found one) and its own time. Verifying an attestation is checking openSig's signature over it; validating its result is a second step, and only a `verified` result's sealed proof must verify. A `not_verified` attestation is evidence of a failed attempt, verified by its signature alone; its sealed proof need not verify, and it may carry no binding. At acceptance the relying party accepts only a `verified` result: it verifies the attestation under openSig's attestation key; verifies the sealed proof itself under the sealed public key over its own recomputed statement digest; checks that the sealed fingerprint is a key it bound and that the licence verification names; checks the sealed challenge reference against its statement; and checks the licence verification under the verifier key it holds, with each proof of possession it records, as the proof's own profile defines the check of a recorded proof. |
| Where it is checked | Inside the relying party's own deployment (ruling 156). The key binding registry, the held wallet records, the openSig attester and its attestation keys, the held verifier keys, each for the licensing authorities it is held for, every revocation received from each verifier, kept as permanent, and every licence verification the relying party has received, with the supersession index it keeps of them, are held there. The practitioner's key stays in the practitioner's custody. The check contacts and waits on nothing outside the deployment. The deployment fetches the verifiers' revocation lists when it can, apart from any check, and a revocation list older than the relying party's freshness bound flags the reliance and never blocks it. |
| What neither states | The content behind the digest, the practitioner's authority, their consent, whether they were present beyond what the declared custody evidences, and whether the sign-off counts. openWallet's licence verification states the licence; openSig's attestation states nothing about it. |

## Design calls

Every call below goes beyond the owner's words and is PROPOSED, and each is put to the
owner. Where a row is marked RULED in part, that part states a ruling's words and
nothing more.

| # | Design call | Where |
|---|---|---|
| PP-1 | The profile is a sibling capability `openxwallet-practitioner-profile` over the core; its holder-class rule is a record rule, and a relying domain may also refuse on its held record's class; no agent carries a verification. | D1 |
| PP-2 | The fields of a licence verification, including the keys it names; no clinical scope; the licence identifier in clear; a random verification id; one verification per licence; the closed status set. **RULED in part (213):** the reliance bound, until the licence expires and at most 12 months; measuring the twelve months from the check is PROPOSED. | D2 |
| PP-3 | A verifier is a holder with its own wallet; Ed25519 over RFC 8785 with signing domains of their own; a recorded proof of possession from each key it names, made in the key's own profile (for a passkey or security key, `wallet-webauthn-proof`, obtained by the verifier itself, as `add-webauthn-proof-profile` recommends, by a related-origin ceremony), within the session in which the verifier identified the licensee by its own means, independently of the deployment, never relayed; for a passkey proof, the relying-party identifier, origin, credential identifier, backup flags and the verifier's statement of an identified session recorded with it; which the relying domain checks, its wallet reference included, by the proof profile's check of a recorded proof; opaque verifier references in the recorded proofs; identity proofing is the verifier's record; the standard does not narrow who may verify. | D3 |
| PP-4 | Held verifier keys are records of the relying domain, with a recorded provenance, `release` or `two_person` (a record no administrator acting through the domain can supply alone, which whoever runs the deployment can still alter), the licensing authorities each is held for and relied on for alone, a state and a compromise time; only a `release` key supports D8's aim, each reliance records its key's provenance, and a relying domain may admit `release` keys only (recommended for openChart version 1); each key arrives with its verifier's newest revocation list; reliances since a compromise are raised. **RULED (210):** the verifier must be independent; how the profile lets a domain hold that, and what it cannot enforce, is PROPOSED. | D4 |
| PP-5 | Checking from six held things: the supersession index among them, which the domain keeps, derives from every verification it receives, and never prunes, except that an entry from a verifier key later recorded as compromised stops applying and is kept for audit; and every revocation received, kept as permanent, with verifiers keeping each revocation in every list until the revoked verification's bound; the list used, its age and the verifier key's provenance recorded on every reliance, flagged and raised past the freshness bound; the worst case; no list rollback; `verifier_not_held_for_authority`; `signature_invalid` covers the recorded proofs and their key and wallet references; `not_checkable` only when the deployment holds nothing to check with, cured by the deployment. **RULED (212):** freshness never blocks, the newest list held is used and its age recorded; the 72 hours and the alert are openChart's. | D5 |
| PP-6 | How a verification ends; the worst case; what the practitioner must do and how often; key retirement per key; the closed reason classes; `issued_in_error` and `verifier_withdrawn` raised to a human; a raised item never goes to the signer alone, and the relying domain names a second recipient. **RULED (213):** the verifier re-checks the board's record monthly and revokes on a change, stated as a duty; the practitioner renews once a year at most. | D6 |
| PP-7 | A verification is never identity or authority; the three-leg match, leg 3 needing the domain's own record of authority, jurisdiction, licence identifier and class. | D7 |
| PP-8 | Reading ruling 214 for this profile: forgery as a sign-off without the practitioner's key; the signer reported from the verification's licence, never the account; the aim holding only for verifier keys that ship with a release, and only where the verifier identified the licensee itself in the session in which each named key proved possession; limits beyond the ruling's words (hiding records, withholding revocation lists, altered software, refusing service, content substitution, a relayed proof, a synced passkey's account); what altering the supersession index or a kept revocation can and cannot do; per-key binding; the held wallet record only from the practitioner; one binding per bound key. **RULED (214):** the aim and its two named limits, in its words. | D8 |
| PP-9 | A sign-off is a proof over the statement digest under `wallet-webauthn-proof`, whose challenge binds what the ratified profile binds and the relying domain; the custody reference form and what a mismatch compares; the relying domain states which custody it accepts, and may ask for per-use authorization on the device as its own acceptance rule, leaving the registry's statement as ratified; the user-verification flag shows on-authenticator verification as far as the authenticator is trusted; a per-use key forces the wallet's own custody; consent owned by the relying domain. **RULED (208):** a passkey or security key, and the profile drafted now; **(209)** openChart's acceptance of synced passkeys on enrolled devices and of security keys. | D9 |
| PP-10 | The wording of the MODIFIED requirement: the exception named by the act, covering the sign-off and the binding it needs; no wallet of the domain's own; ruling 183 as a clarification, including "on whose behalf". | D10 |
| PP-11 | Whichever of this change and `add-trust-anchors-and-machine-holders` archives second regenerates at the union, checked sentence by sentence and scenario by scenario, ignoring line breaks; no sentence widens the exception. | D11 |
| PP-12 | No dependency on trust anchors; possible convergence with an organisation-level anchor set. | D12 |
| PP-13 | The new family in the code leg by an explicit Q7 extension. | D14 |
| PP-14 | Every name, value and code that becomes a machine key; the custody reference form; the release class; the description sentence. | D14 |
| PP-15 | The non-goals and named successors; the passkey and security-key profile drafted as its own change. | D15 |
| PP-16 | The seam with openSig, in the words both designs share. | "The seam between openWallet and openSig" |

## Tensions

- **T1. Ruling 156 against licence freshness.** Never waiting on an outside service
  means a revocation that has not yet reached the deployment cannot stop a sign-off;
  the reliance is flagged and raised instead. The alternative, refusing once the newest
  list held is older than a bound, gives a sharper guarantee and makes accepting a
  decision wait on the verifier's next publication, which ruling 156 rules out. In
  the worst case, with no newer list arriving, the reliance bound (up to twelve
  months) is the only hard stop, and every sign-off until then is flagged.
  **Resolved by ruling 212**, which chooses never waiting (Open question 4).
- **T2. The ratified exclusion of consent.** The possession profile's ratification
  record excludes "explicit human consent" and leaves "separate exact-request human
  consent" to the relying party. A sign-off is consent to an exact request, so this
  change claims none of it, and the relying domain must evidence it (Open question 5).
- **T3. Declared custody and evidence that the holder acted.** openChart's draft
  proposes to accept only `isolated_per_use_authorized`, and nothing in openWallet yet
  verifies that a key's custody is what its wallet declares (Open question 6).
- **T4. A synced passkey and the custody registry.** Ruling 208 settles that a
  practitioner signs with a passkey or a security key, and ruling 209 that a synced
  passkey counts for openChart on an enrolled device. The ratified registry describes
  isolation as a key that "cannot be read, exfiltrated or replayed elsewhere", which a
  key a provider copies to every device in an account may not honestly be. That is
  open in `add-webauthn-proof-profile`, where no synced passkey can be bound until a
  model fits, so ruling 209's yes for synced passkeys waits on it; this change does
  not bend the registry.
- **T5. The operator of the deployment.** Ruling 214 holds against forgery, not against
  deleting records or back-dating. Beyond its words, it holds only for verifier keys
  that ship with a release and where the verifier identified the licensee itself in
  the session in which each named key proved possession, and not against hiding
  records, withholding revocation lists, rebinding an account, substituting the
  statement a gesture signs, a relayed proof, or whoever controls a synced passkey's
  account (D8; Open question 21).
- **T6. A class-named exception in a class-agnostic core.** The core's scenario says "no
  requirement in this capability assumes a particular class", and the exception names
  the practitioner class. It imposes nothing on any holder; it widens what a consuming
  domain may require, for one act. Ruling 154 names the act, so the tension is recorded
  rather than designed away (Open question 17).
- **T7. Ruling 160 and a practice that verifies its own practitioners.** If the practice
  is the verifier, the practice's record and the wallet's are not independent. D4's
  provenance rule makes that visible, never enforced: two people at the practice can
  add its own key. Ruling 210 rules it out for openChart; admitting `release` keys
  only, as recommended for openChart version 1, makes that hold there; the standard
  cannot forbid it (Open question 3).
- **T8. The leg of the new family.** Q7 covers two families; the ratified challenge-proof
  change defaults new schemas to the spec leg (Open question 7).

## Open questions for ratification

Each is a judgment the author made, or a choice the owner must make, with a
recommendation. Rulings 208 to 214 closed questions 1 to 4 and 9; each closed one
keeps its number and says what stays PROPOSED. Questions 20 and 21 are new.

1. **The threat model for whoever runs the practice's deployment.** **Closed by
   ruling 214**, in its words (D8). Still PROPOSED, and put to the owner with it:
   reading "forgery" as a sign-off made without the practitioner's key; reporting
   the signer from the verification, never the account; the aim holding only for
   verifier keys that ship with a release (D4); and the limits beyond the ruling's
   words (hiding records, withholding revocation lists, altered software, refusing
   service, content substitution). Recommendation: accept them.
2. **Which devices, and which proof, version 1 must support.** **Closed by ruling
   208**: a passkey or a security key, under the profile drafted as
   `add-webauthn-proof-profile`; the ratified `wallet-challenge-proof` stays as
   ratified and is not how a practitioner signs in version 1. What remains, which
   custody a synced passkey declares and how a verifier observes a passkey's proof
   of possession, is put to the owner in that change. Recommendation: go-live waits
   for that change's ratification, which ruling 152 already requires.
3. **Who may verify, who verifies for the first practice, and how verifier keys reach a
   deployment.** **Closed by rulings 210 and 211**: the verifier must be independent,
   and for the first practice it is a verification service the owner runs, checking
   each licence against the state board's own record, with its key shipped in
   openChart; until one exists, ruling 152 keeps every decision off. Still
   PROPOSED, with a recommendation: openWallet admits any verifier and keeps both
   provenances for held verifier keys (D4); for openChart version 1, verifier keys
   reach a deployment only with a release of openChart, as ruling 211's key does,
   each with its verifier's newest revocation list, and openChart does not admit
   the two-person path, because a reliance on a two-person key falls outside the
   aim (D8) and would leave ruling 210 merely visible.
4. **Licence freshness against ruling 156.** **Closed by ruling 212**: freshness never
   blocks; the newest list held is used and its age recorded; openChart alerts the
   medical director once it is over 72 hours old; a verification still expires on its
   own date. Still PROPOSED, with a recommendation: a raised item never goes to the
   signer alone, and where the signer is the medical director, as in a
   one-practitioner practice, the practice names a second recipient, such as its
   administrative role or a named outside reviewer (D6); and the worst case is stated:
   with no newer list, the only hard stop is the verification's reliance bound.
5. **Who evidences exact-request consent.** Recommendation: the relying domain, as the
   ratified profile's record says: openChart's signing view and its refusal on a changed
   digest, its re-authentication at signing (CD-10), and its acceptance only of custody
   authorized per use on the device. Neither openWallet's proof nor openSig's attestation
   claims it.
6. **On what evidence may a key's custody be accepted as `isolated_per_use_authorized`,
   and does go-live wait for it?** Recommendation: a successor openWallet change defines a
   custody-acceptance record, such as registration attestation checked when the key is
   bound. Ruling 152 is "until both exist", so holding go-live for custody evidence would
   be a new decision; the owner is asked to make it, and the recommendation is yes.
   Under `add-webauthn-proof-profile` (ruling 208), registration attestation, where an
   authenticator gives one, is the natural custody evidence, and the user-verification
   flag on each use shows verification on the authenticator, as far as the
   authenticator is trusted. Which model a synced passkey declares is open there.
7. **Which leg holds the new family?** Recommendation: the code leg, by an explicit
   extension of the Q7 override (D14).
8. **Bind each sign-off key individually?** Recommendation: yes (D8).
9. **The reliance bound's ceiling, and what it asks of the practitioner.** **Closed by
   ruling 213**: until the licence itself expires, and at most 12 months; the verifier
   re-checks the board's record monthly and revokes on a change. Still PROPOSED, with a
   recommendation: measure the twelve months from when the licence was checked (D2).
10. **How long are verifications, revocation lists, held verifier keys and their states,
    and records of reliance kept?** Recommendation: for as long as the records they
    support, under whatever retention rule counsel sets for those records.
11. **May the licence identifier be carried in clear?** Recommendation: yes. It is needed
    for ruling 160's comparison, authorities commonly publish it, and it never identifies
    a patient.
12. **The names that become machine keys** (D14). Recommendation: confirm or change them
    now, while nothing pins them.
13. **How are licence classes named across jurisdictions?** Recommendation: the
    authority's own designation and the jurisdiction's ISO 3166 code, with no equivalence
    in openWallet; the relying domain maps each (authority, class) pair to the decisions
    it may make.
14. **Several licences in one wallet.** Recommendation: one verification per licence, and
    the relying domain records which one a sign-off relied on.
15. **Which statuses support a sign-off?** Recommendation: openChart relies on `active`
    only in version 1, and treats `active_with_conditions` as not supporting a sign-off
    until a later change can represent conditions.
16. **Does an AI's wallet (ruling 183) need anything from this profile?** Recommendation:
    no. An agent never carries a licence verification, so this profile can never make an
    agent's signature a practitioner's sign-off (ruling 157). Naming an agent as a
    record's author includes naming it as the party on whose behalf a relay wrote it.
17. **Accept a core exception that names a holder class?** (T6) Recommendation: yes; it
    imposes nothing on any holder and is the one exception ruling 154 names.
18. **Where does the key binding registry run?** Recommendation: inside the practice's
    deployment, populated only by openChart's per-key bindings (D8).
19. **What must openChart hold locally to check a sign-off without waiting?**
    Recommendation: the key binding registry; the held wallet records of bound
    practitioners; every licence verification it has received, with the supersession
    index it keeps of them (D5); each held verifier key with its
    provenance and state; each verifier's newest revocation list; and, through openSig's
    draft, the openSig attester and its attestation keys, retired ones included.

20. **The verification service of ruling 211 has no specification.** Ruling 211 names
    it: a service the owner runs, checking each licence against the state board's own
    record, with its key shipped in openChart. This change drafts nothing for it.
    Recommendation: the owner commissions its specification as its own change, in the
    repository he chooses for it, stating how it identifies each licensee by its own
    means, independently of the practice's deployment, in the session in which each
    key proves possession, how it obtains a passkey's proof of possession in that
    session (`add-webauthn-proof-profile`), never relayed, how it keeps its
    signing key, how it re-checks each licence monthly and publishes cumulative
    revocation lists, and who may operate it; until then, ruling 152 keeps every
    decision off.
21. **A deployment that shows one statement and has the key sign another.** No key in
    either profile shows its holder what it signs (D8's limits), so a deployment that
    controls its own code can obtain a genuine signature over a statement the
    practitioner did not see. It uses the practitioner's key and gesture, so it is not
    a sign-off made without the key, and an honest check accepts it. Recommendation:
    accept it as a stated limit of version 1, with two compensating controls in
    openChart, each practitioner seeing every sign-off made with their key and raising
    one they did not intend, and the audit keeping the statement each sign-off bound;
    and name as a successor a second channel the practitioner controls that shows the
    statement before the key signs.

## Status

`Status: proposed`. Five reviews have run: an independent review of the first draft at
`8aa0364`, a confirmation review of the revision at `169120e`, a final check of
`7442ea5` together with an automated review, a confirmation of `4cfef0a` with a
second automated review, and an independent review of `484dd16` together with the
first draft of `add-webauthn-proof-profile`; this revision answers all five and
records rulings 208 to 214, which are rulings and not ratification. `tasks.md` 1.1 still schedules an adversarial reviewer
over this revision before ratification. Ratification is pending, by openWallet's operator
authority, Brett Heap.
