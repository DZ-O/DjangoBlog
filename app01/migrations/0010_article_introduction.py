# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-09-24 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='introduction',
            field=models.CharField(default='这是一段简介', max_length=250, verbose_name='文章简介'),
        ),
    ]