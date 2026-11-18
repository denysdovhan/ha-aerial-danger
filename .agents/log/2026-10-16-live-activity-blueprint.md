---
title: Live Activity blueprint
date: 2026-10-16
status: done
related_paths:
  - blueprints/aerial_danger_live_activity.yaml
  - tests/test_live_activity_blueprint.py
  - readme.md
  - readme.en.md
---

# Live Activity blueprint

## Background

[Automation blueprints](2026-07-30-automation-blueprints.md) cover critical
notifications. Denys Dovhan's
[Live Activity gist](https://gist.github.com/denysdovhan/68a165b86a396ada29aa5c1c2e73e1f6)
follows an alert from start to all-clear, but depends on personal scripts and
Kyiv-specific texts.

## Problem

Users need one reusable Live Activity per air raid alert that shows source
messages and detected dangers without exceeding iOS update throttling.

## Decision

- Start on the Ukraine Alarm sensor turning `on`; end on `on` → `off`, then
  send `clear_notification` after 30 seconds.
- Keep the gist concurrency: `restart` mode, 10/15/30-second holds after start,
  danger, and all-clear. Gate dangers on an active alarm at the automation
  level, so a late detection cannot cancel the all-clear cleanup.
- The stage follows the Aerial Danger device: red while any of its danger
  binary sensors is `on`, with the latest active detection's message;
  otherwise yellow. Alarm start, catch-up, and outage recovery all use it, so
  posts from other sources, outages, or cleared detections cannot contradict
  the integration. Telegram sources often report before Ukraine Alarm, which
  polls every 10 seconds, so an alarm can start red.
- Routine messages start a run only when idle; while a danger is active they
  keep the red stage. After each hold, show the newest message skipped during
  it instead of dropping it.
- Delay routine messages by 1 second. A message Aerial Danger detects as danger
  restarts the run and sends one danger update instead of two.
- Send a detection within 15 seconds of the previous one quietly, so a burst
  from several channels alerts once and spares the iOS update budget.
- Ukraine Alarm outages: `unavailable` → `on` refreshes quietly;
  `unavailable` → `off` only sends `clear_notification`, and only if the
  automation ran within the last 8 hours (iOS ends activities after 8 hours).
  It ends an activity that may still be showing and displays nothing
  otherwise, so restarts do not post false all-clears.
- Ignore attribute-only changes and `unknown`, `unavailable`, or blank states,
  matching the integration's source handling.
- Support several phones with `notify.mobile_app_<registry name>`. Device
  actions take one literal device, and `notify.send_message` drops `data`.
  Skip devices without an available `mobile_app` notify entity; a missing
  action would stop the run for the remaining phones. Send each action once:
  same-name phones share one action.
- Tag each activity by alert sensor (`aerial_danger_live_activity_<object_id>`,
  64 characters max per the Companion docs), so automations for several
  regions on one phone do not end each other's activity.
- Show the stage in the title; iOS updates it. Leave `critical_text` unset: iOS
  shows it beside the title, duplicating it and truncating the title.
- iOS shows two message lines: send the post text only, whitespace collapsed.
- Add `url` and `clickAction` only when a tap path is set.
- Keep colors, icons, and holds fixed; texts are inputs with Ukrainian defaults.

## Tradeoffs & Alternatives

After `unavailable` → `off` the all-clear stage is not shown: the previous
state is unknown, and a visible all-clear would be false after restarts.

iOS may still drop alerting updates sent in quick succession: on a real iPhone,
an all-clear 25 seconds after a danger update did not appear, while one 3
minutes later did.

Out of scope: Telegram refreshing (covered by the Scrape refresh blueprint),
spoken announcements, per-locality or random texts, configurable colors.

## Verification

- [x] `tests/test_live_activity_blueprint.py` runs the blueprint with the
      integration and mocked phones
- [x] End-to-end against Home Assistant 2026.7.0, 2026.9.4, and 2026.10.1
- [x] Physical iPhone through Home Assistant 2026.10.1
- [x] `uv run pre-commit run --all-files`
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-10-16: Verified end-to-end on throwaway Home Assistant instances with a
fake push relay that reports Live Activity tokens like the iOS app: lifecycle,
holds, late dangers, alarm flaps, unusable source states, renamed, push-less,
failing, same-name, and stale phones, two regions on one phone, Android
payloads, and an empty tap path.

2026-10-17: On a physical iPhone, start, quiet routine update, danger,
all-clear, and end on `clear_notification` worked. The title follows the
stage, so `critical_text` was dropped; messages lost the source suffix to fit
two lines; all-clear defaults became «Відбій» / «Відбій повітряної тривоги».
Review added held-message, burst, and outage handling, plus blueprint tests;
a second review based the stage on the danger binary sensors instead of
detection timing. Android 16 not verified.
