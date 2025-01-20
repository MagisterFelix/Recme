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

    def save(self, *args, **kwargs) -> None:
        if not self.image:
            self.image = static("location-default.svg")

        super().save(*args, **kwargs)

    class Meta:
        db_table = "locations"
