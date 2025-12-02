# HA Aerial Danger

This should be an integration for Home Assistant that monitors Telegram channels for messages indicating about dangers in specified areas.

## Integration Structure

Entries with list of keywords for cities and neighborhoods.

Subentries for data channels: ability to specify custom data channels (sensors, attributes, templates, text, text_inputs). Data sources will be configured by user manually: by web scraping integrations or by telegram channel bots, etc.

## User Configurations

User should be able to configure entry's name. Subentries name should be inferred from data source name.

Areas should be specified as a list of words (regexps can be used). For example:

**City:**

```
'\\bки(ї|є)в(а|у|ом|е|і)?\\b' # matches Київ in different cases
```

**Neighborhoods:**

```
'\\bнив(ки|ками|ок)\\b',
'\\bсвятошин(а|у|ом|і)?\\b',
'\\bантонов',
'\\bакадем',
'берковець',
'cирець',
'cирця',
'\\bшулявк(а|и)\\b',
'галаган'
```

## Danger Library (implemented)

Location: `custom_components/aerial_danger/danger/keywords.py` (phrase templates) and `custom_components/aerial_danger/danger/danger.py` (logic). API is exposed via `custom_components.aerial_danger.danger` package.

Public API: `DangerDetector` takes city and neighborhood patterns. Methods `ballistic_danger`, `cruise_missile_danger`, `drone_danger`, `generic_danger`, and composite `danger` (ballistic → cruise → drone → generic order). Each returns a `Detection` dataclass with fields `danger: bool`, `type: DangerType | None`, `area`, `match`, `message`; negative results return `danger=False` and `None` for the rest. `DangerType` is an enum: `ballistic`, `cruise`, `drone`, `generic`.

Matching rules: message is lowercased; regexes are compiled once per detector. Phrase templates live only in `keywords.py`; `{area}` placeholders are expanded against city and neighborhood patterns; `+` means concatenation, `x` means cartesian combinations. First match wins; areas are evaluated in provided order. Generic phrases can match alone or alongside others; detection reports the matched type.

Performance: designed for ~5 sources polled every 5 seconds; regexes are compiled up front.

## Integration logic

Integration should use a library described above. The integration should listen for changes in data channels, each time it receives a new value, it should pass it to danger functions and check for dangers.

Integration should expose these entities:

- `event.<type>_danger` - event is published when danger occurs. Event should contain all the relevant data.
- `binary_sensor.<name>_ballistic_danger` - a safety binary sensor for ballistic danger.
- `binary_sensor.<name>_cruise_danger` - a safety binary sensor for cruise missile danger.
- `binary_sensor.<name>_drone_danger` - a safety binary sensor for drone danger.
- `binary_sensor.<name>_unknown_danger` - a safety binary sensor for generic danger.
- `binary_sensor.<name>_danger` - aggregate safety binary sensor; true if any of the above is true.

When danger is `true` the integration should publish an event with all the relevant data and set the relevant sensors to `true`. When value is `false` sensors should be set to `false`.

## Progress

- Step 1: Danger library implemented in `custom_components/aerial_danger/danger/` with compiled regex matching, `DangerDetector`, `Detection` dataclass, and `DangerType` enum. Keywords isolated to `keywords.py` per design.
- Step 2: Library covered by pytest suite in `tests/test_danger.py`; `scripts/test` runs the suite. `scripts/lint` runs ruff; agents guide updated to run tests when touching library code.

## Next Steps

- Step 3: Implement Home Assistant integration wiring (plan below).
- Step 4: Iterate on UX, robustness, and documentation once integration basics are in place.

## Step 3 Plan: Home Assistant Integration

- Config/Options
  - Extend flows to capture: entry name, city regex list, neighborhood regex list, list of HA source entity_ids (textual states), and scan interval only if we later add polling. Options flow must allow editing all of these. Store patterns/options on the entry and build `DangerDetector` from them.
  - User should be able to add more data source (as subentries) later via options flow.
  - Update manifest `iot_class` to `local_push` (state change subscriptions, no external polling).

- Runtime wiring
  - On entry setup, create one detector and keep it under `hass.data[DOMAIN][entry_id]`.
  - Subscribe to `state_changed` for the configured source entities; no extra polling. Process only when the state text actually changes. Each new state (stringified) is sent to the detector.
  - Composite detection order: ballistic → cruise → drone → generic. First match wins. Generic still surfaces as its own type.
  - Fire distinct events per type: `ballistic_danger`, `cruise_danger`, `drone_danger`, `unknown_danger` with payload: type, area, match, message, source entity_id, timestamp.
  - Maintain last detection per type to drive sensors; flip to False when the next processed update does not match that type.

- Entities
  - Expose five `binary_sensor`s with `device_class: safety`: `ballistic_danger`, `cruise_danger`, `drone_danger`, `unknown_danger` (generic), and aggregated `danger` (true if any type is true). Entity IDs prefixed by entry name.
  - Consider a single device to group the sensors; device info keyed on config entry.

- Translations & docs
  - Add strings for new fields, sensors, and event description in `translations/` (en, uk).
  - README section explaining configuration, sensors, events, and expected message sources.

- Validation & testing
  - Reuse library tests;
  - Do not add tests for HA integration itself yet; focus on manual testing in dev environment.
  - Scripts: keep `scripts/lint` and `scripts/test`; add HA-specific test targets if needed.

- UX specifics
  - Sources field in flows uses HA entity selector with multi-select, filtered to text-like entities. For now read only the entity state; later we can extend to pick an attribute or template.
