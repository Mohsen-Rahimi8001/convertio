# Generated by Django 5.2 on 2025-04-27 14:22

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to=accounts.models.user_directory_path),
        ),
    ]
