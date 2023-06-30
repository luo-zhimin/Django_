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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Django_ import settings
from users.views import IndexView

urlpatterns = [
    # 首页直接进行跳转
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    # path('xadmin/', xadmin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('orgs/', include(('orgs.urls', 'orgs'), namespace='orgs')),
    path('operations/', include(('operations.urls', 'operations'), namespace='operations')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
