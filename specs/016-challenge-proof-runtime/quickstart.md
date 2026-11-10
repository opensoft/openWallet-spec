# Candidate verification

Run in the declared development bench, from the respective feature leg root. Source setup may resolve development dependencies; the tests themselves use no live provider or sibling checkout.

Spec leg:

Use the hash-locked local wheels described in [dependency provenance](../../docs/structural-test-dependencies.md). No registry access is used for structural dependency installation.

```sh
pip --disable-pip-version-check install --no-index --only-binary :all: --find-links tools/structural-test-wheels --require-hashes -r contracts/structural-test-requirements.txt
python -m pytest tests/runtime_contracts -q
python3 scripts/validate-openspec-cli-pin.py --all --tarball tools/openspec-cli-pin/fission-ai-openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef.tgz
```

Code leg, with an isolated environment:

```sh
pip install -e . pytest
python -m pytest tests/ -q
```

Also run the existing syntax gate and validator in plain/strict modes, from this code leg.

Do not use floating branches as runtime pins. Review and merge both legs, then advance the assembly through the shape's lockstep mechanism before consumer acceptance.
