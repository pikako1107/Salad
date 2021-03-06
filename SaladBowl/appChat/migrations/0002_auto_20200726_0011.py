# Generated by Django 2.2.14 on 2020-07-25 15:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appChat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='check',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='uploadplace',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'ogg'])]),
        ),
    ]
