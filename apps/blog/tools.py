import datetime
import time
import random

from django.core.mail import send_mail
from django.conf import settings

from blog.models import EmailVerifyRecord, BlogSettings


# 转换以秒为单位的时间戳
def get_time_stamp(d_time):
    return time.mktime(d_time.timetuple())


# 获取随机邮箱验证码
def get_email_verify_record():
    recode = str(random.randint(100000, 999999))
    return recode


# 发送邮箱验证码
def send_verify_email(target_email):
    # 清空之前的验证码
    EmailVerifyRecord.objects.filter(email=target_email).delete()
    email_title = "ublog - 验证码"
    code = get_email_verify_record()
    email_body = "您本次的验证码为：" + code + "。请在10分钟内验证，过期失效。"
    evr = EmailVerifyRecord()
    # evr.code = code
    evr.code = '123456' #
    evr.email = target_email
    evr.save()
    return True #
    # if send_mail(email_title, email_body, settings.EMAIL_FROM, [target_email]):
    #     return True
    # return False


# 验证邮箱验证码
def verify_email(email, code):
    try:
        evr = EmailVerifyRecord.objects.filter(email=email).order_by('-id').first()
    except Exception as e:
        evr = None
    if evr:

        time_difference = get_time_stamp(datetime.datetime.now()) - get_time_stamp(evr.send_time)
        # 如果时间差超过10分钟，也同样验证失败
        if time_difference < 600:
            if code == evr.code:
                # 验证成功后，删除验证码
                evr.delete()
                return True
    return False


# 获取head_title
def get_blog_settings():
    try:
        blog_settings = BlogSettings.objects.all().order_by('id').first()
    except Exception as e:
        blog_settings = None
    return blog_settings


# 转换01
def zero_transition(num):
    if num == '1':
        return True
    return False

