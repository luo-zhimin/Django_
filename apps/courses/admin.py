from django.contrib import admin
from .models import CourseInfo, ChapterInfo, VideoInfo, SourceInfo

# Register your models here.

admin.site.register(CourseInfo)
admin.site.register(ChapterInfo)
admin.site.register(VideoInfo)
admin.site.register(SourceInfo)
