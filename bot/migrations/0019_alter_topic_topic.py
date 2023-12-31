# Generated by Django 4.2.2 on 2023-06-25 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0018_remove_speaker_event_speaker_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="topic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="bot.event",
            ),
        ),
    ]
