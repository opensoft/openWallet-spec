# openWallet-spec

The **spec leg** of the `openwallet` project: requirements, decisions and
acceptance criteria. The implementation lives in
[`opensoft/openWallet-code`](https://github.com/opensoft/openWallet-code).

**Clone the assembly root, not this repository.** This leg is mounted as a
submodule at `spec/` inside
[`opensoft/openWallet`](https://github.com/opensoft/openWallet), which
is what pins the commit of this repository that the project currently is:

```sh
git clone --recurse-submodules https://github.com/opensoft/openWallet.git
cd openWallet
make bootstrap
```

Working here directly is fine — it is an ordinary repository with an ordinary
branch. What advancing this leg does NOT do is advance the project: that is a
commit in the assembly root moving the gitlink, `contracts/spec-pin.yaml` and
any workflow `@<sha>` reference together.

Being the spec leg confers no authority over specifications. The split is
navigation; authority travels in grants, and a project that keeps spec and
code in one repository is reviewed identically.

Topic: `xf-project-openwallet`.

## Status: pre-carve

Content arrives at the carve from
[opensoft/openXwallet](https://github.com/opensoft/openXwallet) at
`90111df262d6f54f7e82651d860adc12345f83f4`. openXwallet's
`docs/openwallet-carve-manifest.yaml` declares every path that moves here,
byte for byte and at an unchanged repository-relative path. The procedure is the
assembly root's `docs/openwallet-cutover-runbook.md`. Until the carve, this leg
holds its seed files, its own OpenSpec gate and `openspec/config.yaml`, which
the pinned CLI needs before it will validate an empty instance.

## What this leg owns after the split

- the promoted capabilities `openxwallet` and `openxwallet-agent-profile`
  (`openspec/specs/`);
- the archive records of `add-openxwallet` and `add-multi-key-wallets`;
- the active change `add-composition-drift-cascade`, travelling from openXwallet;
- the Speckit features 006 (`openxwallet-contracts`), 010
  (`wallet-validator-ci`) and 015 (`multi-key-wallets`);
- its own OpenSpec gate, below.

The contract families, the corpus, the validator and their tests are in
[`opensoft/openWallet-code`](https://github.com/opensoft/openWallet-code). The
release identity (manifest, CHANGELOG, release records, proof and tag) is in the
assembly root.

## Pinning openWallet

Consumers pin the ASSEMBLY ROOT by commit and digest, never a leg. Domain
descendants pin a version and carry a profile. They never fork: a need a
profile cannot express is an upstream change, made here.

## The OpenSpec gate

`openspec-cli-pin-gate` validates this leg's `openspec/` at `--strict` through
`@fission-ai/openspec@1.12.0`, installed from the tarball committed under
`tools/openspec-cli-pin/` after its SHA-512 and SHA-1 are checked against
`contracts/openspec-cli-pin.yaml`. It reads no upstream tree and no sibling leg,
and it never fetches the artifact from the registry. That is this leg's own
ruling, "Vendor the tarball (Recommended)" (Brett Heap, 2026-10-08). The one
thing it still fetches is the CLI's npm dependency closure. Run it from this
leg's root:

```sh
OPENSPEC_TELEMETRY=0 python3 scripts/validate-openspec-cli-pin.py --all --no-cache \
    --tarball tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz
```

[`docs/openspec-cli-pin.md`](docs/openspec-cli-pin.md) covers:

- what was vendored, and from which openxFactory commit;
- the drift check;
- the gate observed refusing a mutated tarball;
- what 1.12.0 does on an empty instance;
- the dependency-closure residual.

## Agents

See [`AGENTS.md`](AGENTS.md) and [`CLAUDE.md`](CLAUDE.md). Both point at the
shared OpenSpec/Speckit protocol, which runs from the assembly root.
