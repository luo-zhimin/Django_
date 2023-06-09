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

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView

urlpatterns = [
    path('course_list/', CourseListView.as_view(), name='course_list'),
    re_path('course_detail/(\\d+)', CourseDetailView.as_view(), name='course_detail'),
    re_path('course_video/(\\d+)', CourseVideoView.as_view(), name='course_video'),
    re_path('course_comment/(\\d+)', CourseCommentView.as_view(), name='course_comment'),
]
