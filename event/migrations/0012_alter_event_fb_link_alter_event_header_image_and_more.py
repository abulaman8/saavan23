# Generated by Django 4.2.3 on 2023-08-14 10:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0011_event_header_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="fb_link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="header_image",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="ig_link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="meet_link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="misc_links",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="twitter_link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="website_links",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="yt_link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="eventpicture",
            name="image",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="judge",
            name="image",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="mentor",
            name="image",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="speaker",
            name="image",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="sponsor",
            name="logo",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="sponsor",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
    ]
