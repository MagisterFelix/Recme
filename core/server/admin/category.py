from django.contrib import admin
from django.utils.html import format_html

from core.server.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    def preview(self, category: Category) -> str:
        return format_html(f"<img src=\"{category.icon.url}\" style=\"max-width: 128px; max-height: 128px\"/>")

    fieldsets = (
        (None, {
            "fields": (
                "name",
            )
        }),
        ("Information", {
            "fields": (
                "preview", "icon",
            )
        }),
    )
    readonly_fields = ("preview",)
