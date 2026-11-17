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


### Requirement: Bounded operator service configuration
The reference service SHALL admit its CLI configuration only under the invocation directory or a separately operator-selected OPENWALLET_REFERENCE_CONFIG_ROOT. The config operand SHALL NOT choose its own root. Reads SHALL reject links, non-regular or untrusted writable files and excess bytes before registry, TLS, key or listener effects. Existing cwd semantics for paths inside an admitted config SHALL remain unchanged.

#### Scenario: Escaped config operand
- **WHEN** a model-selected config path escapes the bounded operator root or traverses a link
- **THEN** startup SHALL refuse without reading that file or creating service state.

#### Scenario: Existing external operator config
- **WHEN** an operator independently selects a bounded config root and supplies a regular integrity-protected config inside it
- **THEN** startup SHALL use that config with the same relative-path semantics and service authority as before.

### Requirement: Discoverable complete wheel closure
The code leg SHALL publish its existing complete reviewed 18-package version/hash closure as requirements.txt, retain binary/hash-enforced CI installs and an old-lock compatibility include, and SHALL NOT introduce a project build or dependency-version change.

#### Scenario: Canonical CI install
- **WHEN** CI installs its runtime and validation dependencies
- **THEN** the canonical nonempty closure SHALL enforce every prior version and SHA-256 wheel hash without running a source build.

### Requirement: Explicit shared tooling context
The neutral spec SHALL retain the visible canonical OpenSpec implementation and standalone pin/corpus behavior. Shared execution SHALL use the provider's explicit consumer-root API, preserve operator precedence and independent artifacts, and retain all provider assertions plus consumer transport tests.

#### Scenario: Independent consumer roots
- **WHEN** the outer adapter uses the neutral canonical implementation
- **THEN** the adapter SHALL validate its own pin and corpus while standalone neutral invocation continues to validate this leg's own pin and corpus.
