from django.contrib import admin
from .models import UserAskInfo, UserLoveInfo, UserCourseInfo, UserCommentInfo, UserMessageInfo

# Register your models here.

admin.site.register(UserAskInfo)
admin.site.register(UserLoveInfo)
admin.site.register(UserCourseInfo)
admin.site.register(UserCommentInfo)
admin.site.register(UserMessageInfo)
