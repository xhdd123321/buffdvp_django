# Generated by Django 4.0.2 on 2022-03-02 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buff_user', '0005_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
    ]
