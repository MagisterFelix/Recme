from collections import defaultdict

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.server.models import Filter, Recommendation
from core.server.serializers import RecommendationSerializer


class RecommendationListView(ListAPIView):

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset.filter(user__pk=self.request.user.pk)
        return queryset

    def list(self, request: Request, *args, **kwargs) -> Response:
        correct_filters = Filter.objects.values_list("name", flat=True)
        current_filters = request.query_params.dict()

        for _filter in request.query_params.keys():
            if _filter in correct_filters:
                continue

            current_filters.pop(_filter)

        if not current_filters:
            recommendations = super().list(request, *args, **kwargs)

            if not recommendations.data:
                return recommendations

            grouped_recommendations = defaultdict(list)

            for recommendation in recommendations.data:
                filters = recommendation["filters"]

                group_key = tuple(
                    (condition["context"], condition["choice"])
                    for condition in filters.get("conditions", [])
                ) + tuple(
                    (preference["filter"], preference["choice"])
                    for preference in filters.get("preferences", [])
                )

                grouped_recommendations[group_key].append(recommendation)

            data = [
                {
                    "filters": recommendations[0]["filters"],
                    "recommendations": recommendations
                }
                for recommendations in grouped_recommendations.values()
            ]

            response = Response(data=data, status=status.HTTP_200_OK)

            return response

        return super().list(request, *args, **kwargs)


class RecommendationView(UpdateAPIView):

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (IsAuthenticated,)
