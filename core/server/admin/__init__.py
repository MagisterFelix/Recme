from django.contrib import admin
from django.contrib.auth.models import Group

from .user import UserAdmin

admin.site.unregister(Group)
