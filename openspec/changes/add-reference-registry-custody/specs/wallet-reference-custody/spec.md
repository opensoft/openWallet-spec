## Purpose

Provide current trusted wallet bindings and separately held signing keys for
isolated possession-proof integration without widening authentication meaning.

## ADDED Requirements

### Requirement: Durable current binding
The registry SHALL enforce monotonic binding revisions, compare-and-swap
updates, immutable key ownership and persistent revoked-reference tombstones.
Missing, inactive, revoked or unavailable bindings SHALL refuse.

#### Scenario: Revision race or revoked reference
- **WHEN** a stale administrator update or reuse of a revoked binding is attempted
- **THEN** the registry refuses and preserves the current record.

### Requirement: Authenticated restricted custody
The reference service SHALL require mutual TLS and explicit peer action/subject
policy. It SHALL sign only the existing canonical possession preimage for the
current permitted binding and SHALL expose neither key export nor network administration.

#### Scenario: Wrong actor or protocol
- **WHEN** a peer requests another subject, an unauthorized action or another signing domain
- **THEN** no signature is produced.

### Requirement: Isolated qualification boundary
Qualification SHALL use actual private-key operations outside the agent worker,
observe refusal and resource absence after cleanup, and retain the existing
environment-evidence custody ceiling. It SHALL NOT claim human approval or MFA.

#### Scenario: Worker inspection
- **WHEN** the isolated agent worker inspects its own mounts and credentials
- **THEN** custody and verifier private keys are absent.
