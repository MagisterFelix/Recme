import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile


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
