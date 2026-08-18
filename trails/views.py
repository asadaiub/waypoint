from django.shortcuts import get_object_or_404, render

from .models import Park, Trail


def catalog(request):
    """Open trails only, shortest first. Closed trails never reach the page."""
    trails = Trail.objects.filter(is_open=True).select_related("park").order_by("distance_km")

    # Cross-relation query (WP-705): narrow to one park via ?park=<id>.
    park_id = request.GET.get("park", "")
    park = None
    if park_id.isdigit():
        park = Park.objects.filter(pk=park_id).first()
        if park:
            trails = trails.filter(park=park)

    return render(request, "catalog.html", {
        "trails": trails,
        "parks": Park.objects.all(),
        "selected_park": park,
    })


def detail(request, trail_id):
    """One trail, with the time estimate computed by the domain engine."""
    trail = get_object_or_404(Trail, pk=trail_id)
    domain = trail.as_domain()
    return render(request, "detail.html", {
        "trail": trail,
        "estimated_time": domain.estimated_time(),
        "packing_list": domain.packing_list(),
    })
