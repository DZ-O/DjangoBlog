# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-09-19 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20210919_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_Tag',
            field=models.ManyToManyField(through='app01.Article2ArticleTag', to='app01.ArticleTag'),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_types',
            field=models.ManyToManyField(through='app01.Article2ArticleType', to='app01.ArticleType'),
        ),
    ]