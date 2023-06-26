# Generated by Django 4.2.2 on 2023-06-24 15:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0009_alter_event_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]