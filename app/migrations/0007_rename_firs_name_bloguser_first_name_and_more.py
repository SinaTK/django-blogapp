# Generated by Django 4.1.4 on 2023-01-25 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_bloguser_date_bloguser_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloguser',
            old_name='firs_name',
            new_name='first_name',
        ),
        migrations.AlterField(
            model_name='bloguser',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
