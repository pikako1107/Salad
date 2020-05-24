# Generated by Django 2.2.12 on 2020-05-21 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('set_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=45)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('stock', models.IntegerField()),
                ('owner', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('sales_id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('type', models.IntegerField()),
                ('type_id', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('count', models.IntegerField()),
            ],
            options={
                'db_table': 'sales',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SetProducts',
            fields=[
                ('set_id', models.IntegerField(primary_key=True, serialize=False)),
                ('set_name', models.CharField(max_length=45)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
            ],
            options={
                'db_table': 'set_products',
                'managed': False,
            },
        ),
    ]
