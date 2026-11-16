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
  substances stay out. This change reads it (PROPOSED): enrolling a device is the
  relying domain's matter, and what this profile owes a relying domain is the
  means to tell a synced passkey from a device-bound key (D6), and to say what it
  cannot tell. Rulings 134 and 83, which ruling 209 cites, are openChart's and
  openPractice's to encode, not this change's.

## What this change stands on

| Record | Standing | How this change uses it |
|---|---|---|
| Web Authentication Level 3 | W3C Recommendation, 25 August 2026 | What an authenticator signs, the authenticator data and its flags, the client data, how a relying party verifies an assertion, related origins (cited by section throughout). |
| IANA COSE Algorithms registry | last updated 2026-11-13 | The algorithm identifiers (D3). |
| `add-challenge-proof-runtime` (capability `wallet-challenge-proof`) | ratified 2026-11-10, not archived | The pattern this profile follows (a domain separator, RFC 8785, a trusted binding, closed fields), and the limits its ratification states. Not changed. |
| The closed custody registry, version 1 (`openWallet-code` `bb0e9da`) | ratified with the birth change | Which model a credential's key declares (D7). Not changed. |
| The closed `signature_algorithm` set of the wallet record (`openWallet-code` `bb0e9da`) | ratified | Already holds `ecdsa-p256` and `ed25519`; no change to it is needed (D3). |
| `add-practitioner-profile-and-licence-verification` (openWallet-spec#10) | proposed | Its practitioner's sign-off and its licence verification's proofs of possession use this profile, and it records with each verifier's proof what this profile's check of a recorded proof needs (D5); it relies on this change. This change does not depend on it. |
| `add-trust-anchors-and-machine-holders` | proposed | Names as a successor the pinning of fingerprint encodings for algorithms other than Ed25519 (its D8 and D11); this change pins one for P-256 keys bound under this profile (D3). Not changed. |
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
32 bytes, and it is unpredictable only because the statement behind
`challenge_digest` carries a random single-use reference. So the profile makes
that a duty (PROPOSED): whoever issues the challenge puts in the statement a
single-use challenge reference of 32 bytes drawn at random by its own server,
in an environment it trusts, holds it until the ceremony completes and refuses a
second use, which is what §13.4.3 asks of the challenge (requirement 1). Two
requests over the same statement and binding derive the same challenge; single
use is held by the reference, never by the challenge. This departure from the
letter of §13.4.3 is stated rather than hidden (Open question 7).

**One credential per request** (PROPOSED). The challenge binds `credential_id`,
so the relying party knows the credential before it asks, and its request lists
exactly that credential in `allowCredentials` (§5.5). Level 3 says that list
"SHOULD usually include all credential records in the user account", and that
when it is left empty "only discoverable credentials will be utilized", the
client letting the user pick one (§5.5). Neither fits a derived challenge: a
sign-off names its key before it is made, so sign-in with a discoverable
credential, conditional mediation included, is not a way to make a proof under
this profile.

**The wire form** (PROPOSED). A proof is a closed JSON object of at most 8192
bytes, decoded with no repeated key and no constant, as the ratified profile's
design requires of its own proofs: the ten binding fields above, with `alg` a
JSON integer (D3), and `authenticator_data`, `client_data_json` and `signature`,
each the exact bytes
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
| Binding | Not in Level 3. The ratified sibling: "accept binding metadata only from a trusted server registry; client proof data SHALL NOT supply a public key. The binding SHALL be current, unrevoked and time valid" | The same: the binding comes only from the trusted server registry and is current, unrevoked and time valid; the public key, the relying-party identifier and the allowed origins come only from it, never from the proof. A verifier's session binding (D5) and a recorded proof (D5) are the stated exceptions, and a later verification of a proof already verified checks the binding as recorded then, never claiming it is still current. |
| Parsing the client data | §7.2: "an implementation-specific JSON parser" | UTF-8 JSON with no repeated member, so that every verifier reads one origin and one challenge, as the ratified profile refuses "duplicate JSON keys" in its proofs. |
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
| Signature counter | §6.1.1; §7.2: a counter that does not increase "is a signal, but not proof, that the authenticator may be cloned" | Compared once, at the proof's first verification, with the value kept beside the binding; a counter that does not increase is recorded as a flag, never a refusal on its own (Open question 4); a later verification of the same proof reports the recorded flag. |
| Extensions | §7.2: "The Relying Party MAY ignore any or all extension outputs." | Ignored, and bounded by the proof's size. |
| Unknown client data members | §5.8.1: parsers must be "tolerant of unknown keys and of any reordering of the keys" | Tolerated and never read. |

**What a verification returns** (PROPOSED). With the verified facts, the four
flags as the authenticator signed them, named `user_present`, `user_verified`,
`backup_eligible` and `backup_state`, and the counter flag,
`sign_count_not_increasing`. With a refusal, its reason and
`signature_verified`, which says whether the signature verified under the
binding's public key, so that whoever records the refusal, such as openSig, can
tell bytes the authenticator signed from bytes a caller chose (D9). The
signature is checked whenever a binding was found and the proof decoded,
whatever else failed; a signature not checked reports as not verified. A refusal
that reports a verified signature is never evidence of possession: it tells the
caller only what the public key in the binding already lets anyone compute.

**Who keeps the counter and the backup state** (PROPOSED). As in the ratified
profile, the verifier itself keeps no state: "the registry and challenge issuer
own those decisions" (its design). The registry keeps the credential's last
signature counter and current backup state beside the binding, not in its
revisioned record, and updates them after a proof verifies, as §7.2's last step
describes. An update therefore never revises the binding, so it never fails a
proof in flight, whose challenge binds `binding_revision`. The registry, which
alone writes the counter, compares it once for each derived challenge, at the
first verification of a proof with that challenge made against its own record,
and records the flag beside the binding, keyed by the derived challenge rather
than by the proof's bytes, so that a proof whose ES256 signature was rewritten
is not compared again. A verifier that holds only a read-only replica, such as
openSig in some deployments, reports the flag recorded for that challenge and,
where none is recorded yet, has the registry make that first comparison before
it reports. A later verification of the same proof, by openSig, the relying
party or an honest check, reports the recorded flag and does not compare the
counter again, since the counter has since moved on.

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

**At registration** a relying domain offers `-8` and `-7` only. Level 3 says the
fully specified identifiers are "NOT RECOMMENDED in pubKeyCredParams", and that
"the latter identifiers are preferred in pubKeyCredParams for backwards
compatibility" (§5.4). A credential that nonetheless reports `-9` or `-19` is
recorded under `-7` or `-8`.

**The `alg` field** is the COSE algorithm identifier as a JSON integer, and is the
identifier its binding recorded, `-7` or `-8`. A proof naming any other value,
`-9` and `-19` included, is refused, so each scheme has one spelling in a proof.

**Strict encodings.** A P-256 point is checked to be on the curve, as §5.8.5's
note asks; a DER signature is accepted only in its strict form; an Ed25519
signature is 64 bytes and canonical, its S decoded "in the range 0 <= s < L"
(RFC 8032, §5.1.7), as the ratified profile refuses "noncanonical signatures".

**The recorded key form.** A binding and a wallet record hold the public key in
its raw form: for a P-256 key the 33-byte compressed point of the uncompressed
key the registration returned (§5.8.5), for an Ed25519 key its 32 bytes. A
verifier decompresses a P-256 point, checking that it is on the curve, before it
verifies.

**Fingerprints.** The wallet record's closed `signature_algorithm` set already
holds `ecdsa-p256` and `ed25519`, so no change to it is needed. openWallet's one
fingerprint spelling is `sha256:` and the lowercase hex SHA-256 of the raw public
key. For a P-256 key the profile fixes the raw form as the 33-byte compressed
point, the form the `did:key` method gives its P-256 multicodec (`p256-pub`,
`0x1200`, "33 bytes", "compressed"), so that a wallet record's
`public_key_multibase` and the fingerprint agree as they do for Ed25519. The
canonical validator today recomputes fingerprints only from the Ed25519
multicodec; recognizing the P-256 one is realization work (`tasks.md` 3.2).
`add-trust-anchors-and-machine-holders` names "Fingerprint encodings for
non-ed25519 algorithms" as a successor (its D8, and D11 item 5). This change pins
the encoding for P-256 keys bound under this profile; whichever of the two lands
second adopts the other's encoding or reconciles them.

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
required and `-8` and `-7` offered (D3). Level 3 warns that "attestation types
other than self attestation do not include a self-signature to explicitly prove
possession of the credential private key at registration time" (§7.1). So the
binding is made only when a proof under this profile, over a challenge the
domain issued, follows in the same session and verifies under the new public
key.

**What the binding records**, beside the ratified binding's fields: the
relying-party identifier; the allowed origins, by exact string; the credential
identifier; the public key in its raw form and its algorithm (D3); the backup
eligibility and backup state the registration reported; whether user
verification was performed at registration (§7.1's `uvInitialized`); the
attestation format, the attestation object itself, which §7.1 lets a credential
record keep, the authenticator's model identifier (AAGUID) where one was given,
and the result of the domain's attestation policy, including that none was
given (§7.1); the basis of the key's declared custody, `custody_basis`,
`attested` or `declared` (D7); and the holder's declaration (D8, Open question
15), `holder_declaration`. Its shape (PROPOSED): `declared_at`, when the holder
made it; `client`, true where the holder declared that the device, the browser
and its extensions, the passkey provider and the authenticators the client uses,
through which it registers the key and completes any verifier's session, and the
place where the wallet record it presents is kept, are under its control and are
not administered by the relying domain's operator; and `sync_account`, present
only for a multi-device credential once one can be bound (D7), true where the
holder declared that the account it syncs through is its own alone and is not
administered by that operator. A relying domain decides which parts it requires;
each is the holder's word. The signature counter
and the current backup state are kept beside the binding, not in its revisioned
record (D2). A credential identifier already bound is refused, as §7.1
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
name both keys. One deployment may bind more than one credential for a
practitioner, each with its own binding, for instance a second key against loss:
Level 3 says relying parties "SHOULD allow and encourage users to register
multiple credentials to the same user account" (§13.4.6).

## D5 — A proof of possession for a party other than the credential's relying party (PROPOSED, WP-5 and WP-12)

**The problem.** openWallet's draft practitioner profile has the licence
verifier obtain a proof of possession from each key it names, and ruling 214
rests on it: "the verification names the practitioner's own signing keys and is
signed by the independent verifier". A passkey's credential is scoped to the
deployment's relying-party identifier, and the verifier is a different party at
a different origin, which cannot ask for that credential by default (§5.11).

**What a proof at another origin shows, and what it does not.** A proof the
verifier obtains at its own origin shows that a client holding a credential
scoped to the deployment's relying-party identifier signed the verifier's
challenge, with the user present and verified, at the verifier's page. It does
not show whose credential that is. The deployment is that relying party: it can
register a credential of its own, under its own identifier, and present it at
the verifier's page with a wallet record it supplies. A browser, a browser
extension, a device or a passkey provider that the practice administers can do
the same from the practitioner's own screen: it can answer the verifier's request
itself, with a software credential the operator registered under the deployment's
identifier. An assertion carries no attestation (§5.5's request options have no
member for one), and "the authenticator may be embedded in the client, and its
bindings may be no more trustworthy than the client data" (§6.1), so the
verifier cannot tell. And a deployment that can start or join the verifier's
session, for instance through a link or token it hands the practitioner, can
complete the key step from its own client once the practitioner is identified.
So a proof ties a key to the licensee only where the verifier identified the
licensee itself, by its own means and independently of the deployment, in a
session the verifier began with the practitioner's client itself, which the
deployment neither began nor can join, and only as far as that client is the
practitioner's own, which no verifier can tell.

**The options:**

- **(a) Related origins.** "WebAuthn Relying Parties can opt in to allowing
  WebAuthn Clients to enable a credential to be created and used across a limited
  set of related origins" (§5.11). The deployment publishes, at its relying-party
  identifier's well-known URL, an `origins` list that includes the verifier's
  origin; the verifier's own page then asks the practitioner's client for a proof
  under the deployment's relying-party identifier. The client data names the
  verifier's origin; the authenticator data names the deployment's identifier.
  The verifier checks the proof under the public key the practitioner's wallet
  record declares, which ties the proof to that key and no other; that the key
  is the licensee's rests on the verifier's own identification of the licensee
  in that session, and on the client being the practitioner's own. The limits: a client supports it only optionally ("WebAuthn
  Clients supporting this feature", §5.11), and says so through the
  `relatedOrigins` client capability (§5.8.7); the deployment controls the list,
  and can withdraw it, which refuses service and forges nothing.
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
  passkeys held by a platform. A native client writes whatever origin it likes
  into the client data, so the client data cannot tell a proof the verifier
  observed from one relayed to it; only the verifier's own identification of the
  licensee in that session can, and only as far as the client is the
  practitioner's own.

**The condition, as a duty** (PROPOSED). A party other than the credential's
relying party accepts a proof of possession only in a session it began with the
holder's client itself, which the relying party neither began nor can join, in
which it identified the holder by its own means, independently of the relying party, and never on evidence a relying domain holds or could obtain, such as copies of documents, the licence number or personal data from its records, and only from that client. The relying party usually holds the practitioner's
credentialing file, copies of the licence and identity documents among it, so
an identification that what is in that file can pass would let the operator be
identified as the practitioner in a session it began itself. The party records
the holder's declaration for that session, the `client` part of
`holder_declaration` (D4), in its statement of the session, `identified_session`
(below). openWallet's draft practitioner profile states the same
as a duty on the licence verifier: a verification names a key only on such a
proof. The profile cannot tell whether that client, or the authenticator it
uses, is administered by the relying domain's operator; how the verifier
identifies the licensee, and the holder's declaration, are records neither this
profile nor a relying domain can check.

**A relayed proof is never accepted** (PROPOSED). A proof that reached the
verifier through the deployment cannot meet the condition, so no licence
verification names a key on one. The first draft recorded such a proof as
relayed. No use in this change or in its consumers needs that marker, so the
profile carries none, and the proof is refused instead.

**The recommendation is (a)**, with (c) where a practitioner uses a security key
and a client without related origins, each under the condition above (Open
question 2). Whatever the mode, the verifier's binding allows only the
verifier's own origin, and the deployment's binding never allows an origin it
listed for the verifier, so a proof made for the verifier can never be accepted
as a sign-off.

**What a verifier's binding records, and which checks apply** (PROPOSED). It has
no registration behind it. It is made for the session, and records: the
deployment's relying-party identifier; the verifier's own origin, as its only
allowed origin; the credential identifier, as the holder presents it; the public
key and algorithm the holder's wallet record declares for the key, or one the
holder presents whose fingerprint the record declares, since
`public_key_multibase` is optional in a wallet record; and the
backup eligibility and backup state the proof carries. Every check of D2 applies
to it, with three differences: it is current for that session only; backup
eligibility is recorded from the proof rather than compared with a registration;
and no counter is compared, since the verifier keeps none. It records nothing a
registration would give (`uvInitialized`, attestation, model identifier).

**The statement of the session** (PROPOSED). `identified_session` is an object the
verifier puts in what it signs, and its presence is the verifier's statement
that it obtained the proof in a session it began with the holder's client
itself, which no relying party began or can join, and in which it identified the
holder by its own means, never on evidence a relying domain holds or could obtain, such as copies of documents, the licence number or personal data from its records. Its members: `began_at`, when the verifier began the session;
`identification_ref`, an opaque reference to the verifier's own record of how it
identified the holder; and `holder_declaration`, the holder's declaration for
that session, with its `declared_at` and `client` parts.

**Checking a recorded proof** (PROPOSED, WP-12). A licence verification records
each proof with what checking it needs: the relying-party identifier, the
verifier's origin, the credential identifier, the public key, the backup flags
the proof carries, and `identified_session`, with the holder's declaration in
it. The algorithm is the
proof's own `alg`, which the derived challenge binds, unless the record names
one. A relying domain checks a recorded proof from those and the proof alone. It
recomputes the challenge from the proof's fields; checks the client data as D2
does, with the recorded verifier origin as the only allowed origin, and refuses
a recorded origin that it allows for its own sign-offs, which catches a proof
made on the deployment's own page; checks the
relying-party identifier hash against the recorded identifier, the user present
and user verified flags, the attested-data flag, and that the backup flags are
the recorded ones; and verifies the signature under the recorded public key,
whose fingerprint must be the one the verification names. Where the domain bound
that key itself, it also checks that the recorded relying-party identifier is
its own and that the credential identifier is the one it bound. It compares no
counter and checks no binding state, and it cannot check the verifier's
challenge, the statement behind it or the verifier's identification of the
licensee, which are the verifier's own. A record without the verifier's
statement of an identified session is not relied on; openWallet's draft
practitioner profile names that refusal `identified_session_missing`, and the
refusal of a recorded origin the domain allows for its own sign-offs
`origin_is_relying_domain`.

REJECTED:

- **Registering the credential at the verifier's identifier, with the deployment
  as a related origin.** Every sign-off would make the practitioner's client
  fetch the verifier's well-known list, so signing would depend on an outside
  service, against the spirit of ruling 156.
- **A second credential for the verifier.** It would be another key: the
  verification must name the key that signs off.
- **Recording a relayed proof as relayed.** No use needs the marker, and a
  verification must never name a key on such a proof.

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
- **Which account a synced passkey syncs through, and who controls it.** Whoever
  controls or can recover that account can obtain the passkey on a device of
  their own and verify there; the plain case is a managed work account that the
  practice administers. Level 3 gives a relying party no means to learn which
  account holds a credential. It is one case of the wider limit in D8: whoever
  administers or can recover the device, browser, extension or passkey provider
  the practitioner uses. The holder's one declaration covers it (D4), and that
  declaration is the holder's word (Open questions 12 and 15).

## D7 — Custody: which model such a key declares (PROPOSED, WP-7; Open question 1)

The closed registry's model `isolated_per_use_authorized` states: "The key is
isolated from the holder's execution context AND each signature requires an
authorization that context cannot itself supply ... A compromised environment
cannot obtain a signature on its own". Its model `isolated_invocable` describes
isolation as a key "held outside that context ... so it cannot be read,
exfiltrated or replayed elsewhere".

**A single-device credential may fit, on stated evidence.** A security key, or a
passkey kept on one device, keeps its private key in the authenticator, and the
profile requires user verification on every use (D2). It may declare
`isolated_per_use_authorized`. But a clear backup-eligibility flag does not show
that the key is isolated: Level 3 warns that "the authenticator may be embedded
in the client, and its bindings may be no more trustworthy than the client data"
(§6.1), and with `none` attestation (§7.1) a software authenticator can report
the flag clear. So the binding records what the declaration rests on, as
`custody_basis` (PROPOSED), from a closed set of two: `attested`, where the relying domain's
attestation policy accepted attestation evidence that the authenticator keeps the
key isolated and verifies its user; or `declared`, where it rests on the holder's
word. A relying domain sees which, and decides what it accepts. `attested` rests
on the relying domain's own record of its policy's result, which whoever runs the
deployment can alter, so the binding keeps the attestation object (D4) for an
honest check to verify later. Until such a check verifies it against an
attestation root it trusts, `attested` is the relying domain's own claim.

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

**What follows** (PROPOSED). Every key bound under this profile declares a model
of the registry, and none describes a multi-device credential, so until the
registry holds a model that does, no multi-device credential can be bound under
this profile. Ruling 209's yes for a synced passkey on an enrolled device
therefore waits on Open question 1. This change proposes no interim model. Every
key that is bound records its backup eligibility and the basis of its custody
beside its custody, so no reading of the custody can omit them.

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
- withhold or delay proofs, and withdraw the related-origin list;
- register a credential of its own and present it at a verifier's page with a
  wallet record it supplies, which a verifier that did not identify the licensee
  itself, in that session, cannot tell from the practitioner's (D5);
- relay to a verifier a proof from a key of its own, which is why no verification
  names a key on a relayed proof (D5);
- record in its own registry whatever bindings it likes, which matters only
  where a verifier did not identify the licensee and obtain the key's proof
  itself (D5);
- answer a verifier's request from a browser, a browser extension, a device or a
  passkey provider it administers or can recover, with a credential it
  registered, and submit a wallet record declaring that key; or start or join a
  verifier's session and complete its key step from a client of its own, which
  the condition of D5 forbids but the verifier can enforce only for sessions it
  controls (D5);
- where it administers, or can recover, the account a practitioner's synced
  passkey syncs through, obtain that passkey on a device of its own and sign
  with it (D6).

**Ruling 214 under this profile.** Its words: "Yes, against forgery: the
verification names the practitioner's own signing keys and is signed by the
independent verifier. It does not stop that person deleting records or
back-dating; outside timestamps can close that later." This change reads a
forgery, as openWallet's draft practitioner profile does, as a sign-off in a
practitioner's name made without that practitioner's key (PROPOSED). Under this
profile the words hold only on conditions it states and cannot meet by itself:

1. the verification is signed by a verifier key that ships with a release of the
   relying system (openWallet's draft practitioner profile);
2. the verifier identified the licensee itself, by its own means and
   independently of the deployment, never on evidence a relying domain holds or could obtain, such as copies of documents, the licence number or personal data from its records, in a session it began with the practitioner's client itself,
   which the deployment neither began nor can join, and in which each named key
   proved possession (D5); that rests on the
   verifier's own record, which neither this profile nor a relying domain can
   check, and no relayed proof can meet it;
3. the signer is read from the verification, never from an account (openWallet's
   draft practitioner profile).

They do not reach two cases. **A client, device or provider the practice
administers.** Whoever administers or can recover the device, the browser, an
extension in it, or the passkey provider that the practitioner uses to register a
key or to complete the verifier's session can do so without the practitioner. It
can answer the verifier's request with a credential it registered, which the
verifier cannot tell from the practitioner's; where the practitioner registered
through such a browser, every later sign-off can be made without them, which is
a forgery even under the reading above, and an honest check accepts it. Through
a synced passkey's account it can sign with the practitioner's own key, which
under the reading above is not a forgery, yet is what the ruling asks about. The
profile cannot see who administers a client or which account holds a passkey;
it records the holder's declaration (D4), and the limit is put to the owner
(Open questions 12 and 15). **Content substitution.** A deployment that shows one statement and has the key sign
another obtains a genuine signature by the practitioner's key and gesture. That
is not a sign-off made without the key, so it is not a forgery in the sense the
ruling's reason gives, but it is a sign-off the practitioner did not intend, and
nothing in this profile, or in the ratified one, can detect it. openWallet's
draft practitioner profile puts that to the owner (its Open question 21).

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
  public key and algorithm, and the backup eligibility recorded at
  registration): all of it already in the proof and the binding it seals. The
  key's `custody_basis` goes with the custody openSig records. The backup flags and the counter flag are in the signed authenticator
  data and the verification's result.
- **What it may store.** The client data and the authenticator data are bytes a
  caller can choose until the signature binds them, and the client data can carry
  members a client adds (§5.8.1). openSig's rule of sealing the whole proof only
  where every reference matches the binding is therefore not enough for this
  profile: openSig seals a passkey proof whole only where its `credential_id` and
  `binding_revision` also equal the binding's, since a caller could otherwise
  rewrite the credential identifier after signing and have up to 1023 bytes of
  its own text sealed, and only once its signature has also verified under the
  binding it found, which openWallet's verification reports as
  `signature_verified` with any refusal (D2); otherwise it seals only the
  proof's SHA-256. That keeps
  unsigned bytes a caller chose out of openSig's signed, durable record. The
  flags it records are named as D2 names them.
- **The counter flag** it records is the one the registry recorded for the
  proof's derived challenge (D2).
- **Retries.** openSig compares an identical retry by the proof's canonical
  form. An ECDSA signature is not unique (D3), so a malleated repeat differs and
  is refused, never attested twice.
- **Reasons.** openSig's closed reasons gain those this profile adds: client data
  that does not parse, has a repeated member, or has the wrong type, challenge or
  origin (`client_data_invalid`); `crossOrigin` set (`cross_origin_frame`);
  `topOrigin` present (`top_origin_present`); the relying-party identifier
  (`relying_party_mismatch`); user presence or verification
  (`user_not_verified`); the attested-data flag set (`attested_data_present`);
  backup eligibility changed (`backup_eligibility_changed`); a backup state flag
  set while eligibility is clear (`backup_state_invalid`); an algorithm other
  than the binding's (`algorithm_mismatch`). Authenticator data that does not
  parse, and an algorithm this profile does not admit, are `proof_malformed`. A
  binding that is not current, unrevoked and time valid, or a credential
  identifier other than the binding's, is `binding_not_current`. No existing
  reason is renamed, and with these the list is closed: every refusal of D2 and
  D3 has exactly one reason.

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
fields, `custody_basis` and its values and `holder_declaration` with `declared_at`,
`client` and `sync_account` among them; `identified_session` with `began_at`,
`identification_ref` and `holder_declaration`; the names of the returned flags
and `signature_verified` (D2); and the refusal reasons.

**Code surface**, named here and performed by nothing in this change: a verifier
in openWallet's runtime beside the ratified profile's, reusing its RFC 8785
canonicalizer; P-256 and Ed25519 verification; a proof schema; known-answer
vectors made with independent tooling over derived challenges, on feature 016's
precedent; and the validator's recognition of the P-256 multicodec. Level 3's own
examples (§16) are "not normative", use challenges of their own rather than a
derived one, and several have user verification clear (§16.2, §16.3, §16.9 to
§16.11, the Ed25519 example among them, and §16.14 to §16.16). So they serve only
as signature-level vectors, as negative vectors for user verification, and, for
§16.4 and §16.5, as negative vectors for cross-origin use.

**Release class: an ADDITIVE MINOR**, its coordinated values allocated at
realization, and nothing reserved here.

## Design calls

Every call below goes beyond the owner's words and is PROPOSED, and each is put to
the owner.

| # | Design call | Where |
|---|---|---|
| WP-1 | The challenge is SHA-256 over a domain separator and RFC 8785 of the proof's ten unsigned binding fields, so the proof binds what the ratified profile binds and the relying party; the derived challenge, unpredictable only through the statement's reference, which the challenge issuer must draw at random, 32 bytes, server-side, and use once; exactly one credential per request, which rules out discoverable-credential sign-in; the closed wire form, 8192 bytes, `alg` an integer, client data kept as bytes. | D1 |
| WP-2 | The checks on every use: the binding current, unrevoked and time valid and the only source of the key, the relying-party identifier and the origins; client data with no repeated member; type, challenge, exact origin, no cross-origin use, relying-party identifier hash, user presence and verification always, no attested data, backup flags; the counter and current backup state kept beside the binding, outside its revisioned record; a counter that does not increase flagged and recorded, never refused alone; the returned flags named `user_present`, `user_verified`, `backup_eligible`, `backup_state` and `sign_count_not_increasing`, and a refusal reporting `signature_verified`, checked whenever a binding was found and the proof decoded, never evidence of possession; the counter compared once per derived challenge by the registry, which alone writes it; unknown client data members and extensions ignored. | D2 |
| WP-3 | ES256 and EdDSA with Ed25519 only; `-8` and `-7` offered at registration, `-9` and `-19` recorded as them and refused in a proof; strict encodings, canonical Ed25519 signatures; the raw key form and the P-256 fingerprint over the compressed point, cited against the successor `add-trust-anchors-and-machine-holders` names; no reliance on signature uniqueness. | D3 |
| WP-4 | Binding from a registration and a following proof in the holder's own session; what the binding records, the attestation object, `custody_basis` and `holder_declaration` (`declared_at`, `client`, `sync_account`) among it; one relying party per credential, and more than one credential per deployment allowed. | D4 |
| WP-5 | A party other than the relying party accepts a proof only in a session it began with the holder's client itself, which the relying party neither began nor can join, in which it identified the holder itself, never on evidence a relying domain holds or could obtain, such as copies of documents, the licence number or personal data from its records, by related origins or a native client for a security key, recording its statement of the session, `identified_session`, with the holder's declaration in it; the profile cannot tell whether the client is administered by the relying domain's operator; a relayed proof is never accepted, and carries no marker; what a verifier's binding records, its key from the wallet record or presented with a declared fingerprint, and which checks apply to it; a verifier's origin is never a sign-off origin. | D5 |
| WP-6 | Backup eligibility recorded at registration and backup state on each use; what the profile can and cannot tell, the sync account among it; enrolment is the relying domain's. | D6 |
| WP-7 | A single-device credential may declare `isolated_per_use_authorized`, with the basis of the declaration, `attested` or `declared`, recorded, and `attested` the relying domain's own claim until an honest check verifies the kept attestation object; no multi-device credential is bound while no model of the registry describes it, and no interim model is proposed. | D7 |
| WP-8 | The threat model: what origin binding stops, what a deployment can still do, the conditions under which ruling 214's words hold, and the two cases they do not reach: a client, device or provider the practice administers, and content substitution. | D8 |
| WP-9 | openSig attests proofs under this profile, sealing a passkey proof whole only where its credential identifier and binding revision also match and its signature verified; the closed list of reasons, `backup_state_invalid` added; with the revisions D9 names. | D9 |
| WP-10 | The non-goals. | D10 |
| WP-11 | Placement, names, code surface, what Level 3's examples can serve as, and release class. | D11 |
| WP-12 | A relying domain checks a recorded proof from the proof and what is recorded with it, the proof's signed `alg` serving where the record names no algorithm, against its own relying-party identifier and bound credential where it bound the key, refusing a recorded origin it allows for its own sign-offs, and never relies on a record without the recording party's statement of an identified session. | D5 |

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
   consumer reads the registry and should not have to know to look for a flag.
   What follows from (a): every bound key declares a model, and none describes a
   synced passkey, so until a model that fits is ratified no synced passkey can be
   bound under this profile, and ruling 209's yes for synced passkeys waits on
   this question. This change proposes no interim model. What follows from (b):
   ruling 209's yes for synced passkeys takes effect now, at the cost that the
   registry's statement that such a key "evidences that the HOLDER acted" would
   cover a key that an account takeover reaches.
2. **How does a verifier observe a passkey's proof of possession?** (D5)
   Recommendation: related origins, with a native client for a security key where
   related origins are not available, each only in a session the verifier began
   with the practitioner's client, which the deployment neither began nor can
   join, and in which it identified the licensee itself, by its own means and
   independently of the deployment; and no relayed proof, so that
   no verification names a key on one, since with one ruling 214 would rest on
   the deployment. What follows: a practitioner whose browser lacks related-origin
   support and who uses a platform passkey cannot be verified, because the native
   client option serves security keys only.
3. **Which algorithms?** Recommendation: ES256 and EdDSA with Ed25519 only; add
   RS256 only if a practitioner's platform turns out to need it.
4. **What follows from a counter that does not increase?** Recommendation: a flag
   the relying domain raises to a human, never a refusal on its own. Level 3 says
   that then "a cloned authenticator may exist, or the authenticator may be
   malfunctioning, or a race condition might exist", and that an authenticator
   without a counter leaves it "constant at zero" (§6.1.1).
5. **Which attestation does a relying domain require at registration?**
   Recommendation: record whatever is given, `none` included, record whether a
   key's declared custody rests on accepted attestation evidence (`attested`) or
   on the holder's word (`declared`), and leave what evidence of custody is
   required to openWallet's custody-acceptance successor (the practitioner
   profile's Open question 6).
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
12. **A synced passkey whose account someone else controls or can recover.** (D6,
    D8) This arises only once Open question 1 lets synced passkeys be bound.
    Whoever controls or can recover the account a synced passkey syncs through,
    such as a managed work account the practice administers, can sign with the
    practitioner's own key without the practitioner, and the profile cannot see
    which account holds a passkey. Recommendation: accept it as a stated limit of
    version 1, covered by the second part of the one declaration of Open question
    15; a relying domain may require security keys.
13. **A security key with no PIN or biometric set.** Ruling 209 says "A security
    key always counts", and this profile requires user verification on every use
    (D2), which such a key cannot give; the registry counts "a hardware presence
    check" as per-use authorization. Recommendation: keep user verification on
    every use, so a security key must have a PIN or biometric set to be used for a
    sign-off, because otherwise whoever holds the key can sign.
14. **May a relying domain treat a passkey that cannot sync like a security key?**
    Ruling 209 says "A security key always counts". The backup-eligibility flag
    tells a credential that cannot sync from one that can, but not a security key
    from a passkey kept on one device, or from a software authenticator, without
    attestation (D6, D7). Recommendation: yes, treat a passkey that cannot sync
    like a security key, resting on the flag as the authenticator reports it, with
    the basis of its custody (`attested` or `declared`) recorded beside it so that
    a relying domain can ask for attestation where it wants more. What follows: a
    software authenticator that reports the flag clear would count with no device
    enrolment. The alternative: count a passkey that cannot sync like a security
    key only when its basis is `attested`, which keeps software authenticators
    out but turns away a practitioner whose authenticator gives no attestation
    the domain trusts.
15. **A client, device or passkey provider the practice administers.** (D5, D8)
    Whoever administers or can recover the device, the browser, an extension in
    it, or the passkey provider that the practitioner uses to register a key or to
    complete the verifier's session can answer the verifier's request with a
    credential it registered, and no verifier can tell. Recommendation: accept it
    as a stated limit of version 1. The practitioner registers their keys and
    completes the verifier's session on a device and browser that they control and
    the practice does not administer, declares this, and the declaration is
    recorded with the binding at registration and by the verifier for its
    session. The declaration has two parts: the first covers the device, the
    browser and its extensions used to register a key and to complete a verifier's
    session; the second, for a synced passkey once one can be bound, covers the
    account it syncs through (Open question 12); both are fields of
    `holder_declaration` (D4). A relying domain that needs more can require
    security keys whose attestation the verifier checks, which keeps out software
    credentials but not an operator's own security key answered through an
    administered browser; a key the verifier itself issues and recognizes (for
    instance by enterprise attestation, Level 3 §5.4.7) or binds in its own
    presence would reach that, a later change. What follows: a practitioner whose
    only devices are issued and administered by the practice cannot make the
    declaration truthfully, and needs a device of their own for registering a key
    and for the verifier's session.

## Review record

**An independent review of the first draft at `4d32fa1`: not ready, on two major
findings.** Its findings and how this revision disposes of them:

| Finding | Disposition |
|---|---|
| The binding's state was never required. | Taken: requirement 1 and D2; scenarios for a revoked and an expired binding. |
| The threat model overstated what ruling 214 holds against. | Taken: the identified session (D5, requirement 5), no relayed proof, the synced passkey's account (D8). |
| The derived challenge rested on a reference nothing required. | Taken: the challenge issuer's duty (D1, requirement 1). |
| A counter update revised the binding. | Taken: counter and backup state beside the binding, the flag recorded once (D2). |
| A verifier's binding had no registration behind it. | Taken: what it records and which checks apply (D5). |
| No synced passkey can honestly be bound. | Taken: none is bound until the registry has a model (D7, Open question 1). |
| A clear backup flag does not show isolation. | Taken: `custody_basis` (D7). |
| User verification shuts out a security key with no PIN. | Put to the owner (Open question 13). |
| Client data with a repeated member. | Taken: refused (D2). |
| openSig sealed unsigned passkey bytes. | Taken in openSig-spec#4 (D9). |
| Nits: `alg`, the offered algorithms, the key form, test vectors, the credential list, canonical Ed25519, the trust-anchors successor, the PROPOSED marks. | Taken (D1, D3, D11, the rulings section, `.openspec.yaml`). |

**A confirmation of `fbb74f0`: not ready, on one new major finding.** Its findings
and their dispositions:

| Finding | Disposition |
|---|---|
| The verifier cannot tell whether the client that proves the key is the practitioner's own: an administered browser, extension, device or provider, or a session the deployment can start or join. | Taken: the session the verifier began, which the relying party neither began nor can join, and the profile's statement that it cannot tell (requirement 5, D5); the wider limit (D8); the holder's one declaration (D4); put to the owner (Open question 15). |
| The rule on binding data had no exception for later verifications. | Taken (requirement 1). |
| openSig did not compare `credential_id` and `binding_revision`. | Taken in openSig-spec#4 (D9). |
| The list of reasons was not complete. | Taken: `backup_state_invalid`, three mappings, the list closed (D9). |
| `attested` rests on the relying domain's own record. | Taken: the attestation object kept; `attested` is the domain's claim until checked (D4, D7). |
| The owner's questions were not all stated fairly. | Taken (Open questions 1, 2, 12, 14). |
| Nits: the task list, this record, the presented key, `signature_verified`, the first counter comparison, the recorded algorithm, a recorded origin the domain allows. | Taken (D2, D5, requirements 2, 5 and 9, `tasks.md`). |

**A confirmation of `caad224`: ready, with minor findings.**

| Finding | Disposition |
|---|---|
| Requiring attested security keys was said to reach the administered-client case; attestation shows the kind of authenticator, not whose key it is. | Taken: Open question 15 corrected, and what follows for a practitioner with practice-issued devices only. |
| The practice usually holds the practitioner's credentialing file, so an identification it can pass is a third route. | Taken: the identification never rests on evidence a relying domain holds or could obtain, such as copies of documents, the licence number or personal data from its records (D5, D8, requirement 5). |
| Nits: the declaration's name and shape, the statement of the session, D11's names, requirement 4's list, D5(c), requirement 9. | Taken (D4, D5, D11, requirements 4, 5 and 9). |

## Status

`Status: proposed`. Three reviews have run: an independent review of the first
draft at `4d32fa1`, a confirmation of `fbb74f0`, and a confirmation of `caad224`,
which rated it ready with minor findings; this revision answers each finding of
all three, as the review record states. The first found the quotations of the
Recommendation and the registry exact, and the second confirmed the new ones. `tasks.md` 1.1
schedules a further adversarial review. Ratification is pending, by openWallet's
operator authority, Brett Heap.
