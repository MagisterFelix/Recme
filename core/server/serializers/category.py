from collections import OrderedDict

from rest_framework.serializers import ModelSerializer

from core.server.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, category: Category) -> OrderedDict:
        data = OrderedDict(super().to_representation(category))
        return data
