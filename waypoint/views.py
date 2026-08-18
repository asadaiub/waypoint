"""Site-wide pages: the homepage, the trail report form, and search."""

from django.shortcuts import render

SITE_OWNER = "Md Asaduzzaman"


def home(request):
    return render(request, "home.html", {"greeting": SITE_OWNER})


def report(request):
    """GET renders a blank form; POST thanks the reporter by name."""
    if request.method == "POST":
        reporter = request.POST.get("name", "").strip()
        note = request.POST.get("note", "").strip()

        if not reporter or not note:
            return render(request, "report.html", {
                "error": "Please give your name and a short note about the trail.",
                "submitted": request.POST,
            })

        return render(request, "thanks.html", {
            "reporter": reporter,
            "trail": request.POST.get("trail", "").strip(),
        })

    return render(request, "report.html", {})


def search(request):
    """Reads the query safely -- a bare /search/ must not error."""
    query = request.GET.get("q", "")
    return render(request, "search.html", {"query": query})


CATALOG = [
    {"name": "Orchard Trail",     "distance_km": 3.2,  "elevation_gain": 45,   "difficulty": "easy",     "is_open": True},
    {"name": "Cedar Springs",     "distance_km": 5.0,  "elevation_gain": 90,   "difficulty": "easy",     "is_open": True},
    {"name": "Devil's Glen",      "distance_km": 8.1,  "elevation_gain": 310,  "difficulty": "expert",   "is_open": True},
    {"name": "Mizzy Lake",        "distance_km": 10.8, "elevation_gain": 220,  "difficulty": "moderate", "is_open": True},
    {"name": "Bruce Peak Loop",   "distance_km": 12.4, "elevation_gain": 480,  "difficulty": "moderate", "is_open": True},
    {"name": "Highland Traverse", "distance_km": 41.0, "elevation_gain": 1250, "difficulty": "expert",   "is_open": True},
    {"name": "Beaver Pond Spur",  "distance_km": 2.1,  "elevation_gain": 30,   "difficulty": "easy",     "is_open": False},
]


def catalog(request):
    """Renders from a plain list for now; Week 12 swaps in the database."""
    return render(request, "catalog.html", {"trails": CATALOG})
