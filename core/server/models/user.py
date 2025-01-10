from typing import TypeVar

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from core.server.utils import ImageUtils

from .base import BaseManager

T = TypeVar("T", bound="User")


class UserManager(BaseUserManager, BaseManager[T]):

    def create_user(self, name: str, email: str, password: str, **extra_fields) -> T:
        if name is None or name == "":
            raise ValueError("User must have a name.")

        if email is None or email == "":
            raise ValueError("User must have an email.")

        if password is None or password == "":
            raise ValueError("User must have a password.")

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, name: str, email: str, password: str, **extra_fields) -> T:
        if name != "admin":
            raise ValueError("Only 1 superuser can exists.")

        return self.create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser):

    DEFAULT_AVATAR_PATH = "../static/avatar-default-light.svg"

    def upload_image_to(self, filename: str) -> str:
        name = f"user-{self.pk}"
        folder, title = "users", f"{name}-{int(timezone.now().timestamp())}"

        return ImageUtils.upload_image_to(filename, name, folder, title)

    name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    image = models.FileField(
        default=DEFAULT_AVATAR_PATH,
        upload_to=upload_image_to,
        validators=[ImageUtils.validate_image_file_extension]
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects: UserManager["User"] = UserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self):
        return self.name == "admin"

    def has_perm(self, perm: str, obj=None) -> bool:
        return self.is_staff

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_staff

    def delete(self, *args, **kwargs) -> tuple[int, dict]:
        if "static" not in self.image.name:
            ImageUtils.remove_image_from(self.image.path)

        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "user"
