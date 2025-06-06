import json
import os
import uuid

import jwt
import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile
from django.http import HttpResponse
from django.utils import timezone
from jwt.exceptions import InvalidTokenError

from core.server.models.base import BaseModel


class ImageUtils:

    @staticmethod
    def validate_image_file_extension(file: FieldFile) -> None:
        valid_extensions = [".jpg", ".jpeg", ".png", ".svg"]
        extension = os.path.splitext(file.name)[1]

        if not extension.lower() in valid_extensions:
            raise ValidationError("Uploaded file either not an image or a corrupted image.")

    @staticmethod
    def upload_image_to(instance: BaseModel, filename: str) -> str:
        name = f"{instance.__class__.__name__.lower()}-{uuid.uuid4()}"
        folder, title = instance._meta.db_table.lower(), f"{name}-{int(timezone.now().timestamp())}"

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


class GoogleDataUtils:

    GOOGLE_MAPS_REVIEWS_PATH = settings.BASE_DIR / "db_google_maps_reviews.json"

    @staticmethod
    def load_google_reviews() -> dict:
        if not os.path.exists(GoogleDataUtils.GOOGLE_MAPS_REVIEWS_PATH):
            return {}

        with open(GoogleDataUtils.GOOGLE_MAPS_REVIEWS_PATH) as file:
            reviews = json.load(file)

        return reviews

    @staticmethod
    def get_google_review(reviews: dict, key: int) -> dict:
        review = reviews.get(str(key), {
            "rating": 0,
            "num_of_reviews": 0
        })

        return review

    @staticmethod
    def save_google_reviews(data: dict) -> None:
        reviews = GoogleDataUtils.load_google_reviews()

        for key, value in data.items():
            reviews[key] = value

        with open(GoogleDataUtils.GOOGLE_MAPS_REVIEWS_PATH, "w") as file:
            json.dump(reviews, file, indent=4)

    @staticmethod
    def get_nearby_places(latitude: float, longitude: float) -> None:
        from core.server.models import Category, Location

        api_key = settings.GOOGLE_MAPS_API_KEY
        url = "https://places.googleapis.com/v1/places:searchNearby"

        types = [
            "historical_place",
            "museum",
            "casino",
            "internet_cafe",
            "karaoke",
            "movie_theater",
            "night_club",
            "park",
            "tourist_attraction",
            "zoo",
            "bakery",
            "bar",
            "cafe",
            "coffee_shop",
            "pub",
            "restaurant",
            "hotel",
            "beach",
            "playground",
            "shopping_mall",
        ]
        fields = "places.id,places.types,places.location,places.rating,places.userRatingCount,places.displayName"

        data = json.dumps({
            "includedTypes": types,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": 1000.0
                }
            }
        })

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": fields
        }

        response = requests.post(
            url,
            data=data,
            headers=headers
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None

        results = response.json()
        places = results["places"]

        reviews = {}

        for place in places:
            categories = [cat for cat in place["types"] if cat in types]

            if not categories:
                categories.append(place["types"][0])

            category = Category.objects.get_or_none(name=categories[0].capitalize().replace("_", " "))

            if category is None:
                continue

            location, _ = Location.objects.get_or_create(
                name=place["displayName"]["text"],
                category=category,
                latitude=place["location"]["latitude"],
                longitude=place["location"]["longitude"]
            )

            reviews[str(location.pk)] = {
                "rating": place.get("rating", 0),
                "num_of_reviews": place.get("userRatingCount", 0)
            }

        GoogleDataUtils.save_google_reviews(reviews)
