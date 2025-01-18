from django.contrib import admin

from core.server.models import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            "fields": (
                "is_liked",
            )
        }),
        ("Information", {
            "fields": (
                "user", "location", "created_at",
            )
        }),
    )
    readonly_fields = ("created_at",)
