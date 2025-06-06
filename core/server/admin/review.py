from django.contrib import admin

from core.server.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            "fields": (
                "rating",
            )
        }),
        ("Information", {
            "fields": (
                "user", "location", "created_at",
            )
        }),
    )
    readonly_fields = ("created_at",)
