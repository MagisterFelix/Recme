from collections import OrderedDict

from rest_framework.serializers import ModelSerializer

from core.server.models import Filter


class FilterSerializer(ModelSerializer):

    class Meta:
        model = Filter
        fields = "__all__"

    def to_representation(self, _filter: Filter) -> OrderedDict:
        data = OrderedDict(super().to_representation(_filter))
        return data
