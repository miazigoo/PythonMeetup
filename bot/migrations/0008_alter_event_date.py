# Generated by Django 4.2.2 on 2023-06-24 15:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0007_remove_speaker_date_event_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
    ]