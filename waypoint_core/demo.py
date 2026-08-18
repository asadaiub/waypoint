"""Run the engine on its own: python -m waypoint_core.demo (WP-206)."""

from .distance import Distance
from .itinerary import Itinerary
from .trails import BackpackingRoute, DayHike, GuidedDayHike, TrailRun


class FakeTrail:
    """Inherits nothing. Rides the polymorphic loop on shape alone."""

    def __init__(self, name, hours):
        self.name = name
        self.distance = Distance(1, "km")
        self._hours = hours

    def estimated_time(self):
        return self._hours

    def summary(self):
        return f"Stub trail - {self.distance}"


def build_catalog():
    return [
        DayHike("t-1", "Bruce Peak Loop", Distance(12.4, "km"), 480, "moderate"),
        BackpackingRoute(
            "t-2", "Highland Traverse", Distance(41.0, "km"), 1250, "expert", days=3
        ),
        TrailRun("t-3", "Cedar Springs", Distance(5.0, "km"), 90, "easy"),
        GuidedDayHike(
            "t-4", "Devil's Glen", Distance(8.1, "km"), 310, "hard", guide_name="Rosa"
        ),
        FakeTrail("Stub Trail", 1.0),
    ]


def main():
    catalog = build_catalog()

    print("-- one loop, every type (WP-206) --")
    for trail in catalog:
        print(f"  {trail.name:<20} {trail.estimated_time():>5} h   {trail.summary()}")

    guided = catalog[3]
    guided.add_rating(5)
    guided.add_rating(4)
    print("\n-- mixin composition (WP-205) --")
    print(f"  badges: {guided.badges()}")
    print(f"  MRO:    {' -> '.join(c.__name__ for c in type(guided).__mro__)}")

    print("\n-- operators (WP-202) --")
    print(
        f"  {Distance(3, 'km')} + {Distance(2, 'km')} = {Distance(3, 'km') + Distance(2, 'km')}"
    )
    print(
        f"  sorted: {sorted([Distance(9, 'km'), Distance(2, 'mi'), Distance(1, 'km')])}"
    )

    plan = Itinerary("Weekend", catalog[:3])
    print("\n-- itinerary (WP-105) --")
    print(f"  {plan}")


if __name__ == "__main__":
    main()
