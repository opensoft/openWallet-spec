## Why

Four dependency-installation findings and a credential-shaped negative example in openWallet-code are exposed by the openXwallet complete-source scan. Pinned tooling findings must be repaired at their owners and consumed without local forks.

## What Changes

- Hash-lock the complete Python wheel closure for existing CI validation without removing tests.
- Replace current credential-shaped negative-example bytes with deliberately invalid synthetic material while preserving private-material refusal semantics.
- Consume independently verified upstream tooling fixes and publish coherent spec/code/root provenance.
- Preserve historical commits, example identity, machine keys, contract refusal codes and operational boundaries.

## Capabilities

### New Capabilities
- wallet-source-validation: Wheel-only verified CI dependencies and synthetic negative-fixture safety.

### Modified Capabilities
None. Credential carriage remains forbidden.

## Impact

Neutral code workflows and negative fixture, pinned common spec tooling, root shape and leg pins. Authorized by Brett Heap's openXwallet #73 repair instruction on 2026-11-16. Speckit feature 018 owns the only executable implementation task list; this is not runtime activation authority.

## Full-main amendment (2026-11-16 America/La_Paz)

The first complete openXwallet main analysis naturally fixed all eight original
keys, but exposes the reference service's unconfined CLI config read and a
noncanonical lock filename. Complete the same unchanged gate by confining config
reads to an independently selected operator root, retaining bounded descriptor
reads and existing config-field cwd semantics, and publishing the exact reviewed
18-package wheel closure as requirements.txt with a compatible old-lock include.
Consume the provider's explicit consumer-root tooling API so the outer adapter
can execute this leg's visible canonical OpenSpec scripts without copying them.
Standalone spec behavior, local pins/locks/tarball/corpus, offline checks, eight
manifest-owned artifacts and immutable release tags stay intact. Feature 019
owns the amendment's executable list; feature 018 records the original handoff.
