import ast
from collections import defaultdict

from django.db import transaction
from django.db.models import Avg, Count, Q
from django.db.models.expressions import RawSQL
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.server.models import Condition, Context, Filter, Location, Preference, Recommendation, Review
from core.server.recommendation_system import recommendation_system
from core.server.serializers import RecommendationSerializer


class RecommendationListView(ListAPIView):

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset.filter(user__pk=self.request.user.pk)
        return queryset

    def list(self, request: Request, *args, **kwargs) -> Response:
        user = request.user
        params = request.query_params.dict()

        correct_filters = Filter.objects.values_list("name", flat=True)
        filters_data = params.copy()

        for _filter in params.keys():
            if _filter in correct_filters:
                continue

            filters_data.pop(_filter)

        if not filters_data:
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

        if ("latitude" not in params) or ("longitude" not in params):
            data = {
                "details": "Geolocation must be provided."
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        latitude, longitude = params.pop("latitude"), params.pop("longitude")

        if not isinstance(latitude, str) or not isinstance(longitude, str):
            data = {
                "details": "Invalid types of geolocation."
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude, longitude = float(latitude), float(longitude)
        except ValueError:
            data = {
                "details": "Invalid types of geolocation."
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            data = {
                "details": "Invalid values of geolocation."
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        functions = set()
        namespace = dict()

        context = Context.objects.all()
        for obj in context:
            parsed_code = ast.parse(obj.handler)

            if isinstance(parsed_code.body[0], ast.FunctionDef):
                function_name = parsed_code.body[0].name
                functions.add((obj.name, function_name))

            exec(obj.handler, namespace)

        context_data = dict()

        for name, function in functions:
            context_data[name] = namespace[function](latitude=latitude, longitude=longitude)

        summary = ", ".join(map(str, filters_data.values())).lower()
        context = "; ".join(map(lambda item: f"{item[0]}: {item[1]}", context_data.items())).lower()

        locations = Location.objects.annotate(
            distance=RawSQL(
                "6371 * acos(cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude)\
                            - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)))",
                [latitude, longitude, latitude]
            )
        ).filter(Q(distance__lte=1))

        data = []

        for location in locations:
            reviews = Review.objects.filter(location=location).aggregate(
                review_count=Count("id"),
                average_rating=Avg("rating")
            )

            data.append({
                "id": location.pk,
                "name": location.name,
                "category": location.category.name,
                "rating": reviews["average_rating"],
                "num_of_reviews": reviews["review_count"],
                "latitude": latitude,
                "longitude": longitude,
                "context": context,
                "summary": summary
            })

        recommended_locations = recommendation_system.get_recommendations(data)

        filter_set = {(k, v) for k, v in filters_data.items()}
        context_set = {(k, v) for k, v in context_data.items()}

        recommendations = []
        for location_id in recommended_locations:
            location = Location.objects.get(id=location_id)

            existing_recommendations = Recommendation.objects.filter(user=user, location=location)

            recommendation = None

            for ex_recommendation in existing_recommendations:
                preferences = Preference.objects.filter(recommendation=ex_recommendation)
                conditions = Condition.objects.filter(recommendation=ex_recommendation)

                existing_filter_set = {(pref._filter.name, pref.choice) for pref in preferences}
                existing_context_set = {(cond.context.name, cond.choice) for cond in conditions}

                if existing_filter_set == filter_set and existing_context_set == context_set:
                    recommendation = ex_recommendation
                    break

            if recommendation is None:
                with transaction.atomic():
                    recommendation = Recommendation.objects.create(user=user, location=location)

                    Preference.objects.bulk_create([
                        Preference(
                            recommendation=recommendation,
                            _filter=Filter.objects.get(name=name),
                            choice=choice
                        )
                        for name, choice in filters_data.items()
                    ])

                    Condition.objects.bulk_create([
                        Condition(
                            recommendation=recommendation,
                            context=Context.objects.get(name=name),
                            choice=choice
                        )
                        for name, choice in context_data.items()
                    ])

            recommendations.append(recommendation)

        response = self.serializer_class(recommendations, many=True, context={"request": self.request}).data

        return Response(data=response, status=status.HTTP_200_OK)


class RecommendationView(UpdateAPIView):

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (IsAuthenticated,)
