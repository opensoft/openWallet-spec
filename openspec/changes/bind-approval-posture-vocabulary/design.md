# Design: bind-approval-posture-vocabulary

## Context

This is the first change authored natively in this leg's OpenSpec instance.
Everything else in the instance arrived by the carve. opensoft/openWallet-spec#2
(merge `15c15bbd451a803f0acdb24e5234836db829a2d3`) brought it from
opensoft/openXwallet at the carve commit
`90111df262d6f54f7e82651d860adc12345f83f4`:

- the promoted capabilities `openxwallet` and `openxwallet-agent-profile`;
- the archive records of `add-openxwallet` and `add-multi-key-wallets`;
- the active change `add-composition-drift-cascade`.

The carve's only prose edit to the promoted specs was the eleven requirement
subjects, `openXwallet SHALL` to `openWallet SHALL`.

That left one requirement true in openXwallet and untrue here. *Agent
authority is grant scope, not a parallel vocabulary* says openWallet admits
"the neutral job envelope's `approval_policy` values", and openWallet holds
no envelope. openXwallet's ratified `split-openwallet-neutral-core` planned
for this before the carve:

- its D4, "The vocabulary binding", encodes the mechanism, RULED Q6;
- its D8, "Spec movement", drafts the successor text and gives it to this
  leg's birth change;
- its own delta, which retires the requirement from openXwallet, names the
  one difference in its Migration note: the legal terms become the keys of
  one declared binding supplied by the consuming layer, and a posture is
  refused when no binding is declared.

The code moved first. The code leg's declared-edit layer, commit B
`75b990dc7ea99823626c18816b37d971f46e341b` inside opensoft/openWallet-code#2,
already does what this text will say. Hunk (a) removed the envelope, hunk (b)
reads the vocabulary from one declared binding, and the corpus binding was
added beside the corpus. So this change writes down behaviour that is merged
and green. It builds nothing.

## The text, and why each clause is there

D8's successor text, clause by clause, against D4.

**"openWallet SHALL express what an agent may do as the SCOPE of a capability
grant"**: unchanged. Authority lives in a grant's scope and nowhere else.
Scenario one states it.

**"and SHALL admit as legal approval-posture terms exactly the keys of ONE
DECLARED VOCABULARY BINDING"**: D4's form. A binding is a document path plus
a pointer to a mapping, and the KEYS of that mapping are the legal posture
terms. Each term's `type` is read as it was read from the envelope.
"Exactly" cuts both ways: every key the binding holds is legal, and nothing
else is. "ONE" means a consumer binds one vocabulary, not a union of several.

**"supplied by the consuming layer and read at run time, never restated"**:
the vocabulary is not openWallet's to name. openWallet holds no constant
listing posture terms, and no default binding. Either would be a second
vocabulary that nobody declared, which is what rule (g) exists to refuse
(see "Rejected"). Reading at run time is what keeps the bound terms and
their source from drifting apart: there is no copy to go stale.

**"so that an agent's authority and a job's approval posture are stated in
one vocabulary rather than two kept in agreement"**: the purpose, unchanged
in substance. The promoted text says "two that must be kept in agreement".

**"Absent a declared binding, a grant naming any approval posture SHALL be
refused."**: fail closed.

- With no binding the vocabulary is EMPTY. Rule (g) then refuses every key of
  every `approval_posture`, under the EXISTING code
  `authority-vocabulary-parallel`.
- No posture escapes. The grant schema already requires `minProperties: 1` on
  `approval_posture` (`contracts/openxwallet/openxwallet-grant.schema.yaml`,
  in the code leg), so a posture that is present names at least one key, and
  every key is refused.
- A grant that names no posture is outside the sentence.
- The run emits ONE NOTE saying no vocabulary is bound. It is a note and
  never a warning, because every consumer runs `--strict`.

## What stays the same

- **Scenario one, verbatim.** *authority is carried by a grant* keeps its
  three bullets byte for byte.
- **Scenario two's title.** D8 lists this scenario as "the bound vocabulary
  is reused, not duplicated". The delta keeps the promoted title, *the
  approval vocabulary is reused, not duplicated*, and changes only its
  bullets. The pinned CLI decides this. `@fission-ai/openspec@1.12.0`
  compares a MODIFIED block's scenarios with the promoted requirement's BY
  NAME, and both `validate --strict` and `archive` refuse a block that drops
  one. Measured at authoring, in a scratch copy of this leg, with the title
  as D8 lists it, `validate` printed:

  ```
  ✗ [ERROR] openxwallet-agent-profile/spec.md: MODIFIED "Agent authority is grant scope, not a parallel vocabulary" omits scenario(s) the current spec still has: "the approval vocabulary is reused, not duplicated". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
  ```

  `archive` refused the same scenario and printed "Aborted. No files were
  changed." With the promoted title kept, both pass. 1.12.0 offers no other
  route:
  - a MODIFIED block cannot rename a scenario;
  - REMOVED plus ADDED of one requirement in one delta is refused as a
    conflict;
  - a requirement RENAMED is checked against the block it was renamed from,
    and this requirement's title must not move anyway.

  The scenario's SUBSTANCE is D8's: the posture's keys are the declared
  binding's, read at run time and never restated. Only its name is the
  promoted one, and "the approval vocabulary" still names what is reused.
- **The finding code.** `authority-vocabulary-parallel` does not move, and no
  code is added. A posture refused for want of a binding is reported as a
  parallel vocabulary, because with nothing bound, that is what it is.
- **The prefix.** No `kind:` value, finding code, schema `$id`, filename or
  capability id is renamed. RULED "keep the prefix". The capability stays
  `openxwallet-agent-profile`.

## Rejected

D4's three alternatives, for D4's reasons:

- **Vendoring the envelope into openWallet**, so that the corpus and
  standalone consumers could keep reading it. That is the openxFactory input
  the ruling removes.
- **A default binding.** A default is a second vocabulary nobody declared,
  and it would admit on absence: openxFactory's R4 failure in a new place.
- **Restating the keys as a core constant.** That is the parallel vocabulary
  rule (g) exists to refuse, written into the core that enforces it.

## What this design does not decide

- **The binding document's form.** The packet left "the exact spelling of
  the binding's CLI form" and "the corpus binding's filename" to its plan.
  Both belong to the code leg, and both are already realized. A caller's
  binding is a `document`, a `pointer` and an optional `label`. The corpus
  binding is `contracts/openxwallet/examples/approval-vocabulary.binding.yaml`,
  pointer `approval_posture_terms`. The requirement states the obligation,
  not that shape.
- **The adapter's own rules.** How openXwallet binds the envelope, verifies
  its copy and exits when the file is absent belongs to openXwallet's
  capability `openxwallet-factory-binding`, realized in that repository.
- **Two prose residuals in the code leg, observed and not taken on:**
  - Rule (g)'s refusal message still says the key "is not an
    `approval_policy` property of the neutral job envelope (legal terms:
    [...])". D4 says the message "stops naming 'the neutral job envelope'
    and names the bound vocabulary instead". Commit B left the message as
    it was. The behaviour is right and the wording is stale. Fixing it is a
    code-leg edit, not this change's.
  - The grant schema's description and its `approval_posture` comment still
    say the validator reads the envelope. The packet declared this under
    "Stale prose inside digested bytes": correcting it moves a digest, so it
    waits for the next digest-moving release.
