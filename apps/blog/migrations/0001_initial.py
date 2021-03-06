# Generated by Django 2.2 on 2020-02-07 20:31

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogArticle',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('content', models.TextField(default='', verbose_name='内容')),
                ('is_private', models.BooleanField(choices=[(True, '仅自己可见'), (False, '所有人可见')], default=False, verbose_name='是否仅自己可见')),
                ('is_draft', models.BooleanField(choices=[(True, '是'), (False, '否')], default=True, verbose_name='是否草稿')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='修改时间')),
                ('clicks', models.IntegerField(default=0, verbose_name='点击数')),
                ('likes', models.IntegerField(default=0, verbose_name='点赞')),
                ('label', models.CharField(default='', max_length=500, verbose_name='标签')),
                ('cover_picture', models.ImageField(default='images/blog_cover_picture/default-picture.jpg', upload_to='images/blog_cover_picture%Y/%m', verbose_name='封面图')),
            ],
            options={
                'verbose_name': '博客文章',
                'verbose_name_plural': '博客文章',
            },
        ),
        migrations.CreateModel(
            name='BlogLabel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('label_name', models.CharField(max_length=50, verbose_name='标签名')),
            ],
            options={
                'verbose_name': '分类标签',
                'verbose_name_plural': '分类标签',
            },
        ),
        migrations.CreateModel(
            name='BlogSettings',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('site_name', models.CharField(default='Hello World!', max_length=100, verbose_name='站点名称')),
                ('site_address', models.CharField(default='http://u.blog', max_length=500, verbose_name='站点地址')),
                ('site_desc', models.CharField(default='Just So So...', max_length=500, verbose_name='站点描述')),
                ('site_keyword', models.CharField(default='ublog', max_length=500, verbose_name='关键词')),
                ('allow_comment', models.CharField(choices=[('public', '公开'), ('private', '私有')], max_length=20, verbose_name='隐私状态')),
            ],
            options={
                'verbose_name': '系统设置',
                'verbose_name_plural': '系统设置',
            },
        ),
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '邮箱验证码',
                'verbose_name_plural': '邮箱验证码',
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('author', models.CharField(max_length=20, verbose_name='游客名称')),
                ('content', models.CharField(default='', max_length=140, verbose_name='内容')),
                ('is_passed', models.BooleanField(choices=[(True, '是'), (False, '否')], default=False, verbose_name='是否通过审阅')),
                ('article', models.ForeignKey(on_delete=None, to='blog.BlogArticle', verbose_name='文章')),
            ],
            options={
                'verbose_name': '游客评论',
                'verbose_name_plural': '游客评论',
            },
        ),
        migrations.CreateModel(
            name='BlogUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nick_name', models.CharField(blank=True, default='未设置昵称', max_length=50, verbose_name='昵称')),
                ('avatar_image', models.ImageField(default='images/avatar_image/default.png', upload_to='images/avatar_image%Y/%m', verbose_name='头像')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
