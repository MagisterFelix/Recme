from django.contrib import admin

from core.server.models import Context


@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            "fields": (
                "name",
            )
        }),
        ("Information", {
            "fields": (
                "options", "handler",
            )
        }),
    )
