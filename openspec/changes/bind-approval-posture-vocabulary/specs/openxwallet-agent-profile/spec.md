# openxwallet-agent-profile Specification (delta)

## MODIFIED Requirements

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
