"""The Week 7 Trail class, now persistent."""

from django.db import models

from waypoint_core import DIFFICULTIES, DayHike, Distance


class Park(models.Model):
    """A protected area that trails belong to."""

    name = models.CharField(max_length=120, unique=True)
    region = models.CharField(max_length=120)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Trail(models.Model):
    """Mirrors the domain Trail's fields, with the same allowed difficulties."""

    DIFFICULTY_CHOICES = [(value, value.title()) for value in DIFFICULTIES]

    name = models.CharField(max_length=120)
    # on_delete=PROTECT: trails are the valuable records here, and a park being
    # removed is far more likely to be a mistake or a merge than a signal that
    # its trails should vanish. PROTECT forces that call to be made explicitly.
    # null=True lets the Week 12 rows survive this migration without a data
    # migration; the admin can then assign parks at leisure.
    park = models.ForeignKey(
        Park, on_delete=models.PROTECT, related_name="trails", null=True, blank=True
    )
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
