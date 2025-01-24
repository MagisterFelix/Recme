from collections import OrderedDict

from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from core.server.models import Condition, Preference, Recommendation
from core.server.serializers.location import LocationSerializer
from core.server.serializers.user import UserSerializer


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

    def to_representation(self, recommendation: Recommendation) -> OrderedDict:
        data = OrderedDict(super().to_representation(recommendation))

        data["user"] = UserSerializer(recommendation.user, context=self.context).data
        data["location"] = LocationSerializer(recommendation.location, context=self.context).data

        return data
