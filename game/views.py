import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .models import GameResult


def characters(request):
    return render(request, "game/characters.html")


def play(request):
    return render(request, "game/game.html")


@ensure_csrf_cookie
def result(request):
    return render(request, "game/result.html")


def leaderboard(request):
    results = GameResult.objects.select_related("user").all()
    leaderboard_results = [
        {
            "id": item.id,
            "username": item.user.username if item.user else item.player_name,
            "fullName": item.user.get_full_name() if item.user and item.user.get_full_name() else (item.user.username if item.user else item.player_name),
            "character": item.character,
            "characterName": item.character_name,
            "score": item.score,
            "geckosCaught": item.geckos_caught,
            "timeRemaining": item.time_remaining,
            "status": item.status,
            "level": item.level,
            "lives": item.lives,
            "stars": item.stars,
            "completion": item.completion,
            "date": item.created_at.isoformat(),
        }
        for item in results
    ]
    return render(request, "game/leaderboard.html", {"leaderboard_results": leaderboard_results})


def _bounded_int(value, minimum, maximum, default=0):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(value, maximum))


@require_POST
def save_result(request):
    try:
        payload = json.loads(request.body)
    except (TypeError, json.JSONDecodeError):
        return JsonResponse({"error": "بيانات النتيجة غير صالحة."}, status=400)

    submission_key = str(payload.get("submissionKey", "")).strip()
    if not submission_key or len(submission_key) > 64:
        return JsonResponse({"error": "معرّف المحاولة غير صالح."}, status=400)

    character = payload.get("character")
    if character not in {"girl", "boy"}:
        character = "girl"

    result, created = GameResult.objects.get_or_create(
        submission_key=submission_key,
        defaults={
            "user": request.user if request.user.is_authenticated else None,
            "player_name": str(payload.get("playerName", "لاعب زائر")).strip()[:100] or "لاعب زائر",
            "character": character,
            "character_name": str(payload.get("characterName", "صالحة" if character == "girl" else "مفرح")).strip()[:100],
            "score": _bounded_int(payload.get("score"), 0, 100000),
            "geckos_caught": _bounded_int(payload.get("geckosCaught"), 0, 1000),
            "time_remaining": _bounded_int(payload.get("timeRemaining"), 0, 3600),
            "status": "win" if payload.get("status") == "win" else "lose",
            "level": _bounded_int(payload.get("level"), 1, 3, 1),
            "lives": _bounded_int(payload.get("lives"), 0, 3),
            "stars": _bounded_int(payload.get("stars"), 1, 5, 1),
            "completion": _bounded_int(payload.get("completion"), 0, 100),
        },
    )
    return JsonResponse({"id": result.id, "created": created}, status=201 if created else 200)

