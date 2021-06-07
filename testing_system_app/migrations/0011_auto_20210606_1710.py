# Generated by Django 3.2.4 on 2021-06-06 14:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testing_system_app', '0010_auto_20210603_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalreport',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 6, 17, 10, 24, 13734)),
        ),
        migrations.AddField(
            model_name='test',
            name='admin_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 6, 17, 10, 24, 11744)),
        ),
    ]