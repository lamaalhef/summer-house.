from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "register/login.html",
        RedirectView.as_view(pattern_name="accounts:login", permanent=False),
    ),
]