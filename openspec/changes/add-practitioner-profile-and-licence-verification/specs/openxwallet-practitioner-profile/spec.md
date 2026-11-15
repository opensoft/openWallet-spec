# openxwallet-practitioner-profile Specification Delta

## ADDED Requirements

### Requirement: A practitioner holder carries licence verifications

openWallet SHALL let a wallet holder of class PRACTITIONER carry licence
verifications, and SHALL let no holder of another class carry one. A licence
verification is a record, signed by a verifier, stating that the verifier
checked one licence against its source and found it in a stated status. It
SHALL state: the wallet it is bound to; the licensing authority and the
jurisdiction that authority licenses in; the licence, by the authority's own
identifier for it; the licence class or profession, in the authority's own
designation; the status found; when the licence was checked, and against which
source; which verifier issued the verification, and when; and the time until
which it may be relied on. One verification covers one licence, so a holder
with several licences carries one verification for each. A verification states
no clinical scope: which decisions a licence class may make is the relying
domain's to decide.

#### Scenario: a verification names what was checked

- WHEN a licence verification is validated
- THEN it names its wallet, the licensing authority and its jurisdiction, the
  licence identifier, the licence class, the status found, the source, when the
  licence was checked, the verifier, when it was issued, and its reliance bound
- AND a verification missing any of them is a validation failure

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

### Requirement: A licence verification is issued by a named verifier over a proof of possession

openWallet SHALL require every licence verification to name its verifier and to
carry the verifier's signature over a canonical form of every other field it
holds, made under a signing domain distinct from every other signing domain in
this family, so that no proof of possession, grant or other signed record can
be read as a licence verification, nor a licence verification as one of them. A
verifier is a holder with a wallet of its own, and the key it signs with is a
key that wallet declares. Before it issues a verification, the verifier SHALL
have obtained a proof of possession from a key that the bound wallet declares,
over a challenge the verifier issued for that purpose, and the verification
SHALL record that proof's challenge digest and when it was made. A verification
that supersedes an earlier one SHALL name it. How the verifier satisfied itself
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

#### Scenario: the bound wallet proved possession to the verifier

- WHEN a verifier issues a licence verification bound to a wallet
- THEN the verification records the challenge digest of the proof of possession
  the verifier obtained from a key that wallet declares, and when it was made
- AND a verification recording no such proof is a validation failure

### Requirement: A licence verification is checked inside the relying domain with no outside call

openWallet SHALL let a relying domain decide whether to rely on a licence
verification from what it already holds: the verification, as the wallet's
holder presented it; the verifier's public key, obtained ahead of time and kept
with how it was obtained; the latest revocation list that verifier published
and the domain has fetched; and its own clock. Deciding SHALL NOT need the
verifier, the licensing authority, a directory, the wallet or its holder's
device to be contacted, and a domain SHALL NOT learn a verifier's key from the
verification it is checking. A relying domain SHALL refuse to rely on a
verification that: is past its reliance bound; is superseded by a later
verification it holds of the same licence, for the same wallet, from the same
verifier; is revoked in the revocation list it holds; is bound to a wallet
other than the one in use; is signed by a verifier whose key the domain does
not hold, or holds as suspended or revoked; or whose signature does not verify.
A domain whose copy of a verifier's revocation list is older than the
staleness bound the domain declares SHALL treat that verifier's verifications
as not checkable, and SHALL NOT rely on them as current. A domain MAY require
that the verifier is a holder other than itself, and a verification names its
verifier so that it can.

#### Scenario: the decision is the same with the network unavailable

- WHEN a relying domain checks a licence verification while no network outside
  its deployment is reachable
- THEN it decides from the verification, the verifier key it holds, the
  revocation list it holds and its own clock
- AND no verifier, licensing authority, directory or wallet is contacted to
  decide it

#### Scenario: a verification past its reliance bound is not relied on

- WHEN a licence verification is checked after its reliance bound
- THEN the domain does not rely on it
- AND its validity when issued is not accepted as evidence of its validity now

#### Scenario: a verification bound to another wallet is refused

- WHEN a licence verification bound to one wallet is presented with a proof
  from a key of another wallet
- THEN the domain does not rely on it

#### Scenario: a verifier the domain does not hold is refused

- WHEN a licence verification is signed by a verifier whose key the relying
  domain does not hold
- THEN the domain does not rely on it
- AND the key is not taken from the verification itself

#### Scenario: a stale revocation list makes a verification not checkable

- WHEN the relying domain's copy of a verifier's revocation list is older than
  the staleness bound the domain declares
- THEN that verifier's verifications are not checkable
- AND none of them is relied on as current until a newer list is fetched

### Requirement: A licence verification ends by its reliance bound, by supersession or by revocation, checked at reliance

openWallet SHALL make a licence verification stop being relied on: at its
reliance bound, with no grace period; when a later verification of the same
licence, for the same wallet, from the same verifier supersedes it; when its
verifier revokes it; when the bound wallet is revoked, and for as long as it
is suspended; and, from then on, when the relying domain no longer holds the
verifier's key as active. A verifier
SHALL revoke a verification it learns no longer holds, because the licence's
status changed, because it was issued in error, or because the binding to the
wallet no longer holds, and SHALL publish the revocation in a signed revocation
list that names a reason class for each entry. A revoked verification SHALL
NEVER return to force: re-verification is a new verification that names the
one it supersedes. As every revocation in this family is, revocation SHALL be
checked at the moment of reliance, never trusted from issuance. Retiring one
declared key of the bound wallet SHALL NOT end a verification, which is bound
to the wallet and not to a key. A revocation SHALL NOT rewrite a reliance made
while the verification was in force, but a relying domain that receives a
revocation whose reason class says the verification was never true SHALL raise
every reliance it affects to the responsible human through its declared
escalation path.

#### Scenario: no grace period after the reliance bound

- WHEN a licence verification's reliance bound passes
- THEN it is not relied on from that moment
- AND no tolerance or grace period extends it

#### Scenario: an authority's suspension between verifications

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

#### Scenario: retiring one key does not end a verification

- WHEN one declared key of the bound wallet is retired
- THEN the wallet's licence verifications are unchanged
- AND a proof from the retired key is refused under the core's revocation rule

#### Scenario: a verification that was never true reaches a human

- WHEN a relying domain receives a revocation whose reason class says the
  verification was issued in error
- THEN every reliance on that verification is raised to the responsible human
  through the domain's declared escalation path
- AND the record of each reliance is kept, not rewritten

### Requirement: A licence verification is evidence about a licence, never identity or authority

openWallet SHALL treat a licence verification as evidence that a named verifier
found a licence in a stated status and bound it to a wallet, and as nothing
more. A licence verification SHALL NOT be proof of who a person is, SHALL NOT
become a patient or subject identifier, and SHALL NOT confer any authority: it
carries no grant, scope, act or tier. A relying domain SHALL bind its own
account for the practitioner to the wallet itself, by a proof of possession
from a key that wallet declares, over a challenge the domain issued, made in
that account's own session; a verification alone SHALL NOT bind an account. The
verification names the licence so that a relying domain that keeps its own
record of the practitioner's licence can compare the two; neither replaces the
other, and what follows from a difference is the domain's to decide.

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

#### Scenario: the relying domain binds its own account

- WHEN a relying domain binds one of its accounts to a practitioner's wallet
- THEN the binding rests on a proof of possession from a key that wallet
  declares, over a challenge the domain issued, made in that account's own
  session
- AND presenting a licence verification alone binds no account

#### Scenario: the domain's own licence record is compared, not replaced

- WHEN a relying domain keeps its own record of a practitioner's licence
- THEN it can compare the authority, jurisdiction and licence identifier in the
  wallet's verification with that record
- AND neither record replaces the other

### Requirement: A practitioner's sign-off is a proof of possession over the relying domain's statement

openWallet SHALL provide, for a practitioner's sign-off of a medical decision,
a proof of possession made under the possession-only profile ratified as
`wallet-challenge-proof`, whose challenge digest is the digest of the statement
the relying domain asks the practitioner to sign off, which carries the
domain's single-use challenge, and whose binding names the wallet, the key that
signed and the custody that key declares. The relying domain SHALL be able to
resolve that binding from a registry it runs or holds inside its own
deployment, so that checking the proof contacts no service outside it. openWallet
SHALL state what the signing key's custody evidences under the closed custody
registry: a key whose declared custody evidences the HOLDER, which today is
`isolated_per_use_authorized` alone, evidences that the practitioner acted, and
a proof from any other key evidences only their environment. The proof SHALL
NOT state anything about the statement's content, the practitioner's licence or
their authority, and verified possession keeps the limited meaning that profile
gives it. Which custody a sign-off needs is the relying domain's decision.

#### Scenario: the proof binds the statement

- WHEN a practitioner signs off a medical decision
- THEN the proof's challenge digest is the digest of the relying domain's
  statement for that sign-off, which carries the domain's single-use challenge
- AND a proof made over another statement or another challenge does not verify
  for this one

#### Scenario: the custody says what was evidenced

- WHEN the key that made a sign-off proof declares `holder_readable` or
  `isolated_invocable`
- THEN the proof evidences that the practitioner's environment acted, and not
  that the practitioner did
- AND it is never presented as evidence that the practitioner acted

#### Scenario: possession is not authority

- WHEN a sign-off proof verifies
- THEN possession of that key over that statement is established and nothing
  else
- AND the practitioner's licence, their authority and whether the sign-off
  counts are not stated by the proof

#### Scenario: the binding is resolved inside the deployment

- WHEN a relying domain checks a sign-off proof while no network outside its
  deployment is reachable
- THEN it resolves the key binding from the registry it runs or holds inside
  its deployment
- AND the check contacts no service outside it
