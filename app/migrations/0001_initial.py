# Generated by Django 2.2.1 on 2019-05-28 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=128)),
                ('radius', models.CharField(max_length=8)),
                ('period', models.DurationField()),
                ('is_pm1', models.BooleanField()),
                ('is_pm25', models.BooleanField()),
                ('is_pm10', models.BooleanField()),
                ('is_temp', models.BooleanField()),
                ('is_pressure', models.BooleanField()),
                ('is_humidity', models.BooleanField()),
                ('is_wind', models.BooleanField()),
                ('is_clouds', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('configuration', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Configuration')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('configuration', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Configuration')),
                ('group', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
