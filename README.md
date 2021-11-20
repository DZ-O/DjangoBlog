# DjangoBlog
## 模型层

​	由于，Django自带的orm语法，使得我们可以不用书写SQL语句也能操作数据库，并且不用事先创建好数据库，只需要在项目应用目录下的models.py中写下每张表所对用的类，而类中的属性则是表中的字段。可根据需要自行修改，代码：

```python
import time

from django.db import models


# Create your models here.

class Article(models.Model):    # 文章表
    title = models.CharField(max_length=64, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    revise_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    like_count = models.IntegerField(default=0,verbose_name='点赞数')
    article_types = models.ForeignKey(to='ArticleType')
    introduction = models.CharField(max_length=250,verbose_name='文章简介',default='这是一段简介')
   
	# 文章与文章标签多对多关系通过第三张表Article2ArticleTag建立链接
    # 这是半自动创建多对多表关系方式，方便拓展。第三张表的类需要自己手动写。
    # 也可以直接使用，自动多对多关系，就不需要手动创建第三张表
    article_Tag = models.ManyToManyField(to='ArticleTag',
                                         through='Article2ArticleTag',
                                         through_fields=('article', 'article_tag')
                                         )

# 文章分类表
class ArticleType(models.Model):
    types = models.CharField(max_length=32, verbose_name='文章分类')  # 日常、技术、分享.....

# 文章标签表
class ArticleTag(models.Model):
    tag = models.CharField(max_length=32, verbose_name='文章标签')  # java、pyhon.....

# 文章留言表
class Message(models.Model):
    user = models.CharField(max_length=10, verbose_name='留言人')
    message_content = models.CharField(max_length=255, verbose_name='留言')
    message_create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    article = models.ForeignKey(to='Article')


# 文章与文章标签多对多关系表
class Article2ArticleTag(models.Model):
    article = models.ForeignKey(to='Article')
    article_tag = models.ForeignKey(to='ArticleTag')


# 显示在首页的个人目标，可以不写，在首页的页面写死
class Target(models.Model):
    target = models.CharField(max_length=100, verbose_name='目标')

# 显示在首页的文本句子，可以不写，在首页的页面写死
class Text(models.Model):
    text = models.CharField(max_length=100, verbose_name='文本')

# 首页留言表，这里偷了懒，直接新起了一个表，可以修改文章留言表，就不用创建这张表
class HomeMessage(models.Model):
    home_message = models.CharField(max_length=100, verbose_name='首页留言')
    home_article = models.CharField(max_length=10, verbose_name='作者')
    creat_time = models.DateTimeField(verbose_name='留言时间', auto_now_add=True, )

```

​	表模型文件创建完毕后，此时的系统是没有对应的数据库的，需要我们只需数据库迁移命令，在此之前，记得修改项目的`` settings.py``文件中的``DATABASES``中的内容为自己的数据库配置，

![image-20211006004633739](https://cdn.jsdelivr.net/gh/DZ-O/CDN/img/image-20211006004633739.png)

​	如果数据库使用的是MySQL则在项目中的任意``__init.py__``文件下加入如下内容,:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

​	项目根目录下的控制台执行数据库迁移命令：

> python [manage.py](http://manage.py/) makemigrations
>
> python [manage.py](http://manage.py/) migrate

​	执行完毕后你的数据库下将会出现如下几张表：

![image-20211006004519973](https://cdn.jsdelivr.net/gh/DZ-O/CDN/img/image-20211006004519973.png)

## 用户登录及后台管理问题

> 这里有人就发现，我们模型层并没有创建用户类，怎么实现登陆到后台，对自己文章进行发布和管理呢？

​	在这里我们使用Django的Auth模块，他会自动帮我们创建user表。而这个user表中的用户就是Django默认自带的路由``admin/``登录页面中所需要验证的用户，其中user表中的超级用户既可以登录到admin后台。

超级用户创建命令：

> python3 manage.py createsuperuser

​	而这个后台页面，是Django自动生成的，在这里我们可对数据库进行可视化操作。前提是在配置文件中将数据库注册进去。

![image-20211006005526886](https://cdn.jsdelivr.net/gh/DZ-O/CDN/img/image-20211006005526886.png)

​	当然，这个后台页面肯定不是我们需要的，这里我自己手动搭建了一个后台页面，老样子界面依旧简陋：

![image-20211006005952683](https://cdn.jsdelivr.net/gh/DZ-O/CDN/img/image-20211006005952683.png)

​	在这里，就能够对文章进行发布及管理等操作了。

​	当然登录后台的url路由地址也不是使用的Django自动生成admin页面，这里我也自己新建了一个页面：

![image-20211006010313354](https://cdn.jsdelivr.net/gh/DZ-O/CDN/img/image-20211006010313354.png)

​	验证码这一块，我并没有使用画图模块之类的，偷了个懒，使用的是smtplib模块，使用QQ邮箱发送随机验证码邮件到手上，修改`app01/views.py`下大概314行左右代码：

```python
 code += tmp
    # 随机验证码在登陆的视图函数里面需要用到 要比对 所以要找地方存起来并且其他视图函数也能拿到
    request.session['code'] = code
    email_from = "@qq.com"  # 改为自己的发送邮箱
    email_to = "@qq.com"  # 接收邮箱
    hostname = "smtp.qq.com"  # 不变，QQ邮箱的smtp服务器地址
    login = "@qq.com"  # 发送邮箱的用户名
    password = ""  # 发送邮箱的密码，即开启smtp服务得到的授权码。注：不是QQ密码。
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
```

## 静态资源收集

​	项目部署在服务器之前，记得执行项目的静态资源文件收集操作，否则可能会出现静态资源无法访问现象，参考博客：[django项目收集静态文件](
