# Contributing

If you plan to contribute back to this repo, please fork & open a PR.

## How to add translation

Only native speaker can translate to specific language. Use this tool for translating:

[**🌐 Translate via Inlang**](https://inlang.com/editor/github.com/denysdovhan/ha-aerial-danger?ref=badge)

Translation files live in `custom_components/aerial_danger/translations/` (e.g., `en.json`, `uk.json`).

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
