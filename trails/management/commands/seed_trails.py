"""Load a starter catalog: python manage.py seed_trails"""

from django.core.management.base import BaseCommand

from trails.models import Park, Trail

PARKS = [
    ("Bruce Peninsula", "Georgian Bay"),
    ("Algonquin", "Nipissing"),
    ("Rouge Valley", "Greater Toronto"),
]

TRAILS = [
    ("Bruce Peak Loop",     "Bruce Peninsula", "12.4", 480,  "moderate", True),
    ("Devil's Glen",        "Bruce Peninsula", "8.1",  310,  "expert",   True),
    ("Cedar Springs",       "Rouge Valley",    "5.0",  90,   "easy",     True),
    ("Highland Traverse",   "Algonquin",       "41.0", 1250, "expert",   True),
    ("Mizzy Lake",          "Algonquin",       "10.8", 220,  "moderate", True),
    ("Orchard Trail",       "Rouge Valley",    "3.2",  45,   "easy",     True),
    ("Beaver Pond Spur",    "Algonquin",       "2.1",  30,   "easy",     False),
    ("Cliffside Scramble",  "Bruce Peninsula", "6.7",  540,  "hard",     False),
]


class Command(BaseCommand):
    help = "Create the starter parks and trails."

    def handle(self, *args, **options):
        for name, region in PARKS:
            Park.objects.get_or_create(name=name, defaults={"region": region})

        for name, park_name, distance, ascent, difficulty, is_open in TRAILS:
            Trail.objects.get_or_create(
                name=name,
                defaults={
                    "park": Park.objects.get(name=park_name),
                    "distance_km": distance,
                    "elevation_gain": ascent,
                    "difficulty": difficulty,
                    "is_open": is_open,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Park.objects.count()} parks and {Trail.objects.count()} trails."
        ))
