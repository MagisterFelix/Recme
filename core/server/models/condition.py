from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseManager, BaseModel
from .context import Context
from .recommendation import Recommendation


class Condition(BaseModel):

    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    choice = models.CharField(max_length=64)

    objects: BaseManager["Condition"] = BaseManager()

    def __str__(self) -> str:
        return f"{self.choice} for {self.context.name}"

    def clean(self) -> None:
        super().clean()

        errors = {}

        if hasattr(self, "context") and hasattr(self, "choice") and self.choice not in self.context.options:
            errors["choice"] = "Invalid choice. Choice must be from context options."

        if errors:
            raise ValidationError(errors, code="invalid")

    class Meta:
        db_table = "conditions"
