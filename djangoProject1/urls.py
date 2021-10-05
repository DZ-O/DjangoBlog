"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.views.static import serve
from django.conf import settings
from django.views import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^gethomemes/$', views.get_home_mes),
    url(r'^getmessage/$', views.getmessage),
    url(r'^like/$', views.like),
    url(r'^article/article_content.html/$', views.article_content),
    url(r'^article.html$', views.article),
    url(r'^article/q/$', views.article_q),
    url(r'^blogLogin/$', views.blogLogin),
    url(r'^BlogBackstage/$', views.BlogBackstage),
    url(r'^BlogBackstage/homemess/$', views.blogBackstage_homemess),
    url(r'^BlogBackstage/tag/$', views.tag),
    url(r'^BlogBackstage/type/$', views.type),
    url(r'^BlogBackstage/message/$', views.message),
    url(r'^BlogBackstage/message_change/$', views.message_change),
    url(r'^BlogBackstage/update/$', views.update),
    url(r'^BlogBackstage/save/$', views.save),
    url(r'^BlogBackstage/del/$', views.delet),
    url(r'^login_out/$', views.login_out),
    url(r'^upload/',views.upload),
    url(r'^BlogBackstage/add_article/$',views.add_article),


    url(r'^$', views.home),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

]
handler500 = views.page_not_found
