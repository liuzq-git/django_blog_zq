"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications.urls
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from django.conf import settings

from article.views import article_list

urlpatterns = [
    path('admin/', admin.site.urls),
# 新增代码，配置app的url
    path('article/', include('article.urls', namespace='article')),
    path('userprofile/',include('userprofile.urls',namespace='userprofile')),
    path('password-reset/', include('password_reset.urls')),
    path('comment/', include('comment.urls',namespace='comment')),
    path('notice/', include('notice.urls',namespace='notice')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('accounts/', include('allauth.urls')),
    path('',article_list,name='home'),
]
#为以后上传的图片配置好了URL路径
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)