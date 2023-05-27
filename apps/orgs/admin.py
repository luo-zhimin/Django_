from django.contrib import admin
from .models import CityInfo, OrgInfo, TeacherInfo

# Register your models here.
admin.site.register(CityInfo)
admin.site.register(OrgInfo)
admin.site.register(TeacherInfo)
