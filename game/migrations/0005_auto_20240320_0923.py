# Generated by Django 2.1.15 on 2024-03-20 03:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20240302_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spin',
            name='last_spin',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 1, 53, 16, 273016, tzinfo=utc)),
        ),
    ]
