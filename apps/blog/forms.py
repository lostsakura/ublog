import re

from django import forms
from django.core.exceptions import ValidationError


# 仅邮箱验证验证码调用时使用 需带上类型，以验证用户的属性
class EmailForm(forms.Form):
    userEmail = forms.EmailField(required=True)
    type = forms.ChoiceField(required=True, choices=(('1', 'recoverPassword'), ('0', 'initialUser')))


# 博客初始化表单
class BlogStartForm(forms.Form):
    userEmail = forms.EmailField(required=True)
    verifyCode = forms.CharField(required=True)
    userPassword = forms.CharField(required=True, max_length=16, min_length=8)
    userName = forms.CharField(required=True, max_length=20, min_length=4)
    siteName = forms.CharField(required=True)
    siteAddress = forms.URLField(required=False)
    siteDesc = forms.CharField(required=False)
    siteKeyword = forms.CharField(required=True)
    siteAllowComment = forms.ChoiceField(required=True, choices=(('1', True), ('0', False)))

    # 自定义验证
    def clean_verifyCode(self):
        value = self.cleaned_data['verifyCode']
        ret = re.search(r'^[0-9]{6}$', value)
        if not ret:
            raise ValidationError('验证码格式不正确')
        return value


# 登陆表单
class LoginForm(forms.Form):
    userName = forms.CharField(required=True, max_length=20, min_length=4)
    userPassword = forms.CharField(required=True, max_length=16, min_length=8)
    rememberMe = forms.ChoiceField(required=True, choices=(('1', True), ('0', False)))


# 重置密码表单
class RecoverPasswordForm(forms.Form):
    userEmail = forms.EmailField(required=True)
    verifyCode = forms.CharField(required=True)
    newPassword = forms.CharField(required=True, max_length=16, min_length=8)


# 标签编辑表单
class ManageLabelsForm(forms.Form):
    labelName = forms.CharField(required=True)
    labelId = forms.CharField(required=True)


# 删除资源表单
class DeleteResourceForm(forms.Form):
    resourceId = forms.CharField(required=True)
    resourceType = forms.ChoiceField(required=True, choices=(('blog_label', 'blog_label'),
                                                             ('blog_article', 'blog_article'),
                                                             ('blog_page', 'blog_page')))


# 文章编辑表单
class ArticleWriteForm(forms.Form):
    articleTitle = forms.CharField(required=True)
    articleContent = forms.TextInput()
    articleIsPrivate = forms.ChoiceField(required=True, choices=(('0', '所有人可见'), ('1', '仅自己可见')))
    articleLabel = forms.CharField(required=False)
    articleIsDraft = forms.ChoiceField(required=True, choices=(('0', 'not_draft'), ('1', 'is_draft')))
    articleId = forms.CharField(required=True)


# 页面编辑表单
class PageWriteForm(forms.Form):
    pageId = forms.IntegerField(required=True)
    pageTitle = forms.CharField(required=True)
    pageContent = forms.TextInput()
    pageSortId = forms.IntegerField(required=True, min_value=0, max_value=10)
    pageIsDraft = forms.ChoiceField(required=True, choices=(('0', 'is_draft'), ('1', 'not_draft')))


# 用户设置表单
class UserSettingsForm(forms.Form):
    userId = forms.IntegerField(required=True)
    userName = forms.CharField(required=True, max_length=20, min_length=4)


# 系统设置表单
class SystemSettingsForm(forms.Form):
    siteId = forms.IntegerField(required=True)
    siteName = forms.CharField(required=True)
    siteAddress = forms.URLField(required=False)
    siteDesc = forms.CharField(required=False)
    siteKeyword = forms.CharField(required=True)
    siteAllowComment = forms.ChoiceField(required=True, choices=(('1', True), ('0', False)))


# 提交评论表单
class SubmitCommentForm(forms.Form):
    articleId = forms.IntegerField(required=True)
    commentName = forms.CharField(required=True, min_length=2, max_length=20)
    commentEmail = forms.EmailField(required=True)
    commentContent = forms.TextInput()