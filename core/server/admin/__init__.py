from django.contrib import admin
from django.contrib.auth.models import Group

from .category import CategoryAdmin
from .context import ContextAdmin
from .filter import FilterAdmin
from .location import LocationAdmin
from .review import ReviewAdmin
from .user import UserAdmin

admin.site.unregister(Group)
