from django.urls import path

from . import views

app_name = "game"

urlpatterns = [
    path("characters/", views.characters, name="characters"),
    path("play/", views.play, name="play"),
    path("result/", views.result, name="result"),
    path("results/save/", views.save_result, name="save_result"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
