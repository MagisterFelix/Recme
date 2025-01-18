from django.contrib import admin

from core.server.models import Condition


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            "fields": (
                "choice",
            )
        }),
        ("Information", {
            "fields": (
                "recommendation", "context",
            )
        }),
    )
