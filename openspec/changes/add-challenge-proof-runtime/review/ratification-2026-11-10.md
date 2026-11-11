# Owner ratification — 2026-11-10

## Exact decision and approved baseline

Brett Heap was asked first-hand in this chat:

> Do you ratify the possession-only wire contracts in openWallet-spec #8
> (head `778cedb`) and openMFA-spec #2 (head `61ae1cb`)? T006 in both task
> lists explicitly says “Obtain owner acceptance”; the earlier codeXfactory
> #577 approval did not ratify these new contracts. Acceptance would cover the
> wallet proof and bound challenge/receipt profiles, while real custody,
> factor adapters, human approval and live qualification remain separate gates.

His answer was:

> Ratify both possession-only profiles

This repository's approved baseline is
[openWallet-spec #8](https://github.com/opensoft/openWallet-spec/pull/8)
at `778cedb30406e753fee5b4a95d96ac2c18b78ae4`. The other profile is the paired owner decision;
it does not move this repository's ownership or contract boundary.
The reviewed code candidate is
[openWallet-code #4](https://github.com/opensoft/openWallet-code/pull/4)
at `cdce0abda7063b9323ea565ac648949bf2f37be0`; wire ratification does not independently accept
its operational realization.

## Exact approved schema bytes

| Baseline-relative file | SHA-256 |
| --- | --- |
| `contracts/challenge-proof-v0.schema.json` | `ec2770110b8afcddf34deb56754f79b01d2877a0bb414ea1ce59d9ace32362ed` |

The ratification-record commit changes governance standing and records the
owner's act. It changes no schema, technical requirement, algorithm, lifetime,
assurance bound, runtime code, original origin ID or commissioning field.

## Scope and remaining gates

The accepted profiles establish bounded cryptographic possession evidence.
They do not assert MFA, human presence, explicit human consent, workload
composition, delegation or domain permission. The relying party continues to
own permission and separate exact-request human consent.

Real custody, factor/registry adapters, workload composition evidence, human
approval and live qualification remain separate. Reviewed realization,
reviewed leg landings and any accepted assembly/consumer advancement must
satisfy their existing gates; no floating or unmerged leg becomes a product
pin. T006's owner decision is recorded, while its combined realization,
landing and qualification checkbox remains incomplete.

No product release, tag, OpenSpec archive, live provider/credential operation,
deployment or approval bypass is authorized by this record. Feedback remains
deferred and neither previously blocked write was replayed.
