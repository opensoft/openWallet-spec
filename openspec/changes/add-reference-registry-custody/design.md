## Context

The existing proof profile is ratified and its algorithm/canonicalization stay
fixed. The user commissioned portable reference services qualified in isolation.

## Goals / Non-Goals

Provide real current-binding lookup and policy-restricted signing outside the
worker. Qualify software isolation, not HSM backing, holder attribution,
workload attestation, human approval, public hosting or live tenant changes.

## Decisions

Use an operator-owned private SQLite directory. A subject has one current
binding; CAS and strictly increasing revisions prevent rollback/races.
Key identity/public bytes/custody ownership cannot silently move between
subjects. Revoked binding references stay tombstoned. No network mutation API.

Use mutual TLS with explicit CA/hostname validation and an exact client
certificate fingerprint allowlist. Policy maps authenticated peers to actions
and subjects; request JSON never supplies identity or permission. Resolve and
sign are separate permissions. Bound request/response sizes and timeouts,
refuse duplicate keys/noncanonical encodings and disable redirects/proxies.

Keep signing keys in the service's private state volume. Expose only canonical
domain-separated possession signing for current authorized bindings. The
worker sees its short-lived test client credential and public binding only.
A separate verifier has registry-read permission and cannot sign as the agent.
Use the existing isolated_invocable custody model, which evidences environment
execution and does not earn unsupervised authority.

Python's standard HTTP server is an isolated reference transport, not a
production internet server. TLS uses CERT_REQUIRED on both sides, explicit
trust roots and certificate policies. No default development bypass exists.

## Risks / Trade-offs

Software custody is extractable by a compromised custody administrator ->
claim only worker/service separation, preserve separate exact-request human
approval, and require independent hardening before deployment.
Remote registry reads are point-in-time -> recheck before receipt/use, retain
the core's local revocation/time fences and make no distributed-atomicity claim.
A slow peer can occupy a reference worker -> socket/request limits and
bounded qualification; public availability hardening remains outside scope.

## Migration Plan

Additive modules and isolated tests only. Existing proof schemas and legacy
custody vocabulary are unchanged. Remove the reference service configuration
to disable it. Preserve the original assembly pins until reviewed advancement.
