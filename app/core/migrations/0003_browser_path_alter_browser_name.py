# Generated by Django 4.2.1 on 2024-11-06 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_browser'),
    ]

    operations = [
        migrations.AddField(
            model_name='browser',
            name='path',
            field=models.TextField(default='', verbose_name='ubicacion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='browser',
            name='name',
            field=models.CharField(max_length=50, verbose_name='nombre'),
        ),
    ]