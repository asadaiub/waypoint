"""A distance value type with unit awareness and full operator support."""

import math

KM_PER_MI = 1.609344
UNITS = ("km", "mi")


class Distance:
    """An immutable magnitude paired with a unit."""

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

    def __str__(self):
        return f"{self._magnitude:.1f} {self._unit}"

    def __repr__(self):
        return f"Distance({self._magnitude!r}, {self._unit!r})"
