import re

from django import forms
from django.core.exceptions import ValidationError


# 仅邮箱验证
class EmailForm(forms.Form):
    userEmail = forms.EmailField(required=True)


# 博客初始化表单
class BlogStartForm(forms.Form):
    userEmail = forms.EmailField(required=True)
    verifyCode = forms.CharField(required=True)
    userPassword = forms.CharField(required=True, max_length=16, min_length=8)
    userName = forms.CharField(required=True, max_length=20, min_length=4)
    siteName = forms.CharField(required=True)
    siteAddress = forms.URLField()
    siteDesc = forms.CharField()
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
    userEmail = forms.EmailField(required=True)
    userPassword = forms.CharField(required=True, max_length=16, min_length=8)
    rememberMe = forms.ChoiceField(required=True, choices=(('1', True), ('0', False)))
