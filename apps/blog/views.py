from django.shortcuts import render

# Create your views here.


# 首页
def blog_index(request):
    return render(request, 'index.html')


# 后台
def blog_admin(request):
    return render(request, 'admin_main.html')


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
