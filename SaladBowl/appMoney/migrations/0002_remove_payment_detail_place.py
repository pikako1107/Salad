# Generated by Django 2.2.12 on 2020-06-10 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appMoney', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment_detail',
            name='place',
        ),
    ]
