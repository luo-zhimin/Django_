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

from .views import org_list, org_detail, org_detail_course, org_detail_desc, org_detail_teachers

urlpatterns = [
    path('org_list/', org_list, name='org_list'),
    re_path('org_detail/(\\d+)', org_detail, name='org_detail'),
    re_path('org_detail_course/(\\d+)', org_detail_course, name='org_detail_course'),
    re_path('org_detail_desc/(\\d+)', org_detail_desc, name='org_detail_desc'),
    re_path('org_detail_teachers/(\\d+)', org_detail_teachers, name='org_detail_teachers'),
]
