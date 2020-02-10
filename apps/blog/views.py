from django.http import JsonResponse
from django.shortcuts import render, redirect


from blog.forms import BlogStartForm, EmailForm
from blog.tools import send_verify_email, verify_email

# 初始化网站
from blog.models import BlogSettings, BlogUser


def blog_start(request):
    if request.method == 'GET':
        return render(request, 'blog_start.html')
    elif request.method == 'POST':
        # ajax返回的信息
        resp = {'status': None, 'info': None}
        blog_start_form = BlogStartForm(request.POST)
        if blog_start_form.is_valid():

            # new_bu = BlogUser()
            #
            # new_bs = BlogSettings()
            # new_bs.site_name = request.POST['siteName']
            # new_bs.site_address = request.POST['siteAddress']
            # new_bs.site_desc = request.POST['siteDesc']
            # new_bs.site_keyword = request.POST['siteKeyword']
            # new_bs.allow_comment = True if request.POST['siteAllowComment'] == 1 else False

            resp['status'] = 'success'
            resp['info'] = None
            return JsonResponse(resp)
        else:
            reason = blog_start_form.errors.get_json_data()
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
