# Generated by Django 4.2.2 on 2023-06-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0005_alter_speaker_event_alter_topic_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="speaker",
            name="date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]