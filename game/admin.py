from django.contrib import admin

from .models import GameResult


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "player_name",
        "character_name",
        "score",
        "geckos_caught",
        "status",
        "level",
        "lives",
        "stars",
        "completion",
        "created_at",
    ]

    list_filter = [
        "status",
        "character",
        "level",
        "stars",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "character_name",
        "player_name",
    ]

    ordering = [
        "-score",
        "-created_at",
    ]

    readonly_fields = [
        "created_at",
    ]
