from django.shortcuts import redirect

from blog.models import BlogSettings

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
            blog_settings = BlogSettings.objects.filter(id=1).order_by('id').first()
        except Exception as e:
            blog_settings = None
        if blog_settings is None:
            safe_path = request.path
            if not safe_path == '/start/':
                if not safe_path == '/get-verify-code/':
                    if not safe_path == '/admin/':
                        return redirect('/start/')
        return None
