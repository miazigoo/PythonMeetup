# Generated by Django 4.2.2 on 2023-06-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0010_event_created_alter_event_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="created",
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]