# Generated by Django 4.0 on 2021-12-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_myuser_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='city',
            field=models.CharField(default='Mumbai', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='state',
            field=models.CharField(default='Maharashtra', max_length=25),
            preserve_default=False,
        ),
    ]
