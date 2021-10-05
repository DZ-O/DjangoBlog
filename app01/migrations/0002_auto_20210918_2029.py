# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-09-18 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article2ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=32, verbose_name='文章标签')),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='article_types',
            field=models.ManyToManyField(through='app01.Article2ArticleTag', to='app01.ArticleTag'),
        ),
        migrations.AlterField(
            model_name='articletype',
            name='types',
            field=models.CharField(max_length=32, verbose_name='文章分类'),
        ),
        migrations.AddField(
            model_name='article2articletag',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article'),
        ),
        migrations.AddField(
            model_name='article2articletag',
            name='article_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ArticleTag'),
        ),
    ]