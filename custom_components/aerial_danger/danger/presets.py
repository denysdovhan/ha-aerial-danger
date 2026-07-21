"""Area pattern presets for Aerial Danger."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class NeighborhoodPreset:
    """Neighborhood preset definition."""

    name: str
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class RegionPreset:
    """Region preset definition and its neighborhoods."""

    name: str
    patterns: tuple[str, ...]
    neighborhoods: dict[str, NeighborhoodPreset]


PRESETS: Final = {
    "kyiv": RegionPreset(
        name="Kyiv",
        patterns=(
            r"\bки(їв|єва|єві|єву|євом)\b",
            r"\bстолиц(я|і|ю|ею)\b",
        ),
        neighborhoods={
            "kyiv_sviatoshyn": NeighborhoodPreset(
                name="Sviatoshyn", patterns=(r"\bсвятошин(о|а|і)?\b",)
            ),
            "kyiv_akademmistechko": NeighborhoodPreset(
                name="Akademmistechko",
                patterns=(r"\bакадем\b", r"\bакадеммістечк(о|а|у|ом)\b"),
            ),
            "kyiv_antonov": NeighborhoodPreset(
                name="Antonov", patterns=(r"\bантонов(а)?\b",)
            ),
            "kyiv_nyvky": NeighborhoodPreset(
                name="Nyvky", patterns=(r"\bнив(ки|ках|ками|ок)\b",)
            ),
            "kyiv_vynohradar": NeighborhoodPreset(
                name="Vynohradar", patterns=(r"\bвиноградар(а|і|ем)?\b",)
            ),
        },
    )
}


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
