# Generated by Django 4.2.3 on 2023-09-05 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_alter_event_fb_link_alter_event_header_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]