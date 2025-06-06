from collections import OrderedDict

from rest_framework.serializers import ModelSerializer

from core.server.models import Review
from core.server.serializers.location import LocationSerializer
from core.server.serializers.user import UserSerializer


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "required": False
            },
        }

    def validate(self, attrs: dict) -> dict:
        attrs["user"] = self.context["request"].user
        return super().validate(attrs)

    def create(self, validated_data: dict) -> Review:
        data = validated_data.copy()
        data.pop("rating")

        review = Review.objects.get_or_none(**data)

        if review is not None:
            return super().update(review, validated_data)

        return super().create(validated_data)

    def to_representation(self, review: Review) -> OrderedDict:
        data = OrderedDict(super().to_representation(review))

        data["user"] = UserSerializer(review.user, context=self.context).data
        data["location"] = LocationSerializer(review.location, context=self.context).data

        return data
