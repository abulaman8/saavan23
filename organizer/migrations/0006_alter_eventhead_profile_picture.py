# Generated by Django 4.2.3 on 2023-08-14 10:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizer", "0005_alter_eventhead_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventhead",
            name="profile_picture",
            field=models.URLField(blank=True, null=True),
        ),
    ]
