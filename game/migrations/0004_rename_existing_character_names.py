from django.db import migrations


def rename_characters(apps, schema_editor):
    GameResult = apps.get_model("game", "GameResult")
    GameResult.objects.filter(character="girl").update(character_name="صالحة")
    GameResult.objects.filter(character="boy").update(character_name="مفرح")


def restore_character_names(apps, schema_editor):
    GameResult = apps.get_model("game", "GameResult")
    GameResult.objects.filter(character="girl").update(character_name="نورة")
    GameResult.objects.filter(character="boy").update(character_name="راشد")


class Migration(migrations.Migration):
    dependencies = [("game", "0003_alter_gameresult_character_and_more")]

    operations = [migrations.RunPython(rename_characters, restore_character_names)]
