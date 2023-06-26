# Generated by Django 4.2.2 on 2023-06-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0006_speaker_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="speaker",
            name="date",
        ),
        migrations.AddField(
            model_name="event",
            name="date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]