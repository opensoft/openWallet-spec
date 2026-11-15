# openxwallet-practitioner-profile Specification Delta

## ADDED Requirements

### Requirement: A practitioner holder carries licence verifications

openWallet SHALL let a wallet holder of class PRACTITIONER carry licence
verifications, and SHALL let no holder of another class carry one. A licence
verification is a record, signed by a verifier, stating that the verifier
checked one licence against its source, found it in a stated status, and bound
it to a wallet and to named keys of that wallet. It SHALL state: the wallet it
is bound to, and the fingerprint of every key it was issued over; the
licensing authority and the jurisdiction that authority licenses in; the
licence, by the authority's own identifier for it; the licence class or
profession, in the authority's own designation; the status found; when the
licence was checked, and against which source; which verifier issued the
verification, and when; and the time until which it may be relied on. That
reliance bound SHALL be set by the verifier, and SHALL be no later than the
licence's own expiry where the source states one, and no later than twelve
months after the licence was checked. One verification covers one licence, so
a holder with several licences carries one verification for each. A
verification states no clinical scope: which decisions a licence class may
make is the relying domain's to decide.

#### Scenario: a verification names what was checked

- WHEN a licence verification is validated
- THEN it names its wallet and the fingerprints of the keys it was issued over,
  the licensing authority and its jurisdiction, the licence identifier, the
  licence class, the status found, the source, when the licence was checked,
  the verifier, when it was issued, and its reliance bound
- AND a verification missing any of them is a validation failure

#### Scenario: the reliance bound has two ceilings

- WHEN a verifier sets a verification's reliance bound
- THEN it is no later than the licence's own expiry where the source states one
- AND it is no later than twelve months after the licence was checked
- AND a verification whose bound exceeds either is a validation failure

#### Scenario: several licences are several verifications

- WHEN a practitioner holds licences from two authorities
- THEN their wallet carries one verification for each licence
- AND neither verification states anything about the other licence

#### Scenario: a licence verification belongs to the practitioner profile only

- WHEN a licence verification is bound to a wallet whose holder class is not
  practitioner
- THEN the verification is refused
- AND an agent holder never carries a licence verification, so nothing in this
  profile can make an agent's signature a practitioner's sign-off

#### Scenario: a verification states no clinical scope

- WHEN a licence verification is validated
- THEN it carries the authority's own licence class and no list of acts,
  decisions or scopes that the class permits
- AND a verification carrying such a list is a validation failure

### Requirement: A licence verification is issued by a named verifier over a proof of possession from each key it names

openWallet SHALL require every licence verification to name its verifier and to
carry the verifier's signature over a canonical form of every other field it
holds, made under a signing domain distinct from every other signing domain in
this family, so that no proof of possession, grant or other signed record can
be read as a licence verification, nor a licence verification as one of them. A
verifier is a holder with a wallet of its own, and the key it signs with is a
key that wallet declares. Before it issues a verification, the verifier SHALL
obtain a proof of possession from each key the verification will name, over a
challenge the verifier issued for that purpose, and the verification SHALL
record, for each such key, the key's reference, its fingerprint, its public
key, the proof itself and when it was made. A relying domain SHALL check each
recorded proof whenever it checks the verification: that the proof's signature
verifies under the recorded public key, that the proof names the recorded key
reference, and that the recorded fingerprint is that public key's. It cannot
check the verifier's challenge or the verifier's binding of the key, which are
the verifier's own, and SHALL NOT treat a recorded proof as a binding of its
own. The recorded proofs carry the verifier's own subject and binding
references to every relying domain that holds the verification, so a verifier
SHALL use opaque references there that name no person. A verification covers
exactly the keys it names: a key the wallet declares later, or that a held copy
of the wallet record gains later, is not covered by it. A verification that
supersedes an earlier one SHALL name it. How the verifier satisfied itself
that the licensee it checked is the wallet's holder is the verifier's own
record, and the verification SHALL reference it.

#### Scenario: the verifier signs every field

- WHEN any field of a licence verification is changed after the verifier signed
  it
- THEN its signature no longer verifies
- AND the verification is not relied on

#### Scenario: a verification cannot be read as another signed record

- WHEN a proof of possession, or any other record signed by a key of this
  family, is presented as a licence verification
- THEN it does not verify as one, because its signing domain differs
- AND a licence verification presented as a proof of possession does not verify
  as one either

#### Scenario: each named key proved possession to the verifier

- WHEN a verifier issues a licence verification naming two keys of a wallet
- THEN the verification records, for each, its reference, fingerprint and
  public key, the proof of possession it made over the verifier's challenge,
  and when
- AND each recorded proof verifies under the recorded public key, whose
  fingerprint is the one named
- AND a verification naming a key with no recorded proof is a validation failure

#### Scenario: the relying domain checks each recorded proof

- WHEN a relying domain checks a licence verification one of whose recorded
  proofs does not verify under its recorded public key, or names another key
  reference
- THEN the domain does not rely on the verification
- AND it refuses it as it refuses a verification whose signature does not verify

#### Scenario: a key added later is not covered

- WHEN a key is added to the wallet, or to a relying domain's held copy of the
  wallet record, after a verification was issued
- THEN that verification does not cover the added key
- AND a sign-off made with the added key is not supported by it

### Requirement: A relying domain holds verifier keys with provenance its own administrator cannot forge alone

openWallet SHALL require a relying domain to hold each verifier key it relies
on as a record of its own, never as a key the wallet's holder supplies and
never learned from the verification being checked. Each held verifier key SHALL
carry the verifier's identity, the public key and its fingerprint, its state,
and a provenance that the relying domain's own administrator cannot forge
alone: either it was delivered with a release of the relying system, or it was
added by two named people, with the addition announced to the domain's
declared audience. The two differ in what a later check can show. A key
delivered with a release can be checked by anyone who holds that release, on a
copy of the records; a key added by two people rests on the domain's own
records alone, which whoever runs the deployment can alter. Every reliance SHALL
therefore record the provenance of the verifier key it rested on, and a
reliance on a key added by two people SHALL be recorded as such. A verifier key
SHALL arrive together with that verifier's newest revocation list, so that the
domain can check the verifier's verifications from the moment it holds the key.
A held verifier key that is compromised SHALL record the time from which it is
treated as compromised. A relying domain MAY require that the verifier is a
holder other than itself, and MAY admit only verifier keys delivered with a
release; a verification names its verifier so that it can.

#### Scenario: a key added by one administrator is not held

- WHEN one administrator of a relying domain adds a verifier key alone, without
  a second named person or a release of the relying system
- THEN the key is not held
- AND no verification signed by it is relied on

#### Scenario: a key delivered with a release is held

- WHEN a verifier key arrives with a release of the relying system
- THEN the relying domain holds it, recording that release as its provenance
- AND that verifier's newest revocation list arrives with it, so the domain can
  check that verifier's verifications from the first sign-off

#### Scenario: a reliance on a key added by two people is recorded as such

- WHEN a relying domain relies on a verification signed by a verifier key that
  two named people added
- THEN the reliance records that provenance
- AND a check run on a copy of the records with only the verifier keys
  delivered with releases of the relying system does not accept it

#### Scenario: a compromised verifier key

- WHEN a held verifier key is recorded as compromised from a given time
- THEN no verification signed by it is relied on from the moment the compromise
  is recorded
- AND every reliance on a verification it signed, made since that time, is
  raised to the responsible human through the domain's declared escalation path

### Requirement: A licence verification is checked inside the relying domain and never waits on an outside service

openWallet SHALL let a relying domain decide whether to rely on a licence
verification from what it already holds: the verification, as the wallet's
holder presented it; the held verifier key; the newest revocation list from
that verifier that the domain holds; the held record of the bound wallet; and
its own clock. Deciding SHALL NOT contact the verifier, the licensing
authority, a directory, the wallet or its holder's device, and SHALL NOT wait
for any of them. The domain fetches each verifier's revocation list when it
can. At reliance it SHALL use the newest list it holds, SHALL NOT wait for a
newer one, and SHALL record on the reliance which list it used and how old that
list was. A reliance made with a list older than the freshness bound the domain
declares SHALL still stand, SHALL be flagged, and SHALL be raised to a human in
the relying domain. If no newer list reaches the domain, no revocation the
verifier has since published reaches it either: each reliance on that
verifier's verifications keeps standing, flagged and raised, until the
verification's reliance bound stops it, at most twelve months after the licence
was checked. Every item this profile raises to a human SHALL reach a human
other than the practitioner whose sign-off it concerns: where that practitioner
is the one who would receive it, the relying domain SHALL name a second
recipient, and SHALL NEVER raise it to the signer alone. A held revocation list
SHALL NEVER be replaced by one with a lower sequence. A relying domain SHALL
refuse to rely on a verification that is
past its reliance bound; is superseded by a later verification it holds of the
same licence, for the same wallet, from the same verifier; is revoked in the
newest list it holds; is bound to another wallet, or does not name the key that
made the sign-off; is signed by a verifier key it does not hold, or holds as
suspended, revoked or compromised; or whose signature, or any proof of
possession it records, does not verify. A verification is not checkable only
where the domain holds nothing to check it with: no revocation list at all from
its verifier, or no record of the bound wallet. That is cured by the deployment
obtaining what it lacks, never by the signer.

#### Scenario: the decision never waits on an outside service

- WHEN a relying domain checks a licence verification while no network outside
  its deployment is reachable
- THEN it decides from what it holds, and contacts and waits on nothing outside
  the deployment

#### Scenario: an old revocation list does not block

- WHEN the newest revocation list a relying domain holds from a verifier is
  older than the domain's freshness bound
- THEN a reliance on that verifier's verification still stands
- AND the reliance records which list was used and how old it was, is flagged,
  and is raised to a human in the relying domain

#### Scenario: with no newer list, the reliance bound is the only hard stop

- WHEN no revocation list newer than the one it holds reaches a relying domain
  from a verifier
- THEN each reliance on that verifier's verifications stands, is flagged and is
  raised
- AND each verification stops being relied on at its own reliance bound

#### Scenario: a raised item never reaches the signer alone

- WHEN the practitioner whose sign-off an item concerns is the human the
  relying domain would raise it to
- THEN it also reaches the second recipient the relying domain names
- AND it is never raised to the signer alone

#### Scenario: a revocation list is never rolled back

- WHEN a relying domain is offered a revocation list from a verifier whose
  sequence is lower than the list it holds
- THEN it keeps the list it holds

#### Scenario: a verification past its reliance bound is not relied on

- WHEN a licence verification is checked after its reliance bound
- THEN the domain does not rely on it
- AND its validity when issued is not accepted as evidence of its validity now

#### Scenario: a verification that does not name the signing key is refused

- WHEN a sign-off is made with a key whose fingerprint the licence verification
  does not name
- THEN the domain does not rely on that verification for that sign-off

#### Scenario: nothing to check with is cured by the deployment

- WHEN a relying domain holds no revocation list at all from a verifier, or no
  record of the bound wallet
- THEN the verification is not checkable
- AND the deployment, not the signer, cures it by obtaining what it lacks

### Requirement: A licence verification ends by its reliance bound, by supersession or by revocation, checked at reliance

openWallet SHALL make a licence verification stop being relied on: at its
reliance bound, with no grace period; when a later verification of the same
licence, for the same wallet, from the same verifier supersedes it; when its
verifier revokes it; when the bound wallet is revoked, and for as long as it is
suspended; and, from then on, when the relying domain no longer holds the
verifier's key as active. A verifier SHALL re-check the licence against its
source on its own schedule, SHALL revoke a verification it learns no longer
holds, because the licence's status changed, because it was issued in error,
because the binding to the wallet no longer holds or because the verifier
withdraws it, and SHALL publish each revocation in a signed revocation list
with a rising sequence that names a reason class for each entry. A revoked
verification SHALL NEVER return to force: re-verification is a new
verification that names the one it supersedes. As every revocation in this
family is, revocation SHALL be checked at the moment of reliance, never trusted
from issuance. Retiring a key the verification names SHALL stop that key making
a sign-off it supports, and SHALL NOT end the verification for the other keys
it names. A revocation SHALL NOT rewrite a reliance made while the verification
was in force, but a relying domain that receives a revocation whose reason
class says the verification was never true, or that the verifier withdrew it,
SHALL raise every reliance it affects to the responsible human through its
declared escalation path.

#### Scenario: no grace period after the reliance bound

- WHEN a licence verification's reliance bound passes
- THEN it is not relied on from that moment
- AND no tolerance or grace period extends it

#### Scenario: an authority's suspension between checks

- WHEN a licensing authority suspends a licence after a verification of it was
  issued and before that verification's reliance bound
- THEN the verification is relied on only until its verifier's revocation
  reaches the relying domain or its reliance bound passes, whichever comes
  first
- AND a domain holding that revocation does not rely on the verification from
  then on

#### Scenario: re-verification supersedes and a revocation is terminal

- WHEN a verifier re-verifies a licence for the same wallet
- THEN the new verification names the one it supersedes, and the earlier one
  is not relied on once the domain holds the later one
- AND a revoked verification is never returned to force

#### Scenario: revoking the wallet ends its verifications

- WHEN the wallet a licence verification is bound to is revoked
- THEN the verification is not relied on from that moment
- AND while a bound wallet is suspended, its verifications are not relied on

#### Scenario: retiring one named key

- WHEN one of two keys a verification names is retired
- THEN a sign-off made with the retired key is not supported
- AND the verification still supports sign-offs made with the other key

#### Scenario: a verification that was never true, or that was withdrawn, reaches a human

- WHEN a relying domain receives a revocation whose reason class says the
  verification was issued in error, or that its verifier withdrew it
- THEN every reliance on that verification is raised to the responsible human
  through the domain's declared escalation path
- AND the record of each reliance is kept, not rewritten

### Requirement: A licence verification is evidence about a licence, never identity or authority

openWallet SHALL treat a licence verification as evidence that a named verifier
found a licence in a stated status and bound it to a wallet and to named keys,
and as nothing more. A licence verification SHALL NOT be proof of who a person
is, SHALL NOT become a patient or subject identifier, and SHALL NOT confer any
authority: it carries no grant, scope, act or tier. The verification names the
licensing authority, the jurisdiction, the licence identifier and the licence
class, so that a relying domain that keeps its own record of the practitioner's
licence, holding those same four facts, can compare the two; neither replaces
the other, and what follows from a difference is the domain's to decide. A
relying domain MAY also refuse a verification whose bound wallet's held record
declares a holder class other than practitioner.

#### Scenario: a verification is never an identifier

- WHEN a relying domain resolves a person or a patient through a licence
  verification or the licence it names
- THEN the resolution is a validation failure
- AND the person is resolved by the domain's own identifier for them

#### Scenario: a verification confers no authority

- WHEN a licence verification is relied on
- THEN no grant, scope or authority is conferred by it
- AND which decisions its licence class may make is the relying domain's own
  configuration

#### Scenario: the domain's own licence record is compared, not replaced

- WHEN a relying domain keeps its own record of a practitioner's licence,
  holding the authority, jurisdiction, licence identifier and class
- THEN it can compare those four facts with the wallet's verification
- AND neither record replaces the other

### Requirement: A relying domain binds each sign-off key to its account itself

openWallet SHALL require a relying domain to bind each key that may make a
practitioner's sign-off to its account for that practitioner individually, by a
proof of possession from that key over a challenge the domain issued, made in
that account's own session. A licence verification alone SHALL NOT bind an
account or a key. The relying domain SHALL take its held record of the
practitioner's wallet only from that practitioner, in their own session, and
SHALL accept a key added to that record only with a proof of possession from
the added key made in that session; no administrator SHALL add a key to it,
and an administrator MAY suspend the domain's reliance on it. A change to the
held record's state reaches the domain from the practitioner, in their own
session, or from a verifier's revocation list. Each bound key has its own
binding: replacing a key is a new binding, and a sign-off with the new key is
supported only by a verification that names its fingerprint.

#### Scenario: each key is bound by its own proof

- WHEN a practitioner binds a second key to their account
- THEN the binding rests on a proof of possession from that key over the
  domain's challenge, made in that account's own session
- AND the first key's binding does not bind the second

#### Scenario: no administrator adds a key

- WHEN an administrator of the relying domain adds a key to the held record of
  a practitioner's wallet
- THEN the key is not added, and no binding rests on it

#### Scenario: replacing a key needs a new verification

- WHEN a practitioner replaces their sign-off key
- THEN the new key is bound by its own proof
- AND a sign-off with it is supported only once the domain holds a licence
  verification that names its fingerprint

### Requirement: A practitioner's sign-off is a proof of possession over the relying domain's statement

openWallet SHALL provide, for a practitioner's sign-off of a medical decision,
a proof of possession made under the possession-only profile ratified as
`wallet-challenge-proof`, whose challenge digest is the digest of the statement
the relying domain asks the practitioner to sign off, which carries the
domain's single-use challenge. The proof's binding SHALL name the wallet, the
key that signed, and a custody reference of the form
`openxwallet-custody:<registry_version>:<model>`, which SHALL equal the custody
the held wallet record declares for that key under the closed custody registry.
The relying domain SHALL be able to resolve that binding from a registry it
runs or holds inside its own deployment, so that checking the proof contacts no
service outside it. openWallet SHALL state what the signing key's custody
evidences under the closed custody registry: a key whose declared custody
evidences the HOLDER, which today is `isolated_per_use_authorized` alone,
evidences that the practitioner acted, and only where each use is authorized on
the device that holds the key, never by a code typed into the computer that asks
for the signature; a proof from any other key evidences only the practitioner's
environment. For a sign-off, that condition narrows the registry's own
definition, under which the authorization may also be an external policy
approval or a separate custodian. No record declares the narrower condition and
nothing checks it: until openWallet defines a record of the evidence on which a
key's custody is accepted, it is what the relying domain asks of a
practitioner's key, and no proof or declaration shows it. The proof SHALL NOT
state anything about the statement's content, the practitioner's licence or
their authority. It SHALL NOT be presented as the
practitioner's consent to the statement: what the signer was shown, their
re-authentication at signing, and which custody counts as per-use authorization
are the relying domain's to evidence and decide.

#### Scenario: the proof binds the statement

- WHEN a practitioner signs off a medical decision
- THEN the proof's challenge digest is the digest of the relying domain's
  statement for that sign-off, which carries the domain's single-use challenge
- AND a proof made over another statement or another challenge does not verify
  for this one

#### Scenario: the custody reference names the registry model

- WHEN a binding used for a sign-off names its custody
- THEN its custody reference is `openxwallet-custody:` with the registry version
  and the model the held wallet record declares for that key
- AND a custody reference that differs from that declaration is a mismatch, and
  the proof does not support a sign-off

#### Scenario: the custody says what was evidenced

- WHEN the key that made a sign-off proof declares `holder_readable` or
  `isolated_invocable`
- THEN the proof evidences that the practitioner's environment acted, and not
  that the practitioner did
- AND it is never presented as evidence that the practitioner acted

#### Scenario: possession is neither authority nor consent

- WHEN a sign-off proof verifies
- THEN possession of that key over that statement is established and nothing
  else
- AND the practitioner's licence, their authority, their consent to what they
  were shown and whether the sign-off counts are not stated by the proof

#### Scenario: the binding is resolved inside the deployment

- WHEN a relying domain checks a sign-off proof while no network outside its
  deployment is reachable
- THEN it resolves the key binding from the registry it runs or holds inside
  its deployment
- AND the check contacts no service outside it
