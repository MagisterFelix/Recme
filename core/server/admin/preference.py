from django.contrib import admin

from core.server.models import Preference


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            "fields": (
                "choice",
            )
        }),
        ("Information", {
            "fields": (
                "recommendation", "_filter",
            )
        }),
    )
