## Refusal comment correction (2026-11-17)

The refreshed verifier includes the comment correction at openXfactory source
7aaa749d2defc6ab7e18ffd428283c1ab8dd19c0, reviewed in
[openXfactory #1343](https://github.com/opensoft/openXfactory/pull/1343).
The reviewed source is published on main at 44e7b4bf8443f8d97790899c74228d5b56eab54a. The verifier Python AST, installer and
pin bodies remain identical to the preceding refresh.

| File | Provider SHA-256 | Vendored SHA-256 |
| --- | --- | --- |
| scripts/validate-openspec-cli-pin.py | 316af08da61959a75c4934e85b4ba2db781fb4f887ecce0ace918b57ef386cb7 | b1cc6ba31615a9f2deb0592ac61a7ede34368f4b4e5c55039825484dc8fa527c |
| scripts/install-pinned-openspec-cli.py | 2ef0067678926da91009344b006d67aa9931a46504982329c1f0c7b7dfec1052 | e58647c337c7ab2a70d5c2a6402be3220d568b38caa146ce8621a257bebd7f04 |
| contracts/openspec-cli-pin.yaml | 1bab358ce6d5275fcad6fd1af3a4320aebe42d25c158aa0364d680fd4d8fa482 | 98d107669114bf28473b2c05f602f9d575dd031603ed23546c99dc6a4de0b7c5 |

The existing spec suite passed nine tests and six subtests. The packaged\npinned CLI verified its content address and passed all seven strict targets.\nThe preceding source refresh remains recorded below.

## Shared verifier source refresh (2026-11-17)

This refresh takes the shared verifier from the published openXfactory commit
59c4931fd89811f07f1a02046424a0fa78a2c92a. Its tree matches the reviewed source in
[openXfactory #1341](https://github.com/opensoft/openXfactory/pull/1341).
The installer and pin bodies, packaged CLI, dependency closure and workflow
are identical to the previously admitted versions. The consumer provenance
headers identify the published provider commit. Historical records follow.

| File | Provider SHA-256 | Vendored SHA-256 |
| --- | --- | --- |
| scripts/validate-openspec-cli-pin.py | b23d19aecccae650ed72c7e5e331c26f9589ff6e22bb0ecff7a6d36ef2d83dff | 79a5ffd0eb2a0d6616217392bdc75ce62a1db23dc6007ce05b480d09477e67bb |
| scripts/install-pinned-openspec-cli.py | 2ef0067678926da91009344b006d67aa9931a46504982329c1f0c7b7dfec1052 | c8bcf829c88a2aeec78008e5476e9a4a17d97a621ed6d1e23f88774b98c5f889 |
| contracts/openspec-cli-pin.yaml | 1bab358ce6d5275fcad6fd1af3a4320aebe42d25c158aa0364d680fd4d8fa482 | efb1188daa902ace83dbf440ea917d2a2cbd8c3c0f88fcfcaa8e2f48cee151db |
| contracts/openspec-cli-pin.1.12.0.package-lock.json | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca |

## Admitted neutral source and handoff (2026-11-17)

Provider source 41eab21570efbd942f49b6ca728d286492adf02a is admitted on main
at 53475872efea351bd6bd65994428ea6692b150f4. Its merge tree is identical to
the reviewed source. Full source CI and all six PR conditions passed at 98.5%
new coverage and 0.0% duplication, with A ratings and every hotspot reviewed.
Provider post-merge CI is tracked separately.

This spec is admitted at 0fe3151ccc2f3ffe7f72cca35106df46c180b5b7, code at
ed567edb18a866b16515c86049bfdcdd4722dde9, and the coherent neutral root at
050bede0263255b1ce94bb312ad7ca63104c7e18. All eight contract-artifact hashes
and release labels are unchanged. Both actual consumer contexts pass all 214
immutable provider assertions without skips; both real CLI corpora pass seven
strict targets. Standalone spec validation passes nine tests and six subtests.
Exact source-admission evidence is handed to
[openXwallet #73](https://github.com/opensoft/openXwallet/issues/73), whose
separate actual-main quality-gate acceptance remains pending.

The earlier candidate/preparation records below are historical qualification
snapshots, including their then-pending admission states. This documentation
reconciliation does not change common source, pins, artifacts or authority.

## Canonical coverage and validation extraction candidate (2026-11-17)

Status: prepared from openXfactory #1337 at 41eab21570efbd942f49b6ca728d286492adf02a; provider
main admission remains pending. Existing validation/reconciliation and final
reporting are extracted without changing execution order, refusal handling,
messages, return codes or workspace lifetime. Canonical embedding is tested at
its actual source filename, while the separate source/bytecode attack tests
retain their scratch paths. All214 provider assertions pass; all193 original
assertions remain byte-identical. Actual changed-code line/branch coverage is
100% for the installer and98.21% for the verifier. Full hosted CI remains pending.

| File | Provider body SHA-256 | Complete consumer SHA-256 |
| --- | --- | --- |
| scripts/validate-openspec-cli-pin.py | 53437679d7f7a8a398d7408ff173898c645219b85aa3c324f979c39f2d980ba7 | 081e06361fdd030c5782ca708b25089179ba0efbc9aa39252613a2501b38d382 |
| scripts/install-pinned-openspec-cli.py | 2ef0067678926da91009344b006d67aa9931a46504982329c1f0c7b7dfec1052 | a1263f1ebc4e325296b890e1f79d71d211605fbd793e244a7ff25f09787707aa |
| contracts/openspec-cli-pin.yaml | 1bab358ce6d5275fcad6fd1af3a4320aebe42d25c158aa0364d680fd4d8fa482 | 5fcf3ef2d1d4b01afc3f120b88c97b160f79b2daae7255aa0e81190a3c05ec4f |
| contracts/openspec-cli-pin.1.12.0.package-lock.json | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca |

Earlier entries below remain historical evidence.

## Authenticated embedding candidate (2026-11-16)

Status: prepared from openXfactory #1337 at bd9859850a7939c8e3120dfaeada020ecef4b083; provider
main admission remains pending. The trusted Python embedding interface accepts
the verifier module compiled from authenticated source before initializing the
installer. It never rereads verifier source or cached bytecode in embedding mode.
Standalone imports and all pin/profile/context controls retain their behavior.

The provider suite passes all 211 assertions, including source substitution
and timestamp-valid forged bytecode regressions. All 193 original cases remain.

| File | Provider body SHA-256 | Complete consumer SHA-256 |
| --- | --- | --- |
| scripts/validate-openspec-cli-pin.py | 69c658e0e1fb122e9835fafc5e3078e966f9a7b6c33af95654ec245ddbfe4caf | 1be7c94085f497b83c1e78a7293f5a77e41630e3aa91287c4a0b9509bbe72660 |
| scripts/install-pinned-openspec-cli.py | 2ef0067678926da91009344b006d67aa9931a46504982329c1f0c7b7dfec1052 | 2614677787febf47f9d230e0e7eef93c46b5d9bedf5b6d659f7928eb5d1ab62c |
| contracts/openspec-cli-pin.yaml | 1bab358ce6d5275fcad6fd1af3a4320aebe42d25c158aa0364d680fd4d8fa482 | 51d892a992ddc328da73e5fbd960f2c63fb5d040e251fa6fd748df8ac260cb22 |
| contracts/openspec-cli-pin.1.12.0.package-lock.json | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca |

Earlier entries remain historical evidence.

## Shared consumer-context candidate (2026-11-16)

Status: prepared from openXfactory PR #1337 at 91c6f36b2caeba5f230ebd201a604f863ee4bfef;
provider main admission is pending. The consumer context is an explicit trusted
API argument. Standalone defaults and independent operator pin selection retain
their existing precedence. The adapter can delegate to these authenticated
shared sources while retaining its own pin, lock and validation corpus.

The complete provider suite now contains 209 assertions, retaining all 193
original cases and adding 16 context-boundary cases. CLI version, package lock,
tarball and validation strictness are unchanged. This record supersedes the
current-source statement below; all older preparation and admission receipts
remain historical evidence.

| File | Provider body SHA-256 | Complete consumer SHA-256 |
| --- | --- | --- |
| scripts/validate-openspec-cli-pin.py | 69c658e0e1fb122e9835fafc5e3078e966f9a7b6c33af95654ec245ddbfe4caf | 83071ffeaee05b6c516d58a97d0deb63ce1a9df8be3c0d1f303af3f2052c071e |
| scripts/install-pinned-openspec-cli.py | ca335c19e42a88ccc306d1c33543f60183cc070c4419f84758c50ba05577674a | 72a74f605283309273cfc38a5f8c294652faf65e49c1d43ab560ef8a8fddb6bc |
| contracts/openspec-cli-pin.yaml | 1bab358ce6d5275fcad6fd1af3a4320aebe42d25c158aa0364d680fd4d8fa482 | c9a50270f6b1a2c3516c4fbae1bf0922543ae4a0aadf242963b03bad28e7d072 |
| contracts/openspec-cli-pin.1.12.0.package-lock.json | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca |

## Provider main admission (2026-11-16)

openXfactory #1333 is merged at 828d88c2ca9d7bcf551e1759c847a9789c5c2066.
The qualified source e0e0b9a31ec8f4d5ec2d611d373ce0a918abb5de is an ancestor
of that main commit. All four common files and the complete provider test
selection are byte-identical between the reviewed source and admitted main.
Every applicable PR check, including full pytest and Sonar analysis, passed;
Sourcery was separately skipped. All nine local expert roles and the fresh
hosted Codex review were clear at that exact source head.

The current consumer bodies retain their qualified e0e0b9a headers and hashes.
Nine leg tests plus six subtests and all seven strict CLI items passed.
The earlier preparation/admission states below remain historical receipts.

## Prepared storage-error follow-up e0e0b9a31ec8

The candidate source is openXfactory PR #1333 at e0e0b9a31ec8f4d5ec2d611d373ce0a918abb5de; main admission remains pending. This extends the authenticated supplied-artifact repair with a structured refusal for staging write or sync failures. The provider suite passes all 193 cases, including disk-full and quota regressions before npm is invoked. The verifier body SHA-256 is 6498736d58ae5b5c08835375f680082622882e5ed815dd84ab32ef3e47d00bf0. The other three provider bodies, CLI version, dependency lock and committed tarball are unchanged. Earlier records below remain historical evidence.

# Wallet #73 supplied-artifact correction (2026-11-16)

Status: prepared; provider #1333 main admission pending.

Provider candidate: opensoft/openXfactory@2bb3d5fa08c9922dcfd746bb269705d5457ec20a.
Hosted review of openWallet-spec #12 found that a cold npm cache could cause
the earlier implementation to fetch the CLI again after authenticating its
vendored tarball. The correction stages the exact authenticated byte snapshot
inside the controlled private generation and seeds npm's content-addressed
cache before unchanged locked installation. The same 80-package lock, mandatory
SHA-512, corroborating checksum, operator/profile controls and script suppression
remain in force. No active generation or historical artifact is replaced.

All 191 provider pin tests pass, including real npm installation with an empty
private cache and networking disabled. This spec copy passes four tests/six
subtests, including forged-header refusal. The real pinned production CLI
validated all seven OpenSpec items under --strict with npm networking disabled.
Published consumer CI and provider admission remain pending. The original committed tarball is
unchanged; the dependency-only network residual remains the existing contract.

| File | Provider body SHA-256 | Complete consumer SHA-256 |
| --- | --- | --- |
| scripts/validate-openspec-cli-pin.py | 98bb953aef0fb990b301cd62bfda995b46a5e797346ca88cc180cc457cdd5aca | abdb1e460a8430a5ba5e3b15055b4eca6ed1de719d51cc1ddded88651a35be75 |
| scripts/install-pinned-openspec-cli.py | 082d036c18e40e2794e495633680f62a71795115b250ecd38428e451419fb083 | 518fc06d7f052ec29e25780c9028c8bdbbd4259d66562c75ab7db61937823e09 |
| contracts/openspec-cli-pin.yaml | 1bab358ce6d5275fcad6fd1af3a4320aebe42d25c158aa0364d680fd4d8fa482 | d7181832f4f2c930e8a348a7ad4d771f35733d21bc5144aabea7ed208ad4e9b4 |
| contracts/openspec-cli-pin.1.12.0.package-lock.json | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca |

Python copies carry exactly three declared comments after the provider shebang;
YAML carries those three comments before its provider body; JSON is verbatim.
Consumer checks also reject executable or malformed replacement headers.
Earlier records retain their original measurements and are historical evidence.

# Wallet #73 checksum and trust-boundary maintenance (2026-11-16)

Status: provider admitted; neutral root and consumer acceptance pending.

Provider main 4dd7c73daa3fd6dbbd25f39c1d5ff72ca8d7d1c2 merged the reviewed
371809285508ad4eb53d415103ecddaec5588938 head on 2026-11-16. Its ancestry
and unchanged common tooling bodies were verified before consumption.

Provider: opensoft/openXfactory@371809285508ad4eb53d415103ecddaec5588938.
The existing mandatory SHA-512 authentication and 80-package verified closure
remain in force. npm's SHA-1 corroborating checksum is explicitly nonsecurity
for FIPS compatibility. This also brings the neutral spec leg onto the already
qualified credential/profile, artifact, cache and argument boundaries rather
than patching its older copy. The committed CLI tarball and adapted gate remain
unchanged. No runtime authority, exclusions, thresholds or billing changes.

| File | Provider body SHA-256 | Complete consumer SHA-256 |
| --- | --- | --- |
| scripts/validate-openspec-cli-pin.py | 42f966ceb3c2ce9f11e4587f90a956a1afc52b1ca75adc1b5ac17ccc09514e29 | 2e188db58136328263c5ee725f167a624255802428d946a1c0a5f4f66d39cc1d |
| scripts/install-pinned-openspec-cli.py | 082d036c18e40e2794e495633680f62a71795115b250ecd38428e451419fb083 | a2d94ac4b9cf911206761ec28e75b69622c7d6798166ab315d12f79157a22a48 |
| contracts/openspec-cli-pin.yaml | 1bab358ce6d5275fcad6fd1af3a4320aebe42d25c158aa0364d680fd4d8fa482 | ea2efc1c81a9158acbab801b38c23862ac2e0168337e68388319ff40319725bb |
| contracts/openspec-cli-pin.1.12.0.package-lock.json | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca | 696dce86e5e5699007129310d9de532795ce48467218fba03b729d38c829e2ca |

Python bodies exclude the three comments after the shebang. YAML excludes
its three leading comments; JSON is verbatim. The following earlier records
retain their original measurements and are historical evidence.

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
