# Generated by Django 2.2.14 on 2020-07-27 07:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appChat', '0005_auto_20200727_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='uploadplace',
            field=models.FileField(upload_to='appChat/static/media/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'ogg'])]),
        ),
    ]