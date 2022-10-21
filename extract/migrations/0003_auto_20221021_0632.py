# Generated by Django 2.1.15 on 2022-10-21 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('extract', '0002_auto_20221021_0619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='content',
        ),
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Link'),
        ),
    ]