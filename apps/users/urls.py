"""
URL configuration for Django_ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path

from .views import UserRegisterView, UserLoginView, UserLogoutView, UserActiveView, UserForgetView, UserResetView, \
    UserInfoView, UserChangeImageView, UserChangeInfoView, UserChangeEmailView, UserRestEmailView, UserCourseView, \
    UserLoveOrgView, UserLoveCourseView, UserLoveTeacherView, UserMessageView

urlpatterns = [
    # name 必须是 'xxx'
    path('user_register/', UserRegisterView.as_view(), name='user_register'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    # 如果要使用正则表达式 需要使用re_path
    re_path('user_active/(\\w+)/', UserActiveView.as_view(), name='user_active'),

    path('user_forget/', UserForgetView.as_view(), name='user_forget'),
    re_path('user_reset/(\\w+)/', UserResetView.as_view(), name='user_reset'),

    path('user_info/', UserInfoView.as_view(), name='user_info'),
    path('user_change_image/', UserChangeImageView.as_view(), name='user_change_image'),
    path('user_change_info/', UserChangeInfoView.as_view(), name='user_change_info'),
    path('user_change_email/', UserChangeEmailView.as_view(), name='user_change_email'),
    path('user_rest_email/', UserRestEmailView.as_view(), name='user_rest_email'),

    path('user_course/', UserCourseView.as_view(), name='user_course'),
    path('user_love_org/', UserLoveOrgView.as_view(), name='user_love_org'),
    path('user_love_teacher/', UserLoveTeacherView.as_view(), name='user_love_teacher'),
    path('user_love_course/', UserLoveCourseView.as_view(), name='user_love_course'),

    path('user_message/', UserMessageView.as_view(), name='user_message'),
]
