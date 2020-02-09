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
from django.contrib import admin
from django.urls import path
from blog import views as v
urlpatterns = [
    path('adminx/', admin.site.urls),

    # index页面
    path('', v.blog_index),
    # 后台管理
    path('admin/', v.blog_admin),

    # 概要
    path('admin/admin-index/', v.admin_index),

    # 文章编辑
    path('admin/write-article', v.write_article),
    # 独立页面编辑
    path('admin/write-page', v.write_page),

    # 文章管理
    path('admin/manage-articles', v.manage_articles),
    # 独立页面管理
    path('admin/manage-pages', v.manage_pages),
    # 评论管理
    path('admin/manage-comments', v.manage_comments),
    # 标签管理
    path('admin/manage-labels', v.manage_labels),

    # 个人设置
    path('admin/user-setup', v.user_setup),
    # 系统设置
    path('admin/system-setup', v.system_setup),



]
