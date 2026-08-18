from django.contrib import admin

from .models import Park, Trail


class TrailInline(admin.TabularInline):
    model = Trail
    extra = 0
    fields = ("name", "distance_km", "difficulty", "is_open")


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "trail_count")
    search_fields = ("name", "region")
    inlines = [TrailInline]

    @admin.display(description="trails")
    def trail_count(self, park):
        return park.trails.count()


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ("name", "park", "distance_km", "elevation_gain", "difficulty", "is_open")
    list_filter = ("difficulty", "is_open", "park")
    search_fields = ("name", "park__name")
    list_editable = ("is_open",)
