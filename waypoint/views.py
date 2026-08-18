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
