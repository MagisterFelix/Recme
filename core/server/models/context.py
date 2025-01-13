
from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseManager, BaseModel


class Context(BaseModel):

    name = models.CharField(max_length=64, unique=True)
    options = models.JSONField()
    handler = models.TextField()

    objects: BaseManager["Context"] = BaseManager()

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()

        errors = {}

        if hasattr(self, "options") and not isinstance(self.options, list):
            errors["options"] = "Invalid type. Must be a list."

        if hasattr(self, "handler"):
            try:
                compile(self.handler, "handler.py", "exec")
            except SyntaxError as error:
                errors["handler"] = f"Invalid python code: {error.msg}."

        if errors:
            raise ValidationError(errors, code="invalid")

    class Meta:
        db_table = "contexts"
