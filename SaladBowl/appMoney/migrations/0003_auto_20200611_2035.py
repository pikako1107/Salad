# Generated by Django 2.2.12 on 2020-06-11 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appMoney', '0002_remove_payment_detail_place'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='date',
            new_name='payDate',
        ),
        migrations.RenameField(
            model_name='pos',
            old_name='date',
            new_name='posDate',
        ),
    ]
