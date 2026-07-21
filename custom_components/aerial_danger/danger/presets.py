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
