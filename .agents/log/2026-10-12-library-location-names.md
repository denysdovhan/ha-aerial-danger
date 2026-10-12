---
title: Library-owned location names
date: 2026-10-12
status: wip
related_paths:
  - scripts/sync_location_names
  - custom_components/aerial_danger/translations/
  - tests/test_preset_translations.py
  - tests/test_sync_location_names.py
---

# Library-owned location names

## Decision

The user requested location names to be owned by python-aerial-danger, superseding
application-owned labels in the [extraction decision](2026-09-18-extract-danger-library.md).
`scripts/sync_location_names` generates only region/locality selector options for
English and Ukrainian from library `names` maps. Other UI translations stay here.
The check mode reports drift without writing. Tests verify exact library parity,
unrelated content preservation, stale option removal, and no-op reruns.

## Release coordination

Keep this PR draft with the existing published requirement until the library PR
merges and a release containing it appears on PyPI. Then update pyproject.toml,
uv.lock and manifest together, regenerate labels, run normal validation, and push.
Do not commit an editable source override or guess the release version. The user
authorized a chat heartbeat to perform this follow-up, but not merging either PR.

## Verification

- [x] 68 HA tests and lint pass against the locally linked library.
- [x] Generated labels retain every existing label and all unrelated UI data.
- [x] Generator check and no-op rerun pass.
- [ ] Validate against the published library release and check remote CI.
