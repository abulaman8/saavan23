# Generated by Django 4.2.3 on 2023-08-14 10:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0013_rename_stduent_studenteventapplication_student"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="profile_picture",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="studenteventapplication",
            name="artifacts",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="studentteameventapplictaion",
            name="artifacts",
            field=models.URLField(blank=True, null=True),
        ),
    ]
