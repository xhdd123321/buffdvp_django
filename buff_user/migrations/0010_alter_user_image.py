# Generated by Django 4.0.2 on 2022-03-03 11:25

import buff_user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buff_user', '0009_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, storage=buff_user.models.OverwriteStorage(), upload_to=buff_user.models.user_directory_path),
        ),
    ]
