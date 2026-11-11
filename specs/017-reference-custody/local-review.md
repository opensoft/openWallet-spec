# Local review acceptance — 2026-11-10

Brett Heap commissioned: "Go ahead and review openWallet-code #5,
openWallet-spec #9, openMFA-code #3 and openMFA-spec #3 locally, then land them
through the governed process when green." This accepts local review while
final GitHub Codex reviews are quota-limited. It does not manufacture a bot
receipt or change the previously ratified possession-only wire profiles.

## Scope and findings

The coordinator and specialist passes covered architecture, security, data
integrity, performance, API contracts, reliability/concurrency, QA, static
analysis, maintainability and TLS/PKI/Docker integration. Initial reviewed
heads were wallet-code `77f53b83567c5a1ffa10dbeb5e4b5de8f339fd92`,
wallet-spec `3461cd166fbe55ff08322181720b11cc04066fe8`,
MFA-code `9a1cc19276832a264ef34b0bb70d0d8e7860780f` and MFA-spec
`5c8d655088e2831f90fa1e81fbd41c76ad78bae2`.

1. **P2: invalid signing input masked role denial.** The old sign negative
   refused even when verifier sign was accidentally granted. Wallet probes
   now submit canonical messages from owning `create_proof` and provision
   real second-subject bindings. Three policy-grant mutation regressions
   establish that action/subject probes detect accidental grants. MFA now
   attempts a valid owning proof with the current resolved binding, expecting
   the wrapped `signer-unavailable` refusal. Actual isolated qualification
   was repeated. Independent focused contract re-review confirmed the fix.

2. **P2: stale cleanup reports could qualify a failed new run.** The checker
   invalidates its summary, removes each prior child output, requires exit 1,
   and binds cancellation to the nonempty case observed in the current
   `services_started` event. Six regressions cover absent fresh output,
   mismatched case, unexpected exits and fresh success. Independent focused
   reliability re-review confirmed the fix; actual failure/SIGTERM runs were
   repeated with fresh reports and resource-absence readback.

3. **SonarCloud S8707 false positive**, issue
   `AaHIWCvYNluKFQ_qJcgQ`. The reported HTTP source is local
   `argparse.parse_args()` in trusted administrator startup, before serving.
   HTTP dispatch never invokes `main()` or supplies a config path. The
   documented local custody administrator owns this configuration;
   qualification constructs custody directly with fixed per-role paths.
   Independent TLS/security review confirmed no untrusted request/model flow
   reaches the privileged config read. This single issue was marked false
   positive; SonarCloud then read OK and GitHub's check read SUCCESS. No
   threshold, rule or exclusion was changed. Reassess a future wrapper that
   gives untrusted inputs access to this administrative interface.

No actionable finding remains. Final qualified code heads are wallet
`32c9254feffe6a856b9cc823af561fdfc45dc673` and MFA
`ddd59d573ef35390c9bbe70439db07ca62b58283`. Core prerequisite PRs merged
normally; merging those bases into the child branches changed ancestry only,
verified by empty tree diffs. The evidence/review-only spec updates are
checked again before landing; commit-bound GitHub COMMENT reviews will name the
actual final spec heads.

## Validation and landing

Wallet: 141 tests passed plus one existing historical skip; syntax and plain/
strict validators passed. MFA: 83 tests passed. Seventeen deliberately broken
assembly/package inputs refused. Actual source-bound service qualification
passed success, injected failure and SIGTERM cleanup exercises. All run-owned
containers, networks, volumes and images were absent at final readback.
See [evidence.md](evidence.md) and its paired raw artifacts for identities.

Fresh exact `@codex review` comments were posted after meaningful pushes.
Final code requests received usage-limit responses; older receipts are
historical. No clean final-head bot receipt is claimed. Current-head CI and
resolved threads are required before normal protected PR merges. The landing
reviews verify the candidate's exact parents/tree and read back the actual
merge parents/tree; no admin or direct-main push is authorized.

Only portable source conformance is accepted here. Working assembly/consumer
pins and shape digests remain unchanged. Production/HSM custody, human
authentication/approval, live QA, release and archive remain separate gates.
Feedback stays deferred and neither blocked write was replayed.
