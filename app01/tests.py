from django.test import TestCase  # test.py中无需手动导入，手动创建的测试文件需导入

import os
from django.shortcuts import render, HttpResponse
from app01 import models
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from app01.utils.randomName import random_name
from app01.utils.pc_or_mobile import judge_pc_or_mobile
from app01.utils.page_demo import Pagination
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject1.settings")
django.setup()
if __name__ == "__main__":

    types = models.ArticleType.objects.filter().all()
    tags = models.ArticleTag.objects.filter().all()

    # # 1 查询当前所有的分类及分类下的文章数
    type_list = models.ArticleType.objects.filter().annotate(count_num=Count('article__id')).values_list(
        'count_num')

    print(type_list[0][0])
