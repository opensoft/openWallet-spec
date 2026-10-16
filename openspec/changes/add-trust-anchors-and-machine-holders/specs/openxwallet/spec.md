# openxwallet Specification Delta

## MODIFIED Requirements

### Requirement: A wallet is a key, never a record of a key

openWallet SHALL define a neutral wallet as a signing key — or a declared SET
of signing keys — anchored to decentralized identifiers and held by a HOLDER,
where a holder is any subject class the family recognises: a person, a
practitioner, an organisation, an agent, or a machine. The wallet is identified
by the SET of keys it declares, and every key in that set is one the HOLDER
holds, so a wallet declaring several keys is still never a record of SOMEONE
ELSE'S key. The wallet record carries the holder's identifier, a reference to
each key it declares, and each declared key's own custody model; it never
carries key material, and no capability may require key material to be
disclosed to it. A record declaring one key is a set of one and is conformant
unchanged. A declared key's declaration is APPEND-ONLY: retiring a key is a
change to that key's declared state, never a deletion of its declaration,
because an act already attributed to a key must remain readable after the key
is retired. A MACHINE is a computer that holds keys in its own right — the
service credentials its operating system presents, such as the host key each of
its SSH daemons answers with or a client certificate it authenticates to a
resource with — and it declares them as every holder does, each with its own
custody model from the same closed set, which gains no member for it. A public key of ANOTHER holder that a wallet keeps in order to verify that
holder is not declared by the wallet at all: it is a trust anchor the wallet
holds, outside its declared key set.

#### Scenario: the record references, never contains

- WHEN a wallet record is validated
- THEN it carries a key reference and a declared custody model
- AND a record containing private key material is a validation failure

#### Scenario: holders are not restricted to one subject class

- WHEN a domain declares a wallet holder
- THEN the holder may be a person, practitioner, organisation, agent, or machine
- AND no requirement in this capability assumes a particular class

#### Scenario: several keys present one authority

- WHEN a wallet declares more than one key
- THEN each declared key carries its own custody model and its own fingerprint
- AND the wallet's authority is unchanged by how many keys present it
- AND a key declared by that wallet is a key its own holder holds, never a record of another holder's key

#### Scenario: a retired key stays declared

- WHEN a declared key is retired
- THEN its declaration remains in the record with its state changed
- AND deleting the declaration is refused as a way to retire a key
- AND every act already attributed to that key remains resolvable

#### Scenario: a single-key record is a set of one

- WHEN a wallet record declares only its primary key reference
- THEN the record is conformant with no additional declaration
- AND its declared key set is that one key
- AND every rule keyed on the declared set resolves to the behaviour it had before sets were expressible

#### Scenario: a machine declares its service keys as one wallet

- WHEN a computer whose two SSH daemons each answer with their own host key is
  declared as a holder
- THEN it is ONE wallet of holder class machine, whose declared key set is both
  host keys
- AND each host key carries its own custody model and its own fingerprint
- AND the two daemons are two keys presenting one holder's authority, never two
  holders

#### Scenario: a machine's service key is classified by the closed custody set

- WHEN a machine declares a service key that its operating system reads from a
  protected file, or invokes inside a hardware module with no authorization per
  use
- THEN the key's custody is the existing member those facts describe —
  `holder_readable` for the file, `isolated_invocable` for the module
- AND a signature by that key evidences the ENVIRONMENT, under the ceiling that
  member caps, exactly as the same custody would for any other holder
- AND the closed custody set gains no member for machines

#### Scenario: a machine declares a service credential that is not a host key

- WHEN a machine authenticates to a resource with a client certificate
- THEN the certificate's key is a declared key of the machine's wallet, beside
  its host keys, with its own custody model and its own fingerprint
- AND a certificate whose private key the operating system holds
  non-exportable in a hardware-backed store, and may invoke at will, is
  `isolated_invocable`, while the same certificate held as a file the
  machine's execution context can read is `holder_readable`
- AND the address of the resource the credential reaches is not a key and is
  not declared

### Requirement: Authority travels as attenuated grants, never as keys

openWallet SHALL express every authority a wallet confers as a capability
GRANT rather than as access to the key itself, because a raw key can be
neither expired nor revoked and a shared key destroys attribution. A grant
names its audience, its scope, and its expiry; derivation from a grant is
MONOTONICALLY NARROWING, so a derived grant may reduce scope or lifetime
and may never widen either. A grant's audience is a wallet of any holder
class, a MACHINE's included: authority for a computer to reach a resource is a
grant addressed to that machine's wallet, never a credential handed to whatever
runs on it. Where a grant confines its acts to a particular resource outside
this capability, it names that resource among its objects, and the resource's
own access control is the grant's REALIZATION — the enforcement that makes it
live — while the grant is the auditable, attenuable statement of what that
enforcement permits, to whom, and until when. The enforcement's configuration
is the record of whoever administers the resource and SHALL NOT become a field
of the audience's wallet, and the resource's identifier SHALL NOT become the
holder's identifier, nor the holder's identifier the resource's.

#### Scenario: a raw key is never the unit of access

- WHEN a holder authorises another party to act
- THEN a grant is issued naming audience, scope and expiry
- AND handing over the key itself is refused as unrepresentable

#### Scenario: attenuation only narrows

- WHEN a grant is derived from a parent grant
- THEN its scope and lifetime are within the parent's
- AND a derived grant exceeding its parent in either is invalid

#### Scenario: a machine wallet is the audience of a resource grant

- WHEN a tenant permits a machine to read one mailbox
- THEN a grant addressed to the machine's wallet names that mailbox among its
  objects and the read act in its scope, with an expiry
- AND the mailbox's own access control enforces the grant, and that
  enforcement is recorded by the mailbox's administrator, never in the
  machine's wallet
- AND the mailbox's identifier is not the holder's identifier, and a grant
  whose audience names the mailbox rather than a wallet is refused

#### Scenario: a custodian's reads are key-attributed exercises

- WHEN a service on the machine reads the mailbox under that grant
- THEN each exercise names as its presenting key the machine's declared
  service credential, and records that key's custody as the model in force
- AND the service credential is never handed to the processes the service
  serves
- AND an agent the service hands mail to presents nothing in that exercise and
  is not recorded as its actor

### Requirement: The capability is an authority control, never an identity substrate

openWallet SHALL keep wallets composable and optional for domains: a
wallet SHALL NOT become a prerequisite for reconstructing a record,
resolving a subject, or operating a domain, and a wallet identifier SHALL
NOT become a subject identifier. This preserves the ratified constraints in
MedxFactory's `patient-identity-and-assembly` (a wallet address is not
identity proof) and `patient-snapshot-ledger-custody` (custody stays
wallet neutral and reconstructable with no wallet available). A trust anchor
a wallet holds is a fact about which keys that wallet trusts for verification
and nothing more: the decentralized identifier an anchor names SHALL NOT
become a subject identifier, and this capability SHALL NOT make holding
anchors a prerequisite for operating a domain, any more than holding a wallet.

#### Scenario: a domain operating without wallets is conformant

- WHEN a domain adopts no wallets
- THEN its records remain reconstructable and its subjects resolvable
- AND no capability refuses it for the absence

#### Scenario: a wallet identifier never becomes a subject identifier

- WHEN a subject or record carries an optional wallet reference
- THEN the reference is attestation, not identity
- AND resolution treating it as the identifier is a validation failure

#### Scenario: an anchor is a trust fact about a key, never an identity

- WHEN a wallet holds a trust anchor naming another holder's decentralized
  identifier
- THEN the anchor records which of that holder's keys the wallet trusts for
  verification, and nothing about who that holder is
- AND resolving a subject through an anchor's identifier is a validation
  failure
- AND a domain operating with no wallets and no anchors remains conformant

## ADDED Requirements

### Requirement: Trust anchors are held, never declared

openWallet SHALL let a wallet HOLD trust anchors: records owned by that wallet,
each naming ANOTHER holder by decentralized identifier and carrying one or more
of that holder's PUBLIC keys, each with its fingerprint and its own state, so
that the owner can verify what that holder signs. An anchor SHALL state its
role: an ISSUER anchor is a root that vouches for a population it signs, and
SHALL declare the scope of names it may vouch for; a PEER anchor is one
holder's own key, and vouches for that holder only. An anchored key SHALL NOT
be a member of the owning wallet's declared key set and SHALL NOT present the
owner's authority, and an anchor SHALL confer no authority on anyone: it is an
input to verification, never a grant. Anchors are APPEND-ONLY in the way
declared keys are — an anchor or an anchored key is retired by its state,
never by deleting it — and no anchor property may hold key material.

#### Scenario: another holder's key is held as an anchor

- WHEN a wallet keeps the public key of a certificate authority whose
  certificates it verifies
- THEN the key is carried by a trust anchor owned by that wallet, naming the
  authority's decentralized identifier, the key's fingerprint and the key's
  state
- AND the anchor carries the public key and never key material

#### Scenario: an anchored key is never declared

- WHEN a trust anchor names a key that is also in its owning wallet's declared
  key set
- THEN the anchor is refused
- AND a key the wallet holds only to verify another holder never enters the
  wallet's declared key set

#### Scenario: an anchor confers no authority

- WHEN a credential verifies against a held anchor
- THEN the anchor has established only that the credential's signature is
  genuine
- AND no grant, authority tier, or act is conferred by holding the anchor or by
  its role
- AND an exercise presented by an anchored key is refused as presented by a key
  no wallet declares

#### Scenario: an issuer anchor vouches only within its scope

- WHEN an issuer anchor's key signed a credential for a subject outside the
  anchor's declared scope
- THEN that anchor does not vouch for the subject, although the signature
  verifies
- AND an issuer anchor declaring no scope is refused

#### Scenario: a peer anchor vouches for its own holder only

- WHEN an anchor's role is peer
- THEN it vouches for the key of the one holder it names and for no other
  subject
- AND a peer anchor whose scope reaches beyond that holder's own names is
  refused

#### Scenario: a rotated anchored key stays held

- WHEN an anchored key is rotated out or revoked
- THEN its entry remains with its state changed, and the replacement key is
  added beside it with its own provenance
- AND a record that relied on the retired key still resolves

### Requirement: Verification is offline against held anchors

openWallet SHALL require a holder verifying a credential or signature presented
by another party to verify it against trust anchors the holder ALREADY holds —
an issuer anchor's signature over the presented key, or a peer anchor's key —
and SHALL NOT require contacting the issuer, a directory, or an identity
provider to decide it: the issuer is consulted when it issues, never when its
credential is checked. Where an issuer anchor covers a subject, that subject's
leaf keys SHALL NOT be held as trust decisions; a cached leaf is at most a
convenience carrying a staleness bound. Revocation SHALL be checked at use,
from the credential's own validity window and the state of the anchor that
verifies it, together with a revocation list where the consumer distributes
one; a short credential lifetime is the primary revocation mechanism.

#### Scenario: verification decides without the network

- WHEN a holder verifies a host certificate presented when it connects
- THEN it checks the issuer's signature against the issuer anchor it already
  holds
- AND no issuer, directory, or identity provider is contacted to decide it
- AND the decision is the same with the network unavailable

#### Scenario: the issuer is consulted at issuance only

- WHEN a holder obtains a credential and later presents it
- THEN the issuer was contacted to issue it
- AND the verifier does not contact the issuer to check it

#### Scenario: roots are held, not leaves

- WHEN a holder holds an issuer anchor whose scope covers a subject
- THEN the subject's leaf key is not held as a trust decision
- AND a cached leaf for a covered subject carries a staleness bound, and one
  without it is refused

#### Scenario: revocation is checked at use

- WHEN a credential is presented after its validity window has closed, or after
  the anchor that would verify it was suspended or revoked
- THEN verification fails
- AND the credential's validity at issuance is not accepted as evidence of its
  validity now

### Requirement: A verifier is blind to holder class

openWallet SHALL require a resource deciding access to decide it from these
inputs: that the presented credential verifies against a trust anchor the
resource holds; that the credential's principal or scope maps to a local
account or role; that account's or role's own local privilege; and every hard
limit the credential carries, such as a source restriction, a forced command,
or a prohibition on forwarding, each of which the resource SHALL enforce. The
resource SHALL NOT consult the presenting holder's class. Whether a person or
an agent may OBTAIN a credential is issuance policy, decided where the
credential is issued, so a rule that an issuer grants no agent a credential is
enforced by that issuer and never by the resource.

#### Scenario: an identical credential is treated identically

- WHEN a person and an agent each present a credential with the same principal,
  scope and limits, verified against the same anchor
- THEN the resource grants both the same access
- AND nothing in the decision depends on which class presented

#### Scenario: holder-class policy lives at issuance

- WHEN a deployment rules that agents may not obtain credentials from an issuer
- THEN the issuer refuses to issue one to an agent
- AND the resource carries no holder-class rule of its own
- AND a trust anchor's scope cannot name a holder class

#### Scenario: the credential's hard limits bind

- WHEN a verified credential carries a source restriction, a forced command, or
  a prohibition on forwarding
- THEN the resource enforces each limit
- AND access a limit excludes is refused although the credential verifies

#### Scenario: a principal reaches only its local privilege

- WHEN a verified credential names a principal
- THEN the resource maps it to a local account or role
- AND the privilege applied is that account's or role's own, never one the
  credential asserts beyond the mapping
- AND a principal mapped to no local account or role opens nothing

### Requirement: An unknown holder is validated before it is trusted

openWallet SHALL require a holder to validate a key covered by no anchor it
holds BEFORE trusting it, and SHALL record how each anchored key was verified,
from a closed set: an out-of-band fingerprint comparison through a channel the
holder already trusts; resolution of the subject's decentralized identifier
document through the web PKI; attestation by an anchor the holder already
holds; or first use. A holder's first anchor SHALL arrive through a channel the
holder already trusts, with that provenance recorded. For an issuer anchor, the
issuer's self-published record of its own keys SHALL be confirmation and never
the sole evidence, and neither SHALL first use. A holder MAY accept a key on
first use only as an explicitly labelled state carrying a revalidation
deadline, and MAY refuse first use entirely by policy. Trust on first use SHALL
stay distinguishable from verified provenance for as long as the record
exists: it is never rewritten as verified, and an attestation by an anchor
that rests on first use alone establishes nothing.

#### Scenario: the first anchor arrives through a trusted channel

- WHEN a holder takes its first anchor for an issuer
- THEN the anchored key's fingerprint was compared through a channel the holder
  already trusts, such as a fingerprint carried by hand, held in a password
  manager, or committed to a repository the holder trusts
- AND the anchor records that method, when the comparison was made, and its
  source

#### Scenario: self-publication confirms an issuer and never establishes it

- WHEN an issuer anchor's key rests only on the issuer's own published record
  of its keys, or only on first use
- THEN the anchor is refused
- AND the same published record beside an out-of-band comparison or an
  attestation is admitted as confirmation

#### Scenario: an uncovered key is validated before trust

- WHEN a holder meets a key covered by no anchor it holds
- THEN it validates the key, by resolving its holder's decentralized identifier
  document or by attestation from an anchor it holds, before trusting it
- AND a key it has not validated is not trusted for the act it was presented
  for
- AND an attestation naming an anchor the holder does not hold is refused

#### Scenario: first use is labelled and bounded

- WHEN a holder accepts a key on first use
- THEN the anchored key records first use as its provenance and carries a
  revalidation deadline
- AND a first-use record without a revalidation deadline is refused
- AND a holder whose policy refuses first use holds no first-use anchor

#### Scenario: first use is never laundered into verified

- WHEN a key accepted on first use is later verified
- THEN the verification is recorded beside the first-use record and does not
  replace it
- AND an attestation by an anchor that rests on first use alone is refused as
  evidence
