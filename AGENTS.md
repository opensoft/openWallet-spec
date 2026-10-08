This is the **spec leg** of openWallet (`openwallet`): requirements, decisions
and acceptance criteria.

**The project's rules are not here.** They are in the assembly root
`opensoft/openWallet`, in `AGENTS-shape.md` — read that before touching anything
that spans the legs. This leg is mounted there at `spec/`, and the other leg,
`opensoft/openWallet-code`, beside it at `../code/`, once the root is cloned with
`--recurse-submodules`.

Working here is ordinary — an ordinary repository on an ordinary branch. What
advancing this leg does NOT do is advance the project: that is ONE commit in
`opensoft/openWallet` moving the gitlink, `contracts/spec-pin.yaml` and every
workflow `@<sha>` for this leg together.

Being the spec leg confers no authority over specifications. The split is
navigation.

## Shared OpenSpec/Speckit protocol

Use the shared OpenSpec/Speckit workflow from:

- `$HOME/.agents/AGENTS.md`
- `$HOME/.agents/protocols/openspec-speckit-workflow.md`
- `$HOME/.agents/protocols/project-agent-bootstrap.md`

Repository documents remain authoritative for openWallet product facts, contract
ownership, validation, versioning, and release constraints.

This is a three-leg project, and the protocol runs from the assembly root. The
root holds `.specify/`, and Speckit features are worked in
`worktrees/<NNN-feature-name>/{spec,code}/` under it. THIS leg holds the full
`openspec/` instance and the Speckit feature directories `specs/NNN-*`. Run
`openspec` from this leg's root, and only through the pinned CLI (rule 4).

## What this leg is

**Status: pre-carve.** This leg's content arrives at the carve from
opensoft/openXwallet at `90111df262d6f54f7e82651d860adc12345f83f4`. The carve is
governed by openXwallet's `split-openwallet-neutral-core` (tracked in
opensoft/openXwallet#25), and its declared path mapping is openXwallet's
`docs/openwallet-carve-manifest.yaml`. Until the carve, this leg holds its seed
files, its own OpenSpec gate and `openspec/config.yaml`.

After the split this leg owns openWallet's decided record:

- the promoted capabilities `openxwallet` and `openxwallet-agent-profile`, under
  `openspec/specs/`. Their eleven requirement subjects read `openWallet SHALL`;
  that is the only edit the carve makes to them;
- the archive records `openspec/changes/archive/2026-08-08-add-openxwallet/` and
  `openspec/changes/archive/2026-10-08-add-multi-key-wallets/`;
- the active change `openspec/changes/add-composition-drift-cascade/`, which
  travels from openXwallet with its three `openXwallet` occurrences rewritten,
  and archives HERE;
- the Speckit features `specs/006-openxwallet-contracts/`,
  `specs/010-wallet-validator-ci/` and `specs/015-multi-key-wallets/`;
- its own OpenSpec gate (rule 3).

openWallet's birth change is authored in this leg's OpenSpec instance after the
carve lands. It MODIFIES *Agent authority is grant scope, not a parallel
vocabulary* (openXwallet `design.md` D8).

Two things are NOT here. Both contract families, the corpus, the validator and
its tests are in the code leg, `opensoft/openWallet-code`. That placement is a
declared override of openRepoShape's `spec-governance` default (RULED Q7). The
release identity (the manifest, CHANGELOG, release records, proof and tag) is in
the assembly root, because the root is the one commit that names both legs.

## The rules that are not negotiable here

1. **Consumers pin; nobody forks.** Consumers pin openWallet's ASSEMBLY ROOT by
   commit and digest, never this leg directly. The root's one commit is the
   answer to "which openWallet". Domain descendants pin a version and carry a
   profile. They never fork. A need a profile cannot express is an upstream
   change here, made through this leg's OpenSpec instance.
2. **Machine keys do not move casually.** Capability ids, `kind:` values,
   finding codes and filenames are pinned BY NAME by live consumers. The split
   renames none of them: under the ruling "keep the prefix", only the
   requirement subjects change. Renaming one is a breaking change with a
   migration note, never a tidy-up.
3. **Every gate is offline.** No check reads the network, an upstream tree, a
   sibling leg or the root's `contracts/manifest.yaml`. This leg's OpenSpec gate
   installs `@fission-ai/openspec@1.12.0` from the tarball committed at
   `tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz`.
   Before installing anything, it verifies those bytes against the SHA-512 and
   SHA-1 in `contracts/openspec-cli-pin.yaml`, and it refuses
   `pin-integrity-mismatch` on any difference. **RULED for this leg:** Brett
   Heap, 2026-10-08, in session, by multiple choice, label verbatim **"Vendor the
   tarball (Recommended)"**, recorded at 2026-10-08T17:01:43Z (opensoft/openXwallet
   `split-openwallet-neutral-core`, task 3.6). One residual remains, measured and
   not hidden: npm still resolves the CLI's dependency closure from the registry
   (`docs/openspec-cli-pin.md`).
4. **The pinned CLI is the only CLI.** Validate with the gate's own command, and
   archive with the binary the installer prints:

   ```sh
   OPENSPEC_TELEMETRY=0 python3 scripts/validate-openspec-cli-pin.py --all --no-cache \
       --tarball tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz
   "$(python3 scripts/install-pinned-openspec-cli.py 2>/dev/null)" archive <change> --yes
   ```

   An `openspec` that happens to be on PATH decides nothing here.
5. **The vendored gate is not edited here.** `contracts/openspec-cli-pin.yaml`,
   the two `scripts/*openspec-cli*.py` files, the tarball and
   `.github/workflows/openspec-cli-pin-gate.yml` are copies from openxFactory at
   `44d8fbaf7d977668973dcd116040c9405416c2ea`. The workflow differs on one
   declared `run:` line. The drift check and the re-vendoring procedure are in
   `docs/openspec-cli-pin.md`. A defect in them is fixed upstream and reaches
   this leg by re-vendoring.
6. **Run the gate before pushing**, with the command in rule 4, from this leg's
   root. It must end `OK openspec-cli-pin`.
