## ADDED Requirements

### Requirement: Complete source acceptance
Neutral validation SHALL retain the existing source tests, syntax/plain/strict checks and pinned OpenSpec checks. Its openXwallet consumer's complete-assembly analysis SHALL retain all six Sonar way conditions, full scope, runtime matrix and real executed-test coverage. No rule suppression, threshold reduction, false coverage, billing change or operational activation is permitted.

#### Scenario: Published main acceptance
- **WHEN** the neutral repair is merged
- **THEN** its exact revisions SHALL pass their owning validations and be handed to openXwallet #73; the consumer's baseline, evaluated coverage and complete main gate remain its separate acceptance obligation.

### Requirement: Owned and reproducible repairs
Shared files SHALL be fixed at their owners, consumed through coherent immutable pins and verified provenance, and original findings SHALL close through source analysis.

#### Scenario: Consumer propagation
- **WHEN** provider repairs are accepted
- **THEN** the consumer SHALL verify compatible pins, actual provider bytes and the eight original finding keys.

### Requirement: Preservation
The repair SHALL preserve active sessions, unrelated worktrees, historical commits, immutable tags, example identities and refusal semantics.

#### Scenario: Credential-shaped negative example
- **WHEN** current fixture bytes are replaced
- **THEN** deliberately invalid synthetic private material SHALL still trigger the existing refusal, while old history is retained without live credential use.
