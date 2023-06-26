# Generated by Django 4.2.2 on 2023-06-24 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0014_alter_question_options_alter_topic_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="speaker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="speakers_topic",
                to="bot.speaker",
            ),
        ),
    ]