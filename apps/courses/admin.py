from django.contrib import admin
from .models import CourseInfo, ChapterInfo, VideoInfo, SourceInfo


# Register your models here.

class Course(admin.ModelAdmin):
    list_display = ['image', 'name', 'study_time', 'study_num', 'level', 'love_num', 'click_num', 'desc', 'detail',
                    'category', 'course_notice', 'course_need', 'org_info', 'teacher_info']


class Chapter(admin.ModelAdmin):
    list_display = ['name', 'course_info', 'add_time']


class Video(admin.ModelAdmin):
    list_display = ['name', 'study_time', 'url', 'chapter_info', 'add_time']


class Source(admin.ModelAdmin):
    list_display = ['name', 'down_load', 'course_info', 'add_time']


admin.site.register(CourseInfo, Course)
admin.site.register(ChapterInfo, Chapter)
admin.site.register(VideoInfo, Video)
admin.site.register(SourceInfo, Source)
