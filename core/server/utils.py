import os

import jwt
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile
from django.http import HttpResponse
from django.utils import timezone
from jwt.exceptions import InvalidTokenError


class ImageUtils:

    @staticmethod
    def validate_image_file_extension(file: FieldFile) -> None:
        valid_extensions = [".jpg", ".jpeg", ".png", ".svg"]
        extension = os.path.splitext(file.name)[1]

        if not extension.lower() in valid_extensions:
            raise ValidationError("Uploaded file either not an image or a corrupted image.")

    @staticmethod
    def upload_image_to(filename: str, name: str, folder: str, title: str) -> str:
        directory = os.path.join(settings.MEDIA_ROOT, f"{folder}")

        if not os.path.exists(directory):
            os.makedirs(directory)

        for file in os.listdir(directory):
            if file.startswith(f"{name}-"):
                os.remove(os.path.join(settings.MEDIA_ROOT, f"{folder}/{file}"))

        return f"{folder}/{title}{os.path.splitext(filename)[-1]}"

    @staticmethod
    def remove_image_from(path: str) -> None:
        if not os.path.exists(path):
            return None

        os.remove(path)


class AuthorizationUtils:

    @staticmethod
    def get_user_id(token: str) -> int | None:
        if token is None:
            return None

        try:
            user_id = jwt.decode(
                jwt=token,
                key=settings.SIMPLE_JWT["SIGNING_KEY"],
                algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
            )["user_id"]
        except InvalidTokenError:
            return None

        return user_id

    @staticmethod
    def set_access_cookie(response: HttpResponse, token: str, httponly: bool) -> None:
        cookie = {
            "key": "access_token",
            "value": token,
            "expires": timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            "httponly": httponly,
        }

        response.set_cookie(**cookie)

    @staticmethod
    def remove_access_cookie(response: HttpResponse) -> None:
        response.delete_cookie("access_token")

    @staticmethod
    def set_refresh_cookie(response: HttpResponse, token: str, httponly: bool) -> None:
        cookie = {
            "key": "refresh_token",
            "value": token,
            "expires": timezone.now() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            "httponly": httponly,
        }

        response.set_cookie(**cookie)

    @staticmethod
    def remove_refresh_cookie(response: HttpResponse) -> None:
        response.delete_cookie("refresh_token")
