# Generated by Django 3.1.1 on 2020-09-07 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onam_chitty', '0006_auto_20200907_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]