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

## Danger Library

This integration should implement a danger checking library. We already have a simplified implementation for this library as a Jinja template in `danger.jinja` file.

Library takes city and neighborhood keywords (might be regexps) as inputs.

This library already has lists of keywords and phases indicating different kind of dangers: ballistic danger, cruise missile danger, drone danger, generic danger. Each of these phrases can contain regexps for narrowing keywords matching. Each of these phrases can contain `{area}` keywords that will be mapped to each of defined cities or neighborhoods resulting in list of `city x keywords`, or `city + neighborhood x keywords`.

The library should expose functions for checking different kinds of dangers:

- ballistic - `(city + neightborhood) x (ballistic_keywords + generic_keywords)`
- cruise missiles - `(city + neighborhood) x (cruise_keywords + generic_keywords)`
- drone - `neighborhood x (dron_keywords + generic_keywords)`
- danger - `ballistic or cruise_missiles or drone`

These functions should take an input message from data source and check for keyword matches in these input message. The resulting value should contain:

```
danger: bool
type: ballistic or cruise or drone
area: city or neighborhood
match: "string that was matched"
message: "original message"
```

`danger` function should compose the value from the rest of the danger functions.

## Integration logic

Integration should use a library described above. The integration should listen for changes in data channels, each time it receives a new value, it should pass it to danger functions and check for dangers.

Integration should expose these entities:

- `event.<name>_danger` - event is published when danger occurs. Event should contain all the relevant data.
- `sensor.<name>_ballistic_danger` - a boolean safety sensor for ballistic danger.
- `sensor.<name>_cruise_danger` - a boolean safety sensor for cruise missile danger.
- `sensor.<name>_drone_danger` - a boolean safety sensor for drone danger.

When danger is `true` the integration should publish an event with all the relevant data and set the relevant sensors to `true`. When value is `false` sensors should be set to `false`.

## Step 1: Danger Library Implementation Plan

- Location: `custom_components/aerial_danger/lib/keywords.py` (phrase templates) and `custom_components/aerial_danger/lib/danger.py` (logic).
- API: a `Detector` class that takes `cities` and `neighborhoods` at init; methods `ballistic_danger(message)`, `cruise_missile_danger(message)`, `drone_danger(message)`, `generic_danger(message)`, and `danger(message)` (composite).
- Return type: `Detection` dataclass with fields `danger: bool`, `type: DangerType | None`, `area`, `match`, `message`; methods return the first match or a negative Detection (`danger=False`, others `None`). `DangerType` enum includes `ballistic`, `cruise`, `drone`, `generic`.
- Matching rules: lowercase message; Unicode + case-insensitive regex. Expand `{area}` placeholders via cartesian product of phrase templates with provided area patterns. Combine phrase sets per plan semantics (`+` = concatenate lists, `x` = every combination of lists). Evaluate order ballistic → cruise → drone, each paired with generic phrases but generic never stands alone. First match wins; area chosen in provided order.
- Performance: compile all regexes once per `Detector` instance to support ~5 sources polling every 5 seconds.
- Tests: to be added later after phrases are finalized; will cover expansion, ordering, first-match behavior, emoji/markdown tolerance, and no-match cases.
