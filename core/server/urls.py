from django.urls import path

from core.server.views import AuthorizationView, RegistrationView, UserView

urlpatterns = [
    path("sign-in/", AuthorizationView().as_view(), name="sign-in"),
    path("sign-up/", RegistrationView().as_view(), name="sign-up"),
    path("user/", UserView().as_view(), name="user"),
]
