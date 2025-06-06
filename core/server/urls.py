from django.urls import path

from core.server.views import (AuthorizationView, FilterListView, RecommendationListView, RecommendationView,
                               RegistrationView, ReviewListView, UserView)

urlpatterns = [
    path("sign-in/", AuthorizationView().as_view(), name="sign-in"),
    path("sign-up/", RegistrationView().as_view(), name="sign-up"),
    path("user/", UserView().as_view(), name="user"),
    path("filters/", FilterListView().as_view(), name="filters"),
    path("reviews/", ReviewListView().as_view(), name="reviews"),
    path("recommendations/", RecommendationListView().as_view(), name="recommendations"),
    path("recommendation/<pk>/", RecommendationView().as_view(), name="recommendation"),
]
