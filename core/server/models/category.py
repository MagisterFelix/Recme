from django.db import models

from core.server.utils import ImageUtils

from .base import BaseManager, BaseModel


class Category(BaseModel):

    name = models.CharField(max_length=64, unique=True)
    icon = models.FileField(
        upload_to=ImageUtils.upload_image_to,
        validators=[ImageUtils.validate_image_file_extension]
    )

    objects: BaseManager["Category"] = BaseManager()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            obj = Category.objects.get(pk=self.pk)

            if self.icon != obj.icon:
                ImageUtils.remove_image_from(obj.icon.path)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> tuple[int, dict]:
        if "static" not in self.icon.name:
            ImageUtils.remove_image_from(self.icon.path)

        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "categories"
