from django.contrib import admin
from .models import UserProfile, BannerInfo, EmailVerifyCode

# Register your models here.
admin.site.site_header = '管理后台'  # 设置header
admin.site.site_title = '管理后台'  # 设置title
admin.site.index_title = '管理后台'


class Banner(admin.ModelAdmin):
    list_display = ['image', 'url', 'add_time']


class Email(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type']


admin.site.register(UserProfile)
admin.site.register(BannerInfo, Banner)
admin.site.register(EmailVerifyCode, Email)
