# Generated by Django 4.2.3 on 2023-08-10 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("secretary", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="secretary",
            name="proile_picture",
            field=models.URLField(blank=True, max_length=600, null=True),
        ),
    ]