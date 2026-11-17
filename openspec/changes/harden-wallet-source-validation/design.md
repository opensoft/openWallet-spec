## Context

The wallet assembly exposes provider files to static analysis. The repair is authorized by openXwallet #73 and must preserve independent ownership, published history, live sessions and current acceptance matrices.

## Goals / Non-Goals

Goals: fix original findings naturally, retain full test execution, verify published source and the unchanged quality gate.
Non-goals: operational activation, new billing, rule suppression, reduced scope or thresholds.

## Decisions

Repair shared tooling at its original owner and consume byte-identical published versions with recorded provenance. Never edit a shape-pinned copy or invent a provider digest.
Use complete hash-pinned wheel closures for CI installs; execute local source without installing its build backend.
Preserve the negative fixture's identity and refusal class using deliberately invalid private-material placeholders; record provenance without exposing old bytes.
Use executed-test coverage for actual scanned paths. Retain all source scope and existing gate conditions. Choose the oldest retained main analysis as the candidate baseline to avoid hiding retained changes; verify the selected revision remains an ancestor.
Keep one executable task list in the paired Speckit feature. OpenSpec is governance and handoff only.

## Risks / Trade-offs

Unrelated main movement can invalidate pins or evidence: re-read exact heads before merging and verifying.
Automatic analysis omits coverage: replace it with CI-based complete-source analysis using the existing organization secret once the pipeline is qualified.
Historical fixture provenance may remain uncertain: do not test old material against a live provider; preserve the commit and only record safe fingerprints.

## Migration Plan

Land provider fixes, then consuming legs, then the neutral root and adapter pins. Require exact-head tests and independent review. Verify the published main analysis, all eight original finding keys and all original gate conditions. Revert through ordinary reviewed commits if acceptance fails; preserve tags and historical analyses.

## Open Questions

Fixture provenance and final retained-baseline ancestry are verification tasks, not inferred approvals.

## Main-only source amendment

The CLI config operand never establishes its own allowed root. The default is
the invocation directory; OPENWALLET_REFERENCE_CONFIG_ROOT is separate operator
configuration for existing external locations and must select a bounded existing
directory. Admit regular operator/root-owned, non-group/world-writable files,
walk below the selected root without following links, and read at most the
existing request-document bound plus one byte. Refuse invalid paths, permissions,
non-regular files and oversize before registry, key/TLS or listener effects.
Paths inside admitted config JSON keep resolving from process cwd as before.
Keep all runtime dependency versions and wheel hashes unchanged; the canonical
requirements.txt contains the full existing closure and the old lock forwards
without changing binary/hash-enforced installation. No build backend runs.

The neutral spec retains the sole full canonical verifier/installer source.
Re-vendor the provider's explicit consumer-root API with byte provenance; do not
edit a copied provider body. Its own CLI stays standalone and selects this leg's
pin/corpus. A consumer may call the API with its separately verified root to
select that consumer's own pin/corpus. Operator pin authority and every existing
integrity/cache/lock/refusal check remain; no live credential or activation is
part of this source repair.
