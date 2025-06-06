from collections import OrderedDict

from django.db.models import Avg, Count
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from core.server.models import Condition, Preference, Recommendation, Review
from core.server.recommendation_system import recommendation_system
from core.server.serializers.location import LocationSerializer
from core.server.serializers.user import UserSerializer
from core.server.utils import GoogleDataUtils


class RecommendationSerializer(ModelSerializer):

    filters = SerializerMethodField(method_name="get_filters")

    class Meta:
        model = Recommendation
        fields = "__all__"

    def get_filters(self, recommendation: Recommendation) -> dict:
        conditions = [
            {"context": condition["context__name"], "choice": condition["choice"]}
            for condition in Condition.objects.filter(
                recommendation=recommendation
            ).values("context__name", "choice")
        ]
        preferences = [
            {"filter": preference["_filter__name"], "choice": preference["choice"]}
            for preference in Preference.objects.filter(
                recommendation=recommendation
            ).values("_filter__name", "choice")
        ]

        data = {
            "conditions": conditions,
            "preferences": preferences
        }

        return data

    def validate(self, attrs: dict) -> dict:
        if len(attrs) > 1 or "is_liked" not in attrs:
            raise ValidationError("Only the 'is_liked' field can be updated.")

        return super().validate(attrs)

    def update(self, recommendation: Recommendation, validated_data: dict) -> Recommendation:
        reviews = Review.objects.filter(location=recommendation.location).aggregate(
            review_count=Count("id"),
            average_rating=Avg("rating")
        )

        preferences = Preference.objects.filter(recommendation=recommendation)
        conditions = Condition.objects.filter(recommendation=recommendation)

        summary = ", ".join(map(lambda item: item.choice, preferences)).lower()
        context = "; ".join(map(lambda item: f"{item.context.name}: {item.choice}", conditions)).lower()

        google_reviews = GoogleDataUtils.load_google_reviews()
        google_review = GoogleDataUtils.get_google_review(google_reviews, recommendation.location.pk)

        total_reviews = reviews["review_count"] + google_review["num_of_reviews"]

        if total_reviews > 0:
            weighted_rating = (
                (reviews["average_rating"] or 0) * reviews["review_count"] +
                (google_review["rating"] or 0) * google_review["num_of_reviews"]
            ) / total_reviews
        else:
            weighted_rating = 0

        data = {
            "id": recommendation.location.pk,
            "name": recommendation.location.name,
            "category": recommendation.location.category.name,
            "rating": weighted_rating,
            "num_of_reviews": total_reviews,
            "latitude": recommendation.location.latitude,
            "longitude": recommendation.location.longitude,
            "context": context,
            "summary": summary,
            "recommend": 1 if validated_data["is_liked"] else 0
        }

        recommendation_system.fine_tune(data)

        return super().update(recommendation, validated_data)

    def to_representation(self, recommendation: Recommendation) -> OrderedDict:
        data = OrderedDict(super().to_representation(recommendation))

        data["user"] = UserSerializer(recommendation.user, context=self.context).data
        data["location"] = LocationSerializer(recommendation.location, context=self.context).data

        return data
