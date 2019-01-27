from django.contrib import admin

from .models import ActualHubCourse, APClasses, Courses, MajorCourse, HubCourse
# Register your models here.
class APClassesAdmin(admin.ModelAdmin):
	fields = ('examination', 'score', 'course_equivalent', 'bu_hub_area')
	list_display = ('examination', 'score', 'course_equivalent', 'bu_hub_area')

class CoursesAdmin(admin.ModelAdmin):
	fields = ('course',)

class MajorCourseAdmin(admin.ModelAdmin):
	fields = ('department', 'title', 'course_number', 'description')
	list_display = ['department', 'title', 'course_number', 'description']

class ActualHubCourseAdmin(admin.ModelAdmin):
	fields = ('title_course_name', 'subareas', 'title', 'course_number', 'description')
	list_display = ['title_course_name', 'subareas']

class HubCourseAdmin(admin.ModelAdmin):
	fields = ('area', 'subarea', 'title', 'course_number', 'description')
	list_display = ['area', 'subarea', 'title', 'course_number', 'description']

admin.site.register(APClasses, APClassesAdmin)
admin.site.register(Courses, CoursesAdmin)
admin.site.register(MajorCourse, MajorCourseAdmin)
admin.site.register(HubCourse, HubCourseAdmin)
admin.site.register(ActualHubCourse, ActualHubCourseAdmin)