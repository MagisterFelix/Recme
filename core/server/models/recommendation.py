from django.db import models

from .base import BaseManager, BaseModel
from .location import Location
from .user import User


class Recommendation(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_liked = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects: BaseManager["Recommendation"] = BaseManager()

    def __str__(self) -> str:
        return f"{self.location.name} for {self.user.email}"

    class Meta:
        db_table = "recommendations"
