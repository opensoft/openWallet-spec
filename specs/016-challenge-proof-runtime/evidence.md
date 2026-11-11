# Candidate evidence — 2026-11-10

Status: possession-only wire contract ratified; runtime acceptance pending

## Current owner standing

Brett Heap answered "Ratify both possession-only profiles" on 2026-11-10,
accepting spec baseline `778cedb30406e753fee5b4a95d96ac2c18b78ae4`.
The governing proposal's [owner record](../../openspec/changes/add-challenge-proof-runtime/review/ratification-2026-11-10.md)
preserves the question/response, exact schema digests and exclusions. Historical
draft/pending-ratification statements below describe earlier preparation.
Current code candidate remains `cdce0abda7063b9323ea565ac648949bf2f37be0`; real custody,
factor adapters, human approval, live qualification and assembly acceptance
remain separate gates. No technical contract or runtime byte changed to
record this owner decision.

## Commission and source

Parent [codeXfactory #577](https://github.com/codeXfactory/codexFactory/pull/577) merged at `03d0fd28719ad8756dc3b533aa91f2b0ef5397e7` after the corrected required check passed. The owner accepted that proposal's specific origin-ID correction through its recorded disposition. That history does not ratify this new contract.

Code candidate: [PR](https://github.com/opensoft/openWallet-code/pull/4), source `cdce0abda7063b9323ea565ac648949bf2f37be0`. This adds independent known-answer tests to the previous runtime implementation; runtime behavior and wire contracts are unchanged. Governance and new wire contracts remain draft in this spec leg. No assembly pin, product release or consumer execution pin was advanced.

## Local verification

- Code-leg full pytest: **98 passed, 1 skipped**, 127.79 seconds. This includes 61 proof cases and 37 existing cases. The existing historical comparison skips because no git blob for a different previous validator is reachable; it is not a new skip or a signature qualification result.
- Spec-leg structural pytest after review corrections: **5 passed**, in a fresh isolated environment installed solely from the eleven local hash-locked wheels. Structural fixtures, including zero-byte-shaped signature strings, do not assert cryptographic validity.
- Pinned OpenSpec CLI 1.12.0: **5 targets passed, 0 failed**, strict clean. Tarball SHA-512/SHA-1 verified before installation. npm dependency setup still resolves from the registry.
- Scoped strict origin validation from the parent's pinned proposal helper at `93d13d6c8e14008c0b66adea65756d106fef6227`: no origin errors.
- Syntax gate and both plain/strict legacy validators passed: 21 positive examples, 42 negative confirmations, 11/11 requirement coverage, zero errors/warnings. Repository scan: zero live wallet artifacts; this is corpus validation, not live acceptance.
- Both assembly roots passed naming, manifest and lockstep pin/shape validation with original leg pins unchanged.

An isolated development cross-product check also exercised actual wallet math into a signed receipt and one-use retry, refusing cross-challenge replay and later revocation. Its temporary adapter is not shipped as an accepted production factor backend and does not create a dependency pin.

## Execution tracking

The pinned CLI's generic `instructions apply` diagnostic reports no embedded OpenSpec checklist. This is the shared workflow's deliberate Speckit handoff: [tasks.md](tasks.md) is the sole executable list. Planning/validation success does not archive the proposal or imply completed realization.

## CI, review and remaining acceptance

Review corrections: the structural gate now installs a complete SHA-256-locked wheel closure locally with index/version checks disabled. Exact field lengths reject terminal LF/CRLF in digests, signatures; the new fixtures cover both endings. This introduces no offline-gate exception and changes no runtime proof behavior.

CI hardening: the structural-test workflow now permits binary dependencies only. This fixes Sonar rule `githubactions:S8541` found on wallet spec PR #8; the same scoped workflow change is applied here. A no-install resolution check confirmed wheel availability for the declared Python 3.12 dependency closure. No gate, rule or exception is weakened.

Published draft spec: [openWallet-spec #8](https://github.com/opensoft/openWallet-spec/pull/8). The prior Codex bot receipt covered `95bcd6d56c26c5f8713a5b2457f505520c7252dc`, not the later test-only update. A fresh exact `@codex review` request was posted for the current code head. Review/CI are read back separately on each PR; no receipt substitutes for contract ratification or live acceptance.

Current code CI passed at `cdce0abda7063b9323ea565ac648949bf2f37be0`: [pytest run](https://github.com/opensoft/openWallet-code/actions/runs/42926943492) and [wallet validation](https://github.com/opensoft/openWallet-code/actions/runs/42926943430). Previous bot receipts do not cover this later test-only update. Current spec CI and new requested review are read back on their respective PRs.

The source CI workflows and exact `@codex review` request are published on the code PR. A request is not a review receipt. Current PR results and later heads must be checked separately; local evidence above is not a CI claim.

## Independent compatibility prerequisite

T007 is complete at the code head above. Two fixed vectors independently
generated with Node 24.21.0/OpenSSL 3.5.8 cover ASCII, Unicode and the maximum
safe binding revision. Python cryptography used OpenSSL 4.0.2 for verification.
Ten cases passed in 0.31 seconds; the independent Node generator reproduced
the complete committed corpus exactly. Vector SHA-256:
`70d7b9e6c755e891bbb2e01d94c66cfbe44abc8733f73321caedb5d0d2a8f3b1`.
The code-leg `tests/challenge_proof/VECTORS.md` documents provenance,
reproduction and limits. Public test seeds are not custody material.

Exact preimage, signature and canonical wire comparisons pass; independently
signed wrong-domain/changed-byte messages, revoked bindings and wrong expected
digests refuse. This closes candidate known-answer preparation, not accepted
assembly interoperability or real registry/custody qualification.

Owner review/ratification of the new wire profile, accepted assembly compatibility, real factor/registry/custody acceptance, workload composition evidence, provider and human adapters, reviewed leg merges and assembly pins remain pending. Possession evidence confers no MFA, human approval or domain permission. No live tenant, enrollment, identity-provider or deployment operation was performed. No OpenSpec archive or product tag is authorized by this evidence.
