# Generated by Django 4.1.4 on 2023-01-29 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_log_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log_history',
            name='date',
        ),
        migrations.RemoveField(
            model_name='log_history',
            name='user',
        ),
    ]