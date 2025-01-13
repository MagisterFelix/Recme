from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from core.server.models import Filter
from core.server.serializers import FilterSerializer


class FilterListView(ListAPIView):

    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
    permission_classes = (IsAuthenticated,)
