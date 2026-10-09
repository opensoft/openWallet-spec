# Tasks: bind-approval-posture-vocabulary

OpenSpec ratifies this text; nothing is built here.

`[OPERATOR]` = only Brett Heap can perform it. `[GOVERNANCE]` = it needs a
ruling first.

## 1. Governance

- [x] 1.1 Author this change; the leg's gate (AGENTS.md rule 4 command) green
      at --strict over the whole instance.
      Measured at authoring, 2026-10-08, from this leg's root at
      `15c15bbd451a803f0acdb24e5234836db829a2d3` plus this change:
      `Totals: 4 passed, 0 failed (4 items)`, then `OK openspec-cli-pin`. No
      INFO, WARN or ERROR line names this change.
- [ ] 1.2 **[OPERATOR] [GOVERNANCE]** Ratify or return. Brett Heap (openWallet
      operator authority).
- [ ] 1.3 On ratification: `Status: ratified`, the `Ratified:` line with the
      word verbatim, `.openspec.yaml` `approved_by` / `approved_on` filled.

## 2. Realization — already performed, recorded here

Performed under openXwallet's ratified `split-openwallet-neutral-core`, its
tasks 4.2 and 4.4, before this change existed. This change performs none of
it.

- [x] 2.1 Validator hunks (a)-(e) in the code leg's
      `scripts/validate-openxwallet.py`:
      - (a) removes the envelope;
      - (b) takes the vocabulary from ONE DECLARED BINDING the caller
        supplies. With none declared it binds the empty set, refuses every
        `approval_posture` key under the existing
        `authority-vocabulary-parallel`, and says so in one note;
      - (c) and (d) move rule (t) and the register reader out, to the
        adapter;
      - (e) adds the extension points, empty by default.

      Landed in opensoft/openWallet-code#2, merge
      `72313daab1f229c049cb90998931564c1904dbbc`: commit A, the pure carve,
      `32c933551b92d83122a45847215d5ebe92ae6740`; commit B, the declared
      edits, `75b990dc7ea99823626c18816b37d971f46e341b`. Checks
      `wallet-validation` and `pytest-suite` completed success on
      `75b990dc`, and `pytest-suite` read `37 passed, 1 skipped`.
- [x] 2.2 The corpus binding (RULED Q6),
      `contracts/openxwallet/examples/approval-vocabulary.binding.yaml`,
      added in commit B: pointer `approval_posture_terms`, three keys. The
      five positives and three negatives that carry `approval_posture` are
      adjudicated under it, and only the packaged corpus is. On `75b990dc`,
      `wallet-validation` read the note `approval-scope vocabulary: none
      bound; a repo scan refuses every approval_posture key, and the packaged
      corpus is adjudicated under its own binding,
      contracts/openxwallet/examples/approval-vocabulary.binding.yaml`, then
      `corpus: 21 positive example(s), 42 negative confirmation(s) across
      11/11 requirements` and `validate-openxwallet: 0 error(s), 0
      warning(s)`.
- [x] 2.3 The refusal under no binding, OBSERVED at authoring. The code leg's
      validator at `72313da` ran over a scratch tree outside every checkout,
      holding eight records as live records: the five corpus grants and the
      three agent wallets they name (`wal-agent-poster-0001`,
      `wal-agent-council-0011`, `wal-agent-creator-0002`), with no binding
      declared. It read `validate-openxwallet: 15 error(s), 0 warning(s)`.
      All fifteen are `authority-vocabulary-parallel`, three keys for each
      of the five grants, each reporting `legal terms: []`. The wallets are
      part of the measurement tree. With the five grants alone, the same
      run reads `20 error(s)`: the same fifteen plus five
      `custody-ceiling-unresolved`, one per grant, because the audience
      wallet a grant names does not resolve and its ceiling cannot be
      checked. The corpus note was unchanged. No code-leg test asserts this
      refusal today; the packet's proof asserts it in its part three (its
      task 4.6).

Not here: openXwallet's envelope binding. It is the ADAPTER's, realized by
the packet's group 5 in opensoft/openXwallet (task 5.2, open at authoring),
never by this change. This change's archive does not wait on it.

## 3. Archive gate

- [ ] 3.1 After 1.2, archive with the pinned CLI (AGENTS.md rule 4), which
      rewrites the promoted requirement in place; the gate green again at
      --strict.
      Dry run at authoring, in a scratch copy of this leg and never in it:
      `Totals: + 0, ~ 1, - 0, → 0` on `openxwallet-agent-profile`, and the
      promoted file changes in this one requirement only; the CLI also
      normalizes two blank lines around `## Requirements` in the file
      header, one each side, content unchanged. It also archives in either
      order with `add-composition-drift-cascade`, to the same promoted
      text.
- [ ] 3.2 Record the landing and the archive on opensoft/openXwallet#25 and
      tick task 4.8 of `split-openwallet-neutral-core` there.
