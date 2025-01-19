from collections import OrderedDict

from django.db.models import Avg
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.server.models import Location, Review
from core.server.serializers.category import CategorySerializer


class LocationSerializer(ModelSerializer):

    rating = SerializerMethodField(method_name="get_avg_rating")

    class Meta:
        model = Location
        fields = "__all__"

    def get_avg_rating(self, location: Location) -> float | None:
        avg_rating = Review.objects.filter(location=location).aggregate(average=Avg("rating"))["average"]
        return round(avg_rating, 2) if avg_rating is not None else None

    def to_representation(self, location: Location) -> OrderedDict:
        data = OrderedDict(super().to_representation(location))

        data["category"] = CategorySerializer(location.category, context=self.context).data

        return data
