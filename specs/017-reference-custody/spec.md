# Feature 017-reference-custody

Status: commissioned source implementation and isolated qualification

Durable current bindings and mutually authenticated policy-restricted external signing.

The governing [proposal](../../openspec/changes/add-reference-registry-custody/proposal.md) and
capability deltas define acceptance. The user explicitly chose portable
reference services qualified in isolation. Existing ratified proof/challenge/
receipt profiles and authority vocabulary are unchanged.

## User scenarios and acceptance

A separately identified machine proves possession using service-held keys.
A trusted verifier resolves current registry facts and refuses wrong subjects,
keys, revisions, digests, revoked/expired bindings and unavailable services.
No successful software test becomes MFA, human consent or domain permission.
Actual service integration and cleanup must be observed; missing dependencies
or readback fail instead of silently substituting state-test fixtures.

## Scope

Canonical governance stays in this spec leg; code/tests in the paired code
leg. No product release, live service, provider write, enrollment, workload
attestor or human authenticator is provisioned. Normal reviewed advancement
and complete assembly pins remain distinct from candidate source tests.
