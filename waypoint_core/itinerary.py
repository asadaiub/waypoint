"""An ordered plan built from trails (WP-105)."""

from .distance import Distance


class Itinerary:
    """HAS-A list of trails. Composition, not inheritance."""

    def __init__(self, name, trails=None):
        self.name = name
        # Copy the input so two itineraries never share one list.
        self._trails = list(trails) if trails else []

    @property
    def trails(self):
        return tuple(self._trails)

    def add_trail(self, trail):
        self._trails.append(trail)
        return self

    def total_distance(self, unit="km"):
        # Summed by hand for now; Week 8 gives Distance real arithmetic.
        total = 0.0
        for trail in self._trails:
            total += trail.distance.convert(unit).magnitude
        return Distance(total, unit)

    def __len__(self):
        return len(self._trails)

    def __iter__(self):
        return iter(self._trails)

    def __str__(self):
        return f"{self.name}: {len(self)} trails, {self.total_distance()}"
