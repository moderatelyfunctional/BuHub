import json

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat

from courses.models import APClasses, Courses, HubCourse, ActualHubCourse

# Create your views here.
def index(request):
	context = {
		'majors': Courses.objects.all().order_by('course'),
		'aps': APClasses.objects.all().order_by('examination'),
	}
	context['ap_to_hub'] = dict()
	for ap in context['aps']:
		context['ap_to_hub'][ap.examination + '-' + ap.score] = ap.bu_hub_area
	context['ap_to_hub'] = json.dumps(context['ap_to_hub'])
	return render(request, 'index.html', context)

def compute_fewest_hubs(request):
	combined_hubs = HubCourse.objects.annotate(
		unique_name=Concat(
			'course_number', V('-'), 'title',
		    output_field=CharField()
		)
	).all()
	distinct_elements = combined_hubs.order_by().values('unique_name').distinct()
	i = 0
	for element in distinct_elements:
		unique_subareas = combined_hubs.filter(unique_name = element['unique_name']).order_by('subarea').values('subarea').distinct()
		subareas_list = ','.join([element['subarea'] for element in unique_subareas])
		ActualHubCourse.objects.create(title_course_name = element['unique_name'], subareas=subareas_list)
	return HttpResponse()

