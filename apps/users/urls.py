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

from .views import user_register, user_login, user_logout, user_active, user_forget, user_reset, \
    user_info, \
    user_change_image, user_change_info, user_change_email, user_rest_email

urlpatterns = [
    # name 必须是 'xxx'
    path('user_register/', user_register, name='user_register'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    # 如果要使用正则表达式 需要使用re_path
    re_path('user_active/(\\w+)/', user_active, name='user_active'),

    path('user_forget/', user_forget, name='user_forget'),
    re_path('user_reset/(\\w+)/', user_reset, name='user_reset'),

    path('user_info/', user_info, name='user_info'),
    path('user_change_image/', user_change_image, name='user_change_image'),
    path('user_change_info/', user_change_info, name='user_change_info'),
    path('user_change_email/', user_change_email, name='user_change_email'),
    path('user_rest_email/', user_rest_email, name='user_rest_email'),
]
