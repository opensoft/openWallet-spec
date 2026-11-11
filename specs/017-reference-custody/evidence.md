# Reference registry/custody evidence — 2026-11-10

Status: implementation and isolated source qualification complete; local review complete; protected landing requires current-head CI

Brett Heap commissioned implementation and selected portable reference
services qualified in isolation. Tested code is
`32c9254feffe6a856b9cc823af561fdfc45dc673`,
[openWallet-code #5](https://github.com/opensoft/openWallet-code/pull/5),
based on the reviewed proof core from #4.

## Verification

- **141 passed, one existing historical-comparison skip**, 139.16 seconds.
- **43 focused registry/custody cases passed**, including actual mutual TLS and signing, wrong CA/hostname/client identity, role/subject isolation, canonical preimage enforcement, CAS race, persistence, revocation and private-state refusal.
- Syntax and plain/strict corpus validators passed: 21 positives, 42 negative confirmations, 11/11 requirements, zero errors/warnings.
- Exact-head [pytest CI](https://github.com/opensoft/openWallet-code/actions/runs/42943230683) and [wallet validation](https://github.com/opensoft/openWallet-code/actions/runs/42943230816) passed.
- Pinned strict OpenSpec validation passed; existing wire schemas, legacy custody vocabulary and vendored helpers remain unchanged.

The paired openMFA `002-wallet-factor-adapter` qualification uses actual
owning wallet crypto, current registry lookups and opaque service-held signing.
Complete temporary roots are bound by exact commits/trees, leg pin digests,
shape hashes, ratified schema hashes and installed-module/wheel hashes.
The success case `wmq-ebb57bf3c09a468f` passed proof/receipt, exact refusal,
retry/restart, real-clock expiry, outage recovery, key rotation and persistent
revocation gates. Seventeen broken complete-assembly/package inputs refused.

Injected failure `wmq-0a7e21689a564ade` and SIGTERM
`wmq-ded91d4b262344fe` each verified absence of all run-owned containers,
networks, volumes and images. Canonical cross-product raw reports and
reproduction live in the paired MFA spec feature's evidence directory and
quickstart. They do not become accepted product pins.

## Review correction

Codex found that a fresh key reference could reuse public bytes owned by
another subject. Three alias/rotation/custody regressions failed first.
The fix checks historical public-byte ownership across key references and
rejects conflicting prototype state on open; four regression cases pass.
The finding is resolved and a historical bot receipt explicitly names
`77f53b8356` with no major issues. Later paired-spec review status is
separate; the shared review account subsequently reached its usage limit.

## Final local review corrections

The authorized local review corrected two qualification false greens.
Canonical signing probes and real second-subject bindings now detect
accidental permission grants (three mutation regressions). The cleanup
checker invalidates prior evidence, requires fresh reports and exit 1, and
binds cancellation to its observed current case (six regressions).
Independent contract/reliability re-reviews confirmed both fixes.
[local-review.md](local-review.md) also records the independently confirmed
SonarCloud S8707 false-positive disposition and explicit local acceptance.

Actual qualification was repeated at the final code heads above. The fresh
reports and case IDs in this document supersede the earlier qualification
snapshot. The paired MFA raw artifacts bind source, modules and wheels;
all run-owned resources were absent at final readback.

## Boundary

Keys are actual software custody keys in the service-owned state, outside the
worker's mounts and execution context. This is the existing
`isolated_invocable` model: environment evidence, no unsupervised authority
or hardware claim. A production service, workload/composition binding,
human authentication/consent, accepted assembly advancement and live pilot
qualification remain separate. Working roots keep their original leg pins
and all shape digests. Feedback stays deferred and neither blocked write
was replayed.
