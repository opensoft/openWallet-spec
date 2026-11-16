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
openWallet SHALL accept binding data only from a trusted server registry, and
the binding SHALL be current, unrevoked and time valid. The proof SHALL NOT
supply the public key, the relying-party identifier or the allowed origins,
which come only from the binding. Whoever issues the challenge SHALL put in the
statement behind `challenge_digest` a single-use challenge reference of 32 bytes
drawn at random by its own server, in an environment it trusts, SHALL refuse a
second use of it, and SHALL ask the client for exactly the one credential the
proof will name. A proof SHALL be a closed JSON object of at most 8192 bytes,
with no repeated key and no constant, carrying those fields, with `alg` a JSON
integer, and the authenticator data, the client data and the signature, each in
unpadded base64url, the client data exactly as the client produced the bytes it
hashed.

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

#### Scenario: a revoked binding

- WHEN a proof's signature verifies under a binding the registry holds as
  revoked
- THEN verification refuses

#### Scenario: an expired binding

- WHEN a proof is verified after the validity of its binding has ended
- THEN verification refuses

#### Scenario: the proof cannot supply its own key

- WHEN a proof carries a public key, a relying-party identifier or an origin as a
  member of its own
- THEN it is refused, because the proof is a closed object
- AND nothing in a proof ever stands in for what the binding holds

### Requirement: Every use is checked for its type, challenge, origin, relying party, presence and verification

openWallet SHALL refuse a proof under this profile unless every one of these
holds: the client data parses as JSON from UTF-8, with no repeated member; its
`type` is `webauthn.get`; its `challenge` is the base64url encoding of the
challenge the first requirement derives; its `origin` exactly equals one of the
origins the trusted binding allows; `crossOrigin` is absent or false and
`topOrigin` is absent; the authenticator data's relying-party identifier hash is
the SHA-256 of the binding's relying-party identifier; the user present and user
verified flags are both set; the attested credential data flag is not set; the
backup eligibility flag equals the value recorded at registration, and the
backup state flag is not set unless backup eligibility is; and the signature
verifies under the binding's public key and algorithm. Members of the client
data other than those named SHALL be tolerated and SHALL NOT be read, and
extension outputs in the authenticator data SHALL be ignored. The registry SHALL
keep the credential's signature counter and current backup state beside the
binding, not in its revisioned record, so that updating them after a proof never
revises the binding. The signature counter SHALL be compared once, when the
proof is first verified, with the value kept beside the binding: where either is
non-zero and the new value is not greater, the proof SHALL still verify and
SHALL carry a flag that the counter did not increase, for the relying party to
raise. That flag SHALL be recorded with the proof, and a later verification of
the same proof SHALL report the recorded flag and SHALL NOT compare the counter
again. A verified proof SHALL carry the four flags as `user_present`,
`user_verified`, `backup_eligible` and `backup_state`, and the counter flag as
`sign_count_not_increasing`; a refusal SHALL carry its reason and whether the
signature verified under the binding's public key.

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

#### Scenario: a refusal says whether the signature verified

- WHEN a proof whose signature verifies under the binding's public key is refused
  because its client data names an origin the binding does not allow
- THEN the refusal reports that the signature verified, beside its reason

#### Scenario: client data with a repeated member

- WHEN the client data carries the same member twice, such as two `origin`
  members
- THEN verification refuses

#### Scenario: a counter that does not increase is raised, not refused

- WHEN a proof's signature counter is non-zero and not greater than the value
  kept beside the binding at the proof's first verification
- THEN the proof verifies and carries a flag that the counter did not increase

#### Scenario: a counter update does not revise the binding

- WHEN the registry records a proof's signature counter and backup state after
  the proof verifies
- THEN the binding's revision is unchanged
- AND a proof made under that binding before the update still verifies

#### Scenario: a later verification does not compare the counter again

- WHEN a proof that verified is verified again later, after the counter kept
  beside the binding has moved on
- THEN the later verification reports the flag recorded at the first, and raises
  no new one

#### Scenario: an unknown client data member is ignored

- WHEN the client data carries a member other than those this profile names
- THEN verification neither refuses for it nor reads it

### Requirement: The profile admits ES256 and EdDSA with Ed25519 only

openWallet SHALL admit under this profile only the COSE algorithm `-7` (ES256),
with a P-256 public key whose point is on the curve and a signature in strict
ASN.1 DER, and the COSE algorithm `-8` (EdDSA), with an Ed25519 public key and a
64-byte canonical signature whose S is less than the group order, and SHALL
refuse every other algorithm. A relying domain SHALL offer only `-8` and `-7` at
registration, and a credential that reports `-9` or `-19` SHALL be recorded under
`-7` or `-8` respectively, since Web Authentication Level 3 treats them as the
same. A binding's algorithm is fixed at registration; a proof's `alg` SHALL be
that recorded identifier, as a JSON integer, and a proof whose `alg` differs from
it, `-9` and `-19` included, SHALL be refused. A binding and a wallet record
SHALL hold a public key in its raw form: a P-256 key as the 33-byte compressed
point of the uncompressed key the registration returned, and an Ed25519 key as
its 32 bytes. A P-256 key SHALL be declared in its wallet with signature
algorithm `ecdsa-p256` and an Ed25519 key with `ed25519`, and the fingerprint of
a P-256 key SHALL be `sha256:` and the lowercase hex SHA-256 of its 33-byte
compressed point. Because an ECDSA signature can be altered into another valid
one, nothing in this profile SHALL rely on a signature being unique; replay is
refused by the relying party's single-use challenge.

#### Scenario: an RSA credential is not admitted

- WHEN a credential registers with algorithm `-257` (RS256)
- THEN it is not bound under this profile

#### Scenario: a proof naming another algorithm than its binding

- WHEN a proof's `alg` differs from the algorithm its binding recorded
- THEN verification refuses

#### Scenario: a fully specified identifier in a proof

- WHEN a proof names `alg` `-9` under a binding that recorded `-7`
- THEN verification refuses

#### Scenario: a point off the curve

- WHEN a P-256 public key's point is not on the curve
- THEN the credential is not bound, and no proof verifies under it

#### Scenario: a non-canonical Ed25519 signature

- WHEN an Ed25519 signature's S is not less than the group order
- THEN verification refuses

### Requirement: A relying domain binds a credential from a registration and a proof made in the holder's own session

openWallet SHALL let a relying domain bind a Web Authentication credential to a
key of a holder's wallet only from a registration ceremony made in that holder's
own session, followed in that session by a proof under this profile over a
challenge the domain issued, because a registration without self attestation
proves no possession of the private key. The binding SHALL record: the
relying-party identifier the credential is scoped to; the origins it allows; the
credential identifier; the public key, in its raw form, and its algorithm; the
backup eligibility and backup state the registration reported; whether user
verification was performed at registration; the attestation format, the
authenticator's model identifier where one was given, and the result of the
domain's attestation policy, including that none was given; and the basis of the
key's declared custody. The signature counter and the current backup state SHALL
be kept beside the binding, as the second requirement states. The wallet record
SHALL declare the key with its reference, its fingerprint, its signature
algorithm and its custody. A credential identifier already bound SHALL NOT be
bound again. A credential works only for the relying-party identifier it is
scoped to, so a binding at one deployment never supports a proof at another; a
holder MAY bind more than one credential at one deployment, each with its own
binding.

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

### Requirement: A party other than the credential's relying party accepts a proof only in a session in which it identified the holder itself

openWallet SHALL let a party other than the relying party a credential is scoped
to, such as a licence verifier, accept a proof of possession from that
credential only within a session in which that party identified the holder by
its own means, independently of the relying party, and only from the holder's
own client in that session: at an origin that party controls, which the relying
party lists for that purpose as a related origin as Web Authentication Level 3
defines one, or through a native client of that party's, under the credential's
relying-party identifier. Such a proof shows only that a client holding a
credential scoped to the relying party signed at that party's page, and the
relying party can register a credential of its own, so a proof that reached that
party through the relying party, or outside such a session, SHALL NOT be
accepted. That party's binding has no registration behind it. It SHALL be made
for that session only, SHALL allow that party's own origin only, SHALL record the
relying-party identifier, the credential identifier as the holder presents it,
and the backup eligibility and backup state the proof carries, and SHALL take the
public key and algorithm from the key the holder's wallet record declares, so
that a proof from any other credential does not verify under it. Every check of
the second requirement SHALL apply to it, except that backup eligibility is
recorded from the proof rather than compared with a registration, and no
signature counter is compared. A relying party SHALL NOT allow, for its own
purposes, an origin it listed for another party.

#### Scenario: the verifier's page obtains the proof itself, in its identified session

- WHEN a verifier has identified the holder by its own means, and its page, at
  an origin the relying party lists as related, asks the holder's client in that
  session for a proof under the relying party's identifier
- THEN the proof's client data names the verifier's origin, and the verifier
  verifies it under the public key the holder's wallet record declares

#### Scenario: a proof outside the identified session is not accepted

- WHEN a proof reaches the verifier at its own origin, but not within a session
  in which the verifier identified the holder by its own means
- THEN the verifier does not accept it

#### Scenario: a relayed proof is not accepted

- WHEN a proof reaches a verifier only through the relying party
- THEN the verifier does not accept it, and no verification names a key on it

#### Scenario: a verifier-origin proof is never a sign-off

- WHEN a proof whose client data names an origin the relying party listed for a
  verifier is presented to the relying party
- THEN the relying party's verification refuses it, because that origin is not
  among the origins its own binding allows

### Requirement: The profile tells a synced passkey from a device-bound key, and says what it cannot tell

openWallet SHALL record, for every credential a relying domain registers, its
backup eligibility as the registration reported it, which Web Authentication
fixes for the life of the credential, and on every use its backup state. A
credential whose backup eligibility is set is a multi-device credential, such as
a passkey that syncs through the holder's platform account; one whose backup
eligibility is clear is a single-device credential, such as a security key or a
passkey bound to one device. Every verified proof SHALL carry both flags as the
authenticator signed them. The profile SHALL NOT be read as telling: which device
signed with a multi-device credential; whether a single-device credential is a
roaming security key or a platform key, beyond what attestation shows; whether an
authenticator reports backup eligibility truthfully, beyond what the relying
domain's attestation policy trusts; or which account a multi-device credential
syncs through, and who else controls or can recover that account. Where a
multi-device credential is bound, the binding SHALL record the holder's
declaration, made at registration, that the account it syncs through is the
holder's alone and is not administered by the relying domain's operator, and
SHALL NOT present that declaration as more than the holder's word. Whether a
device is enrolled is the relying domain's to evidence, and this profile does
not evidence it.

#### Scenario: backup eligibility does not change

- WHEN a proof's backup eligibility flag differs from the value recorded at
  registration
- THEN verification refuses

#### Scenario: a synced passkey is told apart

- WHEN a registration reports backup eligibility set
- THEN the relying domain knows the credential is a multi-device credential, and
  binds it only as the seventh requirement allows

#### Scenario: no device or account is claimed

- WHEN a relying domain reads the flags a multi-device credential carries
- THEN nothing in them is read as naming the device that signed, or as showing
  that only the holder controls or can recover the account it syncs through

### Requirement: A credential's custody is declared with its backup eligibility and its basis beside it

openWallet SHALL require every key bound under this profile to declare a custody
model of the closed custody registry, and SHALL record beside that declaration
the credential's backup eligibility and the basis of the declaration, from a
closed set of two, recorded as `custody_basis`: `attested`, where the relying
domain's attestation policy
accepted attestation evidence that the authenticator keeps the key isolated and
verifies its user, or `declared`, where it rests on the holder's word; so that no
reading of the custody can omit either. A single-device credential whose
authenticator keeps its private key and verifies its user on every use MAY
declare `isolated_per_use_authorized`. No model of the registry, version 1,
describes a multi-device credential, so a multi-device credential SHALL NOT be
bound under this profile until the registry holds a model that does. This
profile SHALL NOT change the registry.

#### Scenario: a security key declares per-use authorized custody, with its basis

- WHEN a security key registers a single-device credential and verifies its user
  on every use
- THEN its key may be declared `isolated_per_use_authorized`
- AND the binding records whether that declaration rests on accepted attestation
  evidence or on the holder's word

#### Scenario: a synced passkey is not bound while no model describes it

- WHEN a registration reports backup eligibility set
- THEN no binding is made under this profile while the registry holds no model
  that describes a multi-device credential

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

### Requirement: A recorded proof is checked from what is recorded with it

openWallet SHALL let a relying domain check a proof under this profile that
another party obtained and recorded, such as a licence verifier's proof of
possession, from the proof and what is recorded with it: the relying-party
identifier, the origin at which that party obtained it, the credential
identifier, the public key and its algorithm, the backup eligibility and backup
state the proof carries, and that party's statement that it obtained the proof
within a session in which it identified the holder by its own means. The relying
domain SHALL recompute the challenge from the proof's fields; SHALL make every
check of the second requirement on the client data and the authenticator data,
with the recorded origin as the only allowed origin, the recorded relying-party
identifier, and the recorded backup flags as the values the proof must carry;
and SHALL verify the signature under the recorded public key, whose fingerprint
SHALL be the one the record names. Where the relying domain bound that key
itself, it SHALL also check that the recorded relying-party identifier is its
own and that the credential identifier is the one it bound. It SHALL compare no
signature counter, and SHALL NOT treat the check as checking that party's
challenge, the statement behind it or that party's identification of the
holder, which are that party's own. A record without that party's statement of
an identified session SHALL NOT be relied on.

#### Scenario: a recorded proof is checked without the recording party

- WHEN a relying domain checks a licence verifier's recorded proof
- THEN it decides from the proof and what is recorded with it, and contacts
  nothing outside its deployment

#### Scenario: a recorded proof at another origin

- WHEN a recorded proof's client data names an origin other than the recorded
  one
- THEN the check fails

#### Scenario: a recorded proof from another credential

- WHEN a recorded proof's credential identifier differs from the credential the
  relying domain bound for that key
- THEN the check fails

#### Scenario: a record without an identified session

- WHEN a recorded proof carries no statement that the recording party obtained it
  within a session in which it identified the holder
- THEN the relying domain does not rely on it
