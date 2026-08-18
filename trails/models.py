"""The Week 7 Trail class, now persistent."""

from django.db import models

from waypoint_core import DIFFICULTIES, DayHike, Distance


class Trail(models.Model):
    """Mirrors the domain Trail's fields, with the same allowed difficulties."""

    DIFFICULTY_CHOICES = [(value, value.title()) for value in DIFFICULTIES]

    name = models.CharField(max_length=120)
    distance_km = models.DecimalField(max_digits=5, decimal_places=1)
    elevation_gain = models.IntegerField(default=0, help_text="metres of ascent")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="easy")
    is_open = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["distance_km"]

    def __str__(self):
        return self.name

    # -- the bridge back to the domain engine ------------------------
    def as_domain(self):
        """Rebuild this row as a Week 8 domain object."""
        return DayHike(
            trail_id=str(self.pk),
            name=self.name,
            distance=Distance(float(self.distance_km), "km"),
            elevation_gain_m=self.elevation_gain,
            difficulty=self.difficulty,
        )

    def estimated_time(self):
        """Hours on foot, computed by the engine rather than the web layer."""
        return self.as_domain().estimated_time()
