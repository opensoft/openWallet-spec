## ADDED Requirements

### Requirement: A passkey or security key proves possession over a challenge derived from the proof's binding

openWallet SHALL verify a proof under the profile `openwallet.webauthn-proof.v0`
only as a Web Authentication assertion: the authenticator's signature, under the
public key of the trusted binding, over the authenticator data followed by the
SHA-256 of the client data, as Web Authentication Level 3 defines it. The
assertion's challenge SHALL be the SHA-256 of the domain separator
`openWallet.webauthn-proof.v0` and a NUL byte, followed by the RFC 8785
canonical UTF-8 bytes of the proof's unsigned binding fields: `profile`, `alg`,
`challenge_digest`, `binding_ref`, `wallet_ref`, `key_ref`, `subject_ref`,
`custody_ref`, `binding_revision` and `credential_id`. The verifier SHALL
recompute that challenge from the proof and SHALL compare the client data's
challenge with its base64url encoding. It SHALL compare the expected challenge
digest, the five binding references, the binding revision and the credential
identifier with the trusted binding before it returns verified facts, so that a
proof under this profile binds what the ratified `wallet-challenge-proof` binds
and, in addition, the relying party by its relying-party identifier and origin.
A proof SHALL be a closed JSON object of at most 8192 bytes, with no repeated key
and no constant, carrying those fields and the authenticator data, the client
data and the signature, each in unpadded base64url, the client data exactly as
the client produced the bytes it hashed.

#### Scenario: a changed binding field breaks the challenge

- WHEN any of the proof's unsigned binding fields is changed after the
  authenticator signed
- THEN the recomputed challenge no longer equals the client data's challenge
- AND verification refuses

#### Scenario: a proof over another statement does not verify

- WHEN a proof's challenge digest differs from the digest the relying party
  expects
- THEN verification refuses, as it does under the ratified profile

#### Scenario: a proof whose references differ from the binding's

- WHEN a proof names a binding reference, a revision or a credential identifier
  other than the trusted binding's
- THEN verification refuses

### Requirement: Every use is checked for its type, challenge, origin, relying party, presence and verification

openWallet SHALL refuse a proof under this profile unless every one of these
holds: the client data parses as JSON from UTF-8; its `type` is `webauthn.get`;
its `challenge` is the base64url encoding of the challenge the first requirement
derives; its `origin` exactly equals one of the origins the trusted binding
allows; `crossOrigin` is absent or false and `topOrigin` is absent; the
authenticator data's relying-party identifier hash is the SHA-256 of the
binding's relying-party identifier; the user present and user verified flags
are both set; the attested credential data flag is not set; the backup
eligibility flag equals the value recorded at registration, and the backup
state flag is not set unless backup eligibility is; and the signature verifies
under the binding's public key and algorithm. Members of the client data other
than those named SHALL be tolerated and SHALL NOT be read, and extension outputs
in the authenticator data SHALL be ignored. The signature counter SHALL be
compared with the value the binding last recorded: where either is non-zero and
the new value is not greater, the proof SHALL still verify and SHALL carry a
flag that the counter did not increase, for the relying party to raise.

#### Scenario: user verification is required on every use

- WHEN an assertion's authenticator data has the user present flag set and the
  user verified flag clear
- THEN verification refuses

#### Scenario: an origin the binding does not allow

- WHEN the client data's origin is not exactly one of the binding's allowed
  origins
- THEN verification refuses, even where the relying-party identifier hash
  matches

#### Scenario: an assertion made for another relying party

- WHEN the authenticator data's relying-party identifier hash is not the SHA-256
  of the binding's relying-party identifier
- THEN verification refuses

#### Scenario: a registration response is not a proof

- WHEN the client data's type is `webauthn.create`
- THEN verification refuses

#### Scenario: a counter that does not increase is raised, not refused

- WHEN a proof's signature counter is non-zero and not greater than the value
  the binding last recorded
- THEN the proof verifies and carries a flag that the counter did not increase

#### Scenario: an unknown client data member is ignored

- WHEN the client data carries a member other than those this profile names
- THEN verification neither refuses for it nor reads it

### Requirement: The profile admits ES256 and EdDSA with Ed25519 only

openWallet SHALL admit under this profile only the COSE algorithm `-7` (ES256),
with a P-256 public key in uncompressed form whose point is on the curve and a
signature in strict ASN.1 DER, and the COSE algorithm `-8` (EdDSA), with an
Ed25519 public key and a 64-byte signature; it SHALL treat `-9` as `-7` and `-19`
as `-8`, as Web Authentication Level 3 does, and SHALL refuse every other
algorithm. A binding's algorithm is fixed at registration, and a proof whose
`alg` differs from it SHALL be refused. A P-256 key SHALL be declared in its
wallet with signature algorithm `ecdsa-p256` and an Ed25519 key with `ed25519`,
and the fingerprint of a P-256 key SHALL be `sha256:` and the lowercase hex
SHA-256 of its 33-byte compressed point. Because an ECDSA signature can be
altered into another valid one, nothing in this profile SHALL rely on a
signature being unique; replay is refused by the relying party's single-use
challenge.

#### Scenario: an RSA credential is not admitted

- WHEN a credential registers with algorithm `-257` (RS256)
- THEN it is not bound under this profile

#### Scenario: a proof naming another algorithm than its binding

- WHEN a proof's `alg` differs from the algorithm its binding recorded
- THEN verification refuses

#### Scenario: a point off the curve

- WHEN a P-256 public key's point is not on the curve
- THEN the credential is not bound, and no proof verifies under it

### Requirement: A relying domain binds a credential from a registration and a proof made in the holder's own session

openWallet SHALL let a relying domain bind a Web Authentication credential to a
key of a holder's wallet only from a registration ceremony made in that holder's
own session, followed in that session by a proof under this profile over a
challenge the domain issued, because a registration without self attestation
proves no possession of the private key. The binding SHALL record: the
relying-party identifier the credential is scoped to; the origins it allows; the
credential identifier; the public key, in the form the third requirement states,
and its algorithm; the backup eligibility and backup state the registration
reported; whether user verification was performed at registration; the
signature counter; and the attestation format, the authenticator's model
identifier where one was given, and the result of the domain's attestation
policy, including that none was given. The wallet record SHALL declare the key
with its reference, its fingerprint, its signature algorithm and its custody. A
credential identifier already bound SHALL NOT be bound again. A credential works
only for the relying-party identifier it is scoped to, so a binding at one
deployment never supports a proof at another.

#### Scenario: a registration alone binds nothing

- WHEN a credential is registered and no proof under this profile follows in the
  same session
- THEN no binding is made

#### Scenario: a credential identifier is bound once

- WHEN a registration presents a credential identifier the domain has already
  bound
- THEN the registration binds nothing

#### Scenario: a credential bound at one deployment

- WHEN a proof from a credential bound at one deployment is presented at
  another, whose relying-party identifier differs
- THEN verification refuses

### Requirement: A party other than the credential's relying party observes the proof itself

openWallet SHALL let a party other than the relying party a credential is scoped
to, such as a licence verifier, obtain a proof of possession from that
credential only from the holder's own client, under the credential's
relying-party identifier, at an origin that party controls, which the relying
party lists for that purpose as a related origin as Web Authentication Level 3
defines one. That party's binding SHALL allow its own origin only, SHALL record
the relying-party identifier and the credential identifier, and SHALL take the
public key from the key the holder's wallet record declares, so that a proof
from any other credential does not verify under it. A relying party SHALL NOT
allow, for its own purposes, an origin it listed for another party. A proof that
reaches that party only through the relying party SHALL be recorded as relayed,
and SHALL NOT be presented as observed by that party.

#### Scenario: the verifier's page obtains the proof itself

- WHEN a verifier's page, at an origin the relying party lists as related, asks
  the holder's client for a proof under the relying party's identifier
- THEN the proof's client data names the verifier's origin, and the verifier
  verifies it under the public key the holder's wallet record declares

#### Scenario: a verifier-origin proof is never a sign-off

- WHEN a proof whose client data names an origin the relying party listed for a
  verifier is presented to the relying party
- THEN the relying party's verification refuses it, because that origin is not
  among the origins its own binding allows

#### Scenario: a relayed proof is recorded as relayed

- WHEN a proof reaches a verifier only through the relying party
- THEN the verifier records it as relayed, never as observed by itself

### Requirement: The profile tells a synced passkey from a device-bound key, and says what it cannot tell

openWallet SHALL record, for every bound credential, its backup eligibility as
the registration reported it, which Web Authentication fixes for the life of the
credential, and on every use its backup state. A credential whose backup
eligibility is set is a multi-device credential, such as a passkey that syncs
through the holder's platform account; one whose backup eligibility is clear is
a single-device credential, such as a security key or a passkey bound to one
device. Every verified proof SHALL carry both flags as the authenticator signed
them. The profile SHALL NOT be read as telling: which device signed with a
multi-device credential; whether a single-device credential is a roaming
security key or a platform key, beyond what attestation shows; whether an
authenticator reports backup eligibility truthfully, beyond what the relying
domain's attestation policy trusts; or who else can use the account a
multi-device credential syncs through. Whether a device is enrolled is the
relying domain's to evidence, and this profile does not evidence it.

#### Scenario: backup eligibility does not change

- WHEN a proof's backup eligibility flag differs from the value recorded at
  registration
- THEN verification refuses

#### Scenario: a synced passkey is told apart

- WHEN a proof from a credential registered with backup eligibility set
  verifies
- THEN it carries backup eligibility set and its current backup state, and the
  relying domain decides what follows

#### Scenario: no device is claimed

- WHEN a proof from a multi-device credential verifies
- THEN nothing in it is read as naming the device that signed

### Requirement: A credential's custody is declared with its backup eligibility beside it

openWallet SHALL require every key bound under this profile to declare a custody
model of the closed custody registry, and SHALL record the credential's backup
eligibility beside that declaration, so that no reading of the custody can omit
it. A single-device credential whose authenticator keeps its private key and
verifies its user on every use MAY declare `isolated_per_use_authorized`. This
profile SHALL NOT change the registry, and SHALL NOT state that a multi-device
credential's signature evidences that its holder acted on the strength of its
declared custody alone.

#### Scenario: a security key declares per-use authorized custody

- WHEN a security key registers a single-device credential and verifies its user
  on every use
- THEN its key may be declared `isolated_per_use_authorized`

#### Scenario: a synced passkey's custody is read with its backup eligibility

- WHEN a relying domain reads the custody a multi-device credential declares
- THEN it reads the recorded backup eligibility with it

### Requirement: Possession bound to a relying party, and no more

openWallet SHALL treat a verified proof under this profile as evidence that the
bound credential's authenticator, reporting the user present and verified,
signed that challenge for that relying party at that origin, and as nothing
more. It SHALL NOT be presented as evidence that the holder saw what the
challenge digest is a digest of, since no authenticator shows the statement; as
the holder's consent; or as authority. It changes nothing in the ratified
`wallet-challenge-proof`.

#### Scenario: the profile cannot see what the holder was shown

- WHEN a relying party's page shows the holder one statement and asks the
  authenticator to sign the challenge for another
- THEN the proof verifies for the statement whose digest it binds
- AND nothing in the proof shows that the holder saw that statement

#### Scenario: the ratified profile is unchanged

- WHEN a proof under the ratified `wallet-challenge-proof` is verified
- THEN it is verified exactly as that profile states, and nothing in this
  profile applies to it
