# Generated by Django 4.0 on 2021-12-19 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_product_production_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
