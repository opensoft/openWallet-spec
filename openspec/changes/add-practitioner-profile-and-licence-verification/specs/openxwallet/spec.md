# openxwallet Specification Delta

## MODIFIED Requirements

### Requirement: The capability is an authority control, never an identity substrate

openWallet SHALL keep wallets composable and optional for domains: a
wallet SHALL NOT become a prerequisite for reconstructing a record,
resolving a subject, or operating a domain, and a wallet identifier SHALL
NOT become a subject identifier. This preserves the ratified constraints in
MedxFactory's `patient-identity-and-assembly` (a wallet address is not
identity proof) and `patient-snapshot-ledger-custody` (custody stays
wallet neutral and reconstructable with no wallet available).

This rule has ONE named exception, and only one, and it is named by the act:
a consuming domain MAY make a practitioner's wallet a prerequisite for that
practitioner's sign-off of a medical decision, as
`openxwallet-practitioner-profile` states that sign-off, and for the binding
of that wallet to the practitioner's account that the sign-off needs, and for
nothing else. Every other act of the domain SHALL work with no wallet. The
domain SHALL need no wallet of its own to check a sign-off. Reconstructing a
record and resolving a subject SHALL need no wallet, a record that carries a
sign-off included, and no wallet SHALL need to be reachable to read such a
record. Which decisions are medical decisions is the consuming domain's to
define, never this capability's.

A wallet identifier MAY name an agent holder as the author of a record. It
still SHALL NOT identify a patient or a person, and nothing SHALL need the
wallet to be reachable to read the record that names it. Naming an agent
holder as a record's author includes naming it as the party on whose behalf a
relay wrote the record. This paragraph says what a wallet identifier may name;
it is not a second exception to the rule that a wallet is never a
prerequisite.

#### Scenario: a domain operating without wallets is conformant

- WHEN a domain adopts no wallets
- THEN its records remain reconstructable and its subjects resolvable
- AND no capability refuses it for the absence

#### Scenario: a wallet identifier never becomes a subject identifier

- WHEN a subject or record carries an optional wallet reference
- THEN the reference is attestation, not identity
- AND resolution treating it as the identifier is a validation failure

#### Scenario: a domain that requires a wallet only for sign-off works without one

- WHEN a consuming domain makes a practitioner's wallet a prerequisite for that
  practitioner's sign-off of a medical decision and for the binding that
  sign-off needs, and a practitioner has no wallet, or none the domain can use
- THEN every other act of the domain proceeds for that practitioner with no
  wallet
- AND the domain's records remain reconstructable and its subjects resolvable
- AND what becomes of a sign-off attempted without a wallet is the domain's to
  decide

#### Scenario: the exception admits no second act

- WHEN a consuming domain makes a wallet a prerequisite for any act other than
  a practitioner's sign-off of a medical decision and the binding of that
  practitioner's wallet to their account, such as signing in, reading a
  record, entering information, configuring the domain, or holding the keys
  the domain checks a sign-off with
- THEN that prerequisite is outside the one named exception
- AND it makes a wallet a prerequisite for operating the domain, which this
  requirement forbids

#### Scenario: a signed-off record is read with no wallet reachable

- WHEN a record carrying a practitioner's sign-off made with their wallet is
  read or reconstructed while that wallet is unreachable, suspended or revoked,
  or declares only retired keys
- THEN the record is read and reconstructed in full
- AND no wallet is contacted to read it

#### Scenario: a wallet identifier names an agent as a record's author

- WHEN a record names an agent holder as its author, or as the party on whose
  behalf a relay wrote it, by that agent's wallet identifier
- THEN the identifier names that agent holder in that role and identifies no
  patient or person
- AND resolving a patient or a person through that identifier is a validation
  failure
- AND the record is read in full with the wallet unreachable
