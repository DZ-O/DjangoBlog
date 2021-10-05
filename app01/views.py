import datetime
import os

from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from app01.utils.randomName import random_name
from app01.utils.pc_or_mobile import judge_pc_or_mobile
from app01.utils.page_demo import Pagination
import json
from django.http import JsonResponse
from app01.utils import DateJson
from django.db.models import Q
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import random
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings


def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# Create your views here.

def home(request):
    # 判断手机还是电脑
    # 这步是为了返回浏览器打开网页时候的headers，因为user-agent是存在于headers中的
    total = request.META

    # ua就是通过字典取值的方式拿到返回的user-agent,最后传递到pc_or_mobile.py中的ua
    ua = total.get('HTTP_USER_AGENT')
    # 调用pc_or_mobile.py文件里面的函数judge_pc_or_mobile开始判断
    # 将ua的值传到该函数的参数预留项里
    mobile = judge_pc_or_mobile(ua)
    # 输出一下查看状态
    home_messeges = models.HomeMessage.objects.filter().all().order_by('-creat_time')
    target = models.Target.objects.filter().last()
    text = models.Text.objects.filter().last()
    articles = models.Article.objects.all().order_by('-revise_time')
    articles = articles[0:10]
    if not mobile:
        return render(request, 'home.html', locals())
    return render(request, 'm_home.html', locals())


def get_home_mes(request):
    dic_mes = {'error': 100}
    user = request.POST.get('user')
    send_mes = request.POST.get('send_mes')
    home_messeges = models.HomeMessage.objects.filter().all().order_by('-creat_time')
    home_messege_dic = []

    if send_mes.replace(" ", ''):
        if not user:
            user = random_name()
            models.HomeMessage.objects.create(home_article=user, home_message=send_mes,
                                              )
        else:
            models.HomeMessage.objects.create(home_article=user, home_message=send_mes,
                                              )
        dic_mes['error'] = 200
        dic_mes['mes'] = '发送成功'
        for home_messege in home_messeges.values():
            home_messege_dic.append(home_messege)
        dic_mes['home_messeges'] = home_messege_dic

    else:
        dic_mes['error'] = 403
        dic_mes['mes'] = '你发了个寂寞'

    return JsonResponse(dic_mes)


def getmessage(request):
    dic_mes = {'error': 100}
    user = request.POST.get('user')
    id = request.POST.get('id')
    send_mes = request.POST.get('send_mes')
    page_queryset_dic = []
    if send_mes.replace(" ", ''):
        if not user:
            user = random_name()
            models.Message.objects.create(user=user,
                                          message_content=send_mes,
                                          article_id=id
                                          )
        else:
            models.Message.objects.create(home_article=user,
                                          home_message=send_mes
                                          )
        dic_mes['error'] = 200
        dic_mes['mes'] = '发送成功'
        article_messages = models.Message.objects.filter(article=id).all().order_by('-message_create_time')

        current_page = request.GET.get("page", 1)
        url = request.get_full_path().split('?')[-1]

        all_count = article_messages.count()
        page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=5, url=url)
        page_queryset = article_messages[page_obj.start:page_obj.end]
        for page_queryset in page_queryset.values():
            page_queryset_dic.append(page_queryset)
        dic_mes['page_queryset'] = page_queryset_dic

    else:
        dic_mes['error'] = 403
        dic_mes['mes'] = '你发了个寂寞'

    return JsonResponse(dic_mes)


def article(request):
    total = request.META

    ua = total.get('HTTP_USER_AGENT')
    mobile = judge_pc_or_mobile(ua)

    articles = models.Article.objects.filter().all().order_by('-revise_time')
    current_page = request.GET.get("page", 1)
    all_count = articles.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=15)
    page_queryset = articles[page_obj.start:page_obj.end]

    type_count = models.ArticleType.objects.count()
    tag_count = models.ArticleTag.objects.count()
    types = models.ArticleType.objects.filter().all()
    tags = models.ArticleTag.objects.filter().all()

    date_list = models.Article.objects.filter().annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count_num=Count('pk')).values_list('month', 'count_num')

    # # 1 查询当前所有的分类及分类下的文章数
    type_list = models.ArticleType.objects.filter().annotate(count_num=Count('article__id')).values_list('count_num')
    if mobile:
        return render(request, 'm_articles.html', locals())
    return render(request, 'articles.html', locals())


def article_q(request):
    total = request.META

    ua = total.get('HTTP_USER_AGENT')
    mobile = judge_pc_or_mobile(ua)

    type_count = models.ArticleType.objects.count()
    tag_count = models.ArticleTag.objects.count()
    types = models.ArticleType.objects.filter().all()
    tags = models.ArticleTag.objects.filter().all()

    date_list = models.Article.objects.filter().annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count_num=Count('pk')).values_list('month', 'count_num')

    # # 1 查询当前所有的分类及分类下的文章数
    type_list = models.ArticleType.objects.filter().annotate(count_num=Count('article__id')).values_list('count_num')

    q = request.GET.keys()

    if 'Type' in q:
        condition = request.GET.get('Type')

        need = models.ArticleType.objects.filter(pk=condition).values()[0].get('types')
        article_list = models.Article.objects.filter(article_types_id=condition)
    elif 'Tag' in q:
        condition = request.GET.get('Tag')
        need = models.ArticleTag.objects.filter(pk=condition).values()[0].get('tag')
        article_list = models.Article.objects.filter(article2articletag__article_tag=condition)
    elif 'Time' in q:
        condition = request.GET.get('Time')
        need = condition
        time_dic = condition.split('-')
        article_list = models.Article.objects.filter(create_time__month=time_dic[1], create_time__year=time_dic[0])
    elif 'search_val' in q:
        condition = request.GET.get('search_val')
        need = condition
        ques = '?'
        article_list = models.Article.objects.filter(Q(title__icontains=condition) |
                                                     Q(article_Tag__tag__icontains=condition) |
                                                     Q(article_types__types__icontains=condition)
                                                     )
    else:
        condition = request.GET.get('Title')
        article_obj = models.Article.objects.filter(pk=condition).values()

        article_dic = {}
        article_dic = article_obj[0]
        article_obj = json.dumps(article_dic, cls=DateJson.DateJson)

        request.session['article'] = article_obj
        return redirect(r'/article/article_content.html')

    current_page = request.GET.get("page", 1)
    url = request.get_full_path().split('?')[-1]

    all_count = article_list.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=15, url=url)
    page_queryset = article_list[page_obj.start:page_obj.end]

    if mobile:
        return render(request, 'm_article_q.html', locals())
    return render(request, 'article_q.html', locals())


def article_content(request):
    total = request.META

    ua = total.get('HTTP_USER_AGENT')
    mobile = judge_pc_or_mobile(ua)

    type_count = models.ArticleType.objects.count()
    tag_count = models.ArticleTag.objects.count()
    types = models.ArticleType.objects.filter().all()
    tags = models.ArticleTag.objects.filter().all()

    date_list = models.Article.objects.filter().annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count_num=Count('pk')).values_list('month', 'count_num')

    # # 1 查询当前所有的分类及分类下的文章数
    type_list = models.ArticleType.objects.filter().annotate(count_num=Count('article__id')).values_list('count_num')

    article_obj = json.loads(request.session.get('article'))

    article_type = models.ArticleType.objects.filter(article=article_obj.get('id')).first()
    article_messages = models.Message.objects.filter(article=article_obj.get('id')).all().order_by(
        '-message_create_time')

    current_page = request.GET.get("page", 1)
    url = request.get_full_path().split('?')[-1]

    all_count = article_messages.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=5, url=url)
    page_queryset = article_messages[page_obj.start:page_obj.end]

    if mobile:
        atr_tags = models.ArticleTag.objects.filter(article2articletag__article=article_obj.get('id')).all()

        return render(request, 'm_article_content.html', locals())

    return render(request, 'article_content.html', locals())


def like(request):
    like_state = request.POST.get('like_state')

    article_id = request.POST.get('article_id')

    dict = {}

    if like_state == 'Liked':
        Article = models.Article.objects.filter(pk=article_id).values()
        count = Article[0].get('like_count') - 1

        Article.update(like_count=count)
        like_count = Article[0].get('like_count')
        dict = {'error': 100}
    else:
        Article = models.Article.objects.filter(pk=article_id).values()
        count = Article[0].get('like_count') + 1

        if Article.update(like_count=count):
            like_count = Article[0].get('like_count')

            dict['error'] = 200
        else:
            dict = {'error': 400}
    dict['likecount'] = like_count

    return JsonResponse(dict)


def blogLogin(request):
    if request.method == 'POST':
        back_dic = {'code': 1000, 'msg': ''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # 1 先校验验证码是否正确      自己决定是否忽略            统一转大写或者小写再比较
        if request.session.get('code').upper() == code.upper():
            # 2 校验用户名和密码是否正确
            user_obj = auth.authenticate(request, username=username, password=password)
            print(user_obj)
            if user_obj:
                # 保存用户状态
                auth.login(request, user_obj)
                back_dic['url'] = '/BlogBackstage/'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)
        # 随机验证码  五位数的随机验证码  数字 小写字母 大写字母
    code = ''
    for i in range(5):
        random_upper = chr(random.randint(65, 90))
        random_lower = chr(random.randint(97, 122))
        random_int = str(random.randint(0, 9))
        # 从上面三个里面随机选择一个
        tmp = random.choice([random_lower, random_upper, random_int])
        # 将产生的随机字符串写入到图片上
        """
        为什么一个个写而不是生成好了之后再写
        因为一个个写能够控制每个字体的间隙 而生成好之后再写的话
        间隙就没法控制了
        """
        # 拼接随机字符串
        code += tmp
    # 随机验证码在登陆的视图函数里面需要用到 要比对 所以要找地方存起来并且其他视图函数也能拿到
    request.session['code'] = code
    email_from = "2669191008@qq.com"  # 改为自己的发送邮箱
    email_to = "2669191008@qq.com"  # 接收邮箱
    hostname = "smtp.qq.com"  # 不变，QQ邮箱的smtp服务器地址
    login = "2669191008@qq.com"  # 发送邮箱的用户名
    password = "pbjqucdjzjzrebde"  # 发送邮箱的密码，即开启smtp服务得到的授权码。注：不是QQ密码。
    subject = "贝克街验证码"  # 邮件主题
    text = "贝克街验证码:" + code  # 邮件正文内容

    smtp = SMTP_SSL(hostname)  # SMTP_SSL默认使用465端口
    smtp.login(login, password)

    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["from"] = email_from
    msg["to"] = email_to

    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.quit()
    return render(request, 'login.html')


@login_required(login_url='/')
def BlogBackstage(request):
    articles = models.Article.objects.filter().all().order_by('-revise_time')
    current_page = request.GET.get("page", 1)
    all_count = articles.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=12)
    page_queryset = articles[page_obj.start:page_obj.end]
    tags = models.ArticleTag.objects.filter().all()
    types = models.ArticleType.objects.filter().all()
    # homemessage = models.HomeMessage.objects.filter().all()
    # art_message = models.Message.objects.filter().all()
    if request.method == 'POST':
        condition = request.POST.get('search_val')
        article_list = models.Article.objects.filter(Q(title__icontains=condition) |
                                                     Q(article_Tag__tag__icontains=condition) |
                                                     Q(article_types__types__icontains=condition)
                                                     )
        current_page = request.GET.get("page", 1)
        all_count = article_list.count()
        page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=12)
        page_queryset = article_list[page_obj.start:page_obj.end]

    return render(request, 'BlogBackstage.html', locals())


@login_required(login_url='/')
def login_out(request):
    try:
        auth.logout(request)
        return HttpResponse(200)
    except Exception as e:
        print(e)
        return HttpResponse(300)


def upload(request):
    back_dic = {'error': 0, }
    if request.method == 'POST':

        file_obj = request.FILES.get('imgFile')
        file_dir = os.path.join(settings.BASE_DIR, 'media', 'img')
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        file_path = os.path.join(file_dir, file_obj.name)
        with open(file_path, 'wb') as f:
            for lin in file_obj:
                f.write(lin)
        back_dic['url'] = '/media/img/%s' % file_obj.name
    return JsonResponse(back_dic)


@login_required(login_url='/')
def add_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        type = request.POST['type']
        tags = request.POST['tags'].rstrip().split(' ')
        print(tags)
        content = request.POST['content']
        introduction = request.POST['introduction']
        # all_type = models.ArticleType.objects.filter().all().values()
        # all_tag = models.ArticleTag.objects.filter().all().values()
        tag_id_list = []
    try:
        if models.ArticleType.objects.filter(types=type):
            type_id = models.ArticleType.objects.filter(types=type).values('id')[0].get('id')
            print(type_id)
        else:
            res = models.ArticleType.objects.create(types=type)
            type_id = res.objects.filter(types=type).values('id')[0].get('id')
        for tag in tags:
            if models.ArticleTag.objects.filter(tag=tag):
                tag_id_list.append(models.ArticleTag.objects.filter(tag=tag).values('id')[0].get('id'))
            else:
                res = models.ArticleTag.objects.create(tag=tag)
                tag_id_list.append(models.ArticleTag.objects.filter(tag=tag).values('id')[0].get('id'))

        article_obj = models.Article.objects.create(title=title,
                                                    content=content,
                                                    introduction=introduction,
                                                    article_types_id=type_id)

        article_obj_list = []
        for i in tag_id_list:
            tag_article_obj = models.Article2ArticleTag(article=article_obj, article_tag_id=i)
            article_obj_list.append(tag_article_obj)
        # 批量插入数据
        models.Article2ArticleTag.objects.bulk_create(article_obj_list)

        return redirect('/BlogBackstage/')
    except Exception as e:
        print(e)
        return HttpResponse(e)

    return HttpResponse('你想干哈？？')

@login_required(login_url='/')
def update(request):
    art_id = request.POST.get('art_id')

    dict = {'error': 100}
    tag_lis = []
    try:
        article_obj = models.Article.objects.filter(id=art_id).values('title',
                                                                      'content',
                                                                      'introduction',
                                                                      'article_types__types'
                                                                      )[0]

        tags = models.ArticleTag.objects.filter(article2articletag__article_id=art_id).all().values_list('tag')
        for tag in tags:
            tag_lis.append(tag)

        dict = {'error': 200, 'article_obj': article_obj, 'tag_lis': tag_lis}
    except Exception as e:

        dict = {'error': 100,
                'message': '修改请求失败'
                }

    return JsonResponse(dict)

@login_required(login_url='/')
def save(request):
    title = request.POST.get('title')
    type = request.POST.get('types')
    tags = request.POST.get('tags').rstrip().split(' ')
    art_id = request.POST.get('art_id')
    introduction = request.POST.get('introduction')
    content = request.POST.get('content')

    dict = {'error': 100}

    tag_id_list = []
    try:
        if models.ArticleType.objects.filter(types=type):
            type_id = models.ArticleType.objects.filter(types=type).values('id')[0].get('id')

        else:
            res = models.ArticleType.objects.create(types=type)
            type_id = res.objects.filter(types=type).values('id')[0].get('id')
        for tag in tags:
            if models.ArticleTag.objects.filter(tag=tag):
                tag_id_list.append(models.ArticleTag.objects.filter(tag=tag).values('id')[0].get('id'))
            else:
                res = models.ArticleTag.objects.create(tag=tag)
                tag_id_list.append(models.ArticleTag.objects.filter(tag=tag).values('id')[0].get('id'))

    except Exception as e:
        dict['error'] = 300
        dict['message'] = str(e)

    try:
        # type_obj = models.ArticleType.objects.filter(types=type)
        article_obj = models.Article.objects.filter(pk=art_id)
        article_obj.update(title=title, content=content, introduction=introduction, article_types_id=type_id,
                           revise_time=datetime.datetime.now())
        article_tags_obj = models.Article2ArticleTag.objects.filter(article_id=art_id).delete()
        article_obj_list = []
        for i in tag_id_list:
            tag_article_obj = models.Article2ArticleTag(article=article_obj.first(), article_tag_id=i)
            article_obj_list.append(tag_article_obj)
        # 批量插入数据
        models.Article2ArticleTag.objects.bulk_create(article_obj_list)
        dict['error'] = 200
        dict['message'] = '修改成功'
    except Exception as e:
        dict['error'] = 400
        dict['message'] = str(e)

    return JsonResponse(dict)

@login_required(login_url='/')
def delet(request):
    art_id = request.POST.get('art_id')
    dict = {'error': 100}
    try:
        models.Article.objects.filter(pk=art_id).delete()
        dict['error'] = 200
        dict['message'] = '删除成功'
    except Exception as e:
        dict['error'] = 400
        dict['message'] = str(e)
    return JsonResponse(dict)

@login_required(login_url='/')
def blogBackstage_homemess(request):
    articles = models.Article.objects.filter().all().order_by('-revise_time')
    current_page = request.GET.get("page", 1)
    all_count = articles.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=12)
    page_queryset = articles[page_obj.start:page_obj.end]
    tags = models.ArticleTag.objects.filter().all()
    types = models.ArticleType.objects.filter().all()
    # homemessage = models.HomeMessage.objects.filter().all()
    # art_message = models.Message.objects.filter().all()

    homemess_all_obj = models.HomeMessage.objects.filter().all().order_by('-creat_time')
    current_page = request.GET.get("page", 1)
    url = request.get_full_path().split('?')[-1]

    all_count = homemess_all_obj.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=12, url=url)
    page_queryset = homemess_all_obj[page_obj.start:page_obj.end]
    if request.method == 'POST':
        homemess_id = request.POST.get('homemess_id')
        do = request.POST.get('do')
        dict = {'error': 100}
        if do == 'get_mes':
            try:
                homemess_obj = models.HomeMessage.objects.filter(pk=homemess_id).values()[0]
                dict['error'] = 200
                dict['mess'] = homemess_obj
            except Exception as e:
                dict['error'] = 300
                dict['mess'] = str(e)
            return JsonResponse(dict)
        elif do == 'del':
            try:
                models.HomeMessage.objects.filter(pk=homemess_id).delete()
                dict['error'] = 200
                dict['mess'] = '删除成功'
            except Exception as e:
                dict['error'] = 600
                dict['mess'] = str(e)
            return JsonResponse(dict)
        else:
            try:
                homemess_artile = request.POST.get('homemess_artile')
                home_message = request.POST.get('home_message')

                models.HomeMessage.objects.filter(pk=homemess_id).update(home_message=home_message,
                                                                         home_article=homemess_artile)
                dict['error'] = 200
                dict['mess'] = '修改成功'
            except Exception as e:
                dict['error'] = 500
                dict['mess'] = str(e)
            return JsonResponse(dict)

    return render(request, 'BlogBackstage_homemess.html', locals())

@login_required(login_url='/')
def tag(request):
    tags = models.ArticleTag.objects.filter().all()
    types = models.ArticleType.objects.filter().all()

    # art_message = models.Message.objects.filter().all()

    current_page = request.GET.get("page", 1)
    url = request.get_full_path().split('?')[-1]

    all_count = tags.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=12, url=url)
    page_queryset = tags[page_obj.start:page_obj.end]

    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        do = request.POST.get('do')
        dict = {'error': 100}
        if do == 'get_mes':
            try:
                tag_obj = models.ArticleTag.objects.filter(pk=tag_id).values()[0]
                dict['error'] = 200
                dict['mess'] = tag_obj
            except Exception as e:
                dict['error'] = 300
                dict['mess'] = str(e)
            return JsonResponse(dict)
        elif do == 'del':
            try:
                models.ArticleTag.objects.filter(pk=tag_id).delete()
                dict['error'] = 200
                dict['mess'] = '删除成功'
            except Exception as e:
                dict['error'] = 600
                dict['mess'] = str(e)
            return JsonResponse(dict)
        elif do == 'add':
            try:
                tag_name = request.POST.get('tag_name')
                models.ArticleTag.objects.filter().create(tag=tag_name)
                dict['error'] = 200
                dict['mess'] = '添加成功'
            except Exception as e:
                dict['error'] = 700
                dict['mess'] = str(e)
            return JsonResponse(dict)
        else:
            try:
                tag_name = request.POST.get('tag_name')
                models.ArticleTag.objects.filter(pk=tag_id).update(tag=tag_name)
                dict['error'] = 200
                dict['mess'] = '修改成功'
            except Exception as e:
                dict['error'] = 500
                dict['mess'] = str(e)
            return JsonResponse(dict)

    return render(request, 'BlogBackstage_tag.html', locals())

@login_required(login_url='/')
def type(request):
    tags = models.ArticleTag.objects.filter().all()
    types = models.ArticleType.objects.filter().all()

    # art_message = models.Message.objects.filter().all()

    current_page = request.GET.get("page", 1)
    url = request.get_full_path().split('?')[-1]

    all_count = types.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=12, url=url)
    page_queryset = types[page_obj.start:page_obj.end]

    if request.method == 'POST':
        types_id = request.POST.get('types_id')
        do = request.POST.get('do')
        dict = {'error': 100}
        if do == 'get_mes':
            try:
                type_obj = models.ArticleType.objects.filter(pk=types_id).values()[0]
                dict['error'] = 200
                dict['mess'] = type_obj
            except Exception as e:
                dict['error'] = 300
                dict['mess'] = str(e)
            return JsonResponse(dict)
        elif do == 'del':
            try:
                models.ArticleType.objects.filter(pk=types_id).delete()
                dict['error'] = 200
                dict['mess'] = '删除成功'
            except Exception as e:
                dict['error'] = 600
                dict['mess'] = str(e)
            return JsonResponse(dict)
        elif do == 'add':
            try:
                types_name = request.POST.get('types_name')
                models.ArticleType.objects.filter().create(types=types_name)
                dict['error'] = 200
                dict['mess'] = '添加成功'
            except Exception as e:
                dict['error'] = 700
                dict['mess'] = str(e)
            return JsonResponse(dict)
        else:
            try:
                types_name = request.POST.get('types_name')
                print(types_name)
                models.ArticleType.objects.filter(pk=types_id).update(types=types_name)
                dict['error'] = 200
                dict['mess'] = '修改成功'
            except Exception as e:
                dict['error'] = 500
                dict['mess'] = str(e)
            return JsonResponse(dict)

    return render(request, 'BlogBackstage_type.html', locals())

@login_required(login_url='/')
def message(request):
    articles = models.Article.objects.filter().all().order_by('-revise_time')
    current_page = request.GET.get("page", 1)
    all_count = articles.count()
    page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=12)
    page_queryset = articles[page_obj.start:page_obj.end]

    tags = models.ArticleTag.objects.filter().all()
    types = models.ArticleType.objects.filter().all()
    # homemessage = models.HomeMessage.objects.filter().all()
    art_message = models.Message.objects.filter().all()

    art_id = request.POST.get('art_id')
    do = request.POST.get('do')
    dict = {'error': 100}

    if request.method == 'POST':
        if do == 'get_mes':
            try:
                message_list=[]
                message_obj = models.Message.objects.filter(article_id=art_id).all().values()
                for message in message_obj:
                    message_list.append(message)
                dict['error'] = 200
                dict['mess'] = message_list
            except Exception as e:
                dict['error'] = 300
                dict['mess'] = str(e)
            return JsonResponse(dict)
        else:
            try:
                models.Message.objects.filter(article_id=art_id).delete()
                dict['error'] = 200
                dict['mess'] = '删除成功'
            except Exception as e:
                dict['error'] = 500
                dict['mess'] = str(e)
            return JsonResponse(dict)

    return render(request, 'BlogBackstage_message.html', locals())
@login_required(login_url='/')
def message_change(request):
    message_id = request.POST.getlist('message_id')
    models.Message.objects.filter(id__in=message_id).delete()
    return redirect('/BlogBackstage/message/')
def page_not_found(request):
    return render(request, '404.html')
