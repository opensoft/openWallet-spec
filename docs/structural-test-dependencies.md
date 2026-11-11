# Offline structural-test dependencies

The structural gate installs only the eleven committed, unmodified wheels in
`tools/structural-test-wheels/`. `contracts/structural-test-requirements.txt`
pins the complete resolved dependency closure by exact version and SHA-256.
Pip uses `--no-index`, `--only-binary :all:` and `--require-hashes`; its
version check is disabled. Missing or altered artifacts refuse before tests.

Preparation used the public `https://pypi.org/simple` index with binary-only
download for jsonschema 4.25.1 and pytest 9.1.1. The resulting exact versions
and hashes are in the lock, and upstream project pages are
`https://pypi.org/project/<name>/<version>/`. Wheels retain their original
package metadata and license files; third-party licenses are not replaced by
this repository's Apache-2.0 license.

This closure targets Python 3.12 on Linux x86_64, matching this CI job.
The rpds wheel is platform-specific. Another platform requires a separately
reviewed complete closure; it must not silently fetch or build from an index.
No new network exception is introduced. The pre-existing npm resolution
residual belongs only to the OpenSpec installer and does not apply here.
