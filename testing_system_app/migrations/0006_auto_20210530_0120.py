# Generated by Django 3.2.3 on 2021-05-29 22:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing_system_app', '0005_auto_20210530_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='current_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 1, 20, 40, 745264)),
        ),
    ]
