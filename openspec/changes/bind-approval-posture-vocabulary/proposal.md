---
code_surface: ALREADY REALIZED, and no new surface is declared here. The behaviour this text states was realized in the code leg opensoft/openWallet-code by the carve's declared-edit layer under openXwallet's ratified `split-openwallet-neutral-core`, in opensoft/openWallet-code#2, merge `72313daab1f229c049cb90998931564c1904dbbc` (commit A, the pure carve, `32c933551b92d83122a45847215d5ebe92ae6740`; commit B, the declared edits, `75b990dc7ea99823626c18816b37d971f46e341b`; checks `wallet-validation` and `pytest-suite` completed success on `75b990dc`, 37 passed, 1 skipped). That realization is the validator hunks (a)-(e) in `scripts/validate-openxwallet.py`, of which (a) removes the envelope and (b) is the binding this text states, and the corpus binding `contracts/openxwallet/examples/approval-vocabulary.binding.yaml` (RULED Q6). This change performs nothing. Per `release-realization` it archives on that merged, green evidence once ratified.
target_release: unallocated. This change moves no contract byte and no digest, and this leg carries no release identity. The release identity (the manifest, CHANGELOG, release records, proof and tag) is in the assembly root opensoft/openWallet, because the root is the one commit that names both legs (`AGENTS.md`). openWallet's first `wallet-v*` tag is task 4.9 of openXwallet's `split-openwallet-neutral-core`, an operator act. Nothing is reserved here.
Status: proposed
Ratified: pending — held for Brett Heap (openWallet operator authority). The
  substance was ratified with openXwallet's `split-openwallet-neutral-core`
  (`design.md` D8; "ratify 26 and merge", 2026-10-08T17:10:47Z). This
  ENCODING of it is not ratified by its authoring, and only his word
  ratifies it here.
---

# Proposal: bind-approval-posture-vocabulary

## Why

A standalone openWallet has no job envelope to read. Yet the promoted *Agent
authority is grant scope, not a parallel vocabulary* still admits "the
neutral job envelope's `approval_policy` values". That envelope is
openxFactory's hermes job envelope: openxFactory input, which the split
removes from every byte of openWallet a consumer pins or runs.

openXwallet's ratified `split-openwallet-neutral-core` settled the
replacement in its `design.md` D4, RULED Q6 "Document plus pointer, fail
closed (Recommended)": ONE DECLARED VOCABULARY BINDING, a document path plus
a pointer to a mapping whose KEYS are the legal posture terms, supplied by
the consuming layer and read at run time. Its D8 drafted this text.

**Why fail closed.** openxFactory's LOCKED R4 rejected a vocabulary CLI
parameter with no default, because that design ADMITTED on absence. This one
REFUSES on absence: with no binding, every posture is refused.

**This change encodes a ruling. It does not make one.**

## What Changes

One `## MODIFIED Requirements` block, on `openxwallet-agent-profile`, holding
exactly one requirement:

- **MODIFIED `openxwallet-agent-profile` → `Agent authority is grant scope,
  not a parallel vocabulary`.** The title is unchanged, character for
  character. The statement becomes D8's successor text, verbatim:

  > openWallet SHALL express what an agent may do as the SCOPE of a
  > capability grant, and SHALL admit as legal approval-posture terms
  > exactly the keys of ONE DECLARED VOCABULARY BINDING supplied by the
  > consuming layer and read at run time, never restated, so that an
  > agent's authority and a job's approval posture are stated in one
  > vocabulary rather than two kept in agreement. Absent a declared
  > binding, a grant naming any approval posture SHALL be refused.

  Three scenarios, in D8's order:
  - *authority is carried by a grant*: unchanged, bullet for bullet;
  - *the approval vocabulary is reused, not duplicated*: the promoted title,
    kept, with bullets that now name the declared binding instead of the
    envelope's `approval_policy` values. D8 lists this scenario as "the
    bound vocabulary is reused, not duplicated". The promoted title stays
    because the pinned CLI matches scenarios by NAME and refuses a MODIFIED
    block that drops one the promoted spec still has. That refusal was
    measured, and is recorded in `design.md`, "What stays the same";
  - *no binding is declared, so a posture is refused*: NEW. With no binding
    declared, a grant naming any posture is refused, and the posture is not
    admitted on the ground that nothing forbade it.

No capability is added or removed, and no requirement. Eleven promoted
requirements remain eleven.

## What this change does NOT do

- **No other requirement.** The other ten promoted requirements, in both
  capabilities, are untouched.
- **No code.** It performs nothing and declares no new code surface. What
  the text states is already realized (`code_surface`, above).
- **Nothing in the code leg or the assembly root.** No contract, schema,
  corpus file, validator line or test in opensoft/openWallet-code. No
  manifest, CHANGELOG, release record, pin or tag in opensoft/openWallet.
- **No rename.** No `kind:` value, finding code, schema `$id`, filename or
  capability id moves. RULED by Brett Heap, 2026-10-08, "keep the prefix". A
  refusal under no binding reuses the existing code
  `authority-vocabulary-parallel`.
- **It does not touch `add-composition-drift-cascade`.** That change MODIFIES
  a different requirement of the same capability, *A composition change
  revokes the agent's grants immediately*, and it archives on its own.
- **It does not land without Brett Heap's word.** The substance was ratified
  in openXwallet. This encoding of it, in this leg, is ratified only here.

## Impact

- **openXwallet: behaviour unchanged.** It binds the hermes envelope
  unconditionally (D4): the node
  `properties.job.properties.approval_policy.properties` of its vendored,
  digest-verified envelope, the node it reads today, with no flag a caller
  can omit. Its legal terms are exactly the envelope's keys, as before.
- **A standalone consumer must declare a binding.** Without one, every
  posture its grants name is refused. A grant that names no posture is not
  touched by this requirement.
- **The packaged corpus is adjudicated under the corpus binding** in the
  code leg, `contracts/openxwallet/examples/approval-vocabulary.binding.yaml`,
  which names the three keys the corpus uses. Five positives and three
  negatives carry `approval_posture`. A repo scan never reads that binding,
  because a teaching binding must not admit a live record's posture.
- **The text catches up with the code.** The code leg already refuses every
  posture when no binding is declared. Until this change archives, the
  promoted requirement still names the envelope.

## Status

`Status: proposed`. It is not ratified by its authoring. Brett Heap
(openWallet operator authority) ratifies or returns it.

What ratification authorizes: the archive of this change in this leg, with
the pinned CLI (`AGENTS.md` rule 4), which rewrites the promoted requirement
in place. Nothing else. It authorizes no code, no release, no tag and no act
in another repository.

**Provenance.** The successor text was drafted in openXwallet's
`split-openwallet-neutral-core`, `design.md` D8, and its mechanism in D4.
Both were ratified with that packet on opensoft/openXwallet#26 (merge
`bf2dd4db88edbb873d067425b16dacd3784fbaf5`), ruling
https://github.com/opensoft/openXwallet/pull/26#issuecomment-6065121015. That
change is governed on opensoft/openXwallet#25, and this change is its task
4.8. The text this change rewrites arrived here by the carve,
opensoft/openWallet-spec#2 (merge
`15c15bbd451a803f0acdb24e5234836db829a2d3`). The behaviour it states was
realized in opensoft/openWallet-code#2 (merge
`72313daab1f229c049cb90998931564c1904dbbc`).
