# Design: add-webauthn-proof-profile

## Context

Drafted on 2026-11-15 by Claude (Opus 5.5), on Brett Heap's ruling 208, as a
draft for his review. **Nothing here is ratified.** His rulings quoted below are
his decisions; every other choice is a design call, marked PROPOSED where it is
made and listed in "Design calls", so that it can be confirmed or overturned one
by one.

openChart's draft `define-clinical-acts-foundation` (openChart-spec#5) needs a
practitioner's sign-off of every medical decision. openWallet's draft
`add-practitioner-profile-and-licence-verification` (openWallet-spec#10) defines
the licence verification and what a sign-off's proof is, and openSig's draft
`add-wallet-bound-attestation` (openSig-spec#4) attests it. The ratified
possession profile `wallet-challenge-proof` is Ed25519 over a preimage openWallet
chooses, which no passkey or security key can produce. Ruling 208 chose the
passkey or security key, and asked for this change.

Every statement here about Web Authentication cites the current W3C
Recommendation, **Web Authentication: An API for accessing Public Key
Credentials, Level 3**, W3C Recommendation of 25 August 2026
(`https://www.w3.org/TR/2026/REC-webauthn-3-20260825/`), by section. Level 4 is
a First Public Working Draft (15 September 2026) and is not relied on. COSE
algorithm identifiers cite the IANA "COSE Algorithms" registry as last updated
on 2026-11-13.

## The owner's rulings

Every row is a ruling by **Brett Heap**. **Rulings are not ratification.** This
change stays `Status: proposed` until he ratifies it.

On 2026-11-15 he answered the decisions numbered 195 to 214 with the words
"accept your recs for 195-214". Each became a ruling in the words of the
recommendation as last presented to him. The rows that bind this change,
question and ruling verbatim:

| No. | Question | Ruling |
|---|---|---|
| 208 | How does a practitioner sign: with a smart-card style key, or with a passkey or security key? The second needs one more openWallet change, a proof format for them. | A passkey or security key. Draft that change now. A smart card cannot be used from a phone. |
| 209 | May it be a passkey that syncs through the practitioner's Apple or Google account? | Yes, but only on a device the practitioner has enrolled, as ruling 134 allows for approvals. A security key always counts. Controlled substances stay out (ruling 83) and would need stronger keys. |

**What they rule here, and nothing more.**

- **208** rules that a practitioner signs with a passkey or a security key, and
  that this change, a proof format for them, is drafted now. The format itself,
  every name in it and every check it makes are PROPOSED.
- **209** rules openChart's acceptance: a synced passkey counts only on a device
  the practitioner has enrolled, a security key always counts, and controlled
  substances stay out. Enrolling a device is the relying domain's matter. What
  this profile owes a relying domain is the means to tell a synced passkey from
  a device-bound key (D6), and to say what it cannot tell. Rulings 134 and 83,
  which ruling 209 cites, are openChart's and openPractice's to encode, not this
  change's.

## What this change stands on

| Record | Standing | How this change uses it |
|---|---|---|
| Web Authentication Level 3 | W3C Recommendation, 25 August 2026 | What an authenticator signs, the authenticator data and its flags, the client data, how a relying party verifies an assertion, related origins (cited by section throughout). |
| IANA COSE Algorithms registry | last updated 2026-11-13 | The algorithm identifiers (D3). |
| `add-challenge-proof-runtime` (capability `wallet-challenge-proof`) | ratified 2026-11-10, not archived | The pattern this profile follows (a domain separator, RFC 8785, a trusted binding, closed fields), and the limits its ratification states. Not changed. |
| The closed custody registry, version 1 (`openWallet-code` `bb0e9da`) | ratified with the birth change | Which model a credential's key declares (D7). Not changed. |
| The closed `signature_algorithm` set of the wallet record (`openWallet-code` `bb0e9da`) | ratified | Already holds `ecdsa-p256` and `ed25519`; no change to it is needed (D3). |
| `add-practitioner-profile-and-licence-verification` (openWallet-spec#10) | proposed | Its practitioner's sign-off and its licence verification's proofs of possession use this profile; it relies on this change. This change does not depend on it. |
| `add-wallet-bound-attestation` (openSig-spec#4) | proposed | Attests proofs under this profile (D9). |

## D1 — What is signed, and what binds it (PROPOSED, WP-1)

**An authenticator signs what Web Authentication says, not a preimage openWallet
chooses.** In `authenticatorGetAssertion` the signature is "the assertion
signature of the concatenation authenticatorData || hash", where `hash` is the
SHA-256 of the serialized client data (Level 3, §6.3.3). The authenticator data
starts with the SHA-256 of the relying-party identifier the credential is scoped
to, then one byte of flags and a four-byte signature counter (§6.1). The client
data carries `type`, `challenge`, `origin` and the optional `crossOrigin` and
`topOrigin` (§5.8.1). The only value the relying party chooses in all of it is
the challenge.

**So the profile puts what it must bind into the challenge.** The challenge is:

`SHA-256( "openWallet.webauthn-proof.v0" || 0x00 || RFC8785(unsigned binding fields) )`

over the proof's `profile` (`openwallet.webauthn-proof.v0`), `alg`,
`challenge_digest`, `binding_ref`, `wallet_ref`, `key_ref`, `subject_ref`,
`custody_ref`, `binding_revision` and `credential_id`. That is the ratified
profile's construction (its domain separator `openWallet.challenge-proof.v0` and
a NUL byte, then RFC 8785 of every unsigned field), with a separator of its own,
hashed once more because a Web Authentication challenge is a byte string the
client encodes in base64url (§5.8.1). The verifier recomputes it from the proof
and compares it with the client data's `challenge`.

**What a proof under this profile then binds:**

- **the statement and its single-use challenge reference**, through
  `challenge_digest`, which is the SHA-256 of the relying party's RFC 8785
  canonical statement carrying its single-use challenge, as under the ratified
  profile;
- **the wallet, the key, the subject, the custody reference, the binding and its
  revision**, through the derived challenge, and compared with the trusted
  binding;
- **the credential**, through `credential_id`, compared with the binding;
- **the relying party**, twice: by the relying-party identifier hash in the
  authenticator data, which the authenticator computes and the client cannot
  change, and by the `origin` in the client data, which the client sets (§5.8.1,
  §13.4.9).

**The challenge is derived, not drawn at random.** Level 3 says challenges "MUST
be randomly generated by Relying Parties in an environment they trust" and
"SHOULD therefore be at least 16 bytes long" (§13.4.3). The derived challenge is
32 bytes, and it is unpredictable because the statement behind
`challenge_digest` carries the relying party's single-use reference of 32 random
bytes, drawn server-side. The relying party still stores that reference until
the ceremony completes and refuses a second use, which is what §13.4.3 asks of
the challenge. This departure from the letter of §13.4.3 is stated rather than
hidden (Open question 7).

**The wire form** (PROPOSED). A proof is a closed JSON object of at most 8192
bytes, decoded with no repeated key and no constant, as the ratified profile's
design requires of its own proofs: the ten binding fields above, and
`authenticator_data`, `client_data_json` and `signature`, each the exact bytes
the authenticator and client produced, in unpadded base64url. The client data
is kept as bytes because its exact bytes are what was hashed; it is never
re-serialized. A credential identifier is at most 1023 bytes (§4, "Credential
ID"), so the limit holds with room.

REJECTED:

- **Putting the binding references in the client data as members of their
  own.** The client builds the client data and a relying party's page cannot add
  members to it; the challenge is the one field the relying party sets.
- **Using the statement digest itself as the challenge.** It would bind the
  statement, and not the wallet, key, binding or custody reference, which the
  ratified profile binds.

## D2 — What a verifier checks on every use (PROPOSED, WP-2)

The checks follow §7.2, "Verifying an Authentication Assertion", made strict
where a sign-off needs it:

| Check | Level 3 | This profile |
|---|---|---|
| `type` | §7.2: "Verify that the value of C.type is the string webauthn.get." | `webauthn.get`; a registration response (`webauthn.create`) is never a proof. |
| `challenge` | §7.2, §13.4.3 | The base64url encoding of the challenge derived in D1. |
| `origin` | §7.2; §13.4.9: "The Relying Party MUST NOT accept unexpected values of origin" | Exactly one of the origins the binding allows, by exact string; no subdomain matching (§13.4.8). |
| `crossOrigin`, `topOrigin` | §7.2 | Absent, or `crossOrigin` false: a sign-off is never made from inside another site's frame. |
| Relying-party identifier hash | §7.2 | The SHA-256 of the binding's relying-party identifier. |
| User present (UP) | §7.2: "Verify that the UP bit of the flags in authData is set." | Set. |
| User verified (UV) | §7.2: required "if, and only if, pkOptions.userVerification is set to required" | Set on every use: the profile always requires user verification. |
| Attested credential data (AT) | §6.1: "For assertion signatures, the AT flag MUST NOT be set" | Not set. |
| Backup eligibility (BE) and backup state (BS) | §7.2; §6.1.3 | BE equals the value recorded at registration; BS is not set unless BE is. Both are returned (D6). |
| Signature | §7.2: "verify that sig is a valid signature over the binary concatenation of authData and hash" | Under the binding's public key and algorithm (D3). |
| Signature counter | §6.1.1; §7.2: a counter that does not increase "is a signal, but not proof, that the authenticator may be cloned" | Compared with the binding's last value; a counter that does not increase is returned as a flag, never a refusal on its own (Open question 4). |
| Extensions | §7.2: "The Relying Party MAY ignore any or all extension outputs." | Ignored, and bounded by the proof's size. |
| Unknown client data members | §5.8.1: parsers must be "tolerant of unknown keys and of any reordering of the keys" | Tolerated and never read. |

**Who keeps the counter and the backup state.** As in the ratified profile, the
verifier itself keeps no state: "the registry and challenge issuer own those
decisions" (its design). The registry that holds the binding keeps the
credential's last signature counter and backup state, and updates them after a
proof verifies, as §7.2's last step describes.

## D3 — The algorithms the profile admits (PROPOSED, WP-3)

**Admitted: ES256 and EdDSA with Ed25519.**

- **`-7` (ES256).** The IANA registry lists it as "ECDSA w/ SHA-256". Level 3
  requires that a key with this algorithm "MUST specify 1 (P-256) as the crv
  parameter and MUST NOT use the compressed point form" (§5.8.5), and that its
  signature "MUST be encoded as an ASN.1 DER Ecdsa-Sig-Value" (§6.5.5). Level 3
  says "Relying Parties that wish to support a wide range of authenticators SHOULD
  include at least" `-8`, `-7` and `-257` (§5.4), so a profile without ES256 would
  not serve ruling 208.
- **`-8` (EdDSA).** Level 3 requires that a key with this algorithm "MUST specify
  6 (Ed25519) as the crv parameter" (§5.8.5). It is in the same list (§5.4), and
  it is the algorithm of the ratified profile and of the wallets that exist
  today.
- **`-9` (ESP256) and `-19` (Ed25519),** which RFC 9864 introduced, are treated as
  `-7` and `-8`. Level 3 says these "represent the same thing respectively" within
  Web Authentication, and that they are "NOT RECOMMENDED in pubKeyCredParams"
  (§5.4). The IANA registry marks `-9` and `-19` "Recommended: Yes" and `-7` and
  `-8` "Deprecated", because the latter leave the curve to the key; Level 3's
  restrictions in §5.8.5 remove that freedom, which is why the profile follows
  Level 3 here.

**Refused: every other algorithm**, including `-257` (RS256), which Level 3
recommends relying parties list for wide reach (§5.4). An RSA key is larger,
its PKCS #1 v1.5 signature is a second construction to verify, and nothing in
ruling 208 needs it (Open question 3).

**Strict encodings.** A P-256 point is checked to be on the curve, as §5.8.5's
note asks; a DER signature is accepted only in its strict form; an Ed25519
signature is 64 bytes.

**Fingerprints.** The wallet record's closed `signature_algorithm` set already
holds `ecdsa-p256` and `ed25519`, so no change to it is needed. openWallet's one
fingerprint spelling is `sha256:` and the lowercase hex SHA-256 of the raw public
key. For a P-256 key the profile fixes the raw form as the 33-byte compressed
point, the form the `did:key` method gives its P-256 multicodec (`p256-pub`,
`0x1200`, "33 bytes", "compressed"), so that a wallet record's
`public_key_multibase` and the fingerprint agree as they do for Ed25519. The
canonical validator today recomputes fingerprints only from the Ed25519
multicodec; recognizing the P-256 one is realization work (`tasks.md` 3.2).

**Signatures are not unique.** An ECDSA signature `(r, s)` can be rewritten as
`(r, n - s)`, which also verifies, so two serializations of one assertion can
differ in their signature. Nothing in the profile relies on a signature being
unique; replay is refused by the relying party's single-use challenge. openSig's
draft, which compares retries by the proof's canonical form, refuses a
malleated repeat rather than attesting it twice (D9).

## D4 — Binding a credential to a wallet key (PROPOSED, WP-4)

**Registration, then a proof.** A credential comes from a registration ceremony
(§7.1) in the holder's own session at the relying domain: the domain asks for a
credential scoped to its relying-party identifier, with user verification
required and only the algorithms of D3. Level 3 warns that "attestation types
other than self attestation do not include a self-signature to explicitly prove
possession of the credential private key at registration time" (§7.1). So the
binding is made only when a proof under this profile, over a challenge the
domain issued, follows in the same session and verifies under the new public
key.

**What the binding records**, beside the ratified binding's fields: the
relying-party identifier; the allowed origins, by exact string; the credential
identifier; the public key and its algorithm; the backup eligibility and backup
state the registration reported; whether user verification was performed at
registration (§7.1's `uvInitialized`); the signature counter; and the
attestation format, the authenticator's model identifier (AAGUID) where one was
given, and the result of the domain's attestation policy, including that none
was given (§7.1). A credential identifier already bound is refused, as §7.1
recommends.

**What the wallet record declares**: the key's reference, its fingerprint (D3),
its signature algorithm, and its custody (D7), with the backup eligibility
beside the custody.

**One relying party per credential.** By default "the RP ID be equal to the
origin's effective domain, or a registrable domain suffix of the origin's
effective domain" (§5.11), and the authenticator checks that the requested
credential is scoped to exactly the relying-party identifier the client supplies
(§6.1). So a credential registered at one deployment signs only for that
deployment. A practitioner who signs at two practices has two credentials, two
bindings and, under openWallet's draft practitioner profile, verifications that
name both keys.

## D5 — A proof of possession for a party other than the credential's relying party (PROPOSED, WP-5)

**The problem.** openWallet's draft practitioner profile has the licence
verifier obtain a proof of possession from each key it names, and ruling 214
rests on it: "the verification names the practitioner's own signing keys and is
signed by the independent verifier". A passkey's credential is scoped to the
deployment's relying-party identifier, and the verifier is a different party at
a different origin, which cannot ask for that credential by default (§5.11).

**The options:**

- **(a) Related origins.** "WebAuthn Relying Parties can opt in to allowing
  WebAuthn Clients to enable a credential to be created and used across a limited
  set of related origins" (§5.11). The deployment publishes, at its relying-party
  identifier's well-known URL, an `origins` list that includes the verifier's
  origin; the verifier's own page then asks the practitioner's client for a proof
  under the deployment's relying-party identifier. The client data names the
  verifier's origin; the authenticator data names the deployment's identifier.
  The verifier receives the proof from the practitioner's own client, not from
  the deployment, and checks it under the public key the practitioner's wallet
  record declares, so a substituted key fails. The limits: a client supports it
  only optionally ("WebAuthn Clients supporting this feature", §5.11), and says
  so through the `relatedOrigins` client capability (§5.8.7); the deployment
  controls the list, and can withdraw it, which refuses service and forges
  nothing.
- **(b) A proof relayed by the deployment.** The practitioner signs the verifier's
  challenge on the deployment's page, and the deployment forwards it. The
  verifier then sees only what the deployment chose to forward: an operator could
  forward a proof from a key of its own, and the verifier could not tell. The link
  between the key and the person would rest on the deployment, and ruling 214's
  words would not hold for it.
- **(c) A native client for a security key.** An authenticator checks that the
  requested credential is scoped to exactly the identifier the client supplies
  (§6.1), so a native client of the verifier's, speaking to a roaming security key
  directly, could ask for a proof under the deployment's identifier. Level 3 does
  not govern such clients, and the option serves security keys, not synced
  passkeys held by a platform.

**The recommendation is (a)**, with (c) where a practitioner uses a security key
and a client without related origins. A proof that reaches a verifier only
through the deployment is recorded as relayed and never presented as observed by
the verifier (Open question 2). Whatever the mode, the verifier's binding allows
only the verifier's own origin, and the deployment's binding never allows an
origin it listed for the verifier, so a proof made for the verifier can never be
accepted as a sign-off.

REJECTED:

- **Registering the credential at the verifier's identifier, with the deployment
  as a related origin.** Every sign-off would make the practitioner's client
  fetch the verifier's well-known list, so signing would depend on an outside
  service, against the spirit of ruling 156.
- **A second credential for the verifier.** It would be another key: the
  verification must name the key that signs off.

## D6 — Synced or device-bound (ruling 209) (PROPOSED, WP-6)

**What Web Authentication offers.** "The BE flag SHALL be set if and only if the
credential is a multi-device credential. This value MUST NOT change after a
registration ceremony", and "The BS flag SHALL be set if and only if the
credential is a multi-device credential and is currently backed up" (§6.1). A
credential with BE clear "is a single-device credential and the generating
authenticator will never allow the credential to be backed up" (§6.1.3). "It is
RECOMMENDED that Relying Parties store the most recent value of these flags"
(§6.1.3).

**What the profile records.** BE at registration, kept for the life of the
binding; on every use, BE checked against it (§7.2) and BS returned. Every
verified proof carries both, as the authenticator signed them. The registration
attestation and model identifier are recorded where given (D4).

**What it can tell.** Whether a credential is a multi-device credential, such as
a passkey that syncs through the practitioner's Apple or Google account, or a
single-device credential, such as a security key or a passkey kept on one
device: as far as the authenticator reports BE truthfully.

**What it cannot tell.**

- **Which device signed with a synced passkey.** Level 3 defines no means for a
  relying party to learn the device a multi-device credential signed on, so
  ruling 209's "only on a device the practitioner has enrolled" cannot be
  evidenced by this profile. The relying domain must evidence enrolment by its
  own means, for instance by accepting a sign-off only within a session on a
  device it enrolled; that is openChart's to design.
- **Whether a single-device credential is a roaming security key or a platform
  key**, beyond what an attestation shows.
- **Whether the authenticator reports BE truthfully**, beyond what the domain's
  attestation policy trusts: with `none` attestation (§7.1) nothing does.
- **Who else can use the account a synced passkey syncs through.** Whoever takes
  over that account can obtain the passkey on a device of their own and verify
  there.

## D7 — Custody: which model such a key declares (PROPOSED, WP-7; Open question 1)

The closed registry's model `isolated_per_use_authorized` states: "The key is
isolated from the holder's execution context AND each signature requires an
authorization that context cannot itself supply ... A compromised environment
cannot obtain a signature on its own". Its model `isolated_invocable` describes
isolation as a key "held outside that context ... so it cannot be read,
exfiltrated or replayed elsewhere".

**A single-device credential fits.** A security key, or a passkey kept on one
device, keeps its private key in the authenticator, and the profile requires
user verification on every use (D2). It may declare
`isolated_per_use_authorized`, which is what this profile allows.

**A synced passkey does not fit honestly.** Its two properties look right on each
device: no application can read the key, and each use needs verification on the
device. But the provider copies the key to every device in the account, so it
can be "replayed elsewhere" by whoever adds a device to that account, and a
takeover of the account obtains signatures without the practitioner. The
registry's statement does not describe that. This change does not bend it, and
does not propose the registry change here: the registry is a ratified contract
read by every consumer, its `evidences` value is derived from two booleans by
the canonical validator, and adding a model means deciding a third property and
an authority ceiling that reach well beyond openChart. That is put to the owner
(Open question 1), with wording drafted there.

**Meanwhile**, every key bound under this profile records its backup eligibility
beside its custody, so no reading of the custody can omit it, and the profile
never states that a synced passkey's signature evidences that its holder acted
on the strength of its declared custody alone. Ruling 209 still lets openChart
accept a synced passkey on an enrolled device, by openChart's own rule. What the
wallet record declares for such a key is the open question.

## D8 — The threat model, honestly (PROPOSED, WP-8)

**What origin binding stops.**

- A page at another origin cannot obtain a usable proof for the deployment: the
  client refuses a relying-party identifier that the origin may not use (§5.11),
  the authenticator signs only for the identifier the credential is scoped to
  (§6.1), and the verifier checks the origin exactly (§13.4.9).
- A proof made for one deployment does not verify at another: the
  relying-party identifier hash and the origin differ.
- A proof made at a verifier's related origin is never accepted as a sign-off
  (D5).

**What a deployment that controls its own origin can still do.** Level 3 is
plain: "Any malicious code executing on an origin within the scope of a Relying
Party's public key credentials has the potential to invalidate any and all
security guarantees WebAuthn may provide" (§13.4.8). Whoever runs the deployment
controls that code. So it can:

- show the practitioner one statement and ask the authenticator to sign the
  challenge for another, because no authenticator shows what it signs;
- obtain one signature for each gesture the practitioner makes on its page;
- withhold, delay or relay proofs, and withdraw the related-origin list;
- record in its own registry whatever bindings it likes, which matters only
  where a verifier did not observe the key's proof itself (D5).

**Ruling 214 under this profile.** Its words: "Yes, against forgery: the
verification names the practitioner's own signing keys and is signed by the
independent verifier. It does not stop that person deleting records or
back-dating; outside timestamps can close that later." They hold under this
profile, against a sign-off made without the practitioner's key, on two
conditions this profile can meet: the verifier observed each named key's proof
of possession itself (D5, option (a) or (c)); and the signer is read from the
verification, never from an account (openWallet's draft practitioner profile).
They do not hold for a key whose proof the verifier saw only relayed. And they
do not reach content substitution: a deployment that shows one statement and
has the key sign another obtains a genuine signature by the practitioner's key
and gesture. That is not a sign-off made without the key, so it is not a
forgery in the sense the ruling's reason gives, but it is a sign-off the
practitioner did not intend, and nothing in this profile, or in the ratified
one, can detect it. openWallet's draft practitioner profile puts that to the
owner (its Open question 21).

## D9 — openSig can attest it (PROPOSED, WP-9)

openSig's draft `add-wallet-bound-attestation` runs openWallet's verification and
seals the result. Checked against this profile:

- **What it verifies with.** It accepted only proofs under the ratified profile,
  and is revised to accept proofs under either profile and run openWallet's
  verification of the one the proof names, never a second implementation.
- **What it seals.** A `verified` attestation must carry everything a relying
  party needs to verify the sealed proof itself. Under this profile that is the
  proof (with its authenticator data, client data and signature) and the binding
  (with its relying-party identifier, allowed origins, credential identifier,
  public key and algorithm): all of it already in the proof and the binding it
  seals. The backup flags and the counter flag are in the signed authenticator
  data and the verification's result.
- **What it may store.** The client data can carry members a client adds
  (§5.8.1), which openSig seals with a `verified` proof, bounded by the proof's
  8192 bytes and signed by the practitioner's authenticator; openSig's rule of
  sealing the whole proof only where every reference matches the binding
  applies unchanged.
- **Retries.** openSig compares an identical retry by the proof's canonical
  form. An ECDSA signature is not unique (D3), so a malleated repeat differs and
  is refused, never attested twice.
- **Reasons.** openSig's closed reasons gain those this profile adds: the client
  data's type, challenge or origin (`client_data_invalid`); the relying-party
  identifier (`relying_party_mismatch`); user presence or verification
  (`user_not_verified`); backup eligibility changed
  (`backup_eligibility_changed`); an algorithm other than the binding's
  (`algorithm_mismatch`). An algorithm this profile does not admit fails its
  strict decoding, as an unsupported profile does.

Those revisions are made in openSig-spec#4 alongside this change.

## D10 — Non-goals (PROPOSED, WP-10)

1. **Controlled substances**, which ruling 209 keeps out ("would need stronger
   keys", ruling 83).
2. **Any change to the ratified `wallet-challenge-proof`.** It stays as ratified,
   and nothing in this profile applies to it.
3. **A change to the closed custody registry** (Open question 1).
4. **The verification service of ruling 211**, which openWallet's draft
   practitioner profile puts to the owner.
5. **A channel that shows the practitioner the statement before the key signs**,
   a possible successor (D8).
6. **Device enrolment**, which is the relying domain's (ruling 209).

## D11 — Placement, names, code surface and release class (PROPOSED, WP-11)

**Placement.** The ratified challenge-proof change says "New schemas default to
spec leg; legacy wallet Q7 does not automatically cover them". The
recommendation is the same leg as that profile's own schema (Open question 8).

**Names that become machine keys once released**, all PROPOSED and cheapest to
change now: the capability `wallet-webauthn-proof`; the profile constant
`openwallet.webauthn-proof.v0`; the domain separator
`openWallet.webauthn-proof.v0`; the proof's field names; the binding's added
fields; and the refusal reasons.

**Code surface**, named here and performed by nothing in this change: a verifier
in openWallet's runtime beside the ratified profile's, reusing its RFC 8785
canonicalizer; P-256 and Ed25519 verification; a proof schema; known-answer
vectors made with independent tooling, on feature 016's precedent, including
Level 3's own examples (§16); and the validator's recognition of the P-256
multicodec.

**Release class: an ADDITIVE MINOR**, its coordinated values allocated at
realization, and nothing reserved here.

## Design calls

Every call below goes beyond the owner's words and is PROPOSED, and each is put to
the owner.

| # | Design call | Where |
|---|---|---|
| WP-1 | The challenge is SHA-256 over a domain separator and RFC 8785 of the proof's ten unsigned binding fields, so the proof binds what the ratified profile binds and the relying party; the derived challenge, unpredictable through the statement's random reference; the closed wire form, 8192 bytes, client data kept as bytes. | D1 |
| WP-2 | The checks on every use: type, challenge, exact origin, no cross-origin use, relying-party identifier hash, user presence and verification always, no attested data, backup flags; the counter flagged, never refused alone; unknown client data members and extensions ignored; the registry keeps counter and backup state. | D2 |
| WP-3 | ES256 and EdDSA with Ed25519 only, `-9` and `-19` as their equivalents, every other refused; strict encodings; the P-256 fingerprint over the compressed point; no reliance on signature uniqueness. | D3 |
| WP-4 | Binding from a registration and a following proof in the holder's own session; what the binding records; one relying party per credential. | D4 |
| WP-5 | A verifier observes the proof itself, by related origins or a native client for a security key; a relayed proof is recorded as relayed; a verifier's origin is never a sign-off origin. | D5 |
| WP-6 | Backup eligibility recorded at registration and backup state on each use; what the profile can and cannot tell; enrolment is the relying domain's. | D6 |
| WP-7 | A single-device credential may declare `isolated_per_use_authorized`; a synced passkey's model is left open, with backup eligibility recorded beside every custody declaration. | D7 |
| WP-8 | The threat model: what origin binding stops, what a deployment can still do, and where ruling 214's words hold. | D8 |
| WP-9 | openSig attests proofs under this profile, with the revisions D9 names. | D9 |
| WP-10 | The non-goals. | D10 |
| WP-11 | Placement, names, code surface and release class. | D11 |

## Open questions for ratification

Each is a judgment the author made, or a choice the owner must make, with a
recommendation. None is ruled.

1. **Which custody model does a synced passkey declare?** The registry as written
   does not honestly describe a key a provider copies to every device in an
   account (D7). Options: (a) a fourth model, in its own change to the core and
   the registry, worded for instance: `synced_per_use_authorized`, "Key held by
   the holder's platform and copied by its provider to every device in the
   holder's account; each use authorized on the device. A signature evidences
   that someone with a device in that account acted, after verification on that
   device; it does not evidence which device, and an account takeover reaches
   it", with a ceiling the owner sets; (b) the owner accepts that
   `isolated_per_use_authorized` covers such a key, read device by device, with
   the backup eligibility recorded beside it. Recommendation: (a), because every
   consumer reads the registry and should not have to know to look for a flag;
   until it is ratified, openChart can accept a synced passkey only under its own
   rule of ruling 209, and the wallet record's declaration for it waits on this
   question.
2. **How does a verifier observe a passkey's proof of possession?** (D5)
   Recommendation: related origins, with a native client for a security key where
   related origins are not available, and no relayed proof for openChart's
   verifications, since with one ruling 214 would rest on the deployment.
3. **Which algorithms?** Recommendation: ES256 and EdDSA with Ed25519 only; add
   RS256 only if a practitioner's platform turns out to need it.
4. **What follows from a counter that does not increase?** Recommendation: a flag
   the relying domain raises to a human, never a refusal on its own. Level 3 says
   that then "a cloned authenticator may exist, or the authenticator may be
   malfunctioning, or a race condition might exist", and that an authenticator
   without a counter leaves it "constant at zero" (§6.1.1).
5. **Which attestation does a relying domain require at registration?**
   Recommendation: record whatever is given, `none` included, and leave what
   evidence of custody is required to openWallet's custody-acceptance successor
   (the practitioner profile's Open question 6).
6. **Ignore authenticator extensions and unknown client data members?**
   Recommendation: yes, as Level 3 allows, bounded by the proof's size.
7. **Accept a derived challenge where §13.4.3 says challenges "MUST be randomly
   generated"?** Recommendation: yes; it is unpredictable through the statement's
   32 random bytes, which the relying party draws server-side and holds for one
   use.
8. **Which leg holds the proof schema?** Recommendation: the spec leg, as the
   ratified challenge-proof change places new schemas.
9. **The names that become machine keys** (D11). Recommendation: confirm or change
   them now.
10. **The raw form of a P-256 key for its fingerprint.** Recommendation: the
    33-byte compressed point, as `did:key` carries it.
11. **Refuse use from inside another site's frame?** Recommendation: yes; a sign-off
    is made on the relying domain's own page.

## Status

`Status: proposed`. No review has run yet; `tasks.md` 1.1 schedules one.
Ratification is pending, by openWallet's operator authority, Brett Heap.
