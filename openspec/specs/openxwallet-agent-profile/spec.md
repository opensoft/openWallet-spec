# openxwallet-agent-profile Specification

## Purpose
The first profile over the neutral wallet core, covering holders of class AGENT, whose identity IS its declared composition. This capability owns what a composition must cover, what changing it revokes, and why the profile is a SIBLING family over the core rather than an extension of it — so patient and practitioner profiles arrive the same way.

## Requirements

### Requirement: An agent holder declares its composition

openWallet SHALL require a wallet holder of class AGENT to declare the
composition that constitutes its identity — model version, prompt
contract, tool manifest, policy version, parameters, and retrieval corpus
where one applies — as a hash over a declared component set. The component
set is part of the declaration, so a reader can tell what a matching hash
was actually asserting.

#### Scenario: the hash names what it covers

- WHEN an agent holder is declared
- THEN the record carries both the composition hash and the component set it covers
- AND a hash without its component set is a validation failure

#### Scenario: composition belongs to the agent profile only

- WHEN a holder of another class is declared
- THEN no composition is required of it
- AND the core capability imposes none

### Requirement: A composition change revokes the agent's grants immediately

openWallet SHALL treat any change in an agent's declared composition as
the end of that agent's certified identity: its outstanding grants are
revoked at once through the core's revocation-propagation rule, with no
tolerance band and no grace period, and resuming requires re-issuance
against the changed composition. This generalizes to AUTHORITY an
invalidation the family already applies to OUTPUTS — a prompt-contract
version bump invalidated every prior classification, because a judgment by
prompt-v1 is not the same classifier's judgment.

#### Scenario: a changed agent is a different agent

- WHEN an attested composition hash differs from the declared hash
- THEN the agent's outstanding grants are revoked at that moment
- AND an exercise attempt against any of them is refused

#### Scenario: declared change is not a percentage

- WHEN any single component of the declared set changes
- THEN the change alone is sufficient to revoke
- AND no threshold, score, or tolerance band is consulted

### Requirement: Agent authority is grant scope, not a parallel vocabulary

openWallet SHALL express what an agent may do as the SCOPE of a capability
grant, and SHALL admit as legal approval-posture terms exactly the keys of
ONE DECLARED VOCABULARY BINDING supplied by the consuming layer and read at
run time, never restated, so that an agent's authority and a job's approval
posture are stated in one vocabulary rather than two kept in agreement.
Absent a declared binding, a grant naming any approval posture SHALL be
refused.

#### Scenario: authority is carried by a grant

- WHEN an agent's authority is recorded
- THEN it is the scope of a grant the agent holds
- AND no authority exists for that agent outside a grant

#### Scenario: the approval vocabulary is reused, not duplicated

- WHEN a grant's scope names an approval posture
- THEN each key of that posture is a key of the one declared vocabulary binding, read from the binding at run time
- AND a key the binding does not hold is a validation failure, whether it comes from a parallel authority vocabulary or from a copy of the vocabulary restated in openWallet

#### Scenario: no binding is declared, so a posture is refused rather than admitted because nothing forbade it

- WHEN no vocabulary binding is declared and a grant names any approval posture
- THEN the grant is refused
- AND the posture is not admitted on the ground that nothing forbade it
