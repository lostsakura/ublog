from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response

from blog.forms import BlogStartForm, EmailForm
from blog.tools import send_verify_email, verify_email

# 初始化网站
from blog.models import BlogSettings, BlogUser


def blog_start(request):
    try:
        blog_settings = BlogSettings.objects.filter(id=1).order_by('id').first()
    except Exception as e:
        blog_settings = None
    # 初始化后禁止访问
    if blog_settings is not None:
        return forbidden(request)

    if request.method == 'GET':
        return render(request, 'blog_start.html')
    elif request.method == 'POST':
        # ajax返回的信息
        resp = {'status': None, 'info': None}
        blog_start_form = BlogStartForm(request.POST)
        if blog_start_form.is_valid():
            if not verify_email(request.POST['userEmail'], request.POST['verifyCode']):
                resp['status'] = 'error'
                resp['info'] = '邮箱验证码不正确'
                return JsonResponse(resp)
            new_bu = BlogUser()
            new_bu.email = request.POST['userEmail']
            new_bu.password = make_password(request.POST['userPassword'])
            new_bu.save()
            new_bs = BlogSettings()
            new_bs.site_name = request.POST['siteName']
            new_bs.site_address = request.POST['siteAddress']
            new_bs.site_desc = request.POST['siteDesc']
            new_bs.site_keyword = request.POST['siteKeyword']
            new_bs.allow_comment = True if request.POST['siteAllowComment'] == 1 else False
            new_bs.save()
            resp['status'] = 'success'
            resp['info'] = '正在跳转至后台管理页面'
            return JsonResponse(resp)
        else:
            resp['status'] = 'error'
            resp['info'] = '验证没有通过'
            return JsonResponse(resp)


# 首页
def blog_index(request):
    return render(request, 'index.html')


# 后台
def blog_admin(request):
    return render(request, 'admin_main.html')


# 登陆
def blog_login(request):
    return render(request, 'blog_login.html')


# 概要
def admin_index(request):
    return render(request, 'admin_index.html')


# 文章编辑
def write_article(request):
    return render(request, 'admin_write_article.html')


# 独立页面编辑
def write_page(request):
    return render(request, 'admin_write_page.html')


# 文章管理
def manage_articles(request):
    return render(request, 'admin_manage_articles.html')


# 独立页面管理
def manage_pages(request):
    return render(request, 'admin_manage_pages.html')


# 评论管理
def manage_comments(request):
    return render(request, 'admin_manage_comments.html')


# 标签管理
def manage_labels(request):
    return render(request, 'admin_manage_labels.html')


# 个人设置
def user_setup(request):
    return render(request, 'admin_user_setup.html')


# 系统设置
def system_setup(request):
    return render(request, 'admin_system_setup.html')


# 获取邮箱验证码
def tool_get_verify_code(request):
    resp = {'status': None, 'info': None}
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            email = request.POST['userEmail']
            if send_verify_email(email):
                resp['status'] = 'success'
                resp['info'] = '验证码发送成功'
                return JsonResponse(resp)
    resp['status'] = 'error'
    resp['info'] = '验证码发送失败'
    return JsonResponse(resp)


# 403无权限访问
def forbidden(request):
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response


# 404找不到页面
def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 500服务器内部错误
def internal_server_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


# 503服务器出错
def service_unavailable(request):
    response = render_to_response('503.html', {})
    response.status_code = 503
    return response