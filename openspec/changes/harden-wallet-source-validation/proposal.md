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
