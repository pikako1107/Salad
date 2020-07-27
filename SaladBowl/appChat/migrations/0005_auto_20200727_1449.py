# Generated by Django 2.2.14 on 2020-07-27 05:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appChat', '0004_chat_userenglish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='uploadplace',
            field=models.FileField(upload_to='media/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'ogg'])]),
        ),
    ]
