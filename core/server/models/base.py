from typing import Generic, TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseManager(models.Manager[T], Generic[T]):

    def get_or_none(self, *args, **kwargs) -> T | None:
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):

    objects: BaseManager["BaseModel"] = BaseManager()

    class Meta:
        abstract = True
