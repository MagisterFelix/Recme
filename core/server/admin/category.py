from django.contrib import admin
from django.utils.html import format_html

from core.server.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    def preview(self, category: Category) -> str:
        return format_html(f"<img src=\"{category.icon.url}\" style=\"width: 128px; height: 128px\"/>")

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
