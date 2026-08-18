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
        total = Distance(0, unit)
        for trail in self._trails:
            total = total + trail.distance
        return total

    def total_time(self):
        return round(sum(t.estimated_time() for t in self._trails), 2)

    def __len__(self):
        return len(self._trails)

    def __iter__(self):
        return iter(self._trails)

    def __str__(self):
        return f"{self.name}: {len(self)} trails, {self.total_distance()}"
