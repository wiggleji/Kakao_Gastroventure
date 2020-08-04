# Generated by Django 2.2 on 2020-08-04 07:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128)),
                ('name_keyword', models.CharField(blank=True, max_length=128)),
                ('kakao_id', models.IntegerField(unique=True)),
                ('kakao_url', models.URLField(default='http://place.map.kakao.com/')),
                ('address', models.CharField(default='', max_length=256)),
                ('road_address', models.CharField(default='', max_length=256)),
                ('telephone', models.CharField(default='', max_length=256)),
                ('average_rates', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('comment_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writer', models.CharField(blank=True, max_length=128, null=True)),
                ('date', models.DateField()),
                ('rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('content', models.CharField(blank=True, max_length=256, null=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='service.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_date', models.DateField(blank=True)),
                ('before_data', models.CharField(max_length=256)),
                ('after_data', models.CharField(max_length=256)),
                ('reason', models.CharField(max_length=256)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='license', to='service.Restaurant')),
            ],
        ),
    ]
