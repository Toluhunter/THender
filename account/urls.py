from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenBlacklistView

app_name = "account"

urlpatterns = [
    path("signup/", views.RegisterView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("profile/", views.RetrieveUpdateView.as_view(), name="manage"),
    path("profile/<uuid:id>/", views.ProfileView.as_view(), name="profile"),
    path("logout/", TokenBlacklistView.as_view(), name="logout")
]
