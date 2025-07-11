# Generated by Django 5.2.1 on 2025-06-09 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_guide_webinar'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='webinar',
            name='option',
            field=models.CharField(choices=[('podcast', 'Podcast'), ('webinar', 'Webinar'), ('audio', 'Audio')], default='webinar', max_length=30),
        ),
    ]
