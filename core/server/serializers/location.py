from collections import OrderedDict

from django.db.models import Avg, Count
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.server.models import Location, Review
from core.server.serializers.category import CategorySerializer
from core.server.utils import GoogleDataUtils


class LocationSerializer(ModelSerializer):

    image = SerializerMethodField(method_name="get_image_url")
    rating = SerializerMethodField(method_name="get_rating")

    class Meta:
        model = Location
        fields = "__all__"

    def get_image_url(self, location: Location) -> str:
        return self.context["request"].build_absolute_uri(location.get_image())

    def get_rating(self, location: Location) -> dict:
        user = self.context["request"].user

        reviews = Review.objects.filter(location=location).aggregate(
            review_count=Count("id"),
            average_rating=Avg("rating")
        )

        num_of_reviews = reviews["review_count"] if reviews["review_count"] is not None else 0
        avg_rating = round(reviews["average_rating"], 2) if reviews["average_rating"] is not None else 0
        user_rating = Review.objects.get_or_none(location=location, user=user)

        google_reviews = GoogleDataUtils.load_google_reviews()
        google_review = GoogleDataUtils.get_google_review(google_reviews, location.pk)

        total_reviews = reviews["review_count"] + google_review["num_of_reviews"]

        if total_reviews > 0:
            weighted_rating = (
                (avg_rating or 0) * num_of_reviews +
                (google_review["rating"] or 0) * google_review["num_of_reviews"]
            ) / total_reviews
        else:
            weighted_rating = 0

        data = {
            "cnt": total_reviews,
            "avg": weighted_rating,
            "user": user_rating.rating if user_rating is not None else None
        }

        return data

    def to_representation(self, location: Location) -> OrderedDict:
        data = OrderedDict(super().to_representation(location))

        data["category"] = CategorySerializer(location.category, context=self.context).data

        return data
