# Candidate evidence — 2026-11-10

Status: local source gates passed; upstream review and acceptance pending

## Commission and source

Parent [codeXfactory #577](https://github.com/codeXfactory/codexFactory/pull/577) merged at `03d0fd28719ad8756dc3b533aa91f2b0ef5397e7` after the corrected required check passed. The owner accepted that proposal's specific origin-ID correction through its recorded disposition. That history does not ratify this new contract.

Code candidate: [PR](https://github.com/opensoft/openWallet-code/pull/4), source `95bcd6d56c26c5f8713a5b2457f505520c7252dc`. The code commit contains the implementation tested below. Governance and new wire contracts remain draft in this spec leg. No assembly pin, product release or consumer execution pin was advanced.

## Local verification

- Code-leg full pytest: **88 passed, 1 skipped**, 99.03 seconds. This includes 51 new proof cases and 37 existing cases. The existing historical comparison skips because no git blob for a different previous validator is reachable; it is not a new skip or a signature qualification result.
- Spec-leg structural pytest: **1 passed**. Structural fixtures, including zero-byte-shaped signature strings, do not assert cryptographic validity.
- Pinned OpenSpec CLI 1.12.0: **5 targets passed, 0 failed**, strict clean. Tarball SHA-512/SHA-1 verified before installation. npm dependency setup still resolves from the registry.
- Scoped strict origin validation from the parent's pinned proposal helper at `93d13d6c8e14008c0b66adea65756d106fef6227`: no origin errors.
- Syntax gate and both plain/strict legacy validators passed: 21 positive examples, 42 negative confirmations, 11/11 requirement coverage, zero errors/warnings. Repository scan: zero live wallet artifacts; this is corpus validation, not live acceptance.
- Both assembly roots passed naming, manifest and lockstep pin/shape validation with original leg pins unchanged.

An isolated development cross-product check also exercised actual wallet math into a signed receipt and one-use retry, refusing cross-challenge replay and later revocation. Its temporary adapter is not shipped as an accepted production factor backend and does not create a dependency pin.

## Execution tracking

The pinned CLI's generic `instructions apply` diagnostic reports no embedded OpenSpec checklist. This is the shared workflow's deliberate Speckit handoff: [tasks.md](tasks.md) is the sole executable list. Planning/validation success does not archive the proposal or imply completed realization.

## CI, review and remaining acceptance

Published draft spec: [openWallet-spec #8](https://github.com/opensoft/openWallet-spec/pull/8). Exact `@codex review` requests were posted on both legs. Codex code-review receipts from `chatgpt-codex-connector[bot]` completed on the exact code head recorded above with no findings reported. This code-review receipt is not contract ratification or live acceptance. Spec/tooling review and CI must be read from their own PR heads.

Code CI passed on the exact source head recorded above: [pytest run](https://github.com/opensoft/openWallet-code/actions/runs/42868132228). The separate wallet-validation check also passed. Spec-leg CI is still pending publication/readback of its own PR.

The source CI workflows and exact `@codex review` request are published on the code PR. A request is not a review receipt. Current PR results and later heads must be checked separately; local evidence above is not a CI claim.

Owner review/ratification of the new wire profile, independent compatibility vectors, real factor/registry/custody acceptance, workload composition evidence, provider and human adapters, reviewed leg merges and assembly pins remain pending. Possession evidence confers no MFA, human approval or domain permission. No live tenant, enrollment, identity-provider or deployment operation was performed. No OpenSpec archive or product tag is authorized by this evidence.
