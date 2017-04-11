# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 23:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.BigIntegerField()),
                ('created_at', models.DateField()),
                ('text', models.TextField()),
                ('retweet_count', models.IntegerField()),
                ('handle', models.CharField(max_length=255)),
                ('media_type', models.CharField(max_length=255, null=True)),
                ('collected_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
