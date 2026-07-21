"""Utilities for resolving area pattern presets."""

from .presets import PRESETS


def neighborhood_ids(region_ids: list[str]) -> list[str]:
    """Return neighborhood IDs owned by selected regions."""
    return [
        neighborhood_id
        for region_id in region_ids
        if (region := PRESETS.get(region_id)) is not None
        for neighborhood_id in region.neighborhoods
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


def resolve_neighborhood_patterns(
    custom_neighborhood_patterns: list[str],
    region_ids: list[str],
    selected_neighborhood_ids: list[str],
) -> list[str]:
    """Resolve custom and preset neighborhood patterns in stable order."""
    neighborhood_patterns = list(custom_neighborhood_patterns)
    selected_neighborhoods = set(selected_neighborhood_ids)
    for region_id in region_ids:
        if (region := PRESETS.get(region_id)) is None:
            continue
        for neighborhood_id, neighborhood in region.neighborhoods.items():
            if neighborhood_id in selected_neighborhoods:
                neighborhood_patterns.extend(neighborhood.patterns)

    return list(dict.fromkeys(neighborhood_patterns))
