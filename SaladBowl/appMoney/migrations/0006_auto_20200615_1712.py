# Generated by Django 2.2.12 on 2020-06-15 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appMoney', '0005_auto_20200614_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_detail',
            name='work_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
