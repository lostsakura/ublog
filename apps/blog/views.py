from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response

from blog.forms import BlogStartForm, EmailForm, LoginForm, RecoverPasswordForm, ManageLabelsForm, DeleteResourceForm
from blog.tools import send_verify_email, verify_email, get_blog_settings

from blog.models import BlogSettings, BlogUser, BlogLabel


# 初始化网站
def blog_start(request):
    try:
        blog_settings = BlogSettings.objects.all().order_by('-id').first()
    except Exception as e:
        blog_settings = None
    # 初始化后禁止访问
    if blog_settings is not None:
        return page_not_found(request)
    if request.method == 'GET':
        head_title = 'ublog初始化'
        return render(request, 'blog_start.html', {'head_title': head_title})
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
            new_bu.username = request.POST['userName']
            new_bu.email = request.POST['userEmail']
            new_bu.password = make_password(request.POST['userPassword'])
            new_bu.is_staff = True
            new_bu.is_superuser = True
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
            # 自动登陆
            user = authenticate(username=request.POST['userName'], password=request.POST['userPassword'])
            if user is not None:
                login(request, user)
                request.session.set_expiry(0)
            return JsonResponse(resp)
        else:
            print(blog_start_form.errors)
            resp['status'] = 'error'
            resp['info'] = '验证没有通过'
            return JsonResponse(resp)


# 首页
def blog_index(request):
    return render(request, 'index.html')


# 后台
def blog_admin(request):
    head_title = '后台管理 - '
    bs = get_blog_settings()
    if bs:
        head_title = head_title + bs.site_name
    else:
        head_title = head_title + 'ublog'
    return render(request, 'admin_main.html', {'head_title': head_title})


# 登陆
def blog_login(request):
    # ajax返回的信息
    resp = {'status': None, 'info': None}
    if request.method == 'GET':
        head_title = 'login - '
        bs = get_blog_settings()
        if bs:
            head_title = head_title + bs.site_name
        else:
            head_title = head_title + 'ublog'
        return render(request, 'blog_login.html', {'head_title': head_title})
    elif request.method == 'POST':
        # ajax返回的信息
        resp = {'status': None, 'info': None}
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=request.POST['userName'], password=request.POST['userPassword'])
            if user is not None:
                login(request, user)
                if request.POST['rememberMe'] == '0':
                    request.session.set_expiry(0)
                resp['status'] = 'success'
                resp['info'] = '正在跳转至后台管理页面'
                return JsonResponse(resp)
            resp['status'] = 'error'
            resp['info'] = '用户名或密码输入错误'
            return JsonResponse(resp)
        resp['status'] = 'error'
        resp['info'] = '登陆信息验证错误'
        return JsonResponse(resp)


# 找回密码
def recover_password(request):
    if request.method == 'GET':
        head_title = 'recover password - '
        bs = get_blog_settings()
        if bs:
            head_title = head_title + bs.site_name
        else:
            head_title = head_title + 'ublog'
        return render(request, 'recover_password.html', {'head_title': head_title})
    elif request.method == 'POST':
        resp = {'status': None, 'info': None}
        rpf = RecoverPasswordForm(request.POST)
        if rpf.is_valid():
            if not verify_email(request.POST['userEmail'], request.POST['verifyCode']):
                resp['status'] = 'error'
                resp['info'] = '邮箱验证码不正确'
                return JsonResponse(resp)
            else:
                try:
                    user = BlogUser.objects.filter(email=request.POST['userEmail']).order_by('-id').first()
                except Exception as e:
                    user = None
                if user:
                    user.password = make_password(request.POST['newPassword'])
                    user.save()
                    resp['status'] = 'success'
                    resp['info'] = '您的用户名为 【' + user.username + '】'
                    return JsonResponse(resp)
                else:
                    resp['status'] = 'error'
                    resp['info'] = '您的邮箱信息不正确，请检查后重试'
                    return JsonResponse(resp)
        else:
            resp['status'] = 'error'
            resp['info'] = '表单信息提交异常，请检查后重试'
            return JsonResponse(resp)


# 注销
def blog_logout(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()
        resp = {'status': 'success'}
        return JsonResponse(resp)
    return forbidden(request)


# 概要
def admin_index(request):
    section_title = "系统概要"
    return render(request, 'admin_index.html', {'section_title': section_title})


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
    section_title = '标签管理'
    if request.method == 'GET':
        operation_type = request.GET['type']
        update_item = None
        edit_table_title = None
        action_type = None
        is_edit = True
        page_num = int(request.GET['page'])
        if operation_type == 'list':
            section_title = section_title + ' - 添加'
            edit_table_title = '添加标签'
            action_type = 'add'
        elif operation_type == 'update':
            section_title = section_title + ' - 修改'
            edit_table_title = '修改标签'
            try:
                update_item = BlogLabel.objects.filter(id=request.GET['num']).order_by('id').first()
            except Exception as e:
                update_item = None
            if update_item is None:
                is_edit = False
            action_type = 'update'
        # 分页处理
        bl_list = BlogLabel.objects.all().order_by('id')
        table_list = Paginator(bl_list, 10)
        total_page = table_list.num_pages
        # 判断请求的页面是否存在
        if page_num > total_page or page_num <= 0:
            return page_not_found(request)

        return render(request, 'admin_manage_labels.html', {'section_title': section_title,
                                                            'edit_table_title': edit_table_title,
                                                            'bl_list': table_list.page(page_num),
                                                            'total_page': total_page,
                                                            'page_num': page_num,
                                                            'update_item': update_item,
                                                            'action_type': action_type,
                                                            'is_edit': is_edit})
    elif request.method == 'POST':
        mlf = ManageLabelsForm(request.POST)
        resp = {'status': None, 'info': None}
        if mlf.is_valid():
            try:
                cbl = BlogLabel.objects.filter(label_name=request.POST['labelName']).first()
            except Exception as e:
                cbl = None
            if cbl is not None:
                resp['status'] = 'error'
                resp['info'] = '标签已存在'
                return JsonResponse(resp)
            if request.POST['labelId'] != '0':
                try:
                    bl = BlogLabel.objects.filter(id=request.POST['labelId']).first()
                except Exception as e:
                    bl = None
                if bl is not None:
                    bl.label_name = request.POST['labelName']
                    bl.save()
                    resp['status'] = 'success'
                    resp['info'] = '成功修改为' + request.POST['labelName']
                    return JsonResponse(resp)
                else:
                    resp['status'] = 'error'
                    resp['info'] = '要修改的标签不存在，请重试'
                    return JsonResponse(resp)
            bl = BlogLabel()
            bl.label_name = request.POST['labelName']
            bl.save()
            resp['status'] = 'success'
            resp['info'] = '添加成功'
            return JsonResponse(resp)
        resp['status'] = 'error'
        resp['info'] = '您输入的信息不合法，请重试'
        print(mlf.errors)
        return JsonResponse(resp)


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
            if request.POST['type'] == '1':
                try:
                    exist_user = BlogUser.objects.filter(email=request.POST['userEmail']).first()
                except Exception as e:
                    exist_user = None
                if not exist_user:
                    resp['status'] = 'error'
                    resp['info'] = '该用户不存在'
                    return JsonResponse(resp)
            if send_verify_email(request.POST['userEmail']):
                resp['status'] = 'success'
                resp['info'] = '验证码发送成功'
                return JsonResponse(resp)
    resp['status'] = 'error'
    resp['info'] = '验证码发送失败'
    return JsonResponse(resp)


# 删除资源
def deleteResource(request):
    if request.method == 'POST':
        resp = {'status': None, 'info': None}
        drf = DeleteResourceForm(request.POST)
        if drf.is_valid():
            if request.POST['resourceType'] == 'blog_label':
                try:
                    bl = BlogLabel.objects.filter(id=request.POST['resourceId']).first()
                except Exception as e:
                    bl = None
                if bl is not None:
                    bl.delete()
                    resp['status'] = 'success'
                    resp['info'] = '已删除'
                    return JsonResponse(resp)
                else:
                    resp['status'] = 'error'
                    resp['info'] = '删除的项目不存在，请检查后重试'
                    return JsonResponse(resp)
        resp['status'] = 'error'
        resp['info'] = '提交的删除信息有误，请检查后重试'
        return JsonResponse(resp)


# 403无权限访问
def forbidden(request):
    response = render_to_response('error_page.html', {'head_title': '403 - ublog', 'type': '403',
                                                      'msg': '您无权访问该页面'})
    response.status_code = 403
    return response


# 404找不到页面
def page_not_found(request):
    response = render_to_response('error_page.html', {'head_title': '404 - ublog', 'type': '404',
                                                      'msg': '找不到该页面'})
    response.status_code = 404
    return response


# 500服务器内部错误
def internal_server_error(request):
    response = render_to_response('error_page.html', {'head_title': '500 - ublog', 'type': '500',
                                                      'msg': '抱歉，服务器内部错误'})
    response.status_code = 500
    return response


# 503服务器出错
def service_unavailable(request):
    response = render_to_response('error_page.html', {'head_title': '503 - ublog', 'type': '503',
                                                      'msg': '抱歉，服务器出错'})
    response.status_code = 503
    return response
