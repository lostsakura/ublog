"""ublog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from urllib.parse import quote

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from apps.blog.tools import get_labels

from blog import views as v
urlpatterns = [
    path('adminx/', admin.site.urls),

    # 初始化网站
    path('start/', v.blog_start),

    # index页面
    path('', v.blog_index),

    # 后台管理
    path('admin/', v.blog_admin),
    # 后台登陆
    path('login/', v.blog_login),
    # 账户注销
    path('logout/', v.blog_logout),
    # 重置密码
    path('recover-password/', v.recover_password),

    # 概要
    path('admin/admin-index/', v.admin_index),

    # 文章编辑
    path('admin/write-article/', v.write_article),
    # 独立页面编辑
    path('admin/write-page/', v.write_page),

    # 文章管理
    path('admin/manage-articles/', v.manage_articles),
    # 独立页面管理
    path('admin/manage-pages/', v.manage_pages),
    # 评论管理
    path('admin/manage-comments/', v.manage_comments),
    # 标签管理
    path('admin/manage-labels/', v.manage_labels),

    # 个人设置
    path('admin/user-setup/', v.user_setup),
    # 系统设置
    path('admin/system-setup/', v.system_setup),

    # 删除资源
    path('admin/delete-resource/', v.deleteResource),

    # 获取邮箱验证码
    path('get-verify-code/', v.tool_get_verify_code),
    # 错误页面
    path('admin/error/', v.blog_error),

    # 博客列表页面
    re_path('(?P<category>label)/lid_(?P<lid>[1-9][0-9]*)/(?P<page_num>[1-9][0-9]*)/', v.blog_list),
    re_path('(?P<category>page)/(?P<page_num>[1-9][0-9]*)/', v.blog_list),

    # 多媒体用
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 静态资源用
    re_path(r'^static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
