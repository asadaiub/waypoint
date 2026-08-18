"""Waypoint's domain engine: the rules the web layer presents."""

from .distance import Distance
from .itinerary import Itinerary
from .mixins import ElevationMixin, RatingMixin
from .trails import (
    DIFFICULTIES,
    BackpackingRoute,
    DayHike,
    GuidedDayHike,
    LoopTrail,
    Trail,
    TrailRun,
)

__all__ = [
    "Distance",
    "Itinerary",
    "ElevationMixin",
    "RatingMixin",
    "Trail",
    "DayHike",
    "BackpackingRoute",
    "TrailRun",
    "GuidedDayHike",
    "LoopTrail",
    "DIFFICULTIES",
]
