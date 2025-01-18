from collections import OrderedDict

from rest_framework.serializers import ModelSerializer

from core.server.models import Location
from core.server.serializers.category import CategorySerializer


class LocationSerializer(ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"

    def to_representation(self, location: Location) -> OrderedDict:
        data = OrderedDict(super().to_representation(location))

        data["category"] = CategorySerializer(location.category, context=self.context).data

        return data
