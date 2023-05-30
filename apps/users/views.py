from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout


# Create your views here.
# index
def index(request):
    return render(request, 'index.html')


def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']

            # 查询数据库
            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
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
                return redirect(reverse('index'))
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
                login(request, user)
                return redirect(reverse('index'))
            else:
                return render(request, 'login.html', {
                    'msg': '邮箱或者密码错误'
                })
        else:
            return render(request, 'login.html', {
                'msg': user_login_form
            })
