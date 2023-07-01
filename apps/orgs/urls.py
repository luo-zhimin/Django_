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

from .views import OrgListView, OrgDetailView, OrgDetailCourseView, OrgDetailDescView, OrgDetailTeachersView, \
    TeacherListView, TeacherDetailView

urlpatterns = [
    path('org_list/', OrgListView.as_view(), name='org_list'),
    re_path('org_detail/(\\d+)', OrgDetailView.as_view(), name='org_detail'),
    re_path('org_detail_course/(\\d+)', OrgDetailCourseView.as_view(), name='org_detail_course'),
    re_path('org_detail_desc/(\\d+)', OrgDetailDescView.as_view(), name='org_detail_desc'),
    re_path('org_detail_teachers/(\\d+)', OrgDetailTeachersView.as_view(), name='org_detail_teachers'),
    # teacher
    path('teacher_list/', TeacherListView.as_view(), name='teacher_list'),
    re_path('teacher_detail/(\\d+)', TeacherDetailView.as_view(), name='teacher_detail'),
]
