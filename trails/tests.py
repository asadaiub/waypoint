"""Tests across both halves of the project: the web layer and the engine."""

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from waypoint_core import DayHike, Distance, Itinerary
from .models import Park, Trail


class CatalogQueryTests(TestCase):
    """The public catalog must show open trails only, shortest first."""

    @classmethod
    def setUpTestData(cls):
        cls.park = Park.objects.create(name="Bruce Peninsula", region="Georgian Bay")
        cls.other = Park.objects.create(name="Algonquin", region="Nipissing")
        cls.long_trail = Trail.objects.create(
            name="Highland Traverse", park=cls.other,
            distance_km=Decimal("41.0"), elevation_gain=1250, difficulty="expert")
        cls.short_trail = Trail.objects.create(
            name="Cedar Springs", park=cls.park,
            distance_km=Decimal("5.0"), elevation_gain=90, difficulty="easy")
        cls.closed_trail = Trail.objects.create(
            name="Beaver Pond Spur", park=cls.park,
            distance_km=Decimal("2.1"), elevation_gain=30, is_open=False)

    def test_catalog_hides_closed_trails_and_sorts_by_distance(self):
        response = self.client.get(reverse("trails:catalog"))
        self.assertEqual(response.status_code, 200)
        names = [t.name for t in response.context["trails"]]
        self.assertEqual(names, ["Cedar Springs", "Highland Traverse"])
        self.assertNotIn("Beaver Pond Spur", names)

    def test_filtering_by_park_returns_only_that_parks_trails(self):
        response = self.client.get(reverse("trails:catalog"), {"park": self.other.pk})
        self.assertEqual([t.name for t in response.context["trails"]], ["Highland Traverse"])


class TrailDetailTests(TestCase):
    def setUp(self):
        self.trail = Trail.objects.create(
            name="Cedar Springs", distance_km=Decimal("5.0"), elevation_gain=90)

    def test_detail_renders_an_existing_trail(self):
        response = self.client.get(reverse("trails:detail", args=[self.trail.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cedar Springs")

    def test_detail_404s_for_a_missing_trail(self):
        response = self.client.get(reverse("trails:detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class ReportFormTests(TestCase):
    def test_post_thanks_the_reporter_by_name(self):
        response = self.client.post(reverse("report"), {
            "name": "Md Asaduzzaman", "email": "a@example.com",
            "trail": "Cedar Springs", "note": "Washout near the bridge.",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you, Md Asaduzzaman")

    def test_empty_note_is_rejected_with_a_message(self):
        response = self.client.post(reverse("report"), {"name": "Md", "note": "  "})
        self.assertContains(response, "Please give your name and a short note")

    def test_search_without_a_query_still_renders(self):
        self.assertEqual(self.client.get(reverse("search")).status_code, 200)


class DomainRuleTests(TestCase):
    """The engine's rules, tested without any web layer."""

    def test_distance_rejects_a_negative_magnitude(self):
        with self.assertRaises(ValueError):
            Distance(-1, "km")

    def test_distance_addition_and_ordering(self):
        self.assertEqual(Distance(3, "km") + Distance(2, "km"), Distance(5, "km"))
        self.assertTrue(Distance(1, "km") < Distance(1, "mi"))

    def test_invalid_difficulty_is_refused(self):
        with self.assertRaises(ValueError):
            DayHike("t-1", "Bad", Distance(1, "km"), 0, "extreme")

    def test_trails_with_the_same_id_are_equal(self):
        a = DayHike("t-1", "One", Distance(1, "km"), 0)
        b = DayHike("t-1", "Two", Distance(9, "km"), 500)
        self.assertEqual(a, b)

    def test_itineraries_do_not_share_state(self):
        first, second = Itinerary("First"), Itinerary("Second")
        first.add_trail(DayHike("t-1", "One", Distance(5, "km"), 0))
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 0)


class ModelBridgeTests(TestCase):
    def test_model_reuses_the_domain_engine_for_time(self):
        trail = Trail.objects.create(
            name="Cedar Springs", distance_km=Decimal("9.0"), elevation_gain=600)
        # 9 km / 4.5 kmh = 2 h, plus 600 m / 600 = 1 h.
        self.assertEqual(trail.estimated_time(), 3.0)
