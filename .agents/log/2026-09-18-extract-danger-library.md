---
title: Standalone danger matching library
date: 2026-09-18
status: wip
related_paths:
  - custom_components/aerial_danger/
  - tests/
  - pyproject.toml
  - .github/
---

# Standalone danger matching library

## Decision

- Move matching, models, keywords, presets, pattern helpers, and their tests to
  `python-aerial-danger`. Distribution `aerial-danger`, import `aerial_danger`.
- Preserve matcher behavior and the latest-message source reset contract from
  [Source reset on non-danger messages](2026-08-05-source-reset-on-non-danger.md).
- Keep Home Assistant translation parity and runtime tests in this repository.
- Use uv_build, Python 3.10+, and no runtime dependencies in the library.
- Keep registry dependencies in committed metadata. Local development uses
  `uv add --editable ../python-aerial-danger`; uv manages subsequent syncs.
  Do not commit the local source override or its lockfile changes.
- Dependabot checks uv dependencies weekly, without a separate group.
  `scripts/sync_library` copies the project pin to the HA manifest through
  pre-commit or a manual run; a test detects drift. Same-repository Dependabot
  PRs get an automatic manifest commit using the built-in GitHub token.
- `location_presets.py` exports `LOCATION_PRESETS`. Each region and locality
  carries its registry key as `id`, with no localized display name. Applications
  provide labels. This replaces library-owned names from
  [Regional area presets](2026-08-03-regional-area-presets.md), per review.
- The library's published GitHub release runs tests, builds wheel and sdist,
  and publishes through the `pypi` environment using PyPI trusted publishing.

## Tradeoffs & Alternatives

A committed editable source would prevent normal PyPI dependency updates and
require a sibling checkout in CI. Keep it an opt-in local install instead.
The user chose built-in-token automation for Dependabot over GitHub App setup.
The privileged workflow runs only the base branch's sync script. A separate
sparse PR checkout contains only the project metadata and manifest, treated as
data. It never executes PR code. git-auto-commit-action commits only the manifest,
without fetching or switching away from the observed PR head. Subsequent CI may
require a maintainer to approve workflow runs.

## Verification

- [x] Library tests pass on Python 3.10 and 3.14: 63 each.
- [x] Home Assistant lint and 66 tests pass with the editable library.
- [x] Wheel and sdist builds and isolated install smoke checks pass.
- [x] Both README usage examples execute successfully.
- [x] Publish the first package and regenerate the HA registry lockfile.
- [x] Run workflows on GitHub and confirm PyPI trusted publishing.

## Implementation Notes

2026-09-18: PyPI has no `aerial-danger` release. `uv lock --check` fails because
`aerial-danger==0.1.0` cannot resolve. HA's existing lockfile is intentionally
unchanged until publication; local tests use `scripts/link-library` and
`UV_NO_SYNC=1`. Do not merge the integration extraction until `uv lock` and the
normal CI checks pass. No commits, remote repository, or publication performed.

2026-09-23: Review removed the custom linking and pin-sync scripts and release
mutation. Native uv linking was tested in a disposable HA project copy: repeat
`uv sync --locked` and `uv run --locked` retain the editable library and version
pin. Production metadata remains registry-only. Removed extra lint triggers;
[issue #39](https://github.com/denysdovhan/ha-aerial-danger/issues/39) tracks
removing the workflow path filters later. Added named library workflow steps,
CI/PyPI badges, and pip/Poetry installation commands. Tests use location data
directly rather than a duplicate registry-key list; observed spelling examples
remain regression coverage. HA translations remain unchanged and HA-owned.

Review validation: 63 library tests passed on Python 3.10 and 3.14; 66 HA tests
passed against the existing editable development environment. Both rebuilt
distributions passed smoke tests with `--no-cache`; the first wheel check reused
an older cached 0.1.0 artifact. README examples, Ruff, YAML parsing, named-step
checks, and both repository diff checks passed. Registry lock regeneration
remains deferred until publication.

2026-09-24: Applied documentation and spacing review. Removed contributor-facing
release instructions. Added local pre-commit hooks using uv's locked Ruff for
linting and formatting, plus the pre-commit development dependency. Installed
the hook in the library checkout. Hooks passed against all source/test Python
files; config validation, YAML parsing, README examples, lock validation, and
diff checks passed. No commit performed.

2026-09-24: PyPI now serves aerial-danger 0.1.0. Regenerated the HA lockfile
and replaced the editable installation with the registry package. Manifest and
project pins remain aligned at 0.1.0. Normal lint and all 66 integration tests
pass, including in a fresh isolated HA environment. A separate uncached PyPI
installation passed the package smoke check. Removed the obsolete publication
blocker from contributing.md. The library's Publish workflow succeeded:
https://github.com/denysdovhan/python-aerial-danger/actions/runs/36018924034.
No live HA deployment, integration commit, or push performed.

2026-09-24: Review requested automatic manifest pin updates. Added a stdlib-only
sync utility and pre-commit hook, superseding the earlier manual-update decision.
The utility preserves other requirements and skips writes when already aligned.
All 68 tests, lint, and the hook pass. No release-time mutation or bot commit
workflow was added; Dependabot corrections must still be committed by a maintainer.

2026-09-24: User approved minimal Dependabot automation, superseding the earlier
manual-correction decision. Added sync-library.yml for Dependabot-owned,
same-repository PRs targeting main. It creates a manifest-only commit on the
observed PR head; a normal push rejects concurrent branch changes. Local Git
simulation verified the update, no-op rerun, and rejected stale push. GitHub
execution remains unverified until this workflow and the sync script reach main.

2026-09-24: Review replaced custom Git plumbing with separate trusted and sparse
PR checkouts plus stefanzweifel/git-auto-commit-action. The script remains
base-owned; Python isolated mode prevents PR-local imports, and resolved-path
checks reject data files escaping the PR checkout. The action uses a normal
push, preserving rejection of concurrent branch changes. No GitHub run yet.
