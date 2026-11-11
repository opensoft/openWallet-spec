# Tasks: add-trust-anchors-and-machine-holders

Speckit builds these; OpenSpec ratifies them. The realization feature is TO BE
ALLOCATED at handoff (§6). No feature number is reserved here. Every box is
open, because the change is `Status: proposed`.

`[OPERATOR]` = only Brett Heap can perform it. `[GOVERNANCE]` = it needs a
ruling first.

## 1. Governance

- [ ] 1.1 Alignment pass: ONE adversarial reviewer over this packet at
      `Status: proposed`. It reads against the promoted `openxwallet` and
      `openxwallet-agent-profile`, the core contracts, the validator's rules
      (a)–(s) and the packaged corpus. The verdicts go into `design.md` as
      returned, with the disposition of each, as `add-multi-key-wallets` did.
- [ ] 1.2 **[OPERATOR] [GOVERNANCE]** Rule on the fourteen open questions in
      `design.md` ("Open questions for ratification"), by number.
- [ ] 1.3 **[OPERATOR] [GOVERNANCE]** Ratify or return. Brett Heap (openWallet
      operator authority).
- [ ] 1.4 On ratification: `Status: ratified` and a `Ratified:` line carrying
      the ruling's words verbatim in `proposal.md`, plus a ratification record
      in `design.md`. Then re-run the pinned gate (this leg's `AGENTS.md` rule
      4) green. If any delta byte changed after the ruling, re-rule it.

## 2. The schemas — ADDITIVE; one digest moves, one member is new

- [ ] 2.1 `contracts/openxwallet/openxwallet-record.schema.yaml`: the
      `holder.holder_class` enum gains `machine`, APPENDED. Nothing is renamed,
      removed or reordered (design D1). The enum's comment says what a machine
      is and that the custody registry gains no member for it.
- [ ] 2.2 The same file's `description`: the holder classes name `machine`, and
      "never a record of SOMEONE ELSE'S key" gains the sentence that another
      holder's key kept for verification is a TRUST ANCHOR, a separate kind
      held outside the declared key set (design D2).
- [ ] 2.3 The same file's version fields (design D10): the per-file
      `contract_schema_version` moves by one from its value at realization.
      The top-level `schema_version: 1` does NOT move.
- [ ] 2.4 NEW `contracts/openxwallet/openxwallet-trust-anchor.schema.yaml` with:
      - `name: xfactory_wallet_trust_anchor` and
        `contract_id: openxwallet-trust-anchor`;
      - `contract_schema_version: 1`, and a `kind` enum of exactly
        `[xfactory_wallet_trust_anchor]`;
      - `additionalProperties: false` on EVERY object at every depth;
      - no property at any depth that could hold key material (design D2).

      The identifier, DID, `key_fingerprint`, multibase and closed
      `signature_algorithm` grammars are the record schema's, in ONE spelling.
- [ ] 2.5 Top-level fields:
      - REQUIRED `schema_version`, `kind`, `anchor_id`, `owner_wallet_ref`,
        `subject`, `anchor_role`, `keys` and `state`;
      - OPTIONAL `scope` and `created_at`.

      Their shapes:
      - `subject`: REQUIRED `did`; OPTIONAL `holder_class` (the record's closed
        set, descriptive only) and `display_label`. There is NO subject
        identifier property (design D2 invariant 6).
      - `anchor_role`: `issuer` or `peer`.
      - `state`: `active`, `suspended` or `revoked`.
      - `scope`: exactly one property, `names` (unique strings, `minItems: 1`),
        and NO holder-class property (design D4).
- [ ] 2.6 `keys[]` (`minItems: 1`):
      - REQUIRED `key_id`, `public_key_multibase`, `key_fingerprint` and
        `provenance`;
      - OPTIONAL `signature_algorithm`, `state` (absent means `active`),
        `revalidate_by` (date-time) and `display_label`.

      `public_key_multibase` is REQUIRED here and OPTIONAL on a declared key.
      The schema says why: an anchor exists to verify (design D2).
- [ ] 2.7 `keys[].provenance[]` (`minItems: 1`):
      - REQUIRED `method`, from the closed set `out_of_band_fingerprint`,
        `resolver`, `attestation` and `first_use`;
      - REQUIRED `observed_at` and `source` (a bounded string);
      - OPTIONAL `compared_fingerprint`, with a field naming its spelling
        (design D8);
      - `attested_by` (`anchor_ref`, `key_id`), REQUIRED iff
        `method: attestation`.

      The `attested_by` condition may be expressed as a schema conditional or
      left to 3.9. That choice is the realization's, and it is recorded. No
      `verified` boolean exists (design D5).
- [ ] 2.8 Describe IN THE SCHEMA:
      - an anchor is held, never declared, and confers no authority;
      - provenance is per key and append-only, and first use is never rewritten;
      - `revoked` is terminal;
      - the anchored DID is a trust fact and not a subject identifier;
      - which of the three fingerprint spellings `key_fingerprint` is
        (design D8).
- [ ] 2.9 Confirm, BY RECOMPUTATION, that no other digested contract byte
      moves: the custody registry and its schema, the grant, the exercise, the
      distinct-holder constraint, the subject attestation and the agent
      composition. The custody registry is NOT edited (design D1).

## 3. The validator — `scripts/validate-openxwallet.py`

- [ ] 3.1 `KIND_TO_SCHEMA` gains `xfactory_wallet_trust_anchor`, and
      `_ID_FIELDS` gains `anchor_id`. Duplicate anchors are refused under the
      EXISTING `record-id-duplicate`.
- [ ] 3.2 `Context` indexes anchors by owner, and anchored keys by (owner,
      fingerprint). Anchored keys are NEVER indexed into `wallets_by_key`, and a
      test asserts it, so rule (r) refuses an exercise presented by an anchored
      key under the EXISTING `presenting-key-unresolved` (design D2 invariant
      2). The new index is type-guarded like the existing one, which runs
      before schema validation.
- [ ] 3.3 Rule (a) runs over the new kind unchanged (`key-material-embedded`).
      Confirm that no new property name contains a `_KEY_NAME_TOKENS` token,
      and that `_KEY_NAME_ALLOW` needs no edit.
- [ ] 3.4 NEW `trust-anchor-owner-unresolved`: `owner_wallet_ref` resolves to no
      wallet in the adjudicated tree. It is refused rather than passed over,
      because every owner-scoped check below would otherwise never run. That is
      rule (q)'s reasoning for `composition-wallet-unresolved`.
- [ ] 3.5 NEW `trust-anchor-in-declared-set`: an anchored key is a member of
      `declared_keys(owner)`, matched by fingerprint, by
      `public_key_multibase`, or by (`subject.did`, `key_id`) (design D2
      invariant 1). The message names the pair-only limit for a primary key
      that declares neither field.
- [ ] 3.6 NEW `trust-anchor-key-duplicate`: one owner holds one fingerprint more
      than once, within one anchor or across its anchors (design D2 invariant
      4).
- [ ] 3.7 Two NEW scope checks:
      - `trust-anchor-issuer-unscoped`: an `issuer` anchor with no
        `scope.names`;
      - `trust-anchor-peer-scope-widened`: a `peer` anchor whose `scope.names`
        holds a pattern.

      The glob semantics (`*` matches any run of characters, `?` matches one)
      are pinned in the module docstring (design D11.9).
- [ ] 3.8 NEW `trust-anchor-first-use-unbounded`: an anchored key with no
      establishing provenance entry and no `revalidate_by` (design D5).
- [ ] 3.9 Three NEW provenance checks:
      - `trust-anchor-issuer-self-evidenced`: an `issuer` anchor key with no
        `out_of_band_fingerprint` entry and no admissible `attestation` entry;
      - `trust-anchor-attestation-unresolved`: `attested_by` names no anchor
        key held by the SAME owner;
      - `trust-anchor-attestation-unverified`: the attester rests on no
        establishing evidence, or does not cover the attested subject.

      Establishment is computed as a least fixed point, so a cycle establishes
      nothing. Admissibility does NOT read the attester's CURRENT state
      (design D5).
- [ ] 3.10 NEW `trust-anchor-leaf-unbounded`: a peer anchor whose
      `scope.names` fall within an ACTIVE issuer anchor of the same owner, with
      a key that lacks `revalidate_by` (design D3). A peer anchor that names no
      names is reported in a NOTE as not shown to be covered.
- [ ] 3.11 NEW `trust-anchor-fingerprint-mismatch`: for an ed25519 anchored
      key, `key_fingerprint` must recompute from `public_key_multibase` through
      the multi-key decoder. Any other algorithm gets a NOTE, never a refusal
      and never a warning (design D8).
- [ ] 3.12 Rule (q) is unchanged. A composition for a `machine` wallet is
      refused under the EXISTING `composition-on-non-agent` (design D1, D9).
- [ ] 3.13 `REQUIREMENTS` gains four rows, one per ADDED requirement: proposed
      `OXW-R9` to `OXW-R12`, in the delta's order. `OXW-R1`, `OXW-R2` and
      `OXW-R8` keep their ids and titles, because MODIFIED keeps the subject.
      Requirement closure stays two-directional.
- [ ] 3.14 Module docstring: the new rules get NEW letters after (s), and no
      rule letter is reassigned. The "WHAT THIS VALIDATOR DELIBERATELY DOES NOT
      DO" paragraph stays true: it verifies no signature and resolves no DID.
- [ ] 3.15 No finding code is renamed, repurposed or reclassified, and there is
      no new WARNING. Assert it by diffing the code inventory before and after:
      exactly the eleven NEW ERROR codes of 3.4–3.11 and zero new warnings.
      The eleven are `trust-anchor-owner-unresolved`,
      `trust-anchor-in-declared-set`, `trust-anchor-key-duplicate`,
      `trust-anchor-issuer-unscoped`, `trust-anchor-peer-scope-widened`,
      `trust-anchor-first-use-unbounded`,
      `trust-anchor-issuer-self-evidenced`,
      `trust-anchor-attestation-unresolved`,
      `trust-anchor-attestation-unverified`, `trust-anchor-leaf-unbounded` and
      `trust-anchor-fingerprint-mismatch`. They are proposed names, and the
      alignment pass (1.1) may merge them. The mail grant (design D12) adds
      no code: its probes fire under existing codes (4.12).

## 4. The corpus — positives, one negative per new invariant, named probes

- [ ] 4.1 POSITIVE: Eagle's machine wallet. Holder class `machine`.
      `key_reference` is the Windows OpenSSH host key and one `keys:` entry is
      the WSL sshd host key, both `holder_readable`, each fingerprint
      recomputing from its `public_key_multibase` (design D1, D7).

      A SECOND `keys:` entry is the Graph client certificate's key, Eagle's
      THIRD declared key. It carries:
      - `isolated_invocable` custody;
      - a `did:web` under the tenant, with its own `key_id`;
      - a `key_fingerprint`;
      - NO `public_key_multibase`, because an RSA public half does not decode
        as ed25519 and is refused under `declared-key-fingerprint-mismatch`;
      - NO `signature_algorithm`, because `PS256` is in no closed algorithm
        set (design D12, D11.18).

      The wallet's own `custody` stays `holder_readable`, so no declared key
      outranks it.
- [ ] 4.2 POSITIVE: Eagle's user-CA issuer anchor. Owned by Eagle's wallet,
      with the tenant CA's DID as subject and the principals it may certify as
      scope. Its provenance is `out_of_band_fingerprint` (source
      `step ca bootstrap`) PLUS a `resolver` confirmation entry, proving that
      confirmation beside establishment validates (design D5).
- [ ] 4.3 POSITIVE: Raven's wallet (holder class per design open question 8)
      and its host-CA issuer anchor scoped to `eagle`, `*.lan` and
      `192.168.1.*`, with `out_of_band_fingerprint` provenance. Also ONE peer
      anchor for a public code host: subject `did:key` of its own key, literal
      names outside the issuer's scope, provenance `out_of_band_fingerprint`
      from the host's published fingerprints.
- [ ] 4.4 POSITIVE: a rotated issuer root. The retired key (`state: revoked`)
      stays beside its replacement, whose provenance is an `attestation` by the
      retired key. This proves that retirement does not unmake an attestation
      made while the attester was in force (design D5).
- [ ] 4.5 NEGATIVES, one per invariant, each with `# expected_failure:`, an
      `# expected_failure_detail:` pin wherever the generic `schema` finding
      would otherwise swallow it, and a `# requirement:` attribution.

      Attributed to `OXW-R9`:
      - an anchored key in its owner's declared set →
        `trust-anchor-in-declared-set`;
      - an owner that does not resolve → `trust-anchor-owner-unresolved`;
      - one key held twice → `trust-anchor-key-duplicate`;
      - an issuer anchor without scope → `trust-anchor-issuer-unscoped`;
      - a peer anchor scoped by a pattern → `trust-anchor-peer-scope-widened`;
      - a fingerprint that does not recompute →
        `trust-anchor-fingerprint-mismatch`;
      - an anchor carrying a grant-shaped property → `schema`, detail-pinned;
      - an anchor carrying a private key → `key-material-embedded`;
      - an exercise presented by an anchored key → `presenting-key-unresolved`.

      Attributed to `OXW-R10`:
      - a cached leaf under an issuer with no staleness bound →
        `trust-anchor-leaf-unbounded`.

      Attributed to `OXW-R11`:
      - an anchor scoped by holder class → `schema`, detail-pinned.

      Attributed to `OXW-R12`:
      - first use without a deadline → `trust-anchor-first-use-unbounded`;
      - an issuer anchor resting only on its own published record →
        `trust-anchor-issuer-self-evidenced`;
      - an attestation by an anchor the owner does not hold →
        `trust-anchor-attestation-unresolved`;
      - an attestation by an anchor resting on first use alone →
        `trust-anchor-attestation-unverified`.

      Attributed to `OXW-R8`:
      - an anchor naming a subject identifier → `schema`, detail-pinned.

      Attributed to `OXWA-R1`, in the agent-profile corpus:
      - a composition declared for a machine wallet →
        `composition-on-non-agent`.
- [ ] 4.6 Every new `wallet_id`, `anchor_id`, declared `key_id` and anchored
      fingerprint is DISJOINT from the packaged corpus. The disjointness is
      ASSERTED in pytest, not assumed (`add-multi-key-wallets` 3.12).
- [ ] 4.7 The fixtures' public halves are FIXTURE VALUES, derived
      deterministically from each file's own labels, as
      `wallet-agent-council-multi-key.example.yaml` does. Nobody holds a
      private half, no live surface references them, and the real Eagle and
      Raven keys never enter the neutral corpus.
- [ ] 4.8 NAMED-PROBE assertions for every new fixture that attributes to an
      EXISTING code (`presenting-key-unresolved`, `composition-on-non-agent`,
      `key-material-embedded`, the detail-pinned `schema` cases). Requirement
      closure cannot notice a deleted fixture there (`add-multi-key-wallets`
      3.13).
- [ ] 4.9 pytest coverage under `tests/trust_anchors/` for:
      - each new code;
      - the never-indexed assertion (3.2);
      - the attestation fixed point, including a cycle and a rotation;
      - the algorithm-conditional NOTE;
      - the glob semantics.
- [ ] 4.10 POSITIVE: the mail grant (design D12). It is an
      `xfactory_wallet_grant` with:
      - `audience.wallet_ref` Eagle's wallet (4.1), and
        `audience.holder_ref: machine:eagle`;
      - `scope.acts: [read_mail]` and
        `scope.objects: [mailbox:opensoft.dev/eagle]`;
      - `scope.authority_tier: attest`, per design open question 12;
      - NO `approval_posture`;
      - an `expires_at`, `issued_by: opensoft` and `state: active`.

      It validates in the packaged corpus AND in a standalone repo scan with no
      vocabulary binding, which is how the tenant runs it (design D12,
      finding 2).
- [ ] 4.11 POSITIVE: one custodian exercise of 4.10 (design D12, open
      question 13), with:
      - `act: read_mail` and `object_ref: mailbox:opensoft.dev/eagle`;
      - `event_class: authenticated`;
      - a proof block with `presented: true`, `verified: true`,
        `signed_over: request`, `presenting_key_ref` the certificate's key,
        and NO `signature_algorithm`;
      - `key_attributed` attribution naming the same key, Eagle's wallet and
        `machine:eagle`;
      - `custody_model_in_force: isolated_invocable`;
      - a revocation check performed at exercise, with result `active`;
      - `outcome: permitted`.

      Its comment says that the signature is over the token request and that
      the Graph reads within the session ride the bearer token.
- [ ] 4.12 NEGATIVES, under EXISTING codes only, with no new code (design D12,
      finding 6):
      - **A grant whose `audience.wallet_ref` is the mailbox identifier**
        `mailbox:opensoft.dev/eagle` → `custody-ceiling-unresolved`,
        detail-pinned (`does not resolve to a wallet`), with
        `# requirement: OXW-R2`. It is the first packaged fixture for that
        code.
      - **The mail grant at `act_unsupervised`** → `custody-ceiling-exceeded`,
        detail-pinned (`Raising authority requires changing custody`), with
        `# requirement: OXW-R4`. The per-key `presenting-key-evidence-cap`
        CANNOT be provoked through Eagle, whose three keys all cap at `act`,
        the wallet's own ceiling, and the fixture's comment says so.
      - **The exercise of 4.11 recording the primary key's `holder_readable`
        as the custody in force** → `custody-model-mismatch`, detail-pinned on
        the certificate key's `key_id`, with `# requirement: OXW-R4`.
- [ ] 4.13 NAMED-PROBE assertions for the three 4.12 fixtures. Each attributes
      to a requirement that other fixtures already cover (as in 4.8). 4.6's
      disjointness assertion covers every new mail `grant_id`, `exercise_id`
      and `key_id`.
- [ ] 4.14 pytest coverage, under `tests/machine_holders/` or beside 4.9's,
      for:
      - the positive trio (4.1, 4.10, 4.11) validating in a standalone repo
        scan;
      - each 4.12 negative firing its code;
      - the KNOWN GAPS (design D11.15–17).

      Each known gap is a strict `xfail` asserting the behaviour its successor
      would bring, so that closing one turns the test red until it is
      promoted:
      - an object `eagle@opensoft.dev` being admitted;
      - an exercise naming another mailbox under 4.10 being refused;
      - a derived grant narrowing to `mailbox:opensoft.dev/eagle/inbox` being
        admitted.

## 5. Docs and release bookkeeping — at realization

- [ ] 5.1 `contracts/openxwallet/README.md`:
      - the holder-class sentence names `machine`;
      - the record-kinds table gains `xfactory_wallet_trust_anchor`;
      - "What this family deliberately does not do" says it still verifies no
        signature and resolves no DID, and that consumers verify offline
        against held anchors;
      - a sentence saying that a grant's audience may be a machine's wallet,
        and that a resource's own access control is the grant's realization,
        never a wallet field (design D12).

      No digest impact: the README is pinned by commit only.
- [ ] 5.2 Root `contracts/manifest.yaml`:
      - a NEW owned row `openxwallet-trust-anchor`, with `path`
        `code/contracts/openxwallet/openxwallet-trust-anchor.schema.yaml`,
        `source_path`, `type: schema`, `schema_version: 1` and a `sha256:`
        computed from the tree;
      - the `openxwallet-record` row's `sha256:` and `schema_version`
        refreshed;
      - every other row PROVEN unchanged by recomputation;
      - the counts of owned rows in the manifest's comments corrected;
      - the packaged-corpus counts in the same comments (`21 valid + 42
        intended-invalid` today) corrected for every fixture §4 adds;
      - `contract_bundle_version` set to the version allocated at realization
        (design D10).
- [ ] 5.3 Root `contracts/CHANGELOG.md`. The entry states:
      - the change class (ADDITIVE MINOR);
      - the moved digest and the new member;
      - the new codes;
      - the new `holder_class` value;
      - that anchor records written before the pin bump are skipped;
      - what a consumer must do.
- [ ] 5.4 The root release record is cut by recomputation. It selects the new
      member by `member_class` like every owned row. The annotated tag is the
      operator's act, after the proof is green (root `AGENTS.md` rule 5).
- [ ] 5.5 Each leg advance lands at the root as ONE commit moving the gitlink,
      `contracts/<role>-pin.yaml` and every workflow `@<sha>` together
      (`AGENTS-shape.md`).
- [ ] 5.6 `openspec/specs/openxwallet/spec.md` `## Purpose`: the list of what the
      capability owns gains the trust anchor. NO DELTA FORM REACHES
      `## Purpose` (`add-multi-key-wallets` alignment item 12), so this is an
      editorial correction made at archive and ratified by this change.
- [ ] 5.7 The full gate bar is green:
      - in the code leg, the syntax gate, the validator plain AND `--strict`,
        and `pytest tests/ -q`;
      - in this leg, the pinned gate (`AGENTS.md` rule 4), ending
        `OK openspec-cli-pin`;
      - at the root, `make validate`.

## 6. Speckit handoff

- [ ] 6.1 Hand off to exactly ONE Speckit feature in this leg,
      `specs/NNN-trust-anchors-and-machine-holders/`. Its number is TO BE
      ALLOCATED at handoff. The feature is worked in
      `worktrees/<NNN-feature-name>/{spec,code}/` under the assembly root.
- [ ] 6.2 `/speckit-tasks` tags every build task `[H]`, `[S]` or `[O]`. §2 and §3
      change a digested contract and the validator's rules, which the `[H]`
      tier's agent definition excludes.
- [ ] 6.3 Archive this change only after the realization lands and the root pin
      bump carrying it has merged (protocol "Lifecycle", step 7), with the
      binary the pinned installer prints (`AGENTS.md` rule 4).

## 7. Consumer completion — the Eagle and Raven tenant (tracked here, executed there)

- [ ] 7.1 Eagle's machine wallet and its user-CA anchor, recorded with the REAL
      host keys' fingerprints in the family's spelling (design D8) and
      validated by the pinned validator in the tenant's own gate.
- [ ] 7.2 Raven's wallet and its host-CA and peer anchors. `TrustedUserCAKeys`
      and the `@cert-authority` line are materialized from those records
      (design D7).
- [ ] 7.3 The tenant's pin moves to the release carrying this change, so its
      anchor records are adjudicated rather than skipped (design D10).
- [ ] 7.4 The mailbox `eagle@opensoft.dev` (design D7, D12).

      The Microsoft 365 side needs nothing from this change, and may come
      first:
      - the shared mailbox;
      - the Entra app, with application `Mail.Read` only and a certificate
        credential;
      - the access-policy realization, or RBAC for Applications (design open
        question 14);
      - the certificate, non-exportable in Eagle's TPM-backed machine store.

      Once the release is pinned:
      - Eagle's wallet record declares the real certificate key as its third
        key;
      - the mail grant is recorded, `issued_by` the tenant's operator;
      - the custodian records its exercises (design open question 13).

      None of these records carries key material or the Entra and Exchange
      configuration.

## 8. Named successors — NOT taken here (design D11)

- [ ] 8.1 A machine profile: hardware attestation, a TPM endorsement-key
      inventory, enrolment evidence.
- [ ] 8.2 A verification-event record kind, which would make revocation at use
      statically probeable.
- [ ] 8.3 A diff-time append-only check: `revoked` never returns to `active`,
      and no anchored key or provenance entry is deleted or rewritten.
- [ ] 8.4 Fingerprint encodings for non-ed25519 algorithms.
- [ ] 8.5 Recording an SSH session as a key-attributed exercise, which is
      blocked on the ephemeral certificate key.
- [ ] 8.6 A revocation-list carrier.
- [ ] 8.7 Anchor sets shared across wallets.
- [ ] 8.8 A scope grammar beyond literal names and `*`/`?` globs.
- [ ] 8.9 Propagating a compromised anchored key's revocation to the keys it
      attested.
- [ ] 8.10 A mailbox subject-attestation record that carries Eagle's wallet
      reference as attestation (design D11.14). It is named, not built.
- [ ] 8.11 An object grammar that admits a mail address in `scope.objects` and
      `object_ref` (design D11.15).
- [ ] 8.12 Binding an exercise's `object_ref` to its grant's `scope.objects`
      in rule (r) (design D11.16).
- [ ] 8.13 Object containment in attenuation, such as a folder within a
      mailbox (design D11.17).
- [ ] 8.14 RSASSA-PSS in the closed signature-algorithm sets (design D11.18).
- [ ] 8.15 A confidentiality axis on the authority ladder (design D11.19).
