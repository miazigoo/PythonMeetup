# Generated by Django 4.2.2 on 2023-06-24 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0012_alter_event_created"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nikname",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="UserName"
                    ),
                ),
                ("text", models.TextField()),
                (
                    "speaker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="speaker_questions",
                        to="bot.speaker",
                    ),
                ),
            ],
        ),
    ]
