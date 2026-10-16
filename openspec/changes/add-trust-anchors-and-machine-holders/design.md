# Design: add-trust-anchors-and-machine-holders

## Context

Discussed 2026-10-16 by Brett Heap with Claude (Fable 5.1), in session, while
designing SSH access between the workstations Eagle and Raven with a Smallstep
SSH certificate authority and Keycloak. **Nothing here is ruled.** The
decisions below are the design the discussion arrived at, written up for
ratification, and each names the alternatives it rejects so that they are not
re-argued later.

The trigger, in one line: Raven needed to hold the host CA's root key — ONE
entry vouching for every host the CA signs — and the standard had no place for
another holder's key, no holder class for a computer, and no statement of how
verification works or of what a verifier may consider. D1 answers the second
gap, D2 the first, and D3 to D5 the third. D6 and D7 are non-normative and
record the issuer's side and the worked SSH mapping. D8 to D11 settle the
mechanics the first five leave open.

## D1 — A computer is a holder: `machine` joins the closed holder-class set

The closed set becomes `person | practitioner | organisation | agent |
machine`. It is one enum member on `openxwallet-record`'s `holder.holder_class`,
appended, with nothing renamed or reordered.

**A machine wallet uses the multi-key shape unchanged.** Eagle is ONE wallet. Its
declared key set is its two sshd host keys: the Windows OpenSSH key as
`key_reference` and the WSL sshd key as a `keys:` entry. Each carries its own
custody, its own fingerprint and its own state. The two daemons are two
presenters of one host's authority. That is the case `add-multi-key-wallets` D1
built the set for, and nothing here extends it.

**Custody needs NO registry change.** The registry defines each member by two
booleans, and both can be answered for a machine key without interpretation:

| the key | readable by the holder's execution context | per-use authorization outside it | member | evidences | ceiling |
|---|---|---|---|---|---|
| a host key in a root-owned or SYSTEM-ACL'd file | yes | no | `holder_readable` | environment | `act` |
| a TPM-resident key the OS may invoke at will | no | no | `isolated_invocable` | environment | `act` |

The member descriptions already cover both: "a readable file" and "an OS
keystore". So the closed set is closed here too, and no member is added.

**"A machine never evidences a HOLDER acting", stated as a computation and not
as a class rule.** The registry derives `evidences` from the two booleans and
never from holder class, and the core's own scenario says that no requirement
assumes a particular class. So this change does NOT add a class-keyed bar such
as "a machine may not declare `isolated_per_use_authorized`". It states the
consequence for the case that exists. An UNATTENDED service key — one the OS
uses on every connection with no authorization from outside its own context —
has `use_requires_authorization_outside_holder_execution_context: false`. It
therefore falls under one of the two rows above, evidences the environment, and
is capped at `act`. A machine key that genuinely required a per-use
authorization from outside the machine would derive `holder` like any other
key. Whether a non-human authorizer can supply that authorization is the
question `add-multi-key-wallets` D7 records as Q10. That question stays open
and is not answered here (Open question 1).

**The agent profile is untouched.** Its requirement "An agent holder declares
its composition" binds class `agent` only, its scenario "composition belongs to
the agent profile only" already exempts every other class, and validator rule
(q) refuses a composition whose wallet is not `agent` under the existing
`composition-on-non-agent`. A machine therefore owes no composition, and a
composition declared for one is refused with no new code (D9).

REJECTED:

- **Model a computer as `agent`.** The agent profile would demand a composition
  hash — model version, prompt contract, tool manifest — for a host that has
  none, and the profile would have to explain why a class it governs ignores
  half its contract. That is the fault the birth change's design ("Why the first
  draft was wrong") removed from the core, and this change does not reintroduce
  it through the profile.
- **Model a computer as `organisation`.** A host is not the party accountable
  for itself; the organisation that operates it is. Declaring Eagle an
  organisation would conflate the operator with the operated, and every act its
  keys present would read as the organisation's.
- **One wallet per daemon.** It would split one host into two holders and
  multiply authority: two wallets need two grants, or one grant addressed to
  two audiences, which the grant shape does not express. That is
  `add-multi-key-wallets`' own reason for rejecting four seat wallets.
- **A custody member for machines.** A member keyed on holder class could not
  be derived from the two booleans, which is the derivation rule (b) enforces.
  Both real cases already have a member. A member whose booleans repeat an
  existing member's would be a second name for one fact, and no current rule
  would notice: `custody-duplicate-member` compares member ids, not the
  booleans. The way to keep that from happening is not to add one.
- **`service` as the class name.** A service is a role a machine plays. Eagle
  plays it twice, and the holder is the machine that holds both keys.

## D2 — Trust anchors are HELD, never declared: a new core kind `xfactory_wallet_trust_anchor`

The wallet's "contact list". It is a NEW record kind in the core family, with
contract id `openxwallet-trust-anchor` and file
`contracts/openxwallet/openxwallet-trust-anchor.schema.yaml`. An anchor is OWNED
by one wallet, the holder whose trust it records, and names ANOTHER holder's
public key or keys.

**Its fields, at the level the requirement binds** (the schema is realization
work, `tasks.md` 2.4–2.8):

| field | what it carries |
|---|---|
| `anchor_id` | the record's identity. Indexed, with a duplicate refused under the EXISTING `record-id-duplicate` |
| `owner_wallet_ref` | the wallet whose trust this records. REQUIRED, and it must resolve |
| `subject.did` | the anchored holder's DID. REQUIRED. A subject with no DID of its own (a public host publishing a bare host key) is anchored under `did:key` of its own public key, which asserts nothing beyond the key, which is exactly what a peer anchor means |
| `subject.holder_class` | OPTIONAL and descriptive. No rule consults it (D4) |
| `anchor_role` | `issuer` (a root that vouches for a population it signs) or `peer` (one holder's own leaf key) |
| `scope.names` | for an issuer, the names or population it may certify, as patterns (`eagle`, `*.lan`, `192.168.1.*`). For a peer, OPTIONAL literal names that holder answers to, and never a pattern |
| `keys[]` | one or more anchored keys, `minItems: 1`. Each has `key_id`, `public_key_multibase` (REQUIRED, see below), `key_fingerprint` (REQUIRED), `signature_algorithm`, `state`, `provenance[]` and `revalidate_by` |
| `keys[].provenance[]` | how THIS key was verified: `method`, `observed_at`, `source`, and, for `attestation`, `attested_by` (D5). Append-only |
| `keys[].revalidate_by` | the staleness bound (D3, D5) |
| `state` | the anchor's own state: `active`, `suspended` or `revoked` |

**`public_key_multibase` is REQUIRED on an anchored key, where it is OPTIONAL on a
declared one.** The asymmetry is the point of the two kinds. A wallet record is
a REFERENCE: the key lives with its holder, and the record says which key and
what its custody evidences. An anchor exists to VERIFY, and nothing can be
verified against a fingerprint. Requiring the public half is also what lets the
fingerprint be recomputed rather than decorative (D8).

**Provenance is recorded PER KEY, not per anchor.** Keys arrive at different
times through different channels. A CA's replacement root may come attested by
the old root, two years after the old root was compared by hand. An
anchor-level provenance would let a key added later inherit a verification it
never had, which is the laundering D5 exists to prevent.

**State is per anchor AND per key, and `revoked` is terminal.** A key's
effective state is the more restrictive of its own and its anchor's. Suspending
the anchor stops every key it holds; revoking one key leaves its siblings
active. `suspended` may return to `active`; `revoked` never does. That is the
rule the ratified, not-yet-archived `add-composition-drift-cascade` states for
grants ("a revoked grant is never reactivated"), applied to anchored keys.

**The invariants, each as a computation:**

1. **Never in the declared set** (`trust-anchor-in-declared-set`, NEW). Every
   anchored key is compared against `declared_keys(owner)`, the ONE function
   `add-multi-key-wallets` D1 built so that no second traversal can drift. The
   comparison uses `key_fingerprint` where the declared key carries one,
   `public_key_multibase` where it carries one, and the pair (`subject.did`,
   `key_id`) against (`did`, `key_id`). A declared primary key that carries
   neither a fingerprint nor a public half can be matched by the pair only.
   That is the honest limit of the check, and the check says so.
2. **Never presents the owner's authority.** Anchored keys are NEVER indexed
   into `Context.wallets_by_key`. Rule (r) therefore refuses an exercise
   presented by an anchored key under the EXISTING `presenting-key-unresolved`
   ("a presenting key no wallet declares is refused rather than passed over"),
   with no new code and no new branch.
3. **Confers no authority.** The shape carries no property that could name an
   act, a tier, an audience or a grant, and it closes `additionalProperties`
   at every depth. A grant-shaped field is a `schema` failure, so the wrong
   reading cannot be represented.
4. **One entry per key per owner** (`trust-anchor-key-duplicate`, NEW). An owner
   holds a given fingerprint at most once across all of its anchors. An
   (owner, fingerprint) index is last-write-wins, so a duplicate would let
   entry order decide which provenance and which state a verification reads.
   That is `declared-key-duplicate`'s reasoning at a new site.
5. **No key material.** Rule (a) runs over the new kind unchanged
   (`key-material-embedded`). The new property names avoid every blocklisted
   token, and `public_key_multibase` is already on the allow list.
6. **The anchored DID is a trust fact, not a subject identifier.** The anchor
   names `subject.did` and no subject identifier property at all. A record
   that tries to add one is a `schema` failure, and the MODIFIED non-substrate
   requirement says why.

**Why a separate kind, and not an `anchors:` list inside the wallet record.**
REJECTED, for three reasons:

- **The record's invariant would stop being a property of the document.** Today
  every key in a wallet record is one its holder holds. With anchors inside it,
  that becomes "every key in two of this record's lists", and every reader has
  to know which list it is reading. A reader that does not know is the failure
  mode: `wallets_by_key` is built by walking the record.
- **Anchors churn at a different rate.** Contacts come and go and roots rotate,
  and every such change would rewrite the wallet record, the governed
  declaration of a holder's authority, for a fact that confers none.
- **An anchor has a lifecycle the declared-key shape lacks**: provenance,
  scope and a staleness bound. The record schema would grow a second key shape
  anyway, digested together with the first.

Also REJECTED:

- **Put other holders' keys in `keys:`.** That breaks the record's load-bearing
  invariant directly. Rule (r) would then resolve a presenting key to the wallet
  that merely TRUSTS it, and an exercise signed by the CA would be attributed to
  Raven.
- **Store the contact list in Keycloak user attributes.** Keycloak is an
  identity provider: it binds a login to a holder at issuance. It has no
  key-validation endpoint, a reverse lookup needs an administrative credential,
  and its attribute values are not sized to hold RSA public keys. It is not a
  verifier, and a verifier that had to reach it would not be offline (D3).
- **A flat known_hosts-style list of leaf keys.** One entry per host is what the
  issuer role exists to replace. It is trust-on-first-use at scale, and it
  records no provenance.
- **One record per anchored key.** Rotation would have no shape. The new root
  would be a new record whose relation to the old one is unstated, so the
  requirement's "the replacement key is added beside it" could not be
  expressed. One anchor per (owner, subject, role) with a key list reuses the
  multi-key shape.

**A name collision, recorded so that it is not tripped over.** openXwallet, the
factory-layer adapter that pins this standard, has an "issuer anchor" of its
own: an organisation's anchor for who may issue its root review-authority grants
(validator rows `OXWR-R1` and `OXWR-R2`, feature `012-wallet-issuer-anchor`).
The root `AGENTS.md` places it in openXwallet and openxFactory. It is a
different thing. That one says who may ISSUE GRANTS; the `issuer` role here
says which root a verifier trusts to have SIGNED A KEY. Nothing of openXwallet's
concept moves, and the role value `issuer` is the discussion's word (Open
question 4).

## D3 — Verification is offline against held anchors; the issuer is consulted at issuance only

A holder verifying a credential or signature presented by another party checks
it against anchors it ALREADY holds. For a certificate, that is an issuer
anchor's signature over the presented key; for a bare key, a peer anchor's key.
It does not contact the issuer, a directory or an identity provider at
verification time. The issuer is consulted when it ISSUES. `resolver`
provenance fetches a DID document when an anchor is TAKEN (D5), never when one
is used.

**Cache roots, not leaves.** Where an issuer anchor covers a subject, that
subject's leaf keys are not held as trust decisions. A cached leaf is at most a
convenience with a staleness bound. This is the one part of the requirement a
static validator can see, and it is made checkable
(`trust-anchor-leaf-unbounded`, NEW). For each peer anchor of owner O whose
`scope.names` include a name matched by an ACTIVE issuer anchor of O, every
anchored key must carry `revalidate_by`. A peer anchor naming no names cannot
be shown to be covered. That is honest rather than checked, and the realization
reports it as a NOTE.

**Revocation is checked at use.** The inputs are the credential's own validity
window, the effective state of the anchor key that verifies it (D2), and a
revocation list where the consumer distributes one, fetched ahead of time and
never per verification. Short credential lifetimes are the PRIMARY mechanism.
A 16-hour user certificate needs no revocation infrastructure to stop working
tomorrow.

**What the validator does, and does not, do here.** The canonical validator
already "does not verify signatures, resolve DIDs, or contact a key store", and
that is unchanged: this requirement binds the CONSUMERS that verify. Its static
probe is the leaf rule above, together with the anchor states it reads.
Use-time revocation would need a verification-event record before it could be
probed statically, and that is a named successor (D11).

**Why the revocation clause is HERE and not in "Revocation propagates through the
chain".** The active change `add-composition-drift-cascade` MODIFIES that
requirement. Two concurrent MODIFIED blocks on one requirement collide at
archive: whichever archives second replaces the other's text. This leg has
already measured that failure, as the scenario-loss refusal recorded in
`add-multi-key-wallets`' archive notes. Anchor revocation is a property of
verification, not of grant derivation, so it belongs with R10 anyway.

REJECTED:

- **Online validation against the CA per use.** It adds an availability
  dependency on every login, so that the CA being down means Eagle is
  unreachable. It leaks to the CA who connected to what and when. And it buys
  nothing, because the signature already carries the proof the online check
  would re-derive.
- **A central "trust service" on the internet.** The web PKI reached through
  `did:web` already is one, and it is used for exactly one thing: `resolver`
  provenance when an anchor is taken. Building a second one would put a
  network service back in the verification path that D3 removes.

## D4 — The verifier is holder-class blind; authorization is credential plus local mapping

A resource decides access from these inputs:

1. the presented credential verifies against an anchor the resource holds;
2. its principal or scope maps to a local account or role;
3. that account's or role's own local privilege applies;
4. every hard limit the credential carries is enforced: a source restriction, a
   forced command, no forwarding.

It does not consult holder class. Whether a person or an agent may OBTAIN a
credential is ISSUANCE policy. That is where the tenant's ruling that this CA
issues no agent credentials lives: on the CA's OIDC provisioner, not on Eagle.

This is the existing rule "Agent authority is grant scope, not a parallel
vocabulary", seen from the resource's side. What an agent may do is the scope
of what it holds. A resource that ALSO checked the holder's class would be
running a second authority vocabulary beside the credential's scope, which is
the outcome that requirement forbids. So the profile needs no change (D9).

**The shape enforces it.** An anchor's `scope` has no holder-class property, so
an issuer anchor cannot be scoped to "persons only". `subject.holder_class` (D2)
describes the ANCHORED holder (the CA is an organisation, Eagle is a machine),
never the presenter, and no rule reads it.

**Role-shaped principals are the guidance, not a requirement.** `eagle-admin`
rather than `brett`. The issuer then decides who gets a role, and the resource
decides what the role opens. A person-shaped principal turns every resource's
mapping into a list of people and moves the who-gets-it decision into each of
them. It is guidance because principal naming is the consumer's vocabulary, not
the standard's.

**How this sits beside the core's grant model.** An SSH certificate has a grant's
three properties: an audience (the certified key and its principals), a scope
(principals and limits) and an expiry (its validity window). But it is the
ISSUER's carrier and not an `xfactory_wallet_grant`. This change does not make
it one, and it records no SSH session as a key-attributed exercise (D11,
Open question 6).

REJECTED:

- **A verifier-side class check.** The class a resource would read is asserted
  by the presenter's own wallet record. A resource checking it trusts a
  self-declaration, which is the laundering surface rule (r) exists to close.
  The same policy repeated in N resources drifts, where at the issuer it lives
  in one place. And the check would be the parallel vocabulary named above.
- **Person-shaped principals as the convention.** See above.

## D5 — An unknown holder is validated before it is trusted; bootstrap is out of band

**The provenance methods form a closed set, ordered by what each establishes:**

| method | what it is | establishes trust? |
|---|---|---|
| `out_of_band_fingerprint` | a fingerprint compared through a channel the holder already trusts: carried by hand, from a password manager, or from a repository the holder trusts | yes |
| `attestation` | signed or vouched for by an anchor the holder ALREADY holds | yes, iff the attester is admissible (below) |
| `resolver` | the subject's DID document, fetched over the web PKI | yes for a PEER; for an ISSUER, confirmation only |
| `first_use` | accepted because it was seen | never. Labelled, with `revalidate_by` REQUIRED |

**The rules, as computations over one owner's anchors:**

- **An issuer anchor needs establishing evidence**
  (`trust-anchor-issuer-self-evidenced`, NEW). Every key of an `issuer` anchor
  carries at least one `out_of_band_fingerprint` entry or one admissible
  `attestation` entry. `resolver` and `first_use` entries may sit beside them,
  and alone they are refused. The reason is blast radius: an issuer anchor
  vouches for its whole scope. If its only evidence were the issuer's own
  published record, a compromise of the issuer's web origin would substitute a
  root for the whole population. The out-of-band comparison is what makes the
  root's trust independent of the origin it protects. That `first_use` is
  refused here as well is this design's extension of the discussion's rule
  (Open question 2).
- **First use is bounded** (`trust-anchor-first-use-unbounded`, NEW). A key
  whose provenance contains no establishing entry must carry `revalidate_by`.
- **An attestation must resolve** (`trust-anchor-attestation-unresolved`, NEW).
  `attested_by` names an anchor held by the SAME owner and a key in it. A
  deleted anchored key reds every attestation that cited it, which is how
  "retired by state, never deleted" gets its teeth in one tree, exactly as
  `presenting-key-unresolved` gives them to declared keys.
- **An attestation must come from an admissible attester**
  (`trust-anchor-attestation-unverified`, NEW). The attesting key itself rests
  on establishing evidence, so trust on first use cannot be laundered through
  one hop. And it COVERS the attested subject: either an issuer anchor whose
  scope matches the attested anchor's names, or a peer anchor naming the same
  subject DID (a holder attesting its own key rotation). Establishment is
  computed as a least fixed point from the `out_of_band_fingerprint` (and peer
  `resolver`) entries upward, so a cycle (A attests B, B attests A)
  establishes nothing.
- **Admissibility does NOT read the attester's CURRENT state.** A first draft
  required the attester to be `active`, and that was wrong for the ordinary
  case. A CA root retired by routine rotation would then turn every attestation
  it made, while it was in force, into a finding, and committed history would be
  invalidated by a rotation. That is the defect `add-multi-key-wallets` D9
  closed for declared keys. Current state decides USE (D3); evidence and
  coverage decide ESTABLISHMENT. A COMPROMISED attester is a different case:
  what it attested is the holder's to revoke explicitly, and propagating that
  revocation automatically, with a reason class like the drift cascade's, is a
  named successor (D11).
- **First use is never rewritten.** Verifying a first-use key later APPENDS an
  establishing entry and leaves the `first_use` entry in place. There is no
  `verified: true` field to set: the only way to claim verification is an entry
  with an establishing method, its own `observed_at` and its own `source`. One
  tree cannot see that an entry was rewritten in place, so a diff-time check is
  a named successor (D11).
- **Refusing first use entirely is a policy, and the standard represents it by
  absence.** A holder that refuses first use holds no first-use entries. No
  field records the policy.

**Bootstrap.** The first anchor arrives through a channel the holder already
trusts, and that provenance is recorded with its source. An issuer's
self-published record, such as the tenant's DID document listing its CA roots,
is CONFIRMATION recorded beside the out-of-band entry, never instead of it. A
subject covered by no held anchor is validated by `resolver` or by `attestation`
before trust.

REJECTED:

- **A boolean `verified` beside the method.** Two spellings of one fact, which
  can disagree. The one that says "verified" is the one a reader believes, and
  a `first_use` method beside `verified: true` is the laundering this
  requirement forbids.
- **Trust on first use as the default.** It is what a flat known_hosts list
  does, and it is what the issuer role replaces (D2).
- **`resolver` as sufficient evidence for an issuer.** See the blast-radius
  argument above.

## D6 — Enrolment of a machine with an issuer (design note, largely non-normative)

An issuer signs a machine's key only on proof from a provisioner. The proof is
one of three things:

- a single-use, short-lived token minted by an authorised operator and bound to
  the names the certificate may carry;
- an authenticated administrative identity;
- hardware attestation: a TPM endorsement key registered BEFORE enrolment, so
  that the inventory exists before the host does.

The issuer keeps no "slot" per name. Two certificates for one name can coexist,
so uniqueness is policy plus audit of the issuance log. Renewal is proof of
possession of the CURRENT credential, so a host that was never enrolled has no
later way in.

**Enrolment evidence is the ISSUER's record. The machine wallet records custody
only, and NO new record field is needed.** REJECTED: an `enrolment` block on the
wallet record. It would put the issuer's decision on the subject's own record,
the subject asserting its own vetting. A verifier could not check that claim
offline and must not trust it. Whatever the issuer decided is already carried,
signed, by the certificate it issued.

## D7 — Worked consumer mapping: SSH with Smallstep (non-normative)

This records how the standard's terms land on a real deployment, so the terms
can be checked against one. Product details are as of 2026-10-16.

**Server side: Eagle's machine wallet.**

| the standard | sshd |
|---|---|
| holder class `machine`; declared keys = the two host keys, both `holder_readable` | `C:\ProgramData\ssh\ssh_host_ed25519_key` (Windows OpenSSH, SYSTEM/Administrators ACL) and `/etc/ssh/ssh_host_ed25519_key` (WSL sshd, root-owned) |
| each declared key's issuer credential | `HostCertificate`, one per daemon, signed by the host CA. The certificate is the issuer's record, not a wallet field (D6) |
| an issuer anchor for the USER CA root, scoped to the principals it may certify | `TrustedUserCAKeys` in both `sshd_config` files |
| the local mapping (D4) | `AuthorizedPrincipalsFile`: principal to account, holder-class blind |
| the credential's hard limits (D4) | certificate critical options (`source-address`, `force-command`) and withheld extensions (no `permit-port-forwarding`, no `permit-agent-forwarding`), enforced by sshd |
| a revocation list, where distributed (D3) | `RevokedKeys` (a KRL) |

**Client side: Raven's wallet.**

| the standard | ssh |
|---|---|
| an issuer anchor for the HOST CA root, scoped to `eagle`, `*.lan`, `192.168.1.*` | ONE `@cert-authority eagle,*.lan,192.168.1.* <host CA key>` line, served by `KnownHostsCommand` from the wallet or written once into `known_hosts` |
| roots, not leaves (D3) | NO per-host entries for tenant hosts |
| peer anchors | only for services that publish bare host keys (a public code host), as ordinary `known_hosts` lines |
| the wallet's long-lived declared key | Raven's DID identity |
| the SSH user certificate's key | EPHEMERAL, minted per login and held in the agent the wallet exposes (`IdentityAgent`). It is NOT declared, on `add-multi-key-wallets` D7's precedent: an ephemeral key cannot be enumerated in a static record |

**Provenance of both roots: `out_of_band_fingerprint`, source `step ca
bootstrap`.** One nuance belongs in the record and not in a footnote.
`step ca bootstrap --fingerprint` compares the SHA-256 of the CA's X.509 ROOT
CERTIFICATE. The SSH user and host CA keys are then fetched over TLS
authenticated by that root (`step ssh config --roots`, with `--host` for the
host CA). Recording the SSH roots as `out_of_band_fingerprint` is exact when
their OWN fingerprints were compared by hand. When what was compared is the
X.509 root's fingerprint, the strictly faithful record is an anchor for the
X.509 root (`out_of_band_fingerprint`) plus `attestation` by it for the two SSH
roots (Open question 5).

**Keycloak** is an OIDC provisioner on the CA. It binds the human login to a
principal at ISSUANCE, and it is where "no agent credentials" is enforced. It is
absent from verification (D3, D4).

**Defaults at time of writing**: step-ca issues user certificates for 16 hours
and host certificates for 30 days by default, configurable per provisioner. The
16-hour window is the primary user-side revocation mechanism (D3).

## D8 — Fingerprints: one spelling in records, the compared spelling in provenance

Three fingerprints meet in this deployment, over three different byte strings:

- the family's `key_fingerprint`: `sha256:` plus the lowercase hex of SHA-256
  over the RAW public key, as the multi-key change pinned it;
- OpenSSH's `ssh-keygen -l`: `SHA256:` plus unpadded base64 of SHA-256 over the
  key's SSH wire-format blob;
- `step ca bootstrap --fingerprint`: hex SHA-256 over the root's DER
  certificate.

A record that copied one of these into another's field would carry a
fingerprint that never recomputes. So an anchored key's `key_fingerprint` is
ALWAYS the family's spelling, and a provenance entry MAY record the fingerprint
that was actually compared, in its source's spelling, with the spelling named.
That keeps both the join token and the evidence honest.

**Recomputation is algorithm-conditional.** The existing recomputation
(`add-multi-key-wallets` D5) decodes `did:key`'s ed25519 multicodec only. Where
an anchored key is ed25519, its fingerprint is recomputed from the now-required
`public_key_multibase`, under a NEW `trust-anchor-fingerprint-mismatch`. Where
it is another algorithm (a CA key may well be ECDSA P-256), the family has not
yet pinned which byte encoding "the raw public key" means. The fingerprint is
then honest rather than checked, and the validator says so in a NOTE. It never
refuses a key merely for being another algorithm. Pinning the encodings is a
named successor (D11).

Why a NEW code rather than the existing `declared-key-fingerprint-mismatch`:
that code's name says the key is DECLARED, which an anchored key by definition
is not. `add-multi-key-wallets` D4 had to correct a message that a change made
false, and this avoids creating a code that is false on arrival
(Open question 7).

## D9 — Where this lives: the core, not a profile

Every statement here is holder-class agnostic, and D4 says so outright, so it
belongs in `openxwallet`. The agent profile was checked requirement by
requirement:

- **"An agent holder declares its composition"** binds class `agent` only. A
  machine is "a holder of another class", whose scenario already says no
  composition is required of it.
- **"A composition change revokes the agent's grants immediately"** is about
  agents' grants and untouched.
- **"Agent authority is grant scope, not a parallel vocabulary"** is the rule
  D4 restates from the resource's side, and it is consistent as written.

So no `openxwallet-agent-profile` delta. A MACHINE profile (hardware
attestation, enrolment evidence, TPM inventory) would be a sibling capability
over the core, the way the birth change shaped profiles. It is a named
successor gated on a consumer of its own (D11).

## D10 — Release class: an ADDITIVE MINOR, one digest moves and one member is added

- `openxwallet-record.schema.yaml` changes by one enum member and its
  description, so its `sha256:` moves. Its per-file `contract_schema_version`
  moves by one from its value at realization (2 today). The file's top-level
  `schema_version: 1`, the document meta version shared across the bundle,
  does not move. That is the reading `add-multi-key-wallets` D8 recorded.
- `openxwallet-trust-anchor.schema.yaml` is a NEW owned member at
  `contract_schema_version: 1`. That is a new row in the root's
  `contracts/manifest.yaml`, selected into the release record by
  `member_class` like every owned row. Every count of owned rows the manifest's
  own comments carry is corrected with it.
- No other digested byte moves. The custody registry and its schema, the grant,
  the exercise, the distinct-holder constraint, the subject attestation and the
  agent composition are to be PROVEN unchanged by recomputation.
- No finding code is renamed, repurposed or reclassified, and there is no new
  WARNING. The new codes are ERRORs, and the honest-not-checked cases are
  NOTES.
- `REQUIREMENTS` gains four rows, one per ADDED requirement (proposed
  `OXW-R9` to `OXW-R12`, in the delta's order), each with at least one negative
  confirmation, so that requirement closure stays two-directional.

MINOR and not MAJOR, because nothing a consumer declares today becomes invalid.

**A behaviour to state in the CHANGELOG.** The repository sweep adjudicates only
kinds in `KIND_TO_SCHEMA` and skips the rest, so a consumer that writes anchor
records before moving its pin gets them SKIPPED, not refused. The pin bump is
what brings them under adjudication. A consumer whose own code matches
`holder_class` exhaustively meets one new value.

The bundle version, the tag and the release commit are allocated at
realization, and nothing is reserved here.

## D11 — Non-goals and named successors

Each of these is OUT for a reason, not by omission:

1. **A change to the closed custody registry.** None is needed (D1).
2. **A machine profile**: hardware attestation, a TPM endorsement-key inventory,
   enrolment evidence. That is the issuer's record (D6), and the profile is a
   sibling capability gated on a consumer (D9).
3. **A verification-event record kind.** A use-time record of which anchor
   verified which credential. It would make D3's revocation-at-use statically
   probeable. Today it is a runtime obligation.
4. **A diff-time append-only check**: that `revoked` never returns to `active`,
   that no anchored key or provenance entry is deleted or rewritten. It needs
   history, so it is a consumer CI concern, not a check one tree can make.
5. **Fingerprint encodings for non-ed25519 algorithms** (D8).
6. **Recording an SSH session as a key-attributed exercise.** The presenting
   key would be the ephemeral certificate key, which no wallet declares, so
   rule (r) would refuse it. `add-multi-key-wallets` D7 kept ephemerals as
   runtime evidence, and nothing here changes that.
7. **A revocation-list carrier.** The KRL stays the consumer's file.
8. **Anchor sets shared across wallets**, such as an organisation-level anchor
   set distributed to every host. Each anchor is owned by one wallet. Sharing
   needs a rule for whose provenance a shared anchor carries.
9. **A scope grammar beyond literal names and `*`/`?` globs**: negation, CIDR
   ranges, principal-versus-host namespaces. The realization pins the glob
   semantics, and anything richer waits for a consumer.
10. **Any change to `Revocation propagates through the chain`** (D3).
11. **Propagating a compromised anchored key's revocation to the keys it
    attested** (D5). The holder revokes them explicitly today. An automatic,
    reason-classed cascade is the anchor analogue of
    `add-composition-drift-cascade`, and it waits for a consumer.

## Open questions for ratification

Each is a judgment the author made that the operator should confirm or
overturn. None is ruled.

1. **No class-keyed custody bar for machines** (D1). "A machine never evidences
   a holder acting" is encoded as a consequence of the registry's booleans for
   unattended service keys, not as a rule that a machine may not declare
   `isolated_per_use_authorized`. A class bar would be the core's first
   holder-class-conditional rule, against its own scenario "no requirement in
   this capability assumes a particular class".
2. **Issuer anchors refuse first use as well as self-publication** (D5). The
   discussion said self-publication is confirmation, never sole evidence, and
   that the first anchor arrives out of band. Refusing `first_use`-only issuer
   anchors extends that. The alternative is to admit them, labelled and bounded
   like any first use.
3. **Provenance per key, append-only** (D2, D5), where the discussion listed
   provenance among the anchor's fields.
4. **Names that become machine keys once released**: the kind
   `xfactory_wallet_trust_anchor`, the role values `issuer` and `peer` (beside
   openXwallet's unrelated "issuer anchor"), the provenance methods, and the
   `trust-anchor-*` codes. They are pinned by name from the first release, so
   they are cheapest to change now.
5. **The bootstrap provenance of the SSH CA roots** (D7):
   `out_of_band_fingerprint` as discussed, or an X.509-root anchor plus
   `attestation` when only the X.509 root's fingerprint was compared.
6. **The SSH certificate's relation to the core's grant model** (D4): it has a
   grant's properties and is not an `xfactory_wallet_grant`. This change does
   not reconcile the two.
7. **A new `trust-anchor-fingerprint-mismatch` rather than reusing
   `declared-key-fingerprint-mismatch`** (D8).
8. **Raven's wallet holder class** (D7, `tasks.md` 4.3). The corpus example
   models Raven's wallet as a `machine`, matching "Raven's wallet" and "Raven's
   DID identity". The verifying process acts for the person who logged in
   through Keycloak, and a deployment may prefer to hold the client-side
   anchors in that person's wallet. D4 makes the choice invisible to Eagle
   either way.
9. **Attester admissibility ignores the attester's current state** (D5). It is
   judged on evidence and coverage, so a routine rotation does not invalidate
   history. The cost is that a compromised attester's attestations stand until
   the holder revokes them (D11.11).

## Status

`Status: proposed`. No alignment pass has run yet. The exemplar ran one
adversarial reviewer before ratification, and `tasks.md` 1.1 schedules the
same here. Ratification is pending, by openWallet's operator authority.
