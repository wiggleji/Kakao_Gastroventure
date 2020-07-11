# Generated by Django 2.2 on 2020-07-06 06:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='average_rates',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='kakao_url',
            field=models.URLField(default='http://place.map.kakao.com/'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='road_address',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='telephone',
            field=models.CharField(default='', max_length=256),
        ),
    ]
