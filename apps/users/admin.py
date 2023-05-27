from django.contrib import admin
from .models import UserProfile,BannerInfo,EmailVerifyCode

# Register your models here.
admin.site.site_header = '管理后台'  # 设置header
admin.site.site_title = '管理后台'  # 设置title
admin.site.index_title = '管理后台'


# class User_Manage(admin.ModelAdmin):
#     ist_display = ['id', 'username', 'password', 'nick_name', 'birthday', 'gender', 'address', 'phone', 'address',
#                    'add_time', 'created_time', 'update_time']


admin.site.register(UserProfile)
admin.site.register(BannerInfo)
admin.site.register(EmailVerifyCode)
