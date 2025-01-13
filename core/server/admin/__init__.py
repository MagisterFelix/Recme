from django.contrib import admin
from django.contrib.auth.models import Group

from .context import ContextAdmin
from .filter import FilterAdmin
from .user import UserAdmin

admin.site.unregister(Group)
