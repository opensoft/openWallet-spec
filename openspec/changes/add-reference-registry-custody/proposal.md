---
Status: commissioned implementation; isolated reference qualification
code_surface: openwallet_runtime registry, custody transport, reference service and isolated tests
target_release: unallocated; no production service or product release
---

## Why

The ratified possession profile has real cryptographic primitives but no
trusted current registry or separate signing custody. The first codeXfactory
pilot needs working integration that refuses unavailable/revoked bindings and
keeps machine signing distinct from human authentication and permission.

## What Changes

- Add a durable SQLite current-binding registry with monotonic revisions,
  compare-and-swap updates, immutable key ownership and persistent revocation.
- Add a portable reference signer/registry service with mutual TLS, pinned
  client-certificate policy, bounded JSON and no network administration/export.
- Add remote registry and opaque signer clients. Sign only canonical possession
  preimages for the authenticated caller's current allowed binding.
- Qualify actual crypto, transport, revocation, role isolation and cleanup with
  disposable services. Use the existing `isolated_invocable` custody vocabulary;
  it evidences the environment and grants no unsupervised authority.

## Capabilities

### New Capabilities
- `wallet-reference-custody`: isolated registry and policy-restricted signing for the existing possession profile.

### Modified Capabilities
None. Existing proof bytes, algorithms, assurance meaning and legacy contracts
remain unchanged. The reference control API is an implementation interface,
not a new neutral identity or authority vocabulary.

## Impact

Brett Heap directly instructed implementation and answered: "Build portable
reference services and qualify them in isolation". This commissions source
implementation and isolated qualification; it does not claim production
custody, hardware backing, workload composition, human approval or live QA.
The reference HTTP service is for isolated qualification, not public hosting.
Implementation and tests belong in the paired code leg. The sole executable
list is [feature 017](../../../specs/017-reference-custody/tasks.md).
Any assembly advancement follows reviewed leg merges and lockstep pins.
Feedback stays deferred and neither previously blocked write is replayed.
