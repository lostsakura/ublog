from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# 系统设置model
class BlogSettings(models.Model):
    id = models.BigAutoField(verbose_name="id", primary_key=True)
    site_name = models.CharField(verbose_name='站点名称', default='Hello World!', max_length=100)
    site_address = models.CharField(verbose_name='站点地址', default='http://u.blog', max_length=500)
    site_desc = models.CharField(verbose_name='站点描述', default='Just So So...', max_length=500)
    site_keyword = models.CharField(verbose_name='关键词', default='ublog', max_length=500)
    allow_comment = models.BooleanField(verbose_name="是否可以评论", choices=((False, "禁用评论"), (True, "启用评论")),
                                        default=False)

    class Meta:
        verbose_name = "系统设置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.id)


# 用户model 继承内置的User，并添加新的字段
class BlogUser(AbstractUser):
    nick_name = models.CharField(verbose_name="昵称", max_length=50, default="未设置昵称", blank=True)
    avatar_image = models.ImageField(verbose_name='头像', upload_to="images/avatar_image%Y/%m",
                                     default="images/avatar_image/default.png")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.username, self.email)


# 文章model
class BlogArticle(models.Model):
    id = models.BigAutoField(verbose_name="id", primary_key=True)
    title = models.CharField(verbose_name="标题", null=False, max_length=50)
    content = models.TextField(verbose_name="内容", default="")
    is_private = models.BooleanField(verbose_name="是否仅自己可见", choices=((True, "仅自己可见"), (False, "所有人可见")),
                                     default=False)
    is_draft = models.BooleanField(verbose_name="是否草稿", choices=((True, "是"), (False, "否")), default=True)
    created_time = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    update_time = models.DateTimeField(verbose_name="修改时间", null=False)
    clicks = models.IntegerField(verbose_name="点击数", default=0)
    likes = models.IntegerField(verbose_name="点赞", default=0)
    label = models.CharField(verbose_name="标签", max_length=500, default="")
    cover_picture = models.ImageField(verbose_name='封面图', upload_to="images/blog_cover_picture%Y/%m",
                                      default="images/blog_cover_picture/default-picture.jpg")

    class Meta:
        verbose_name = "博客文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.title)


# 分类标签
class BlogLabel(models.Model):
    id = models.BigAutoField(verbose_name="id", primary_key=True)
    label_name = models.CharField(verbose_name="标签名", null=False, max_length=50)

    class Meta:
        verbose_name = "分类标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.label_name)


# 游客评论
class ArticleComment(models.Model):
    id = models.BigAutoField(verbose_name="id", primary_key=True)
    article = models.ForeignKey(BlogArticle, verbose_name="文章", on_delete=None)
    author = models.CharField(verbose_name="游客名称", null=False, max_length=20)
    content = models.CharField(verbose_name="内容", default="", max_length=140)
    is_passed = models.BooleanField(verbose_name="是否通过审阅", choices=((True, "是"), (False, "否")), default=False)

    class Meta:
        verbose_name = "游客评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}{1}'.format(self.article, self.author)


# 邮箱验证码
class EmailVerifyRecord(models.Model):
    id = models.BigAutoField(verbose_name="id", primary_key=True)
    code = models.CharField(max_length=20, verbose_name="验证码", )
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)