"""A distance value type with unit awareness and full operator support."""

import math

KM_PER_MI = 1.609344
UNITS = ("km", "mi")


class Distance:
    """An immutable magnitude paired with a unit.

    Mixed-unit arithmetic auto-converts to the *left* operand's unit rather
    than raising. Rejecting mixed units would make the common case -- summing
    a catalog whose rows arrived from different feeds -- impossible without
    callers normalising first, and the left operand is the one the caller
    already chose to work in.
    """

    __slots__ = ("_magnitude", "_unit")

    def __init__(self, magnitude, unit="km"):
        magnitude = float(magnitude)
        if magnitude < 0:
            raise ValueError(f"distance cannot be negative: {magnitude}")
        if unit not in UNITS:
            raise ValueError(f"unit must be one of {UNITS}, got {unit!r}")
        self._magnitude = magnitude
        self._unit = unit

    # -- read-only accessors (WP-101) --------------------------------
    @property
    def magnitude(self):
        return self._magnitude

    @property
    def unit(self):
        return self._unit

    def convert(self, unit):
        """Return an equivalent Distance expressed in `unit`."""
        if unit not in UNITS:
            raise ValueError(f"unit must be one of {UNITS}, got {unit!r}")
        if unit == self._unit:
            return Distance(self._magnitude, unit)
        if unit == "mi":
            return Distance(self._magnitude / KM_PER_MI, "mi")
        return Distance(self._magnitude * KM_PER_MI, "km")

    def _as_km(self):
        return self._magnitude if self._unit == "km" else self._magnitude * KM_PER_MI

    # -- operators (WP-202) ------------------------------------------
    def __add__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented
        return Distance(
            self._magnitude + other.convert(self._unit).magnitude, self._unit
        )

    def __sub__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented
        # A negative result is not a distance, so __init__ rejects it.
        return Distance(
            self._magnitude - other.convert(self._unit).magnitude, self._unit
        )

    def __eq__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented
        return math.isclose(self._as_km(), other._as_km(), rel_tol=1e-9, abs_tol=1e-12)

    def __lt__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented
        return self._as_km() < other._as_km()

    def __gt__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented
        return self._as_km() > other._as_km()

    def __hash__(self):
        return hash(round(self._as_km(), 9))

    def __str__(self):
        return f"{self._magnitude:.1f} {self._unit}"

    def __repr__(self):
        return f"Distance({self._magnitude!r}, {self._unit!r})"
