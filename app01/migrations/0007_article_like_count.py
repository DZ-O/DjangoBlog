# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-09-22 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20210919_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
    ]