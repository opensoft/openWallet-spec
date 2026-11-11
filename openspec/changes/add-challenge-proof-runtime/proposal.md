---
Status: ratified
Ratified: 2026-11-10 by Brett Heap for the possession-only wire profile; see review/ratification-2026-11-10.md for the approved baseline and limits.
code_surface: Offline Ed25519 possession proof over an authenticated challenge digest with current server-resolved key binding and opaque signing custody.
target_release: unallocated; no product version or release tag is reserved here.
---

# add-challenge-proof-runtime

## Why

The existing design capture does not provide a cryptographic runtime. Offline Ed25519 possession proof over an authenticated challenge digest with current server-resolved key binding and opaque signing custody.

Brett Heap commissioned this upstream prerequisite after ratifying [codeXfactory PR #577](https://github.com/codeXfactory/codexFactory/pull/577), merged at `03d0fd28719ad8756dc3b533aa91f2b0ef5397e7`. That commission authorized candidate preparation. On 2026-11-10 he separately ratified this possession-only wire profile at `778cedb30406e753fee5b4a95d96ac2c18b78ae4`; the [owner record](review/ratification-2026-11-10.md) preserves the exact response, schema digests and exclusions. Runtime realization, custody/factor acceptance, human approval and live qualification remain separate gates.

## What Changes

Add the candidate contract and a bounded Python runtime with substantive adversarial tests. The new proof schema belongs to this spec leg; legacy Q7 covers the existing two families only. Existing schemas and validator behavior stay intact.

## Capabilities

### New Capabilities
- `wallet-challenge-proof`: Offline Ed25519 possession proof over an authenticated challenge digest with current server-resolved key binding and opaque signing custody.

### Modified Capabilities
None. Existing released contracts are unchanged.

## Impact

Canonical contracts and full governance live in this spec leg. Implementation and offline tests live in the paired code leg. The assembly root and any consumer advance only after reviewed leg PRs merge, through lockstep pins. Development metadata `0.0.0.dev0` is not an allocated release. No live identity, credential, enrollment, tenant policy or deployment action is part of this change.

## Implementation Handoff

[Feature 016-challenge-proof-runtime](../../../specs/016-challenge-proof-runtime/plan.md) owns the sole executable task list. Do not archive before the leg reviews and assembly pin PR land.
