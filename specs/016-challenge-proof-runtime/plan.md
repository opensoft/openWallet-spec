# Implementation Plan: 016-challenge-proof-runtime

**Status**: Draft candidate implementation
**Date**: 2026-11-10
**Spec**: [spec.md](spec.md)
**Governance**: [add-challenge-proof-runtime](../../openspec/changes/add-challenge-proof-runtime/proposal.md)

## Summary

Offline Ed25519 possession proof over an authenticated challenge digest with current server-resolved key binding and opaque signing custody.

## Technical Context

Python 3.12; cryptography 50.0.1; rfc8785 0.1.4. Offline Ed25519 and opaque signing interface. No network calls or live credentials in the candidate gate. Tests generate ephemeral keys in memory.

## Constitution and boundaries

No project constitution is present; follow the assembly instructions and shared protocol. Governance/contracts stay in this spec leg; code/tests stay in the paired code leg. No sibling checkout reads in code gates. No unmerged leg pins, release tag, authority vocabulary fork or approval-rule change.

## Project Structure

- Spec leg: `contracts/*-v0.schema.json`, `tests/runtime_contracts/`, this feature and OpenSpec change.
- Code leg: `openwallet_runtime/proof.py`, `pyproject.toml`, substantive tests and source CI.

## Research and data model

See [research.md](research.md), [data-model.md](data-model.md) and [quickstart.md](quickstart.md). Fixed algorithms/canonicalization and exact bound contexts are chosen to make independent compatibility vectors possible. The schemas are candidates, not an accepted dependency.

## Sequence and validation

The sole executable list is [tasks.md](tasks.md). Capture governance and schema first, implement candidate math/state second, then run the spec and code gates, reconcile evidence, open paired draft PRs and request Codex review. Keep owner acceptance, merges and root pins pending.

## Analysis

### Continuing prerequisite preparation

T007 adds independently produced known-answer vectors before T006. The Node.js
generator uses built-in crypto/OpenSSL and a deliberately bounded canonicalizer
for the profile's strings, safe integers, arrays, objects and null. It imports
neither the Python implementation nor its canonicalizer. Committed public test
seeds, canonical preimages, public keys and signatures make reproduction
auditable. Python tests compare exact generated proofs, wire bytes and refusal
cases against the fixed vectors. No runtime dependency, wire contract, custody
claim or approval requirement changes. Node is a maintainer reproduction tool;
the ordinary Python gate consumes static vectors and requires no Node runtime.

FR subjects map one-to-one to the capability requirements. Code tests cover each subject and critical negative/race paths; schema tests cover structure only. Synthetic state-test factors cannot clear real adapter acceptance. No unresolved clarification is delegated to code; future integration gates are explicit exclusions.
