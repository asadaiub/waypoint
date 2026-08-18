"""The trail hierarchy: one abstract base, several concrete pacings."""

from abc import ABC, abstractmethod

from .distance import Distance
from .mixins import ElevationMixin, RatingMixin

DIFFICULTIES = ("easy", "moderate", "hard", "expert")


class Trail(ABC):
    """Base for every kind of trail.

    Encapsulates difficulty behind a validating setter, and leaves pacing and
    presentation to subclasses.
    """

    # Class state: the unit new trails default to when a feed omits one.
    default_unit = "km"

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty="easy"):
        self._id = trail_id
        self.name = name
        self._distance = distance
        self._elevation_gain_m = self.validate_elevation(elevation_gain_m)
        self.__difficulty = None
        self.set_difficulty(difficulty)

    # -- read-only state ---------------------------------------------
    @property
    def id(self):
        return self._id

    @property
    def distance(self):
        return self._distance

    @property
    def elevation_gain_m(self):
        return self._elevation_gain_m

    @property
    def difficulty(self):
        return self.__difficulty

    def set_difficulty(self, value):
        """Guarded mutator -- the only way difficulty ever changes (WP-102)."""
        self.__difficulty = self.validate_difficulty(value)

    # -- static validators (WP-103) ----------------------------------
    @staticmethod
    def validate_difficulty(value):
        if value not in DIFFICULTIES:
            raise ValueError(f"difficulty must be one of {DIFFICULTIES}, got {value!r}")
        return value

    @staticmethod
    def validate_elevation(value):
        value = int(value)
        if value < 0:
            raise ValueError(f"elevation gain cannot be negative: {value}")
        return value

    # -- alternate constructor / class state (WP-103) ----------------
    @classmethod
    def from_dict(cls, payload):
        """Build a trail from an API-shaped dict.

        Called on a concrete subclass (``DayHike.from_dict(...)``), since
        Week 8 made Trail abstract.
        """
        return cls(
            trail_id=payload["id"],
            name=payload["name"],
            distance=Distance(
                payload["distance"], payload.get("unit", cls.default_unit)
            ),
            elevation_gain_m=payload.get("elevation_gain_m", 0),
            difficulty=payload.get("difficulty", "easy"),
        )

    @classmethod
    def set_default_unit(cls, unit):
        """Change the platform default. Existing trails keep their own unit."""
        if unit not in ("km", "mi"):
            raise ValueError(f"unsupported unit: {unit!r}")
        cls.default_unit = unit

    # -- identity (WP-104) -------------------------------------------
    def __eq__(self, other):
        if not isinstance(other, Trail):
            return NotImplemented
        return self._id == other._id

    def __hash__(self):
        # Hash matches __eq__ so a set() de-duplicates imported trails.
        return hash(self._id)

    # -- polymorphic surface (WP-201) --------------------------------
    @abstractmethod
    def estimated_time(self):
        """Hours on foot, by this trail type's own pacing."""

    @abstractmethod
    def summary(self):
        """One human-readable line for the catalog."""

    def badges(self):
        """Base of the cooperative badge chain the mixins extend."""
        return [self.difficulty]

    def packing_list(self):
        return ["water", "map", "layers"]

    def __str__(self):
        return f"{self.name} ({self.distance})"

    def __repr__(self):
        return (
            f"{type(self).__name__}(id={self._id!r}, name={self.name!r}, "
            f"distance={self.distance!r}, difficulty={self.difficulty!r})"
        )


class DayHike(Trail):
    """Naismith-style pacing: 4.5 km/h, plus an hour per 600 m of ascent."""

    PACE_KMH = 4.5

    def estimated_time(self):
        km = self.distance.convert("km").magnitude
        return round(km / self.PACE_KMH + self.elevation_gain_m / 600, 2)

    def summary(self):
        return f"Day hike - {self.distance}, about {self.estimated_time()} h"


class BackpackingRoute(Trail):
    """Multi-day travel: slower under load, and split across days."""

    PACE_KMH = 3.0

    def __init__(
        self, trail_id, name, distance, elevation_gain_m, difficulty="easy", days=2
    ):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        if days < 1:
            raise ValueError("a backpacking route needs at least one day")
        self.days = days

    def estimated_time(self):
        km = self.distance.convert("km").magnitude
        return round(km / self.PACE_KMH + self.elevation_gain_m / 450, 2)

    def summary(self):
        return f"Backpacking route - {self.distance} over {self.days} days"

    def packing_list(self):
        # Extends rather than replaces (WP-204).
        return super().packing_list() + ["tent", "stove", "sleeping bag"]


class TrailRun(Trail):
    """Running pace, and a deliberately minimal kit."""

    PACE_KMH = 9.0

    def estimated_time(self):
        km = self.distance.convert("km").magnitude
        return round(km / self.PACE_KMH + self.elevation_gain_m / 900, 2)

    def summary(self):
        return f"Trail run - {self.distance}, about {self.estimated_time()} h"

    def packing_list(self):
        # Genuinely different, so it replaces the base list (WP-204).
        return ["water flask", "gels"]


class GuidedDayHike(ElevationMixin, RatingMixin, DayHike):
    """A day hike with a guide, grade reporting and star ratings (WP-203/205).

    MRO: GuidedDayHike -> ElevationMixin -> RatingMixin -> DayHike -> Trail
    -> ABC -> object. A badges() call therefore walks down to Trail, then
    RatingMixin appends stars on the way out, then ElevationMixin appends grade.
    """

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty="easy",
        guide_name="staff",
    ):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self.guide_name = guide_name

    def estimated_time(self):
        # Groups move slower than solo hikers: extend the inherited pacing.
        return round(super().estimated_time() * 1.2, 2)

    def summary(self):
        return f"Guided day hike with {self.guide_name} - {self.distance}"


class LoopTrail(DayHike):
    """A day hike that returns to its trailhead."""

    def summary(self):
        return f"Loop - {self.distance}, back where you started"
