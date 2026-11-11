# Tasks: 017-reference-custody

- [x] T001 [O] Capture commissioned scope and paired feature governance; files: `openspec/changes/add-reference-registry-custody/**, specs/017-reference-custody/**`; verify from spec leg: `python3 scripts/validate-openspec-cli-pin.py --all --tarball tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz`.
- [x] T002 [O] Implement durable registry, monotonic CAS, immutable ownership and tombstones; files: `openwallet_runtime/registry.py, tests/registry/**`; verify: `python -m pytest tests/registry -q`. Historical public-byte aliases and conflicting prototype state are covered by regression tests.
- [x] T003 [O] Implement bounded mutual-TLS clients and restricted reference custody service; files: `openwallet_runtime/custody.py, openwallet_runtime/reference_service.py, tests/custody/**`; verify: `python -m pytest tests/custody -q`. Combined registry/custody focused suite: 40 passed.
- [x] T004 [O] Run complete leg gates and reconcile isolated evidence/provenance; files: `docs/reference-custody.md, .github/workflows/*.yml, specs/017-reference-custody/evidence.md`; verify: `python -m pytest tests/ -q`. Full suite: 138 passed, one pre-existing skip; syntax/plain/strict validators passed; exact-source isolated success/failure/cancellation and 17 negative assembly gates passed.
- [ ] T005 [O] Publish paired reviewable PRs and verify current-head CI/Codex evidence; files: `PR metadata and feature evidence`; verify: `current-head CI and actual Codex receipt readback`.

T001 → T002 → T003 → T004 → T005. No parallel-agent execution is required.
The user's direct implementation/isolation instruction commissions these
source tasks; it is not a release, archive or live operational acceptance.

T005 publication is prepared, but review acceptance remains separate: code
head 77f53b83567c5a1ffa10dbeb5e4b5de8f339fd92 has green CI and an exact-head
clean Codex receipt. Later paired-spec review status is read back on its PR;
the shared review account subsequently reached its usage limit. No older
receipt or quota failure is represented as a clean review of a new head.
