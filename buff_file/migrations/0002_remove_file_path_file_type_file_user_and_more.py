# Generated by Django 4.0.2 on 2022-03-03 15:50

import buff_file.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buff_file', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='path',
        ),
        migrations.AddField(
            model_name='file',
            name='type',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='file',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=buff_file.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='file',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
