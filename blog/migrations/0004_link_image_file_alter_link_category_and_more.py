# Generated by Django 4.1.1 on 2022-10-07 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_link_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='image_file',
            field=models.ImageField(default=0, upload_to='images'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='link',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.category'),
        ),
        migrations.AlterField(
            model_name='link',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.company'),
        ),
        migrations.AlterField(
            model_name='link',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.country'),
        ),
        migrations.AlterField(
            model_name='link',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.language'),
        ),
    ]
