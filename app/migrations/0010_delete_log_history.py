# Generated by Django 4.1.4 on 2023-01-31 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_log_history_date_remove_log_history_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='log_history',
        ),
    ]