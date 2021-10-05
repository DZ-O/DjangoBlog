# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2021-09-19 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20210919_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_message', models.CharField(max_length=100, verbose_name='首页留言')),
                ('home_article', models.CharField(max_length=10, verbose_name='作者')),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='留言时间')),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='article',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app01.Article'),
            preserve_default=False,
        ),
    ]
