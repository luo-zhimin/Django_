from django.contrib import admin
from .models import UserAskInfo, UserLoveInfo, UserCourseInfo, UserCommentInfo, UserMessageInfo


class UserAsk(admin.ModelAdmin):
    list_display = ['name', 'phone', 'course', 'add_time']


class UserLove(admin.ModelAdmin):
    list_display = ['love_man', 'love_id', 'love_type', 'love_status', 'add_time']


class UserCourse(admin.ModelAdmin):
    list_display = ['study_man', 'study_course', 'add_time']


class UserComment(admin.ModelAdmin):
    list_display = ['comment_man', 'comment_course', 'comment_content', 'add_time']


class UserMessage(admin.ModelAdmin):
    list_display = ['message_man', 'message_content', 'message_status', 'add_time']


# Register your models here.
admin.site.register(UserAskInfo, UserAsk)
admin.site.register(UserLoveInfo, UserLove)
admin.site.register(UserCourseInfo, UserCourse)
admin.site.register(UserCommentInfo, UserComment)
admin.site.register(UserMessageInfo, UserMessage)
