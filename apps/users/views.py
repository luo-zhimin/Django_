from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, HttpResponse

from courses.models import CourseInfo
from operations.models import UserCourseInfo, UserLoveInfo, UserMessageInfo
from orgs.models import OrgInfo, TeacherInfo
from utils import page_tool, common_tool
from utils.send_mail_tool import send_email_code
from .forms import UserRegisterForm, UserLoginForm, UserForgetForm, UserResetForm, UserChangeImageForm, \
    UserChangeInfoForm, UserChangeEmailForm, UserRestEmailForm
from .models import UserProfile, EmailVerifyCode, BannerInfo


# Create your views here.
# index
def index(request):
    banners = BannerInfo.objects.all().order_by('-add_time')[:5]
    courses = CourseInfo.objects.filter(is_banner=False).all().order_by('-add_time')[:6]
    banner_courses = CourseInfo.objects.filter(is_banner=True).all().order_by('-add_time')[:6]
    orgs = OrgInfo.objects.all().order_by('-add_time')[:15]
    return render(request, 'index.html', {
        'banners': banners,
        'banner_courses': banner_courses,
        'courses': courses,
        'orgs': orgs
    })


def user_register(request):
    if request.method == 'GET':
        # 验证码
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html', {
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
                return render(request, 'users/register.html', {
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
                common_tool.message_save(request=request, content=fr'欢迎{user.username}注册爱教育系统')
                # return redirect(reverse('index'))
                return HttpResponse("请尽快前往您的邮箱进行激活，否则无法登陆")
        else:
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form
            })


def user_login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
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
                    common_tool.message_save(request=request, content=fr'欢迎{user.username}登陆，爱教育系统')
                    return redirect(reverse('index'))
                else:
                    return HttpResponse("请去您的邮箱进行激活操作，否则无法登陆")
            else:
                return render(request, 'users/login.html', {
                    'msg': '邮箱或者密码错误'
                })
        else:
            return render(request, 'users/login.html', {
                'user_login_form': user_login_form
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


def user_forget(request):
    if request.method == 'GET':
        # return render(request, 'forgetpwd.html')
        # 验证码
        user_forget_form = UserForgetForm()
        return render(request, 'users/forgetpwd.html', {
            'user_forget_form': user_forget_form
        })
    else:
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(username=email)
            if user_list:
                send_email_code(email, 2)
                return HttpResponse('请尽快去您的邮箱重置密码')
            else:
                return render(request, 'users/forgetpwd.html', {
                    'msg': '用户不存在'
                })
        else:
            return render(request, 'users/forgetpwd.html', {
                'user_forget_form': user_forget_form
            })


def user_reset(request, code):
    print(fr'user_reset code:{code}')
    if code:
        if request.method == 'GET':
            return render(request, 'users/password_reset.html', {
                # 为post form 表单 提供参数 不然需要去其他页面拼接参数 前端去做 页面优化
                'code': code
            })
        else:
            user_reset_form = UserResetForm(request.POST)
            # print(fr'user_reset :{user_reset_form}')
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password1 = user_reset_form.cleaned_data['password1']

                print(fr'password:{password} password1:{password1}')
                if password == password1:
                    email_list = EmailVerifyCode.objects.filter(code=code)
                    print(fr'user_reset email_list :{email_list}')
                    if email_list:
                        email_verify = email_list[0]
                        user_list = UserProfile.objects.filter(username=email_verify.email)
                        if user_list:
                            user = user_list[0]
                            user.set_password(password)
                            user.save()
                            return redirect(reverse('users:user_login'))
                        else:
                            return HttpResponse('用户不存在')
                    else:
                        return HttpResponse('用户不存在')
                else:
                    # return HttpResponse('密码不一致 请确认后重新操作')
                    return render(request, 'users/password_reset.html', {
                        'msg': '密码不一致 请确认后重新操作',
                        'code': code
                    })
            else:
                return render(request, 'users/password_reset.html', {
                    'user_reset_form': user_reset_form,
                    'code': code
                })
    else:
        # return HttpResponse('验证码不存在，请重新获取')
        return render(request, 'users/login.html', {
            'msg': '验证码不存在，请重新获取'
        })


def user_info(request):
    return render(request, 'users/usercenter-info.html')


def user_change_image(request):
    # instance 指明实列是什么 修改时候 不指明的话会被当作创建对象去执行
    user_change_image_form = UserChangeImageForm(request.POST,
                                                 request.FILES,
                                                 instance=request.user)
    if user_change_image_form.is_valid():
        user_change_image_form.save(commit=True)
        return JsonResponse({'statsu': 'ok'})
    else:
        return JsonResponse({'statsu': 'fail'})


def user_change_info(request):
    user_change_info_form = UserChangeInfoForm(request.POST, instance=request.user)
    if user_change_info_form.is_valid():
        user_change_info_form.save(commit=True)
        return JsonResponse({'statsu': '200', 'msg': '修改成功'})
    else:
        return JsonResponse({'statsu': '500', 'msg': '修改失败'})


def user_change_email(request):
    user_change_email_form = UserChangeEmailForm(request.POST)
    if user_change_email_form.is_valid():
        email = user_change_email_form.cleaned_data['email']
        user_list = UserProfile.objects.filter(Q(email=email) | Q(username=email))
        if user_list:
            return JsonResponse({'statsu': 500, 'msg': '邮箱已经被绑定'})
        else:
            email_verify = EmailVerifyCode.objects.filter(email=email, send_type=3).order_by('-add_time')[0]
            if email_verify:
                # 间隔1分钟
                if (datetime.now() - email_verify.add_time).seconds <= 60:
                    return JsonResponse({'statsu': 500, 'msg': '请不要重复发送验证码，1分钟后重试'})
                else:
                    # send email 可以保留 也可以删除 现在是只保留最后一条
                    email_verify.delete()
                    send_email_code(email=email, send_type=3)
                    return JsonResponse({'statsu': 200, 'msg': '请尽快去邮箱中获取验证码'})
            else:
                send_email_code(email=email, send_type=3)
                return JsonResponse({'statsu': 200, 'msg': '请尽快去邮箱中获取验证码'})
    else:
        return JsonResponse({'statsu': 500, 'msg': '您的邮箱有误，请检查后重新填写'})


def user_rest_email(request):
    user_rest_email_form = UserRestEmailForm(request.POST)
    if user_rest_email_form.is_valid():
        email = user_rest_email_form.cleaned_data['email']
        code = user_rest_email_form.cleaned_data['code']
        email_verify = EmailVerifyCode.objects.filter(email=email, code=code)[0]
        if email_verify:
            if (datetime.now() - email_verify.add_time).seconds <= 60:
                request.user.username = email
                request.user.email = email
                request.user.save()
                return JsonResponse({'statsu': 200, 'msg': '邮箱修改成功'})
            else:
                return JsonResponse({'statsu': 500, 'msg': '验证码失效，请重新获取验证码'})
        else:
            return JsonResponse({'statsu': 500, 'msg': '您的邮箱或者验证码有误'})
    else:
        return JsonResponse({'statsu': 500, 'msg': '您的邮箱或者验证码有误'})


def user_course(request):
    user_courses = UserCourseInfo.objects.filter(study_man=request.user)
    courses = [userCourse.study_course for userCourse in user_courses]

    return render(request, 'users/usercenter-mycourse.html', {
        'courses': courses
    })


def user_love_org(request):
    user_love_orgs = UserLoveInfo.objects.filter(love_type=1, love_man=request.user, love_status=True)
    org_ids = [o.love_id for o in user_love_orgs]
    orgs = OrgInfo.objects.filter(id__in=org_ids)
    return render(request, 'users/usercenter-fav-org.html', {
        'orgs': orgs
    })


def user_love_teacher(request):
    user_love_teachers = UserLoveInfo.objects.filter(love_type=3, love_man=request.user, love_status=True)
    teachers_ids = [o.love_id for o in user_love_teachers]
    teachers = TeacherInfo.objects.filter(id__in=teachers_ids)
    return render(request, 'users/usercenter-fav-teacher.html', {
        'teachers': teachers
    })


def user_love_course(request):
    user_love_courses = UserLoveInfo.objects.filter(love_type=2, love_man=request.user, love_status=True)
    courses_ids = [o.love_id for o in user_love_courses]
    courses = CourseInfo.objects.filter(id__in=courses_ids)
    return render(request, 'users/usercenter-fav-course.html', {
        'courses': courses
    })


def user_message(request):
    messages = UserMessageInfo.objects.filter(message_man=request.user.id).order_by('-add_time')
    pages = page_tool.page(request, messages)
    return render(request, 'users/usercenter-message.html', {
        'messages': messages,
        'pages': pages
    })
