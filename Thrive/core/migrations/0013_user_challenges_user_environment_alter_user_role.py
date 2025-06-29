# Generated by Django 5.2.1 on 2025-06-12 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_merge_20250612_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='challenges',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='environment',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'ADMIN'), ('manager', 'MANAGER'), ('employee', 'EMPLOYEE'), ('therapist', 'THERAPIST')], default='employee', max_length=20),
        ),
    ]
