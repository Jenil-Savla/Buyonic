# Generated by Django 4.0 on 2021-12-19 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_myuser_city_myuser_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='address',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='contact',
            field=models.BigIntegerField(max_length=10, null=True, unique=True),
        ),
    ]
