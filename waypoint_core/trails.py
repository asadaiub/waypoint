"""The Trail class: encapsulated state with guarded mutation."""

from .distance import Distance

DIFFICULTIES = ("easy", "moderate", "hard", "expert")


class Trail:
    """A named trail with a distance, an ascent, and a guarded difficulty."""

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
        """Build a trail from an API-shaped dict."""
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

    def __str__(self):
        return f"{self.name} ({self.distance})"

    def __repr__(self):
        return (
            f"Trail(id={self._id!r}, name={self.name!r}, "
            f"distance={self.distance!r}, difficulty={self.difficulty!r})"
        )
