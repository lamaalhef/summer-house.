from django.conf import settings
from django.db import models


class GameResult(models.Model):
    STATUS_CHOICES = [
        ("win", "فوز"),
        ("lose", "خسارة"),
    ]

    CHARACTER_CHOICES = [
        ("girl", "صالحة"),
        ("boy", "مفرح"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_results",
        verbose_name="المستخدم",
        null=True,
        blank=True,
    )

    player_name = models.CharField(
        "اسم اللاعب",
        max_length=100,
        default="لاعب زائر",
    )

    submission_key = models.CharField(
        "معرّف المحاولة",
        max_length=64,
        unique=True,
        null=True,
        blank=True,
    )

    character = models.CharField(
        "الشخصية",
        max_length=20,
        choices=CHARACTER_CHOICES,
        default="girl",
    )

    character_name = models.CharField(
        "اسم الشخصية",
        max_length=100,
        default="صالحة",
    )

    score = models.PositiveIntegerField(
        "النقاط",
        default=0,
    )

    geckos_caught = models.PositiveIntegerField(
        "عدد الوزغ",
        default=0,
    )

    time_remaining = models.PositiveIntegerField(
        "الوقت المتبقي",
        default=0,
    )

    status = models.CharField(
        "حالة اللعبة",
        max_length=10,
        choices=STATUS_CHOICES,
        default="lose",
    )

    level = models.PositiveIntegerField(
        "المستوى",
        default=1,
    )

    lives = models.PositiveIntegerField(
        "القلوب المتبقية",
        default=0,
    )

    stars = models.PositiveIntegerField(
        "عدد النجوم",
        default=1,
    )

    completion = models.PositiveIntegerField(
        "نسبة الإنجاز",
        default=0,
    )

    created_at = models.DateTimeField(
        "تاريخ اللعب",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "نتيجة لعبة"
        verbose_name_plural = "نتائج اللعبة"
        ordering = ["-score", "-created_at"]

    def __str__(self):
        username = (
            self.user.username
            if self.user
            else "زائر"
        )

        return f"{username} - {self.score} نقطة"





