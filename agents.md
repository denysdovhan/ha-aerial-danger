# AI Coding Agents Guide

## Purpose

Act as a concise, senior Python collaborator. Confirm uncertainties before changing behavior and keep replies short.

## Important directives

<important>
In all interactions and commit messages, be extremely concise and sacrifice grammar for the sake of concision.
</important>

<important>
If anything here is unclear, tell me what you want to do and I'll expand these instructions.
</important>

<important>
If you struggle to find a solution, suggest to add logger statements and ask for output to get more context and understand the flow better. When logger output is provided, analyze it to understand what is going on.
</important>

<important>
When updating this file (`agents.md`), DON'T CHANGE the structure, formatting or style of the document. Just add relevant information, without restructuring: add list items, new sections, etc. NEVER REMOVE tags, like <important> or <instruction>.
</important>

<important>
At the end of each plan, give me a list of unresolved questions to answer, if any. Make the questions extremely concise. Sacrifice grammar for the sake of concision.
</important>

<instruction>Keep this guide updated as functionality is implemented.</instruction>

## Design Log

- Before any repository work, read `.agents/log/index.md`.
- Search `.agents/log/` by touched paths and 2-3 task keywords, then read matching entries in full.
- Treat `done` entries as binding and `wip` entries as current direction. Newer decisions win. Surface conflicts before proceeding.
- Cite relevant entries when explaining existing behavior or past decisions.
- Never edit `done` entries. Keep matching `wip` entries and the index current for significant work; skip routine chores.
- Treat matcher fixes as continued detector maintenance: update an existing matching `wip` entry; never create a per-fix entry. If none exists, skip agent-log for routine matcher fixes.

## Project Overview

This repository implements the Home Assistant custom integration **Aerial Danger**. It detects aerial danger messages from user-selected Home Assistant source entities and exposes safety binary sensors, diagnostic match sensors, and danger events. The integration code lives in `custom_components/aerial_danger`.

### Code structure (current)

- `__init__.py` — sets up/unloads each config entry and listens to source state changes.
- `runtime.py` — defines typed direct-push `ConfigEntry.runtime_data` and derives aggregate state from active detections per source.
- `config_flow.py` — multi-entry config flow with user-defined entry titles and options for area regex patterns and text-state source entities; requires patterns and sources and rejects invalid regex patterns.
- `const.py` — grouped configuration, attribute, state, event, logger, and integration constants.
- `entity.py` — shared runtime and device setup for integration entities.
- `binary_sensor.py` — safety binary sensors for IRBM, MLRS, guided bomb, ballistic, cruise, drone, unknown, and aggregate danger; all expose stable matched-message, area, danger, and source attributes.
- `sensor.py` — diagnostic sensors mirroring the aggregate matched message, area, danger, and friendly source name; inactive sensors show clear and IRBM area shows nationwide.
- `event.py` — native Home Assistant event entity for IRBM, MLRS, guided bomb, ballistic, cruise, drone, and unknown detections.
- `trigger.py` — target-based automation triggers for aggregate danger and each native danger event type.
- `triggers.yaml` — target definitions for automation triggers.
- `diagnostics.py` — provides redacted config-entry diagnostics and privacy-safe runtime state details.
- `danger/` — logger-free, Home Assistant agnostic danger detection library, keyword templates, and data models; detections preserve exact matched text and regex patterns.
- `translations/` — English and Ukrainian strings for configuration, entities, and triggers.
- `manifest.json` — Home Assistant manifest pointing to this repo.

### How it works

- Each config entry builds a detector from configured region and locality regex patterns and subscribes to selected Home Assistant source entities.
- Changed source text is checked in order: IRBM, MLRS, guided bomb, ballistic, cruise, drone, then generic danger. First match wins.
- Runtime tracks active detections per source. Every usable changed source state is authoritative: danger stores a detection and any non-danger message clears that source. Binary sensors aggregate remaining detections, and the event entity records each new detection.
- Diagnostic sensors mirror the latest active aggregate detection and return to clear when no danger remains.
- Target-based triggers fire for aggregate danger or filter event-entity updates by danger type, including repeated detections.
- Source data collection stays outside this integration. The `danger/` library stays Home Assistant agnostic and logger-free.

### Parsing data

Here are a few notes on parsing data from external sources. Here are words that always have the same meaning:

- Ballistic missile are usually refered as:
  - `отрк`
  - `бр`
  - `кинджал`
  - `іскандер`
- Intermediate-range ballistic missiles are usually refered as:
  - `брсд`
  - `бсд`
  - `рсд`
  - `орєшнік`
  - `орешник`
  - `кедр`
  - `кєдр`
  - `рс-26`
  - `рубіж`
- IRBM alerts are nationwide and do not require an area match.
- Multiple launch rocket systems are usually refered as:
  - `рсзв`
- Guided bombs are usually refered as:
  - `каб`
  - `керована авіабомба`
  - `керовані авіабомби`
  - `керовані авіаційні бомби`
  - `🟡💣` followed by a locality
- Use `IRBM`, `MLRS`, and `GAB` in short English UI names, and `БРСД`, `РСЗВ`,
  and `КАБ` in short Ukrainian UI names. In longer descriptions, introduce the
  full name followed by its abbreviation in parentheses. Add README footnotes
  for these abbreviations.
- MLRS and guided-bomb alerts require a configured locality match, like drones;
  configured region patterns alone do not activate these danger types.
- Cruise missile are usually refered as:
  - `кр`
  - `крупа кр`
  - `крилаті ракети`
  - `х-101`
  - `калібр`
  - `онікс`
- Drones are usually refered as:
  - `бплa`
  - `безпілотник`
  - `дрон`
  - `шахед`

### Tooling

- Python deps tracked in `pyproject.toml` and `uv.lock`; use `scripts/bootstrap` for dev installs.
- CI workflows (`lint.yml`, `validate.yml`) install uv via `astral-sh/setup-uv` and run tooling with `uv run`.
- Run python tools via `uv run <tool>` to ensure consistent environment.
- Each time you make changes to Python code, run `scripts/lint` to check for errors and formatting issues. Fix any issues reported by the linter.
- Dev config lives under `config/` for local HA runs.

### Development Scripts

Use these scripts for common development tasks. When you make changes and want to validate your work, use these scripts.

- `scripts/bootstrap` - sets up dev environment (creates venv, installs dependencies).
- `scripts/bump_version` - bumps version in manifest.json.
- `scripts/develop` - starts a development Home Assistant server instance on port 8123. Use this script for checking changes in the browser.
- `scripts/lint` - runs linter/formatter. Always use this script for checking for errors and formatting.
- `scripts/setup` - installs dependencies and installs pre-commit.

### Development Process

- Ask for clarification when requirements are ambiguous; surface 2–3 options when trade-offs matter.
- Update documentation and related rules when introducing new patterns or services.
- Keep `readme.md` (Ukrainian) and `readme.en.md` (English) synchronized whenever either file changes.
- When unsure or need to make a significant decision ASK the user for guidance
- Always run `scripts/lint` after making changes to ensure code quality.
- Always run `scripts/test` when modifying library code.
- Commit only when directly asked to do so. Write descriptive commit messages.

## Code Style

Standard Python. 2-spaces indentation.
Never import modules in functions. All imports must be located on top of the file.

## Translations

- Translations: copy `translations/en.json` to add locales; translate values only where appropriate per HA guidelines.
- Entities: Use the `translation_key` defined in sensor/calendar entity descriptions.
- Placeholders: Reference `{region}`, `{provider}`, and `{group}` from `translation_placeholders` supplied by `device_info` when rendering device names.
- Add locales by copying `translations/en.json` and translating values per HA guidelines.

## Home Assistant API

Carefully read links to the Home Assistant Developer documentation for guidance.

Use these code quality guidelines by Home Assistant developers:
https://github.com/home-assistant/core/raw/refs/heads/dev/.github/copilot-instructions.md

Fetch these links to get more information about specific Home Assistant APIs directly from its documentation:

- File structure: https://developers.home-assistant.io/docs/creating_integration_file_structure
- Config Flow: https://developers.home-assistant.io/docs/config_entries_config_flow_handler
- Fetching data: https://developers.home-assistant.io/docs/integration_fetching_data
- Repairs: https://developers.home-assistant.io/docs/core/platform/repairs
- Sensor: https://developers.home-assistant.io/docs/core/entity/sensor
- Events: https://developers.home-assistant.io/docs/core/entity/event
- Config Entries: https://developers.home-assistant.io/docs/config_entries_index
- Data Entry Flow: https://developers.home-assistant.io/docs/data_entry_flow_index
- Manifest: https://developers.home-assistant.io/docs/creating_integration_manifest

## Monitoring data

Here is a list of Telegram channels that report danger. You can use them to fetch examples of messages to test your regex patterns:

- https://telegram.me/s/operinform
- https://telegram.me/s/war_monitor
- https://telegram.me/s/AerisRimor
- https://telegram.me/s/kpszsu
- https://telegram.me/s/nebo_raketa (kyiv only)
- https://telegram.me/s/kyiv_airdef (kyiv only)
- https://telegram.me/s/kyiv_monit0ring (kyiv only)

Kyiv only channels might omit Kyiv city or region in names, so keep that in mind.

When authoring area presets, research the relevant listed Telegram histories. Use live, actionable alert wording and exclude aftermath or summary wording.

### Telegram research workflow

- Open public histories in Browser and search with `https://telegram.me/s/<channel>?q=<term>`.
- Search weapon names, abbreviations, euphemisms, likely misspellings, and word stems; repeat with area names to find terse alerts.
- Open each result in its channel and read neighboring messages before classifying it as an active alert, forecast, analysis, aftermath, or all-clear.
- Use `war_monitor` and `AerisRimor` for precise live wording, `kpszsu` for official terminology, and Kyiv-only channels for terse locality forms.
- Preserve exact spelling, punctuation, emojis, line breaks, and word order in test messages. Do not retain channel names or message IDs in tests.

### Danger matcher authoring

- Start from observed live messages. Require a configured locality for MLRS, guided bombs, and drones; require `{area}` for other non-IRBM alerts. Channel context alone must not bypass area gating.
- Prefer multiple simple one-line regexes for different word orders. Join only equivalent spellings, inflections, or terms with `(|)`.
- Use the smallest observed bounded gap, such as `.{0,48}`, instead of `.*`; do not cross lines unless an observed alert requires it.
- Keep weapon wording in its domain list, target/vector wording in `GENERIC_DANGER`, and resolved or retrospective wording in `SAFETY`. Do not infer a weapon type from an area or target count alone.
- Use strict positive MLRS and guided-bomb regexes; do not add their forecast, analysis, or aftermath wording to `SAFETY`. These posts stay detector-neutral and clear their source under latest-message runtime semantics.
- Anchor bare-area, direct-target, and direction-only generic alerts to the complete message; weapon-specific posts must not match generic danger from an area substring or suffix.
- Treat `☄`/`☄️` as ballistic and `🛵` as drone; do not allow these markers through generic alert prefixes.
- Add exact strings to the matching domain test, use shared region/locality patterns from `tests/danger/common.py`, and deduplicate cases that differ only by area. Add safety negatives for general domains; verify any non-matching source message clears only that source's active danger.

## Commit messages

When generating commit messages, always use this format:

```
<type>(<scope>): summary up to 40 characters

Longer multiline description only for bigger changes that require additional explanations.
```

Summary should be concise and descriptive. Summary should not contain implicit or generic words like (enhance, improve, etc), instead it should clearly specify what is changed.

Use longer descriptions occasionally to describe complex changes, only when it's really necessary.
