# Generated by Django 2.2.12 on 2020-06-10 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWorks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='works',
            name='completion_date',
        ),
        migrations.AddField(
            model_name='works',
            name='completion',
            field=models.BooleanField(default=False),
        ),
    ]
