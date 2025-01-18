from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseManager, BaseModel
from .filter import Filter
from .recommendation import Recommendation


class Preference(BaseModel):

    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    _filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    choice = models.CharField(max_length=64)

    objects: BaseManager["Preference"] = BaseManager()

    def __str__(self) -> str:
        return f"{self.choice} for {self._filter.name}"

    def clean(self) -> None:
        super().clean()

        errors = {}

        if hasattr(self, "_filter") and hasattr(self, "choice") and self.choice not in self._filter.options:
            errors["choice"] = "Invalid choice. Choice must be from filter options."

        if errors:
            raise ValidationError(errors, code="invalid")

    class Meta:
        db_table = "preferences"
