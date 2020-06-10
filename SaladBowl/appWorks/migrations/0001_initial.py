# Generated by Django 2.2.12 on 2020-06-10 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Works',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('writer', models.TextField(max_length=45)),
                ('editor', models.TextField(max_length=45)),
                ('illustrator', models.TextField(max_length=45)),
                ('animator', models.TextField(max_length=45)),
                ('completion_date', models.DateField()),
            ],
        ),
    ]
