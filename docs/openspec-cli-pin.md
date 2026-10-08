# The fleet-pinned OpenSpec CLI in this leg

`openspec validate --strict` is the gate every spec delta in this leg passes,
and `openspec archive` is the act that moves a ratified delta into canon. This
leg carries the estate's pinned CLI so that CI can say which tool ran: the
content-addressed `@fission-ai/openspec@1.12.0`, verified against
`contracts/openspec-cli-pin.yaml` before anything is installed.

This is the spec leg's OWN gate. It was **vendored fresh for this leg and not
carved** (opensoft/openXwallet `split-openwallet-neutral-core`, `design.md` D7):
openXwallet's copy rests on a ruling taken for openXwallet's `AGENTS.md` rule 4,
and carving it would stretch that ruling to a repository it did not name. This
leg holds the same shape under a ruling of its own (below).

## The ruling

Brett Heap, 2026-10-08, in session, by multiple choice, label verbatim:

> **"Vendor the tarball (Recommended)"**

It is recorded at 2026-10-08T17:01:43Z in opensoft/openXwallet
`openspec/changes/split-openwallet-neutral-core/` (`proposal.md`, the spec
leg's OpenSpec gate; `.openspec.yaml`, ruling `tasks-3.6`), and was realized by
that change's task 3.6. Its effect: this leg commits the content-addressed
1.12.0 tarball, and its gate installs from the committed bytes rather than
fetching the artifact from the registry. `AGENTS.md` carries it as this leg's
offline-gate rule.

## What is here

| File | Role | SHA-256 (as vendored here) |
| --- | --- | --- |
| `contracts/openspec-cli-pin.yaml` | the pin: package, version, npm SHA-512 integrity and SHA-1, tarball, rollback entry, and the estate's `dispositions:` block | `37810bbf1bc17866ea01e0d5acded35e517ddaec2caea7587bd444a9b8c561b6` |
| `scripts/validate-openspec-cli-pin.py` | the consumer entrypoint. It obtains the artifact, recomputes both digests, refuses on a mismatch, installs, asserts the reported version, then runs `openspec validate … --strict` through the installed binary | `5d823c290ee03e017c4006f8780381aa8b17cf873ccf4f3b08782ef18d728093` |
| `scripts/install-pinned-openspec-cli.py` | installs the verified binary and prints its path (and appends it to `$GITHUB_PATH` in CI). An install, never a verdict | `ff3ea122db9ecf89d740d660264f9d37f1d3339e0b3462bc5bdd8e890cc974bb` |
| `.github/workflows/openspec-cli-pin-gate.yml` | runs the entrypoint with `--all --no-cache --tarball <the committed artifact>` on every pull request to `main` | `1a673d05c48e56181b69126de6036e014d5968af6ce970cc05a8a4c12c4abaff` |
| `tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz` | the pinned artifact itself, 477 381 bytes. The file NAME carries the pin's SHA-1, so a version bump cannot silently reuse the path | `ec9737f8211099ef211f9bc7db195fb9a2afe95a52668670b61a5e8d16e1adcc` (supplementary: the pin's referent is the SHA-512 `integrity` and SHA-1 `shasum` in `contracts/openspec-cli-pin.yaml`) |

Each SHA-256 is over the file's full bytes as committed, header included. The
three files above the workflow are byte-identical to openXwallet's vendored
copies, because both were taken from the same openxFactory commit under the same
three-line header. The workflow is this leg's own copy: its header names this
leg and this leg's ruling.

`openspec/config.yaml` is not part of the vendored set. It is here because the
pinned CLI needs it (see "An empty instance" below).

## The drift check

The first three files are **byte-identical** to their openxFactory originals
below a vendoring header block. The fourth, the workflow, is byte-identical
below its 13-line header except for **ONE DECLARED DIVERGENCE**: its final
`run:` line. A copy that can drift silently is worse than no copy, so drift is
one command away:

```bash
# from a checkout of this leg, with any openxFactory checkout reachable
OXF=../openxFactory
C=44d8fbaf7d977668973dcd116040c9405416c2ea
diff <(tail -n +4 contracts/openspec-cli-pin.yaml)               <(git -C "$OXF" show "${C}:contracts/openspec-cli-pin.yaml")
diff <(sed '2,4d'   scripts/validate-openspec-cli-pin.py)        <(git -C "$OXF" show "${C}:scripts/validate-openspec-cli-pin.py")
diff <(sed '2,4d'   scripts/install-pinned-openspec-cli.py)      <(git -C "$OXF" show "${C}:scripts/install-pinned-openspec-cli.py")
diff <(tail -n +14  .github/workflows/openspec-cli-pin-gate.yml) <(git -C "$OXF" show "${C}:.github/workflows/openspec-cli-pin-gate.yml")
```

Write the revision as `"${C}:path"`, with the braces. Under zsh, `$C:` followed
by a letter is read as a history modifier, and `git show` then fails with
"ambiguous argument" instead of comparing anything.

Empty output from the FIRST THREE means those files are exactly openxFactory's
at `44d8fbaf7d977668973dcd116040c9405416c2ea`. Any output is drift, and the fix
is to re-vendor from openxFactory, never to edit anything here.

The fourth prints **exactly this one hunk and nothing else**:

```
101c101
<         run: python3 scripts/validate-openspec-cli-pin.py --all --no-cache --tarball tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz
---
>         run: python3 scripts/validate-openspec-cli-pin.py --all --no-cache
```

Anything beyond that hunk is drift. openXwallet's copy of the same workflow also
carries a `# ---- openXwallet DIVERGENCE` comment block above its `run:` line.
This leg's copy does not: the divergence is stated once, in the header, and the
body differs from openxFactory's on that one line only.

**Measured when this leg's copy was vendored (2026-10-08):** against an
openxFactory checkout carrying `44d8fbaf7d977668973dcd116040c9405416c2ea`, the
first three `diff`s printed nothing (exit 0 each), and the fourth printed
exactly the hunk above (exit 1).

### The artifact itself

The file name is the claim, and this recomputes it:

```bash
python3 - <<'PY'
import base64, hashlib, pathlib
b = pathlib.Path("tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz").read_bytes()
print("bytes    ", len(b))
print("integrity sha512-" + base64.b64encode(hashlib.sha512(b).digest()).decode())
print("shasum   ", hashlib.sha1(b).hexdigest())
PY
# must equal `integrity:` and `shasum:` in contracts/openspec-cli-pin.yaml:
#   477381
#   sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==
#   c844543999f673cdd72445879b86a4abea4c07ef
```

Nothing has to trust this document for that. The gate recomputes both digests
over the committed bytes on every run and refuses `pin-integrity-mismatch`
before installing anything. That refusal was observed before the gate was
trusted (next section).

## The gate, observed refusing before it was trusted

On 2026-10-08, in a scratch copy of this leg, a copy of the tarball had one byte
flipped (offset 238 690, `xor 0x01`; its SHA-256 became
`5cfe17ea2e9fbde1a12b1c5c91cf7fa399f5257a012671fd7606257bdf04e11c`). The gate's
own command was then pointed at the mutated copy:

```
$ OPENSPEC_TELEMETRY=0 python3 scripts/validate-openspec-cli-pin.py --all --no-cache --tarball <mutated copy>
REFUSE pin-integrity-mismatch: fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz: INTEGRITY DRIFT
  recorded   sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==
  recomputed sha512-TR07E5CQH359G6uIsclee7nQmmfBTiY7o0tF2yS7V/mgmX7lawlAwWmTOAa44tIDD4FltUUGeH7ZrcLNBXj86g==
the bytes the registry served are not the bytes this repository pins; the version label matching proves nothing, because the label is not the referent
Remediation: … never edit an integrity value to make this pass. See docs/contract-versioning-policy.md.
$ echo $?
2
```

The same command over the unmutated tarball, in the same scratch copy, exited 0.
The mutated copy kept the pinned file name, so the refusal turned on the bytes
alone. Its trailer names `docs/contract-versioning-policy.md`, which lives in
openxFactory and not here (see "Findings in the vendored code").

## The gate, green over this leg

The gate's own command, run from this leg's root on 2026-10-08 with this leg's
`openspec/` holding only `config.yaml`:

```
$ OPENSPEC_TELEMETRY=0 python3 scripts/validate-openspec-cli-pin.py --all --no-cache \
    --tarball tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (<temporary prefix>/bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
-> <temporary prefix>/bin/openspec validate --all --strict --json  (in <this leg>)
Totals: 0 passed, 0 failed (0 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
$ echo $?
0
```

`0 items` is the honest count before the carve: this leg has no specs and no
changes yet. They arrive at the carve (`README.md`).

## An empty instance: what 1.12.0 needs, measured

Before anything was added under `openspec/`, the gate's command was run over a
scratch copy of this leg in four states:

| State of `openspec/` | Result | Exit |
| --- | --- | --- |
| absent | `REFUSE pin-no-target: … carries no openspec/ directory …` | 2 |
| an empty directory | `REFUSE pin-report-unreadable: validate --all --strict --json emitted a JSON document carrying neither items nor itemFindings (keys: status)`. The CLI's own JSON reported `"code": "no_openspec_root"` | 2 |
| `openspec/config.yaml` alone, `schema: spec-driven` | `Totals: 0 passed, 0 failed (0 items)`, then `OK` | 0 |
| `config.yaml` plus empty `specs/` and `changes/` | the same `OK` | 0 |

So the pinned CLI needs `openspec/config.yaml` and nothing else. The empty
`specs/` and `changes/` directories change nothing, and git would not record
them anyway, so no placeholder files were added. With `config.yaml` committed,
the gate is green over an empty instance. Without it, the gate refuses.

**Why this file and the carve do not collide.** `openspec/config.yaml` is also a
carved row. In opensoft/openXwallet `docs/openwallet-carve-manifest.yaml` it is
`moved_verbatim` to `openwallet_spec`, with SHA-256
`85b53dd24fbe7d19c8b0f0ddccf5e82600c5c372c76b57a2a89dc34dfb0fc5b9`. The file
committed here holds the same 20 bytes. Its git blob is
`b4bbeb946f4c4d9310ee8730c5f89564bc95e9f0`, the same blob openXwallet holds at
`90111df262d6f54f7e82651d860adc12345f83f4:openspec/config.yaml`. The carve's
`--allow-unrelated-histories` merge therefore meets one identical addition on
both sides, which git resolves without a conflict. The cutover runbook in the
assembly root records this as the one path both a birth commit and the carve
add.

## Why the estate's `dispositions:` are inert here

The pin's `dispositions:` block carries four accepted findings, each naming a
`repo:` (`openxFactory` twice, `codexFactory` twice). The entrypoint reads the
validated tree's identity from `git config --get remote.origin.url`, which in
this leg ends `openWallet-spec`. So every one of those entries is out of scope
here: neither applied nor checked for staleness. No edit was needed to get that.
A tree with no `origin` at all would refuse `pin-repo-unidentified`, because the
pin declares dispositions and the run cannot say which repository it is
validating.

## Archiving through the pinned CLI

This leg vendors the gate and not openxFactory's archive routing
(`scripts/proposal-support.py`). That wrapper runs the origin gate, refuses a
change with open task boxes and packages supporting documents, and it imports
openxFactory's own packages. To archive with the pinned binary, run from this
leg's root:

```sh
"$(python3 scripts/install-pinned-openspec-cli.py 2>/dev/null)" archive <change> --yes
```

That fixes WHICH VERSION archives. It does not supply the governance checks, and
it should not be mistaken for them.

## Making the check required

The workflow reports; it does not block. A check cannot be selected as required
until it has reported once. So this leg's ruleset goes EVALUATE, then one
trivial pull request so `openspec-cli-pin` reports, then ACTIVE. In `opensoft`
the rulesets are organisation-sourced, so this is an org-admin act. It is Brett
Heap's (opensoft/openXwallet `split-openwallet-neutral-core` task 4.7), and it is
not attempted here.

## The offline rule and its residual

**The artifact is offline. Its dependency closure is not.** The tarball is
resolved from this tree and verified by SHA-512 before installation. But the
installer runs `npm install --global --prefix … --ignore-scripts <tarball>`, and
`@fission-ai/openspec@1.12.0` declares ten runtime dependencies. Nine are at
caret ranges and `cross-spawn` is pinned exactly at `7.0.6`. npm resolves all
ten from the registry. So the gate still needs the registry to assemble the
CLI's dependency tree, as a fresh runner's `npm install` always does. Because of
the caret ranges, the code the gate executes can also change when a dependency
is republished, with no movement in the pin.

opensoft/openXwallet `docs/openspec-cli-pin.md` measured this residual for the
same installer. With no network and a cold npm cache, the gate refuses
`pin-unresolvable` with `npm error code EAI_AGAIN`. With no network and a warm
cache, it passes end to end. Here, the same no-network, cold-cache run
(`unshare -rn`, an empty `npm_config_cache`) did not finish within 240 seconds
and was killed. The registry is needed either way.

Closing the residual is an openxFactory change, not something this leg may do.
One option is to let `--tarball` honour the install cache. Another is to add a
mode that accepts an already-installed tree carrying the digest stamp. Either
change reaches this leg by re-vendoring.

## Findings in the vendored code, recorded and NOT fixed here

A fix applied here would fork the estate's one pin verifier, and would break the
property that makes vendoring safe: an empty `diff` against openxFactory. So
these are recorded here and belong upstream:

- **The refusal trailer and `resync_runbook:` name
  `docs/contract-versioning-policy.md`**, which lives in openxFactory and not in
  this leg. No code reads either as a path, so nothing breaks. But a reader who
  follows the trailer from here finds nothing. This leg's re-vendoring runbook is
  this document.
- **`--path-mode` overstates what it checked.** It resolves `openspec` from PATH
  and asserts only the reported version. The gate never uses it.
- **`resolve_pinned()` can race on a shared cache directory.** The gate runs
  `--no-cache` on a fresh runner.
- **The workflow's prose describes openxFactory.** Its references to `tests/`
  and `pytest-suite.yml` name things that live there, as the header says. The
  prose is kept verbatim so that drift stays a `diff`.

## Re-vendoring

Re-vendor from openxFactory and never edit in place. Do it in one commit that:

- copies the three files below their headers, and the workflow below its
  13-line header;
- re-applies the one declared `run:` line;
- updates the header's commit;
- re-runs the four `diff`s above;
- updates all five SHA-256s in the table.

A version bump of the pinned CLI changes the tarball's name, bytes and digests
together. It is a human-only governed change in openxFactory, and it reaches
this leg by that re-vendoring.
