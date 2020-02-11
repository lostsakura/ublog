import re

from django.shortcuts import redirect

from blog.models import BlogSettings
from blog.views import forbidden

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


"""
初始化网站拦截器
用于在未初始化网站的情况下
拦截所有的请求并转发到初始化页面
"""


class StartInterceptor(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        try:
            blog_settings = BlogSettings.objects.all().order_by('id').first()
        except Exception as e:
            blog_settings = None
        if blog_settings is None:
            path = request.path
            safe_list = ['/get-verify-code/', '/start/']
            if path not in safe_list:
                return redirect('/start/')
        return None


"""
访问后台管理系统时进行的权限认证
"""


class PermissionInterceptor(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        access_path = request.path
        pattern = r'/admin/'
        if re.match(pattern, access_path):
            if not request.user.is_authenticated:
                return forbidden(request)
