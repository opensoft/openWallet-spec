# Tasks: 016-challenge-proof-runtime

Status: possession-only wire profile ratified; implementation/operational acceptance pending

- [x] T001 [S] Capture commissioned scope, draft origin and governance; files: openspec/changes/add-challenge-proof-runtime/**, specs/016-challenge-proof-runtime/**; verify: source and boundaries named before code.
- [x] T002 [O] Define exact-field draft wire contracts in the spec leg and structural checks; files: contracts/*-v0.schema.json, tests/runtime_contracts/**; verify: schema positives and negatives.
- [x] T003 [O] Implement real proof math and trusted-binding checks; files: openwallet_runtime/**, tests/challenge_proof/**; verify: substantive positive, tamper, expiry, revocation cases pass.
- [x] T004 [S] Run declared leg gates and reconcile evidence; files: specs/016-challenge-proof-runtime/evidence.md, .github/workflows/**; verify: report source/CI/limitations separately.
- [x] T005 [S] Publish paired draft PRs and request Codex review; files: PR descriptions and exact-head review requests; verify: source heads and review receipt status recorded.
- [x] T007 [O] Add independent, reproducible known-answer proof vectors without changing the candidate wire profile; files: code-leg `tests/challenge_proof/generate_vectors.cjs`, `tests/challenge_proof/vectors.json`, `tests/challenge_proof/test_vectors.py`, `tests/challenge_proof/VECTORS.md`, spec-leg `specs/016-challenge-proof-runtime/{plan,evidence,tasks}.md`; verify: `python -m pytest tests/challenge_proof/test_vectors.py -q` in the code leg, plus `node tests/challenge_proof/generate_vectors.cjs` independently reproduces the committed bytes. Ten cases and exact Node reproduction passed; full suite: 98 passed, one existing skip. This is candidate preparation under Brett Heap's instruction to continue upstream runtime prerequisites, not contract ratification or real custody acceptance.
- [ ] T006 [O] Obtain owner acceptance, land reviewed legs, advance the root in lockstep and qualify accepted adapter/custody/compatibility evidence. This owner/landing gate remains pending; no product release or live acceptance is claimed.

No other executable task list is created in the OpenSpec packet. No parallel-agent execution is required. Archive only after assembly advancement and actual acceptance.

T007 precedes T006. All current verification remains offline. Brett Heap completed T006's wire-contract owner decision on 2026-11-10: "Ratify both possession-only profiles", approving `778cedb30406e753fee5b4a95d96ac2c18b78ae4`. The governing proposal's `review/ratification-2026-11-10.md` binds the exact schema bytes and scope. T006 remains unchecked because reviewed realization/leg landings, root advancement and real adapter/custody/compatibility acceptance remain separate outstanding gates. No release or live qualification is inferred.
