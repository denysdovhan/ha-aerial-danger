# Contributing

If you plan to contribute back to this repo, please fork & open a PR.

## How to add translation

Only native speaker can translate to specific language. Use this tool for translating:

[**🌐 Translate via Inlang**](https://inlang.com/editor/github.com/denysdovhan/ha-aerial-danger?ref=badge)

Translation files live in `custom_components/aerial_danger/translations/` (e.g., `en.json`, `uk.json`).

## Submit region and locality regular expressions

Built-in region and locality patterns live in
[`python-aerial-danger/src/aerial_danger/location_presets.py`](https://github.com/denysdovhan/python-aerial-danger/blob/main/src/aerial_danger/location_presets.py).

- A **region** is an administrative oblast. Cities, raions, and other places are
  not regions.
- A **locality** is any named place within a region, including a settlement,
  landmark, neighborhood, microdistrict, or similar area.

First [clone and link the library](#develop-the-matcher-locally). Then submit new patterns:

1. Add the region to `LOCATION_PRESETS`, or add the locality under its owning region.
2. Include patterns for observed spellings and grammatical forms used in active
   danger messages. Keep patterns bounded and exclude forecasts, analysis,
   aftermath, and all-clear wording.
3. Add English and Ukrainian labels in
   `custom_components/aerial_danger/translations/`.
4. Add aliases, inflections, or alternate spellings to `PRESET_EXAMPLES` in
   `python-aerial-danger/tests/test_location_presets.py`. Do not add a separate test for each preset.
5. Run the library's tests, then `scripts/lint` and `scripts/test` here. Open pull requests in both repositories with examples
   of the active alert wording that supports the patterns.

## How to run locally

1. Clone this repo to wherever you want:
   ```sh
   git clone https://github.com/denysdovhan/ha-aerial-danger.git
   ```
2. Go into the repo folder:
   ```sh
   cd ha-aerial-danger
   ```
3. Open the project with [VSCode Dev Container](https://code.visualstudio.com/docs/devcontainers/containers)
4. Start a HA via `Run Home Assistant on port 8123` task or run a following command:
   ```sh
   scripts/develop
   ```

Now you have a working Home Assistant instance with this integration installed. You can test your changes by editing the files in `custom_components/aerial_danger` folder and restarting your Home Assistant instance.

## Develop the matcher locally

From the `ha-aerial-danger` repository root, clone
[`python-aerial-danger`](https://github.com/denysdovhan/python-aerial-danger)
next to it and link the package. Skip the clone command if it already exists.

```sh
git clone https://github.com/denysdovhan/python-aerial-danger.git ../python-aerial-danger
uv add --editable ../python-aerial-danger
scripts/test
scripts/develop --skip-pip-packages aerial-danger
```

uv records an editable path in `tool.uv.sources` and keeps it linked on subsequent
`uv sync` and `uv run` commands. Restart Home Assistant after source changes.
The skip flag prevents HA from replacing the local package with its manifest version.
Use a different path if needed; a dev container must also have access to that path.

Keep the local source override and its lockfile changes out of commits.
To return to PyPI, remove the `aerial-danger` entry from `tool.uv.sources`, keep
the published version pin in `project.dependencies`, then run `uv sync`.

## Update the library dependency

Dependabot checks PyPI weekly and updates `pyproject.toml` and `uv.lock`.
Pre-commit copies the library pin from `pyproject.toml` to the HA manifest.
If the hook changes the manifest, stage it and retry the commit.
The `Sync library requirement` workflow commits the matching manifest pin to
same-repository Dependabot pull requests using the built-in GitHub token.
After that commit, GitHub may show **Approve workflows to run** on the PR.
Approve those checks before merging. No extra secrets are required.

You can also run the sync manually:

```sh
uv run python scripts/sync_library
```

For manual dependency updates, commit the manifest with the dependency update.
The requirement test rejects mismatched pins.
