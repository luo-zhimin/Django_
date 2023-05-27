from django.contrib import admin
from .models import CityInfo, OrgInfo, TeacherInfo


class City(admin.ModelAdmin):
    list_display = ['name', 'add_time']


class Org(admin.ModelAdmin):
    list_display = ['image', 'name', 'course_num', 'study_num', 'love_num', 'click_num', 'address', 'remark',
                    'detail', 'category', 'city_info', 'add_time']


class Teacher(admin.ModelAdmin):
    list_display = ['image', 'name', 'work_year', 'work_position', 'work_style', 'work_company', 'age', 'love_num',
                    'click_num', 'add_time']


# Register your models here.
admin.site.register(CityInfo, City)
admin.site.register(OrgInfo, Org)
admin.site.register(TeacherInfo, Teacher)
