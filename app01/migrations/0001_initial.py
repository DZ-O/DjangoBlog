# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-09-18 11:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('revise_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
        migrations.CreateModel(
            name='Article2ArticleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(max_length=32, verbose_name='文章种类')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_content', models.CharField(max_length=255, verbose_name='留言')),
                ('message_create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article')),
            ],
        ),
        migrations.AddField(
            model_name='article2articletype',
            name='article_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ArticleType'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_types',
            field=models.ManyToManyField(through='app01.Article2ArticleType', to='app01.ArticleType'),
        ),
    ]
