"""Utilities for resolving area pattern presets."""

from .presets import PRESETS


def locality_ids(region_ids: list[str]) -> list[str]:
    """Return locality IDs owned by selected regions."""
    return [
        locality_id
        for region_id in region_ids
        if (region := PRESETS.get(region_id)) is not None
        for locality_id in region.localities
    ]


def resolve_region_patterns(
    custom_region_patterns: list[str],
    region_ids: list[str],
) -> list[str]:
    """Resolve custom and preset region patterns in stable order."""
    region_patterns = list(custom_region_patterns)
    for region_id in region_ids:
        if region := PRESETS.get(region_id):
            region_patterns.extend(region.patterns)

    return list(dict.fromkeys(region_patterns))


def resolve_locality_patterns(
    custom_locality_patterns: list[str],
    region_ids: list[str],
    selected_locality_ids: list[str],
) -> list[str]:
    """Resolve custom and preset locality patterns in stable order."""
    locality_patterns = list(custom_locality_patterns)
    selected_localities = set(selected_locality_ids)
    for region_id in region_ids:
        if (region := PRESETS.get(region_id)) is None:
            continue
        for locality_id, locality in region.localities.items():
            if locality_id in selected_localities:
                locality_patterns.extend(locality.patterns)

    return list(dict.fromkeys(locality_patterns))
