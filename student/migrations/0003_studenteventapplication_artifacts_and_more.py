# Generated by Django 4.2.3 on 2023-07-27 06:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0002_speaker_remove_event_organizers_event_fb_link_and_more"),
        ("student", "0002_studenteventapplication"),
    ]

    operations = [
        migrations.AddField(
            model_name="studenteventapplication",
            name="artifacts",
            field=models.URLField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="events",
            field=models.ManyToManyField(related_name="participants", to="event.event"),
        ),
    ]
