from django.contrib import admin

from .models import MajorCourse, HubCourse
# Register your models here.

class MajorCourseAdmin(admin.ModelAdmin):
	fields = ('department', 'title', 'course_number', 'description')
	list_display = ['department', 'title', 'course_number', 'description']

class HubCourseAdmin(admin.ModelAdmin):
	fields = ('area', 'subarea', 'title', 'course_number', 'description')
	list_display = ['area', 'subarea', 'title', 'course_number', 'description']

admin.site.register(MajorCourse, MajorCourseAdmin)
admin.site.register(HubCourse, HubCourseAdmin)