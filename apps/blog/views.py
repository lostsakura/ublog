import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response

from blog.forms import BlogStartForm, EmailForm, LoginForm, RecoverPasswordForm, ManageLabelsForm, DeleteResourceForm, \
    ArticleWriteForm, PageWriteForm, UserSettingsForm, SystemSettingsForm, SubmitCommentForm, BatchUpdateResourceForm
from blog.tools import send_verify_email, verify_email, get_blog_settings, zero_transition, batch_delete

from blog.models import BlogSettings, BlogUser, BlogLabel, BlogArticle, BlogPage, ArticleComment


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
            new_bs.allow_comment = zero_transition(request.POST['siteAllowComment'])
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
    return blog_list(request=request)


# 列表页面
def blog_list(request, category='page', lid=1, page_num=1):
    bs = BlogSettings.objects.all().order_by('id').first()
    us = BlogUser.objects.all().order_by('id').first()
    bl = BlogLabel.objects.all().order_by('id')
    bp = BlogPage.objects.filter(is_draft=False).order_by('sort_id')
    show_type = category
    ba_list = None
    label_name = None
    is_login = False

    if request.user.is_authenticated:
        is_login = True
    if category == 'page':
        if is_login:
            ba_list = BlogArticle.objects.filter(is_draft=False).order_by('-created_time')
        else:
            ba_list = BlogArticle.objects.filter(is_draft=False, is_private=False).order_by('-created_time')
    elif category == 'label':
        show_type = '分类标签'
        try:
            ln = BlogLabel.objects.get(id=int(lid)).label_name
        except Exception as e:
            ln = None
        if ln is not None:
            label_name = ln
            try:
                if is_login:
                    ba_list = BlogArticle.objects.filter(label=ln, is_draft=False).order_by('-created_time')
                else:
                    ba_list = BlogArticle.objects.filter(label=ln, is_draft=False, is_private=False) \
                        .order_by('-created_time')
            except Exception as e:
                ba_list = None
    recent_article = BlogArticle.objects.filter(is_draft=False, is_private=False).order_by('-created_time')[:5]
    # 分页处理
    table_list = Paginator(ba_list, 7)
    total_page = table_list.num_pages

    return render(request, 'blog_list.html', {'blog_setting': bs,
                                              'user_setting': us,
                                              'label_list': bl,
                                              'blog_page': bp,
                                              'recent_article': recent_article,
                                              'article_list': table_list.page(page_num),
                                              'total_page': total_page,
                                              'show_type': show_type,
                                              'page_num': page_num,
                                              'page_id': 0,
                                              'lid': lid,
                                              'label_name': label_name})


# 文章详情
def blog_article(request, article_id):
    bs = BlogSettings.objects.all().order_by('id').first()
    us = BlogUser.objects.all().order_by('id').first()
    bl = BlogLabel.objects.all().order_by('id')
    ba = BlogArticle.objects.get(id=article_id)
    ba.clicks = int(ba.clicks) + 1
    ba.save()
    bp = BlogPage.objects.filter(is_draft=False).order_by('sort_id')
    recent_article = BlogArticle.objects.filter(is_draft=False, is_private=False).order_by('-created_time')[:5]
    return render(request, 'blog_article.html', {'blog_setting': bs,
                                                 'user_setting': us,
                                                 'label_list': bl,
                                                 'blog_page': bp,
                                                 'blog_article': ba,
                                                 'recent_article': recent_article,
                                                 'total_page': 1})


# 独立页面
def blog_page(request, page_id):
    bs = BlogSettings.objects.all().order_by('id').first()
    us = BlogUser.objects.all().order_by('id').first()
    bp = BlogPage.objects.filter(is_draft=False).order_by('sort_id')
    try:
        bpi = BlogPage.objects.get(id=page_id)
    except Exception as e:
        bpi = None
    if bpi is None:
        return page_not_found(request)
    return render(request, 'blog_page.html', {'blog_setting': bs,
                                              'user_setting': us,
                                              'blog_page': bp,
                                              'blog_page_item': bpi})


# 提交评论
def blog_comment(request):
    if request.method == 'POST':
        resp = {'status': None, 'info': None}
        scf = SubmitCommentForm(request.POST)
        if scf:
            try:
                ba = BlogArticle.objects.get(id=request.POST['articleId'])
            except Exception as e:
                ba = None
            if ba is not None:
                ac = ArticleComment()
                ac.article = ba
                ac.author = request.POST['commentName']
                ac.email = request.POST['commentEmail']
                ac.content = request.POST['commentContent']
                ac.save()
                resp['status'] = 'success'
                resp['info'] = '评论已成功提交至博主审核'
                return JsonResponse(resp)
        resp['status'] = 'error'
        resp['info'] = '提交的信息有误，请检查后重试'
        return JsonResponse(resp)


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


# 重置密码
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
                    # 如果处于登陆状态，则退出登录状态
                    if request.user.is_authenticated:
                        logout(request)
                        request.session.flush()
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
        if request.user.is_authenticated:
            logout(request)
            request.session.flush()
            resp = {'status': 'success'}
            return JsonResponse(resp)
    return forbidden(request)


# 概要
def admin_index(request):
    section_title = "系统概要"
    article_count = BlogArticle.objects.filter(is_draft=False).count()
    draft_count = BlogArticle.objects.filter(is_draft=True).count()
    all_comment_count = ArticleComment.objects.count()
    recent_articles_list = BlogArticle.objects.filter(is_draft=False).order_by('created_time')[:7]
    recent_comments_list = ArticleComment.objects.filter(is_passed=False).order_by('-id')[:7]
    recent_comment_count = ArticleComment.objects.filter(is_passed=False).count()
    return render(request, 'admin_index.html', {'section_title': section_title,
                                                'article_count': article_count,
                                                'draft_count': draft_count,
                                                'all_comment_count': all_comment_count,
                                                'recent_comment_count': recent_comment_count,
                                                'recent_articles_list': recent_articles_list,
                                                'recent_comments_list': recent_comments_list})


# 文章编辑
def write_article(request):
    if request.method == 'GET':
        # 撰写新的文章
        bl_list = BlogLabel.objects.all().order_by('id')
        if request.GET['type'] == 'add':
            section_title = '撰写新文章'
            return render(request, 'admin_write_article.html', {'section_title': section_title,
                                                                'bl_list': bl_list})
        elif request.GET['type'] == 'update':
            section_title = '编辑文章'
            try:
                ba = BlogArticle.objects.get(id=request.GET['num'])
            except Exception as e:
                ba = None
            return render(request, 'admin_write_article.html', {'section_title': section_title,
                                                                'bl_list': bl_list,
                                                                'ba_item': ba})
    elif request.method == 'POST':
        resp = {'status': None, 'info': None}
        awf = ArticleWriteForm(request.POST)
        ba = None
        if awf.is_valid():
            if request.POST['articleId'] == '0':
                ba = BlogArticle()
            else:
                try:
                    ba = BlogArticle.objects.get(id=request.POST['articleId'])
                except Exception as e:
                    ba = None
                if ba is None:
                    resp['info'] = '提交信息有误，请检查后重试'
                    resp['status'] = 'error'
                    return JsonResponse(resp)
            ba.title = request.POST['articleTitle']
            ba.content = request.POST['articleContent']
            ba.is_private = zero_transition(request.POST['articleIsPrivate'])
            if zero_transition(request.POST['articleIsDraft']):
                ba.is_draft = True
                resp['info'] = '草稿保存成功'
            else:
                ba.is_draft = False
                resp['info'] = '文章发布成功'
            if request.POST['articleLabel'] != '0':
                ba.label = BlogLabel.objects.get(id=request.POST['articleLabel']).label_name
            ba.update_time = datetime.now()
            ba.save()
            resp['status'] = 'success'
            return JsonResponse(resp)
        else:
            resp['info'] = '提交信息有误，请检查后重试'
            resp['status'] = 'error'
            return JsonResponse(resp)


# 独立页面编辑
def write_page(request):
    if request.method == 'GET':
        section_title = None
        page_item = None
        if request.GET['type'] == 'add':
            # 如果独立页面数超过7个，则跳转错误页面
            if BlogPage.objects.count() >= 7:
                return blog_error(request, '独立页面数最多不能超过7个')
            section_title = '添加新页面'
        elif request.GET['type'] == 'update':
            try:
                page_item = BlogPage.objects.get(id=request.GET['num'])
            except Exception as e:
                page_item = None
            section_title = '修改页面'
        return render(request, 'admin_write_page.html', {'section_title': section_title,
                                                         'page_item': page_item})
    elif request.method == 'POST':
        resp = {'status': None, 'info': None}
        pwf = PageWriteForm(request.POST)
        bp = None
        if pwf.is_valid():
            if request.POST['pageId'] == '0':
                bp = BlogPage()
            else:
                try:
                    bp = BlogPage.objects.get(id=request.POST['pageId'])
                except Exception as e:
                    bp = None
                if bp is None:
                    resp['info'] = '提交信息有误，请检查后重试'
                    resp['status'] = 'error'
                    return JsonResponse(resp)
            bp.title = request.POST['pageTitle']
            bp.content = request.POST['pageContent']
            bp.sort_id = request.POST['pageSortId']
            bp.update_time = datetime.now()
            if zero_transition(request.POST['pageIsDraft']):
                bp.is_draft = True
                resp['info'] = '草稿保存成功'
            else:
                bp.is_draft = False
                resp['info'] = '页面发布成功'
            bp.save()
            resp['status'] = 'success'
            return JsonResponse(resp)
        else:
            resp['info'] = '提交信息有误，请检查后重试'
            resp['status'] = 'error'
            return JsonResponse(resp)


# 文章管理
def manage_articles(request):
    if request.method == 'GET':
        section_title = '文章管理'
        page_num = request.GET['page']
        list_type = request.GET['list']
        ba_list = None
        if list_type == 'public':
            section_title = section_title + ' - 公开'
            ba_list = BlogArticle.objects.filter(is_private=False, is_draft=False).order_by('-id')
        elif list_type == 'private':
            section_title = section_title + ' - 隐私'
            ba_list = BlogArticle.objects.filter(is_private=True, is_draft=False).order_by('-id')
        elif list_type == 'draft':
            section_title = section_title + ' - 草稿'
            ba_list = BlogArticle.objects.filter(is_draft=True).order_by('-id')
        # 分页处理
        table_list = Paginator(ba_list, 10)
        total_page = table_list.num_pages
        return render(request, 'admin_manage_articles.html', {'section_title': section_title,
                                                              'ba_list': table_list.page(page_num),
                                                              'list_type': list_type,
                                                              'total_page': total_page,
                                                              'page_num': page_num})


# 独立页面管理
def manage_pages(request):
    if request.method == 'GET':
        section_title = '独立页面管理'
        bp_list = BlogPage.objects.all().order_by('-sort_id')
        return render(request, 'admin_manage_pages.html', {'section_title': section_title,
                                                           'bp_list': bp_list})


# 评论管理
def manage_comments(request):
    if request.method == 'GET':
        page_num = request.GET['page']
        list_type = request.GET['list']
        ac_list = None
        if list_type == 'passed':
            ac_list = ArticleComment.objects.filter(is_passed=True).order_by('-id')
        elif list_type == 'under_review':
            ac_list = ArticleComment.objects.filter(is_passed=False).order_by('-id')
        # 分页处理
        table_list = Paginator(ac_list, 5)
        total_page = table_list.num_pages
        return render(request, 'admin_manage_comments.html', {'list_type': list_type,
                                                              'ac_list': table_list.page(page_num),
                                                              'page_num': page_num,
                                                              'total_page': total_page})


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
    if request.method == 'GET':
        section_title = '个人设置'
        bu = BlogUser.objects.order_by('id').first()
        return render(request, 'admin_user_setup.html', {'blog_user': bu,
                                                         'section_title': section_title})
    elif request.method == 'POST':
        resp = {'status': None, 'info': None}
        usf = UserSettingsForm(request.POST)
        bu = None
        if usf.is_valid():
            try:
                bu = BlogUser.objects.get(id=request.POST['userId'])
            except Exception as e:
                bu = None
            if bu is None:
                resp['status'] = 'error'
                resp['info'] = '提交的信息有误，请检查后重试'
                return JsonResponse(resp)
            bu.username = request.POST['userName']
            bu.save()
            resp['status'] = 'success'
            resp['info'] = '用户信息修改成功'
        else:
            resp['status'] = 'error'
            resp['info'] = '提交的信息有误，请检查后重试'
        return JsonResponse(resp)


# 系统设置
def system_setup(request):
    if request.method == 'GET':
        section_title = '系统设置'
        try:
            bs = BlogSettings.objects.order_by('id').first()
        except Exception as e:
            bs = None
        return render(request, 'admin_system_setup.html', {'blog_settings': bs,
                                                           'section_title': section_title})
    elif request.method == 'POST':
        resp = {'status': None, 'info': None}
        ssf = SystemSettingsForm(request.POST)
        bs = None
        if ssf.is_valid():
            try:
                bs = BlogSettings.objects.get(id=request.POST['siteId'])
            except Exception as e:
                bs = None
            if bs is None:
                resp['status'] = 'error'
                resp['info'] = '提交的信息有误，请检查后重试'
                return JsonResponse(resp)
            bs.site_address = request.POST['siteAddress']
            bs.site_name = request.POST['siteName']
            bs.site_desc = request.POST['siteDesc']
            bs.site_keyword = request.POST['siteKeyword']
            bs.allow_comment = zero_transition(request.POST['siteAllowComment'])
            bs.save()
            resp['status'] = 'success'
            resp['info'] = '系统信息修改成功'
        else:
            resp['status'] = 'error'
            resp['info'] = '提交的信息有误，请检查后重试'
        return JsonResponse(resp)


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
def updateResource(request):
    resp = {'status': None, 'info': None}
    if request.method == 'POST':
        burf = BatchUpdateResourceForm(request.POST)
        if burf.is_valid():
            bur_list = json.loads(request.POST['resourceId'])
            print(bur_list)
            rt = request.POST['resourceType']
            rp = request.POST['resourceParameter']
            if bur_list is not None:
                for item in bur_list:
                    if rt == 'article_comment' and rp == 'is_passed':
                        ac = ArticleComment.objects.get(id=str(item))
                        ac.is_passed = not ac.is_passed
                        ac.save()
                        resp['status'] = 'success'
                        resp['info'] = '状态更新成功'
                return JsonResponse(resp)
    resp['status'] = 'error'
    resp['info'] = '提交的信息有误，请检查后重试'
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
            elif request.POST['resourceType'] == 'blog_article' \
                    or request.POST['resourceType'] == 'blog_page' \
                    or request.POST['resourceType'] == 'article_comment':
                return JsonResponse(batch_delete(resource_type=request.POST['resourceType'],
                                                 resource_ids=request.POST['resourceId']))
        resp['status'] = 'error'
        resp['info'] = '提交的删除信息有误，请检查后重试'
        return JsonResponse(resp)


# 错误信息
def blog_error(request, msg=""):
    return render(request, 'admin_error.html', {'error_message': msg})


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
