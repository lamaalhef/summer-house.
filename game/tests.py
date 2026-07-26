import json

from django.test import Client, TestCase
from django.urls import reverse

from .models import GameResult


class GameResultFlowTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True, HTTP_HOST="localhost")
        self.payload = {
            "submissionKey": "test-game-run-0001",
            "playerName": "لاعب الاختبار",
            "character": "girl",
            "characterName": "صالحة",
            "score": 3400,
            "geckosCaught": 24,
            "timeRemaining": 45,
            "status": "win",
            "level": 3,
            "lives": 2,
            "stars": 4,
            "completion": 100,
        }

    def save_result(self):
        response = self.client.get(reverse("game:result"))
        token = response.cookies["csrftoken"].value
        return self.client.post(
            reverse("game:save_result"),
            data=json.dumps(self.payload),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

    def test_result_is_saved_and_is_idempotent(self):
        response = self.save_result()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(GameResult.objects.count(), 1)
        result = GameResult.objects.get()
        self.assertEqual(result.player_name, "لاعب الاختبار")
        self.assertEqual(result.score, 3400)
        self.assertEqual(result.status, "win")

        duplicate_response = self.save_result()
        self.assertEqual(duplicate_response.status_code, 200)
        self.assertEqual(GameResult.objects.count(), 1)

    def test_leaderboard_reads_database_results(self):
        self.save_result()
        response = self.client.get(reverse("game:leaderboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["leaderboard_results"][0]["username"], "لاعب الاختبار")
        self.assertEqual(response.context["leaderboard_results"][0]["score"], 3400)


