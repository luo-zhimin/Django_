# Generated by Django 4.2.1 on 2023-06-29 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinfo',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
    ]
