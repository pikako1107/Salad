# Generated by Django 2.2.14 on 2020-07-24 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='EnglishName',
            field=models.TextField(default='', max_length=45),
        ),
    ]
