from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from core.server.models import Review
from core.server.serializers import ReviewSerializer


class ReviewListView(CreateAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)
