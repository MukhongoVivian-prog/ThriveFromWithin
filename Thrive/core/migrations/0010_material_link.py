# Generated by Django 5.2.1 on 2025-06-10 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_affirmation_scene_sound_remove_webinar_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='link',
            field=models.TextField(blank=True),
        ),
    ]
