# Generated by Django 2.1.15 on 2024-01-20 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20240105_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='user',
        ),
        migrations.AddField(
            model_name='link',
            name='pointsperday',
            field=models.FloatField(default=0),
        ),
    ]