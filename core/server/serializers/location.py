from collections import OrderedDict

from django.db.models import Avg
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.server.models import Location, Review
from core.server.serializers.category import CategorySerializer


class LocationSerializer(ModelSerializer):

    image = SerializerMethodField(method_name="get_image_url")
    rating = SerializerMethodField(method_name="get_rating")

    class Meta:
        model = Location
        fields = "__all__"

    def get_image_url(self, location: Location) -> str:
        if location.image and location.image.startswith("/static/"):
            return self.context["request"].build_absolute_uri(location.image)

        return location.image

    def get_rating(self, location: Location) -> dict:
        user = self.context["request"].user

        avg_rating = Review.objects.filter(location=location).aggregate(average=Avg("rating"))["average"]
        user_rating = Review.objects.get_or_none(location=location, user=user)

        data = {
            "avg": round(avg_rating, 2) if avg_rating is not None else None,
            "user": user_rating.rating if user_rating is not None else None
        }

        return data

    def to_representation(self, location: Location) -> OrderedDict:
        data = OrderedDict(super().to_representation(location))

        data["category"] = CategorySerializer(location.category, context=self.context).data

        return data
