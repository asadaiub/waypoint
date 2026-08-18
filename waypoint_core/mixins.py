"""Small, composable behaviours shared across trail types (WP-205)."""


class ElevationMixin:
    """Adds grade reporting to anything with a distance and an elevation gain."""

    def grade_percent(self):
        metres = self.distance.convert("km").magnitude * 1000
        if metres == 0:
            return 0.0
        return round(self.elevation_gain_m / metres * 100, 1)

    def badges(self):
        return super().badges() + [f"{self.grade_percent()}% grade"]


class RatingMixin:
    """Adds star ratings. Each instance keeps its own list of scores."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ratings = []

    def add_rating(self, stars):
        if not 1 <= stars <= 5:
            raise ValueError("stars must be between 1 and 5")
        self._ratings.append(stars)

    def average_rating(self):
        if not self._ratings:
            return None
        return round(sum(self._ratings) / len(self._ratings), 1)

    def badges(self):
        average = self.average_rating()
        label = "unrated" if average is None else f"{average} stars"
        return super().badges() + [label]
