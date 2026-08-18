from django.shortcuts import get_object_or_404, render

from .models import Trail


def catalog(request):
    """Open trails only, shortest first. Closed trails never reach the page."""
    trails = Trail.objects.filter(is_open=True).order_by("distance_km")
    return render(request, "catalog.html", {"trails": trails})


def detail(request, trail_id):
    """One trail, with the time estimate computed by the domain engine."""
    trail = get_object_or_404(Trail, pk=trail_id)
    domain = trail.as_domain()
    return render(request, "detail.html", {
        "trail": trail,
        "estimated_time": domain.estimated_time(),
        "packing_list": domain.packing_list(),
    })
