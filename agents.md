# AI Coding Agents Guide

## Purpose

Act as a concise, senior Python collaborator. Confirm uncertainties before changing behavior and keep replies short.

## Project Overview

This repository scaffolds a Home Assistant custom integration **Aerial Danger**. It currently includes a manifest, minimal config/option flows, and an empty sensor platform; data fetching and business logic are intentionally absent and will be added later. The integration code lives in `custom_components/aerial_danger`.

### Code structure (current)

- `__init__.py` — sets up/unloads the config entry and forwards platforms; stores per-entry data in `hass.data[DOMAIN]`.
- `config_flow.py` — single-instance config flow that captures a name only; options flow placeholder.
- `const.py` — domain/name constants and platform list.
- `sensor.py` — platform stub; adds no entities yet.
- `translations/` — English and Ukrainian strings for the basic flow.
- `manifest.json` — Home Assistant manifest pointing to this repo.

### Workflow

- Python deps pinned in `pyproject.toml`/`uv.lock`; use `uv` for installs.
- `scripts/bump_version` updates the manifest version in `custom_components/aerial_danger/manifest.json`.
- Dev config lives under `config/` for local HA runs.

<instruction>Keep this guide updated as functionality is implemented.</instruction>
