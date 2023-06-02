from random import choice

from django.core.mail import send_mail

from Django_.settings import DEFAULT_FROM_EMAIL
from users.models import EmailVerifyCode


def get_random_code(code_length):
    # 码原
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for c in range(code_length):
        code += choice(code_source)
    return code


def send_email_code(email, send_type):
    # 创建邮箱验证码对象 保存数据库 用来验证
    code = get_random_code(6)
    mail = EmailVerifyCode()
    mail.email = email
    mail.send_type = send_type
    mail.code = code
    mail.save()

    # 发送邮件
    send_title = ''
    send_body = ''
    if send_type == 1:
        send_title = '欢迎注册爱时尚教育'
        send_body = '请点击以下链接进行激活您的账号：\n' \
                    'http://localhost:8000/users/user_active/' + code
    # send
    send_mail(send_title, send_body, DEFAULT_FROM_EMAIL, [email])
