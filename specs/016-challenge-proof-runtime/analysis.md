# Cross-artifact analysis

Status: local candidate analysis; owner acceptance pending

| Requirement | Task | Evidence |
| --- | --- | --- |
| FR-001 context-bound possession | T003 | Real round trip, literal canonical message, tamper and cross-protocol/challenge cases |
| FR-002 trusted binding/custody interface | T003 | Wrong registry key, changed revision, revoked/expired binding, wrong signer and sanitized backend failures |
| FR-003 strict profile and limited meaning | T002/T003 | Exact-field schema, missing/unknown claims, strict JSON, canonical signature encoding and no assurance result |

Every executable task is in this feature. There is no task duplication in the OpenSpec packet. New origin IDs are present before ratification; no ratification is invented. Source, schema, CI and live acceptance gates are recorded separately. The legacy wallet skip and empty live scan are explicit. No source gate reads a sibling checkout. No owner-act, release, upstream acceptance or archive task is marked complete by this analysis.
