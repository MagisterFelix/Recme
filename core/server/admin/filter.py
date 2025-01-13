from django.contrib import admin
from django.utils.html import format_html

from core.server.models import Filter


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):

    def preview(self, filter: Filter) -> str:
        return format_html(f"<img src=\"{filter.icon.url}\" style=\"max-width: 128px; max-height: 128px\"/>")

    fieldsets = (
        (None, {
            "fields": (
                "name",
            )
        }),
        ("Information", {
            "fields": (
                "options", "preview", "icon",
            )
        }),
    )
    readonly_fields = ("preview",)
