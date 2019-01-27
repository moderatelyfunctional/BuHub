from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
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