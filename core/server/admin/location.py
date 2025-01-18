from django.contrib import admin
from django.utils.html import format_html

from core.server.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    def preview(self, location: Location) -> str:
        return format_html(f"<img src=\"{location.image}\" style=\"max-width: 128px; max-height: 128px\"/>")

    fieldsets = (
        (None, {
            "fields": (
                "name",
            )
        }),
        ("Information", {
            "fields": (
                "category", "latitude", "longitude", "preview", "image",
            )
        }),
    )
    readonly_fields = ("preview",)
