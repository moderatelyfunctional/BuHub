from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class ActualHubCourse(models.Model):
	title_course_name = models.CharField(_('title_course_name'), max_length=128)
	subareas = models.TextField(_('subareas'))

class APClasses(models.Model):
	examination = models.CharField(_('examination'), max_length=64)
	score = models.CharField(_('score'), max_length=16)
	course_equivalent = models.CharField(_('course_equivalent'), max_length=64)
	bu_hub_area= models.CharField(_('bu_hub_area'), max_length=64, blank=True)

class Courses(models.Model):
	course = models.CharField(_('course'), max_length=24)

class MajorCourse(models.Model):
	department = models.CharField(_('department'), max_length=32)
	title = models.CharField(_('title'), max_length=64)
	course_number = models.IntegerField(_('course_number'), default=0)
	description = models.TextField(_('description'), default='This is blank')

class HubCourse(models.Model):
	area = models.CharField(_('area'), max_length=16, default='')
	subarea = models.CharField(_('subarea'), max_length=16, default='')
	title = models.CharField(_('title'), max_length=64)
	course_number = models.IntegerField(_('course_number'), default=0)
	description = models.TextField(_('description'), default='This is blank')