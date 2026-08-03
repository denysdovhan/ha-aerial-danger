# Contributing

If you plan to contribute back to this repo, please fork & open a PR.

## How to add translation

Only native speaker can translate to specific language. Use this tool for translating:

[**🌐 Translate via Inlang**](https://inlang.com/editor/github.com/denysdovhan/ha-aerial-danger?ref=badge)

Translation files live in `custom_components/aerial_danger/translations/` (e.g., `en.json`, `uk.json`).

## Submit region and locality regular expressions

Built-in region and locality patterns live in
`custom_components/aerial_danger/danger/presets.py`.

- A **region** is an administrative oblast. Cities, raions, and other places are
  not regions.
- A **locality** is any named place within a region, including a settlement,
  landmark, neighborhood, microdistrict, or similar area.

To submit new patterns:

1. Add the region to `PRESETS`, or add the locality under its owning region.
2. Include patterns for observed spellings and grammatical forms used in active
   danger messages. Keep patterns bounded and exclude forecasts, analysis,
   aftermath, and all-clear wording.
3. Add English and Ukrainian labels in
   `custom_components/aerial_danger/translations/`.
4. Add aliases, inflections, or alternate spellings to `PRESET_EXAMPLES` in
   `tests/danger/test_presets.py`. Do not add a separate test for each preset.
5. Run `scripts/lint` and `scripts/test`, then open a pull request with examples
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
