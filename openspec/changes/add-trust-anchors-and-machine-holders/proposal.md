---
code_surface: openWallet code leg (`opensoft/openWallet-code`) — `contracts/openxwallet/openxwallet-record.schema.yaml` (ADDITIVE, `machine` joins the closed `holder_class` enum), a NEW `contracts/openxwallet/openxwallet-trust-anchor.schema.yaml` (kind `xfactory_wallet_trust_anchor`), `scripts/validate-openxwallet.py` (one new kind, new ERROR codes in a `trust-anchor-*` family, four new requirement rows, no rename, no new warning), the packaged corpus and `contracts/openxwallet/README.md`; and at the assembly root the bookkeeping of a release (a moved digest, a NEW owned manifest member, the CHANGELOG entry, the release record). The custody registry is NOT touched. Per `release-realization`, this change archives only on merged, green realization evidence for that surface.
target_release: unallocated. The realization is expected to be an ADDITIVE MINOR in which one digested contract byte moves (`openxwallet-record`) and one owned member is added (`openxwallet-trust-anchor`), so every consumer's pin moves with it. Per the root AGENTS.md rule 5 the five coordinated values are allocated at realization and nothing is reserved here.
Status: proposed
Discussed: 2026-10-16, Brett Heap with Claude (Fable 5.1) in session, while designing SSH access between the workstations Eagle and Raven with a Smallstep SSH CA and Keycloak; ratification pending.
---

# Proposal: add-trust-anchors-and-machine-holders

## Why

Two workstations are being joined for SSH with a Smallstep SSH certificate
authority. Eagle is a server running TWO SSH daemons — Windows OpenSSH and a
Linux sshd inside WSL — each with its own host key, on its own port. Raven is a
client. A user CA signs short-lived user certificates after a Keycloak (OIDC)
login, and a host CA signs each daemon's host key.

The question that stopped the design was where the host CA's root public key
lives on Raven. The answer reached in the discussion was: in Raven's wallet, as
ONE entry that vouches for every host the CA signs. The standard has no place
for that entry, and the reason is three gaps rather than one:

1. **Another holder's key has nowhere to go.** "A wallet is a key, never a
   record of a key" is correct and load-bearing: every key in a wallet's
   declared set is one its own holder holds. The CA's root is not Raven's key,
   so it cannot be a declared key, and nothing else in the family holds a key.
2. **A computer is not a holder.** The closed `holder_class` set is person,
   practitioner, organisation and agent. Eagle holds two host keys in its own
   right and is none of those.
3. **Nothing says how verification works.** The core says what a signature
   evidences. It says nothing about verifying another party's credential
   against keys the verifier already holds, that doing so needs no network, or
   that the verifier must not care who presents.

The third gap is not abstract. The tenant has ruled that this CA issues no
agent credentials, and the obvious place to enforce that, Eagle, is the wrong
one. Eagle does not care whether a caller is a person or an agent, only whether
its credential verifies and what it is authorized for. That is the existing
rule "Agent authority is grant scope, not a parallel vocabulary", seen from the
resource's side, and the standard does not yet say it.

## What was discussed

The design was worked through in session on 2026-10-16 by Brett Heap with
Claude, while laying out SSH access between Eagle and Raven. **Nothing here is
ruled.** The change is `Status: proposed` and awaits ratification by openWallet's
operator authority. What the discussion settled as the design to propose:

- **A computer is a holder.** `machine` joins the closed holder-class set. A
  machine wallet declares its service keys with the existing multi-key shape —
  Eagle is ONE wallet whose two declared keys are its two sshd host keys — and
  their custody needs no registry change: a root-owned key file is
  `holder_readable`, a TPM-resident key the OS may invoke freely is
  `isolated_invocable`, and both evidence the environment (`design.md` D1).
- **Trust anchors are HELD, never declared.** A new core record kind, the
  wallet's "contact list": owned by one wallet, naming ANOTHER holder's public
  keys, with a role (`issuer` for a root that vouches for a scoped population,
  `peer` for one holder's own key), a scope, per-key provenance, a staleness
  bound and an append-only state. It is never in the owner's declared key set
  and confers no authority on anyone (D2).
- **Verification is offline against held anchors.** The issuer is consulted at
  issuance only. Roots are held, not leaves. Revocation is checked at use from
  the credential's validity window and the anchor's state, and short lifetimes
  are the primary revocation mechanism (D3).
- **The verifier is holder-class blind.** A resource decides from the
  credential, the held anchor, a local principal mapping and the credential's
  hard limits. Whether an agent may obtain a credential is issuance policy, and
  that is where a "no agent credentials" rule lives (D4).
- **An unknown holder is validated before it is trusted.** The first anchor
  arrives out of band. An issuer's self-published record confirms and never
  establishes. First use is labelled, bounded and never laundered into
  "verified" (D5).
- **Enrolment of a machine with an issuer** is the issuer's record, not the
  wallet's: no new record field (D6, non-normative).
- **The worked consumer mapping, SSH with Smallstep**, is recorded so the
  standard's terms can be checked against a real deployment (D7, non-normative).

Explicitly NOT in this change, and named so nobody reads them into the delta:
a change to the closed custody registry; a machine PROFILE (hardware
attestation, enrolment evidence); a use-time verification record; any change to
`Revocation propagates through the chain`, which the active change
`add-composition-drift-cascade` already MODIFIES; and recording an SSH session as
a key-attributed exercise. See `design.md` D11.

## What Changes

Two `## MODIFIED Requirements` and four `## ADDED Requirements` on the existing
capability `openxwallet`. No new capability, and no change to
`openxwallet-agent-profile` (`design.md` D9). One new record kind; no renamed
machine key.

1. **MODIFIED "A wallet is a key, never a record of a key".** The holder classes
   gain `machine`, with what a machine is and the rule that the closed custody
   set gains no member for it. The requirement now says outright that another
   holder's key that a wallet keeps for verification is a trust anchor held
   OUTSIDE the declared key set. The existing five scenarios are kept, one of
   them extended to name `machine`. Two are added: a machine declaring its
   service keys as one wallet, and a machine's service key classified by the
   existing closed custody set.
2. **MODIFIED "The capability is an authority control, never an identity
   substrate".** Gains one sentence and one scenario: an anchor is a trust fact
   about a key, never an identity. Its identifier never becomes a subject
   identifier, and a domain with no wallets and no anchors stays conformant.
3. **ADDED "Trust anchors are held, never declared"** (D2).
4. **ADDED "Verification is offline against held anchors"** (D3).
5. **ADDED "A verifier is blind to holder class"** (D4).
6. **ADDED "An unknown holder is validated before it is trusted"** (D5).

## Backward compatibility

**Every existing record remains valid, unchanged.** The schema changes are
ADDITIVE:

- `holder_class` gains one enum member, `machine`. No member is renamed,
  removed or reordered, and no record that validates today stops validating.
- `xfactory_wallet_trust_anchor` is a NEW kind that no existing record uses.
  A domain that writes none is refused by nothing, because the non-substrate
  rule now covers anchors as it covers wallets.
- The closed custody registry and its schema are not touched. The two members
  a machine's service keys fall under already exist (D1).
- No finding code is renamed, repurposed or reclassified, and no new WARNING
  is introduced, because LedgerxFactory runs this validator with `--strict`,
  where a warning is an exit code. The new codes are ERRORs in a
  `trust-anchor-*` family. Facts the validator cannot check are reported as
  NOTES (D8).

**Digested contract bytes move.** `openxwallet-record.schema.yaml` changes, so
its `sha256:` in the root's `contracts/manifest.yaml` and in every consumer's
pin moves. A NEW owned member, `openxwallet-trust-anchor.schema.yaml`, joins the
manifest. The other owned rows are unchanged, and that is to be proven by
recomputation at realization rather than asserted (D10).

**One behaviour to know about at the pin bump:** a consumer that writes anchor
records BEFORE moving its pin finds them SKIPPED rather than refused, because
the validator's repository sweep adjudicates only the kinds it knows. The pin
bump is what brings them under adjudication (D10). A consumer that matches
`holder_class` exhaustively in its own code meets one new value.

## Impact

- **openWallet code leg**: one additive schema edit, one new schema, a
  validator extension (one new kind, the `trust-anchor-*` codes, four new
  requirement rows), corpus additions, README.
- **openWallet assembly root**: a MINOR release whose number is allocated at
  realization: the moved `openxwallet-record` digest, a new owned manifest row,
  the CHANGELOG entry and the release record.
- **openWallet spec leg**: this change, then its Speckit feature (number to be
  allocated at handoff), then the `## Purpose` editorial update that no delta
  form reaches (`tasks.md` 5.6).
- **openXwallet, openxFactory, LedgerxFactory, MedxFactory and other pinning
  consumers**: a pin bump when they next re-sync. Nothing they declare becomes
  invalid. openXwallet's factory-layer "issuer anchor" for review authority is
  a different concept from the `issuer` anchor role here, and nothing of it
  moves (D2).
- **The consuming tenant (Eagle and Raven)**: can record Eagle's machine wallet
  and Raven's anchors once a release carrying this is pinned. Nothing in its
  SSH setup waits on this change, because sshd needs only the materialized
  files (`TrustedUserCAKeys`, `@cert-authority`), whose mapping is D7.
