import time

from django.db import models


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=64, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    revise_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    like_count = models.IntegerField(default=0,verbose_name='点赞数')
    article_types = models.ForeignKey(to='ArticleType')
    introduction = models.CharField(max_length=250,verbose_name='文章简介',default='这是一段简介')
    article_Tag = models.ManyToManyField(to='ArticleTag',
                                         through='Article2ArticleTag',
                                         through_fields=('article', 'article_tag')
                                         )


class ArticleType(models.Model):
    types = models.CharField(max_length=32, verbose_name='文章分类')  # 日常、技术、分享.....


class ArticleTag(models.Model):
    tag = models.CharField(max_length=32, verbose_name='文章标签')  # java、pyhon.....


class Message(models.Model):
    user = models.CharField(max_length=10, verbose_name='留言人')
    message_content = models.CharField(max_length=255, verbose_name='留言')
    message_create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    article = models.ForeignKey(to='Article')


# class Article2ArticleType(models.Model):
#     article = models.ForeignKey(to='Article')
#     article_type = models.ForeignKey(to='ArticleType')


class Article2ArticleTag(models.Model):
    article = models.ForeignKey(to='Article')
    article_tag = models.ForeignKey(to='ArticleTag')


class Target(models.Model):
    target = models.CharField(max_length=100, verbose_name='目标')


class Text(models.Model):
    text = models.CharField(max_length=100, verbose_name='文本')


class HomeMessage(models.Model):
    home_message = models.CharField(max_length=100, verbose_name='首页留言')
    home_article = models.CharField(max_length=10, verbose_name='作者')
    creat_time = models.DateTimeField(verbose_name='留言时间', auto_now_add=True, )
