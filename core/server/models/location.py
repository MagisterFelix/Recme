from django.db import models
from django.templatetags.static import static

from .base import BaseManager, BaseModel
from .category import Category


class Location(BaseModel):

    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.URLField(blank=True)

    objects: BaseManager["Location"] = BaseManager()

    def __str__(self) -> str:
        return self.name

    def get_image(self) -> str:
        return self.image or static("location-default.svg")

    class Meta:
        db_table = "locations"
