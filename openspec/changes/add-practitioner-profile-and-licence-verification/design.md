# Design: add-practitioner-profile-and-licence-verification

## Context

Drafted on 2026-11-15 by Claude (Opus 5.5), on Brett Heap's ruling 153, as a
draft for his review. **Nothing here is ratified.** The owner's rulings quoted
below are his decisions; every other choice in this change is a design call,
marked PROPOSED where it is made and listed in "Design calls" below, so that it
can be confirmed or overturned one by one.

The consumer is openChart's draft `define-clinical-acts-foundation`
(openChart-spec#5, read at `e9ba497`). Its practitioner's sign-off makes four
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
  `openxwallet-agent-profile`, the four open changes, the three archives, the
  plan of Speckit feature 006 and all of feature 016; and pull request #6 at
  `4d83535`;
- `opensoft/openWallet-code` at `bb0e9da`, read only: the record schema, the
  closed custody registry, the subject attestation and the validator's kinds;
- `opensoft/openSig-spec`: `main` at `23ebbfe`, pull request #1 at `8668f30` and
  pull request #2 at `a05fcee`;
- openChart-spec#5 at `e9ba497`: Decision 4, Decision 19, Open Questions 9, 10,
  11, 16 and 24, the requirements AU-03, AU-07, AN-02, AN-08, AN-14, CA-04,
  CA-08 and CA-14, and the content schema's sign-off evidence.

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

Ruling 98, cited by ruling 160, is recorded in openChart-spec#5: "A second named
person confirms; a one-administrator practice records licence verification
against the board's public record." That is the practice's own check, and it
stays the practice's (D6).

Ruling 157, accepted in the same words, is not this change's to encode but
bears on it: "151. An AI only ever makes recommendations until a practitioner
signs. Limited and full practice as designed would need a new ruling." Nothing
here can make an agent's signature a practitioner's sign-off (D1).

## What this change stands on

Checked on 2026-11-15 at the heads above.

| Change or record | Standing | How this change uses it |
|---|---|---|
| `openxwallet`, `openxwallet-agent-profile` | canonical, ratified, archived | The core this profile sits over; the agent profile is its pattern (D1). |
| `add-challenge-proof-runtime` (capability `wallet-challenge-proof`) | **ratified** 2026-11-10 for its possession-only wire profile ("Ratify both possession-only profiles"), not yet archived; runtime acceptance pending | A sign-off's proof is that profile, unchanged (D7, D11). |
| `add-composition-drift-cascade` | ratified 2026-08-28, not yet archived | Its restatement of "Revocation propagates through the chain" is the revocation rule D5 relies on. Not modified here. |
| `add-reference-registry-custody` | commissioned implementation and isolated qualification; not a ratified contract | Its registry is one way to run the key binding registry the ratified profile requires (D7, D11). |
| `add-trust-anchors-and-machine-holders`, and its amendment in pull request #6 | proposed, not ratified | Held keys verified offline; it MODIFIES the same requirement as this change (D9, D10). Not edited here. |
| The closed custody registry, version 1 (`openWallet-code` `bb0e9da`) | ratified with the birth change | What a sign-off key's custody evidences (D7). |
| The closed `holder_class` set | ratified; already includes `practitioner` | No schema change is needed for the class (D1). |

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

**What the profile carries.** The licence verification and its revocation list,
what a relying domain checks and refuses, how a verification ends, what it never
is, and what openWallet provides for a practitioner's sign-off. Nothing else: no
composition (that is the agent profile's), no clinical vocabulary, no grant
semantics, and no rule about which decisions a licence permits.

**The holder-class rule is a record rule.** A licence verification bound to a
wallet whose holder is not a `practitioner` is refused, in the way the agent
profile's composition is refused for a non-agent wallet (validator code
`composition-on-non-agent`). That is a rule about the record, checked where
records are validated. It is not a rule a relying domain applies to the class a
presenter declares for itself: a relying domain relies on a verifier-signed
verification, never on a wallet's own statement of its class. That keeps faith
with the proposed rule "A verifier is blind to holder class"
(`add-trust-anchors-and-machine-holders` D4), whose reason is that a class read
from the presenter's own record is a self-declaration.

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
| `verification_id` | The record's identity. A duplicate is refused under the existing `record-id-duplicate`. |
| `subject.wallet_ref`, `subject.did` | The bound wallet: its `wallet_id`, and the DID of its primary key reference. |
| `licence.authority` | The licensing authority, by an identifier the relying domain's held verifier key is scoped to (D10). |
| `licence.jurisdiction` | Where the authority licenses: an ISO 3166-1 alpha-2 country code, or an ISO 3166-2 subdivision code. |
| `licence.licence_id` | The authority's own identifier for the licence, as issued (see "The licence identifier is carried in clear" below). |
| `licence.licence_class` | The licence class or profession, in the authority's own designation. |
| `licence.licence_class_label` | OPTIONAL, for display only. No rule reads it. |
| `licence.expires_on` | OPTIONAL: the licence's own expiry, where the source states one. |
| `status_found` | Closed: `active`, `active_with_conditions`, `inactive`, `expired`, `suspended`, `revoked`. `conditions_ref` is REQUIRED with `active_with_conditions` and refused otherwise. |
| `source.kind` | Closed: `authority_record` (the authority's own record, read directly), `authority_publication` (a register the authority publishes), `designated_source` (a source the authority designates as primary for this fact). |
| `source.ref`, `source.checked_at` | What was consulted, and when. |
| `verifier.wallet_ref`, `verifier.did`, `verifier.key_id` | The verifier's wallet and the declared key that signed. |
| `issued_at`, `rely_until` | When the verification was issued, and its reliance bound. `rely_until` is later than `issued_at`, and `issued_at` is not earlier than `source.checked_at`. |
| `supersedes` | OPTIONAL: the `verification_id` this one supersedes, from the same verifier, for the same licence and wallet. |
| `binding_proof.challenge_digest`, `binding_proof.observed_at` | The proof of possession the verifier obtained from the bound wallet (D3). |
| `identity_evidence_ref` | An opaque reference to the verifier's own record of how it satisfied itself that the licensee is the wallet's holder (D3). |
| `signature` | `alg` and `value`, over the canonical form of every other field (D3). |

**No clinical scope.** The record has no property that could list acts,
decisions or scopes, and closes `additionalProperties` at every depth, so the
wrong reading cannot be represented. Which decisions a licence class may make
is the relying domain's own configuration (D6). openChart's sign-off evidence
records what a verification "covers"; under this profile that is openChart's
own mapping from the verification's authority, jurisdiction and class, never a
field of the verification.

**The licence identifier is carried in clear.** The relying domain needs it to
compare the wallet's verification with its own record of the practitioner's
licence, which ruling 160 requires to hold beside it (D6), and openChart's AU-03
already asks whether the two "differ about the licence itself". Licensing
authorities commonly publish licence identifiers. It identifies a licence, never
a patient, and it never becomes a subject identifier (D6). Open question 6.

**One verification per licence.** A practitioner with licences from two
authorities carries two. A change to one licence then supersedes or revokes one
verification and leaves the other alone.

**The status set.** A verifier records what it found. Only some statuses can
support anything, and which ones a relying domain accepts is its own decision
(Open question 10).

REJECTED:

- **A profession taxonomy across jurisdictions.** Whether one authority's class
  is equivalent to another's is a legal judgment for the relying domain, not a
  fact a neutral standard can own (Open question 8).
- **One verification listing every licence a holder has.** A change to one
  licence would reissue all of them, and supersession would stop being per
  licence.
- **A digest of the licence identifier instead of the identifier.** A digest of
  a small, structured number space can be reversed by trying them all; a salted
  commitment needs its salt shared with the very party that already holds the
  number.

## D3 — Who issues a licence verification, and how (PROPOSED, PP-3)

**A verifier is a holder with a wallet of its own,** typically of class
`organisation`, and signs with a key that wallet declares. A relying domain
relies only on verifiers whose keys it already holds (D4).

**The signature.** Ed25519 over a domain separator and the RFC 8785 canonical
UTF-8 bytes of every field but `signature`: `openWallet.licence-verification.v1`
and a NUL byte for a verification, `openWallet.licence-revocation-list.v1` and a
NUL byte for a revocation list. That is the construction of the ratified
possession-only profile (`openWallet.challenge-proof.v0` and a NUL byte, then
RFC 8785), with separators of its own, so no record of one kind verifies as
another. It reuses one canonicalizer, one algorithm and the known-answer vector
practice of feature 016 (its T007).

**A proof of possession at issuance.** Before it issues, the verifier issues a
challenge and obtains a `wallet-challenge-proof` from a key the bound wallet
declares, and the verification records the challenge digest and when the proof
was made. The binding to a wallet is the verifier's claim about that wallet,
and possession of one of its declared keys is the one fact about a wallet that
the verifier can check for itself. Without it, a verifier could bind a licence
to a wallet whose keys the licensee does not hold.

**Identity proofing is the verifier's own record.** openWallet defines no
identity-proofing standard. How the verifier satisfied itself that the licensee
it checked and the wallet's holder are the same person is its own record,
referenced by `identity_evidence_ref`, in the way
`add-trust-anchors-and-machine-holders` D6 keeps enrolment evidence the issuer's
record. A relying domain does not depend on that record alone: it binds its own
account to the wallet itself and compares the licence with its own record (D6).

**Who may be a verifier is not narrowed by the standard,** beyond holding a
declared key. Each relying domain decides which verifiers' keys it holds. The
verification names its verifier, so a relying domain that requires a verifier
other than itself can refuse one it issued itself. Ruling 160 asks for two
records that both hold, which is worth little if one party issues both. The
recommendation for openChart is Open question 2.

REJECTED:

- **Only the licensing authority may verify.** No authority issues such records
  today, so the consumer would wait indefinitely; the standard can admit an
  authority as a verifier when one does.
- **The holder's own statement of its licence.** A holder asserting its own
  licence is the `asserted_identity` the closed custody registry excludes in
  spirit: proof replaced by assertion.
- **openSig as the verifier.** Ruling 155: openSig only attests that the
  signature came from that wallet.

## D4 — Checking a verification with no outside call (ruling 156) (PROPOSED, PP-4)

A relying domain decides from four things it already holds: the verification,
as the holder presented it; the verifier's public key, obtained ahead of time
with its provenance; the verifier's latest revocation list that the domain has
fetched; and its own clock. It contacts no verifier, licensing authority,
directory, wallet or holder device to decide. The revocation list is fetched
ahead of time and never per check, as `add-trust-anchors-and-machine-holders` D3
proposes for revocation lists in general.

**Three outcomes** (PROPOSED names): `relied_on`; `refused`, with a reason from a
closed list (`reliance_bound_passed`, `superseded`, `revoked`, `wallet_mismatch`,
`verifier_not_held`, `verifier_not_active`, `signature_invalid`, `wallet_not_active`,
`status_not_accepted`); and `not_checkable`, with a reason (`revocation_list_stale`,
`revocation_list_missing`). `not_checkable` is kept distinct from `refused`
because it is a fact about the domain's copy of the list, not about the licence.
A consumer may treat it as a failure the signer can cure by trying again once a
newer list is fetched; openChart's AN-14 has that class of failure.

**Supersession is decided from what the domain holds.** A later verification
names the one it supersedes, so a domain knows of it once it holds it.

**The staleness bound is the domain's.** The verifier states, in each list, the
time by which it will publish the next; the domain declares how old a copy it
will accept. Neither number is openWallet's (Open question 3).

REJECTED:

- **Asking the authority or the verifier at the moment of reliance.** It puts an
  outside service in the path of every sign-off, which ruling 156 forbids; it
  makes the domain unable to accept a decision when that service is down; and it
  tells a third party who relied on whose licence and when, the leak
  `add-trust-anchors-and-machine-holders` D3 names for online certificate checks.

## D5 — How a verification ends (PROPOSED, PP-5)

A verification stops being relied on at its reliance bound, with no grace
period; when the domain holds a later verification that supersedes it; when its
verifier revokes it; when the bound wallet is revoked, and while it is
suspended; and from the moment the domain stops holding the verifier's key as
active.

**The gap between an authority's action and the relying domain is stated, not
hidden.** If an authority suspends a licence after a verification was issued,
the verification is relied on until the verifier's revocation reaches the
domain or its reliance bound passes, whichever comes first. That gap is bounded
by the reliance bound, by how fast the verifier learns of the change and
publishes, and by the domain's staleness bound. The standard requires all three
to exist and leaves their values to the parties (Open question 3).

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
already restates (D11).

**Retiring a key does not end a verification.** A verification is bound to the
wallet, and a wallet's keys rotate under its own rules. A proof from a retired
key is refused under the core's rule regardless.

**Reason classes** (PROPOSED, closed): `licence_status_changed`, `issued_in_error`,
`binding_lost`, `wallet_revoked`, `verifier_withdrawn`. Only `issued_in_error` says
the verification was never true. A revocation never rewrites a reliance made
while the verification was in force, but one of that class is raised, for every
reliance it affects, to the responsible human through the relying domain's
declared escalation path. The drift cascade records a reason class that is
never consulted to narrow propagation; this class is consulted only to widen who
is told, never to spare anything.

REJECTED:

- **A grace period after the reliance bound.** It turns the bound into a
  suggestion.
- **Ending a verification when one key retires.** It would make routine key
  rotation look like a licence event.
- **Rewriting past reliances on revocation.** The record of what a decision
  rested on at the time is the audit; what to do about it is a human's decision.

## D6 — What a verification never is, and how the relying domain matches it to its own account (rulings 151 and 160) (PROPOSED, PP-6)

A licence verification is evidence that a named verifier found a licence in a
stated status and bound it to a wallet. It is not proof of who a person is, not
a patient or subject identifier, and not authority.

**The match openChart's Open Question 9 asks for has three legs,** and no single
party supplies all of them:

1. **The verifier's leg.** The verifier states that the licensee it checked is
   the wallet's holder (`identity_evidence_ref`), and the wallet proved
   possession to it (`binding_proof`).
2. **The relying domain's binding.** The domain binds its own account to the
   wallet by a proof of possession from a key the wallet declares, over a
   challenge the domain issued, in that account's own session. A verification
   alone never binds an account. openChart's AU-07 is this leg.
3. **The relying domain's own licence record.** The domain compares the
   authority, jurisdiction and licence identifier in the verification with its
   own record of that account's licence. openChart's AU-03 attestations and
   ruling 98's check are this record.

So: the account's person holds the wallet (leg 2), the wallet's holder holds the
licence according to the verifier (leg 1), and the practice's own record says the
account's person holds that licence (leg 3). Ruling 160's "both must hold" is
legs 1 and 3 together, and it is worth most when the verifier is not the practice
(Open question 2).

**The wallet identifier still never becomes a person's identifier.** The domain
resolves the person by its own account identifier. The wallet identifier on a
sign-off is evidence of which wallet signed.

REJECTED:

- **Carrying the holder's name or date of birth in the verification so that a
  domain can match it.** It would make the wallet a carrier of personal identity,
  and the domain already knows who its account belongs to.

## D7 — The sign-off: a proof over the relying domain's statement, and what its key's custody evidences (PROPOSED, PP-7)

**The proof is the ratified possession-only profile, unchanged.** A practitioner's
sign-off is a `wallet-challenge-proof` whose `challenge_digest` is `sha256:` and
the SHA-256 of the relying domain's RFC 8785 canonical statement for that
sign-off. The statement carries the domain's single-use challenge, so the proof
binds that challenge. Under the profile the domain is the challenge's "owning
issuer", which "enforces freshness, caller binding and one-use". The proof's own
fields bind the wallet, the key, the subject, the custody reference, the binding
and its revision. For openChart the statement is its sign-off statement and the
digest is its `statement_sha256` (its CD-53).

**The binding is resolved inside the relying domain's deployment.** The profile
accepts binding metadata "only from a trusted server registry". Ruling 156 puts
that registry inside the practice's deployment: the domain runs it, or holds a
current replica of it. For openChart, the account-to-wallet binding made under
its AU-07 is what populates it, and the binding's subject is the domain's own
reference for that account. That reference is the domain's identifier for its
account; the wallet identifier does not become it. `add-reference-registry-custody`
shows one way to run such a registry; its reference custody service, which is
`isolated_invocable`, can never be the practitioner's custody for a sign-off that
openChart accepts.

**What the signing key's custody evidences** is already stated by the closed
custody registry. A key whose declared custody is `isolated_per_use_authorized`
evidences that the HOLDER acted; `holder_readable` and `isolated_invocable`
evidence only the holder's environment. Which custody a sign-off needs is the
relying domain's decision: openChart accepts only `isolated_per_use_authorized`
(its CA-04).

**A declaration is not proof.** The ratified profile's design says it "does not
attest that the referenced custody or agent composition is actually isolated. A
trusted registry supplies those facts and their acceptance." So the evidence on
which the registry accepted a key's custody matters, and openWallet defines no
standard for it yet (Open question 4, tension T3).

**The algorithm limits the hardware.** The ratified profile is Ed25519 over an
exact, domain-separated preimage. WebAuthn authenticators sign their own
authenticator-data structure over a hash of the client data, not an arbitrary
preimage, so a passkey or platform authenticator cannot produce this proof, and
many platform authenticators offer P-256 only. A key that is authorized per use
and can sign the profile's preimage with Ed25519 exists in a narrower class of
hardware, such as a smart card or a security key applet that signs arbitrary
data and requires a touch or a PIN for each signature (Open question 5,
tension T4).

**Possession is not authority.** The proof states nothing about the statement's
content, the practitioner's licence or their authority, and keeps the profile's
limited meaning: "Verified possession SHALL NOT imply MFA, human presence,
composition attestation, delegation or domain permission."

REJECTED:

- **A new sign-off proof profile in this change.** The ratified profile already
  binds what a sign-off needs. A WebAuthn assertion profile would be a separate
  change, gated on the owner's answer to Open question 5.
- **A profile rule that a practitioner's keys must be `isolated_per_use_authorized`.**
  A practitioner's wallet may declare keys for other uses, and the core's custody
  rule already caps what each evidences. The relying domain decides what it
  accepts for a sign-off.

## D8 — The exception of ruling 154 and the sentence of ruling 183 (the exception RULED; its wording PROPOSED, PP-8)

The MODIFIED block keeps every word of the canonical requirement and both of its
scenarios, and adds two paragraphs and four scenarios.

**One named exception, and only one.** A consuming domain MAY require a
practitioner's wallet for that practitioner's sign-off of a medical decision,
and for nothing else. The scenario "the exception admits no second act" makes
"one" testable: a domain that requires a wallet to sign in, to read a record or
to enter information is outside the exception.

**Why the exception is in the core.** Ruling 154 amends the core's rule. A
generic hook, such as "a profile may name an act that needs a wallet", would let
any later profile add an exception without amending the core, which is not one
named exception. The core names the act and points to the profile for what that
sign-off is.

**"Medical decision" is the consuming domain's term.** openChart keeps the list
of what counts as a decision. openWallet does not define it, and the exception
says so.

**The rest still works without a wallet.** Ruling 154: "The rest of the chart
still works without a wallet." Ruling 183: "nothing needs the wallet to be
reachable to read the chart." So reconstructing a record and resolving a subject
need no wallet, a signed-off record included, and reading a signed-off record
contacts no wallet. What a domain does with a sign-off attempted without a
wallet is the domain's to decide.

**Ruling 183, in openWallet's terms.** The ruling's "AI" is a holder of class
`agent`. The sentence lets a wallet identifier name an agent holder as the author
of a record, and nothing more. "Never identifies a person" covers practitioners
too: a practitioner's wallet identifier on a sign-off is evidence of which wallet
signed, and the person is the domain's own account.

**No validator or schema behaviour changes for the core.** The subject
attestation still refuses `reconstructable_without_wallet: false` and still
resolves only by `subject_ref`; the exception concerns making a sign-off, not
reconstructing a record. Only that schema's description, which quotes the rule,
gains a sentence (D12).

REJECTED:

- **The exception in the profile alone.** A profile cannot override the core's
  rule; the core would still forbid it.
- **The exception for any sign-off.** The ruling names a sign-off of a medical
  decision.
- **Letting a wallet identifier name any holder as an author.** The ruling names
  an AI.

## D9 — The collision with `add-trust-anchors-and-machine-holders` (PROPOSED, PP-9)

That change, `Status: proposed`, also MODIFIES "The capability is an authority
control, never an identity substrate". It appends one sentence to the
requirement's paragraph, on trust anchors, and adds the scenario "an anchor is a
trust fact about a key, never an identity". Its open amendment, pull request #6
at `4d83535`, does not touch this requirement: it adds a MODIFIED "Authority
travels as attenuated grants, never as keys", which this change does not modify.

**How the two compose.** A MODIFIED block replaces the whole requirement when it
archives, and the pinned CLI refuses an archive whose MODIFIED block omits a
scenario the current spec still has. This leg measured that refusal at
`add-multi-key-wallets`' archive. Both deltas are written against the canonical
text at `a2d554d`, so both validate today. **Whichever of the two archives second
SHALL first regenerate its MODIFIED block at the union** and re-run the pinned
gate. Neither delta removes or rewrites the other's text, so the union is
mechanical but for one sentence.

**The union**, for whichever regenerates:

1. the canonical first paragraph, with that change's appended sentence on
   anchors;
2. this change's two paragraphs, unchanged;
3. the scenarios: the two canonical ones, that change's "an anchor is a trust
   fact about a key, never an identity", and this change's four.

**The one sentence to harmonize.** That change says this capability "SHALL NOT
make holding anchors a prerequisite for operating a domain, any more than
holding a wallet". Under the exception, a wallet is a prerequisite for one act,
and checking a licence verification needs the verifier's key held, which would
be an anchor (D10). PROPOSED union wording: "…any more than holding a wallet;
the one named exception below covers the anchors a domain holds to check that
sign-off, and nothing else."

This change does not edit that change, and does not comment on its pull request.

## D10 — The held verifier key, and the unratified trust anchors (PROPOSED, PP-10)

The requirement says what the relying domain holds in neutral words: "the
verifier's public key, obtained ahead of time and kept with how it was
obtained". It does not name the proposed anchor kind, so its text does not
depend on an unratified change.

**If `add-trust-anchors-and-machine-holders` is ratified as proposed,** the held
verifier key is one of the relying domain's trust anchors:

- role `issuer`, because the verifier vouches for a population, the licences it
  verifies;
- scope: the licensing authorities it may verify for, as literal names under a
  `licensing-authority:` prefix. That change admits literal names and globs, and
  lists namespaces among its deferred items (its D11.9), so a prefixed literal
  works today, and this profile is the consumer that change said a richer scope
  would wait for;
- provenance: the first anchor arrives out of band (`out_of_band_fingerprint`),
  and a verifier's self-published keys only confirm (its D5);
- state: an anchor `suspended` or `revoked` is a verifier key "held as suspended
  or revoked" in this change's requirement;
- its "Verification is offline against held anchors" is ruling 156 for this case.

An anchor is owned by a wallet, so the relying domain's deployment would hold
its anchors in a wallet of its own, of class `organisation` or, under that
change, `machine`.

**If it is changed,** the mapping above changes and this change's requirements
do not. **If it is returned,** the realization adds a minimal held-verifier-key
record to the practitioner profile family instead (the verifier's DID, key and
fingerprint, provenance and state), and the requirements still do not change
(`tasks.md` 6.2). Either way the two can be ratified in either order.

## D11 — Composition with the other changes this change touches

- **`add-challenge-proof-runtime`** (ratified wire profile, not archived). Used
  unchanged; no byte of it moves. Its capability `wallet-challenge-proof` is not
  yet canonical. If its archive renames it, this change's reference to it moves
  editorially. Its limits are kept: possession only, no claim of MFA, human
  presence or permission (D7).
- **`add-composition-drift-cascade`** (ratified, not archived). It MODIFIES
  "Revocation propagates through the chain". This change does not, so the two
  cannot collide; D5 relies on its principles.
- **`add-reference-registry-custody`** (commissioned). Its registry is the kind
  of trusted registry D7 needs inside a deployment. Its reference custody is
  `isolated_invocable`, which evidences the environment, so it is never a
  practitioner's custody for a sign-off openChart accepts.
- **`add-trust-anchors-and-machine-holders`** and pull request #6: D9 and D10.

## D12 — Placement, names, code surface and release class (PROPOSED, PP-11 and PP-12)

**Which leg holds the new contract family is open (Open question 1).** The
declared Q7 override places `contracts/openxwallet/` and
`contracts/openxwallet-agent-profile/` in the code leg, beside the validator that
resolves every contract path from its own location, and covers those two
families only. The ratified challenge-proof change says "New schemas default to
spec leg; legacy wallet Q7 does not automatically cover them", and put its own
schema in this leg's `contracts/`. Feature 006's plan expects a profile to
arrive as "a third directory" beside the two. The recommendation is the code
leg, by an explicit extension of the Q7 override, because Q7's reason holds for
a family validated by the same validator: "The schemas, the corpus and the
validator are one release unit."

**Names that become machine keys once released** (root AGENTS.md rule 3), all
PROPOSED and cheapest to change now:

- the capability `openxwallet-practitioner-profile`, and the directory
  `contracts/openxwallet-practitioner-profile/`;
- the kinds `xfactory_wallet_licence_verification` and
  `xfactory_wallet_licence_revocation_list`, keeping the `xfactory_wallet_*`
  prefix the family keeps;
- the contract ids `openxwallet-licence-verification` and
  `openxwallet-licence-revocation-list`;
- the signing domains `openWallet.licence-verification.v1` and
  `openWallet.licence-revocation-list.v1`;
- the closed values of `status_found`, `source.kind`, the reason classes and
  the check outcomes and reasons;
- the finding-code family `licence-verification-*`.

The spelling is "licence", the noun as openChart's drafts spell it.

**The validator** gains two kinds in `KIND_TO_SCHEMA`, ERROR codes in the new
family, and one requirement row per ADDED requirement (proposed `OXWP-R1` to
`OXWP-R6`), each with at least one negative confirmation. No code is renamed,
repurposed or reclassified, and there is no new WARNING, because LedgerxFactory
runs the validator with `--strict`. Facts the validator cannot check, such as a
verifier's signature, are reported as NOTES, as the canonical validator "does not
verify signatures, resolve DIDs, or contact a key store".

**One description sentence moves one digest.** The subject attestation schema's
description quotes the rule this change amends. Left alone it would state the
rule without its exception, a description false on arrival.

**Release class: an ADDITIVE MINOR.** Two owned members are added and one
digested byte moves. Nothing a consumer declares becomes invalid. The five
coordinated values are allocated at realization and nothing is reserved here.

## D13 — Non-goals and named successors

Each is out for a reason, not by omission:

1. **An identity-proofing standard.** The verifier's record (D3).
2. **Equivalence of licence classes across jurisdictions.** The relying domain's
   judgment (D2).
3. **A custody-acceptance record**: the evidence on which a registry accepts a
   key's declared custody, such as hardware attestation at binding (Open
   question 4).
4. **A WebAuthn assertion proof profile** (Open question 5).
5. **A sign-off made in another system.** Ruling 186: openChart only, in version
   1; it counts later, once openWallet and openSig can prove it to the chart. A
   proof over a statement whose challenge the chart did not issue needs its own
   change.
6. **A patient profile.** Still a named successor gated on a consumer of its own.
7. **Practitioner credentials other than a licence**: a controlled-substance
   registration, a board certification, hospital privileges. openChart keeps
   prescriber facts as practice attestations.
8. **A scheme accrediting verifiers.** Each relying domain decides which
   verifier keys it holds.
9. **A use-time reliance record kind**, which would make reliance statically
   checkable, like the verification-event record that
   `add-trust-anchors-and-machine-holders` names as a successor.

## The seam between openWallet and openSig

This section is written in the same words in openWallet's
`add-practitioner-profile-and-licence-verification` and in openSig's
`add-wallet-bound-attestation`. A change to it in one draft is a change to it
in both. Every line of it is PROPOSED.

**The split.** openWallet owns the keys, the proof of possession and the
licence verification. openSig owns the durable attestation that a given
signature over a given digest came from a given wallet. The relying party
(openChart, for a practitioner's sign-off of a medical decision) issues the
single-use challenge, writes the statement, checks the attestation, checks the
licence verification, checks its own account's binding to the wallet, and alone
decides whether the sign-off counts. Neither openWallet nor openSig decides
clinical meaning. openWallet's draft calls the relying party the relying domain,
after its core's "consuming domain"; the two words name one party.

| Question | The answer both drafts give |
|---|---|
| What identifies a wallet | The `wallet_id` of its openWallet wallet record. It is `wallet_ref` in a proof and in an attestation, and `openwallet_id` in openChart's sign-off evidence. It is attestation, never the identifier of a person or a patient. |
| What identifies a key | The pair (`did`, `key_id`) under which the wallet declares it, and its `key_fingerprint`: `sha256:` and the lowercase hex SHA-256 of the raw public key, openWallet's one spelling. It is `key_ref` in a proof, written as the DID URL `<did>#<key_id>`. An attestation records the reference and the fingerprint recomputed from the public key that the binding named. |
| What custody a key declares | One model of openWallet's closed custody registry (`openxwallet-custody`, registry version 1), declared for that key in its wallet record: `holder_readable`, `isolated_invocable` or `isolated_per_use_authorized`. openWallet states what each evidences, and only `isolated_per_use_authorized` evidences that the holder acted. A declaration is not proof: neither openWallet's proof nor openSig's attestation shows that the key's custody is what the wallet declares. |
| Which custody a sign-off needs | The relying party decides. openChart accepts only `isolated_per_use_authorized` for a practitioner's sign-off. openSig records the model the key declares and never raises it. |
| What the proof is made over | openWallet's ratified possession-only profile, `wallet-challenge-proof` (`openwallet.challenge-proof.v0`): Ed25519 over its domain separator and the RFC 8785 canonical form of every unsigned proof field. Its `challenge_digest` is `sha256:` and the SHA-256 of the relying party's RFC 8785 canonical statement, which carries the relying party's single-use challenge. For openChart that statement is the sign-off statement, and the digest is its `statement_sha256`. The proof also binds the wallet, the key, the subject, the custody reference, the binding and its revision. openSig is given the digest, never the statement. |
| Who verifies what | openWallet's verification checks the proof against the key's current binding. openSig runs that verification, never a second implementation of it, and seals its result together with the proof and the binding it rested on. The relying party verifies openSig's attestation against openSig's attestation key, checks the licence verification against its verifier's key, and checks its own account's binding to the wallet. |
| Where it is checked | Inside the relying party's own deployment (ruling 156). The key binding registry, the openSig attester, openSig's attestation keys and the licence verifiers' keys are held there. The practitioner's key stays in the practitioner's custody, and the check contacts nothing outside the deployment. |
| What neither states | The content behind the digest, the practitioner's authority, whether the holder was present beyond what the declared custody evidences, and whether the sign-off counts. openWallet's licence verification states the licence; openSig's attestation states nothing about it. |

## Design calls

Every call below goes beyond the owner's words and is PROPOSED.

| # | Design call | Where |
|---|---|---|
| PP-1 | The profile is a sibling capability `openxwallet-practitioner-profile` over the core; its holder-class rule is a record rule; no agent carries a verification. | D1; requirement "A practitioner holder carries licence verifications" |
| PP-2 | The fields of a licence verification; no clinical scope; the licence identifier in clear; one verification per licence; the closed status set. | D2 |
| PP-3 | A verifier is a holder with its own wallet; Ed25519 over RFC 8785 with signing domains of their own; a proof of possession from the bound wallet at issuance; identity proofing is the verifier's record; the standard does not narrow who may verify. | D3 |
| PP-4 | Checking from four held things; three outcomes, `not_checkable` distinct from `refused`; the staleness bound is the domain's. | D4 |
| PP-5 | The five ways a verification ends; revocation terminal; key retirement does not end it; the closed reason classes; `issued_in_error` raised to a human. | D5 |
| PP-6 | A verification is never identity or authority; the three-leg match; the relying domain binds its own account. | D6 |
| PP-7 | A sign-off is the ratified possession-only proof over the relying domain's statement digest; the binding registry inside the deployment; custody as declared; the binding's subject is the domain's account reference. | D7 |
| PP-8 | The wording of the MODIFIED requirement: the exception in the core, "and only one", the four scenarios, ruling 183 read as an agent holder. | D8 |
| PP-9 | Whichever of this change and `add-trust-anchors-and-machine-holders` archives second regenerates at the union, with one harmonized sentence. | D9 |
| PP-10 | The held verifier key named neutrally, mapped to an `issuer` anchor if that change is ratified, and carried by this profile if it is returned. | D10 |
| PP-11 | The new family in the code leg by an explicit Q7 extension. | D12 |
| PP-12 | Every name, value and code that becomes a machine key; the release class; the description sentence. | D12 |
| PP-13 | The seam with openSig, in the words both designs share. | "The seam between openWallet and openSig" |

## Tensions

- **T1. A class-named exception in a class-agnostic core.** The core's scenario
  says "no requirement in this capability assumes a particular class", and the
  exception names the practitioner class. It imposes nothing on any holder; it
  widens what a consuming domain may require, for one act. Ruling 154 names the
  act, so the tension is recorded rather than designed away (Open question 12).
- **T2. Ruling 160 and a practice that verifies its own practitioners.** If the
  practice is the verifier, the practice's record and the wallet's are not
  independent, and "both must hold" adds little (Open question 2).
- **T3. Declared custody and evidence that the holder acted.** openChart accepts
  only `isolated_per_use_authorized`, and nothing in openWallet yet verifies that
  a key's custody is what its wallet declares (Open question 4).
- **T4. The ratified algorithm and practitioners' hardware.** Ed25519 over an
  exact preimage excludes passkeys and most platform authenticators (Open
  question 5).
- **T5. The harmonized sentence in the union** with
  `add-trust-anchors-and-machine-holders` (D9).
- **T6. The leg of the new family.** Q7 covers two families; the ratified
  challenge-proof change defaults new schemas to the spec leg (Open question 1).

## Open questions for ratification

Each is a judgment the author made, or a choice the owner must make, with a
recommendation. None is ruled.

1. **Which leg holds the new contract family?** Recommendation: the code leg,
   by an explicit extension of the Q7 override, because the schemas, corpus and
   validator are one release unit (D12).
2. **Who may be a verifier, and may a practice verify its own practitioners?**
   Recommendation: openWallet admits any verifier a relying domain holds. For
   openChart, the owner rules that the wallet's verification must come from a
   verifier other than the practice, such as the licensing authority itself or an
   independent verifier that checks the authority's own record, so that ruling
   160's two records are independent; the practice's own check stays its record
   (ruling 98, openChart's AU-03).
3. **How often is a licence re-verified, and what covers the gap when an
   authority suspends a licence between verifications?** Recommendation, as
   openChart's configuration and not openWallet's text: a reliance bound of at
   most 30 days after the licence was checked; a verifier that watches the
   authority and revokes within one business day of learning of a change; a
   revocation list republished at least daily; and an openChart staleness bound
   of 72 hours, past which a sign-off is not checkable and fails in the way the
   signer can cure.
4. **On what evidence may a key's custody be accepted as
   `isolated_per_use_authorized`?** Recommendation: a successor openWallet change
   defines a custody-acceptance record, such as hardware attestation verified
   when the key is bound. Until then openChart records the custody as declared,
   and ruling 152 already keeps every real decision from being recorded; going
   live waits for the successor.
5. **The ratified profile is Ed25519 over an exact preimage. Accept the narrower
   hardware it allows, or add a profile?** Recommendation: version 1 accepts only
   keys that can make the ratified proof with per-use authorization, such as
   smart-card class devices; if the owner wants passkey-class devices, a
   successor change adds a WebAuthn assertion profile. This change does not widen
   the ratified profile.
6. **May the licence identifier be carried in clear?** Recommendation: yes. It
   is needed for ruling 160's comparison, authorities commonly publish it, and it
   never identifies a patient.
7. **The names that become machine keys** (D12). Recommendation: confirm or
   change them now, while nothing pins them.
8. **How are licence classes named across jurisdictions?** Recommendation: the
   authority's own designation and the jurisdiction's ISO 3166 code, with no
   equivalence in openWallet; the relying domain maps each (authority, class)
   pair to the decisions it may make.
9. **Several licences in one wallet.** Recommendation: one verification per
   licence, and the relying domain records which one a sign-off relied on.
10. **Which statuses support a sign-off?** Recommendation: openChart relies on
    `active` only in version 1, and treats `active_with_conditions` as not
    supporting a sign-off until a later change can represent conditions.
11. **Does an AI's wallet (ruling 183) need anything from this profile?**
    Recommendation: no. An agent never carries a licence verification, so this
    profile can never make an agent's signature a practitioner's sign-off (ruling
    157).
12. **Accept a core exception that names a holder class?** (T1) Recommendation:
    yes; it imposes nothing on any holder and is the one exception ruling 154
    names.
13. **Where does the key binding registry run?** Recommendation: inside the
    practice's deployment, populated by openChart's account-to-wallet binding
    (D7).
14. **What must openChart hold locally to check a sign-off offline?**
    Recommendation: the key binding registry; the wallet records of bound
    practitioners; the licence verifications as presented; each verifier's key
    and its latest revocation list; and, through openSig's draft, the openSig
    attester and its attestation keys, retired ones included.

## Status

`Status: proposed`. No alignment pass has run yet; `tasks.md` 1.1 schedules one
adversarial reviewer before ratification, as this leg's other changes did.
Ratification is pending, by openWallet's operator authority, Brett Heap.
