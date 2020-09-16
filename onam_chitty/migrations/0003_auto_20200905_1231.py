# Generated by Django 3.1 on 2020-09-05 07:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onam_chitty', '0002_auto_20200904_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='price_given',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(10000)]),
        ),
    ]