from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, HttpResponse

from utils.send_mail_tool import send_email_code
from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile, EmailVerifyCode


# Create your views here.
# index
def index(request):
    return render(request, 'index.html')


def user_register(request):
    if request.method == 'GET':
        # 验证码
        user_register_form = UserRegisterForm()
        return render(request, 'register.html', {
            'user_register_form': user_register_form
        })
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']

            # 查询数据库
            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            print(f"user_register: {user_list}")
            if user_list:
                return render(request, 'register.html', {
                    'msg': '用户已经存在'
                })
            else:
                # register
                user = UserProfile()
                user.username = email
                user.set_password(password)
                user.email = email
                user.save()
                # redirect 函数可以将用户重定向到指定的 URL
                # reverse 函数则是用于根据 URL 名称解析出对应的 URL 地址

                # 发送邮件
                send_email_code(email, 1)
                # return redirect(reverse('index'))
                return HttpResponse("请尽快前往您的邮箱进行激活，否则无法登陆")
        else:
            return render(request, 'register.html', {
                'msg': user_register_form
            })


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user:
                # 控制是否激活
                if user.status:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse("请去您的邮箱进行激活操作，否则无法登陆")
            else:
                return render(request, 'login.html', {
                    'msg': '邮箱或者密码错误'
                })
        else:
            return render(request, 'login.html', {
                'msg': user_login_form
            })


def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def user_active(request, code):
    print(fr'active code:{code}')
    if code:
        # 是否会有问题 一个码出现多次 是否需要加用户的标识 有几率出现
        email_verify_list = EmailVerifyCode.objects.filter(code=code)
        if email_verify_list:
            email_verify = email_verify_list[0]
            email = email_verify.email
            user_list = UserProfile.objects.filter(username=email)
            # 修改 激活
            if user_list:
                user = user_list[0]
                user.status = True
                user.save()
                return redirect(reverse('users:user_login'))
            else:
                print(fr'this code:{code} not find user:{email}')
                return HttpResponse('该用户不存在，请确认后重新登陆')
        else:
            return HttpResponse('验证码不存在，请重新获取')
    else:
        return HttpResponse('验证码不存在，请重新获取')
