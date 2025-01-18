from django.db import models

from .base import BaseManager, BaseModel
from .category import Category


class Location(BaseModel):

    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.URLField()

    objects: BaseManager["Location"] = BaseManager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "locations"
