from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from core.server.models.user import User


@admin.register(User)
class UserAdmin(UserAdmin):

    def avatar(self, user: User) -> str:
        return format_html(f"<img src=\"{user.image.url}\" style=\"max-width: 128px; max-height: 128px\"/>")

    list_display = ("name", "email",)
    list_filter = ("name",)
    fieldsets = (
        (None, {
            "fields": (
                "email", "password",
            )
        }),
        ("Personal info", {
            "fields": (
                "name", "avatar", "image",
            )
        }),
        ("Important dates", {
            "fields": (
                "last_login",
            )
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "email", "password1", "password2",)
            }
        ),
    )
    readonly_fields = ("avatar", "last_login",)
    search_fields = ("name", "email",)
    ordering = ("email",)
    filter_horizontal = ()
