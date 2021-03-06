# Generated by Django 3.1.1 on 2020-09-16 12:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import onam_chitty.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chitty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('on', 'Onam Chittty'), ('ch', 'Usuall Chitty')], max_length=2)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(1000)])),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('chitty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onam_chitty.chitty')),
            ],
            bases=(onam_chitty.mixins.TimeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('price_given', models.PositiveIntegerField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onam_chitty.member')),
            ],
            bases=(onam_chitty.mixins.TimeMixin, models.Model),
        ),
    ]
