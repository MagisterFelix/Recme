from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .base import BaseManager, BaseModel
from .location import Location
from .user import User


class Review(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects: BaseManager["Review"] = BaseManager()

    def __str__(self) -> str:
        return f"{self.location.name} by {self.user.email}"

    class Meta:
        db_table = "reviews"
