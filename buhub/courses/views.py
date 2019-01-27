import json

from django.shortcuts import render
from django.http import HttpResponse

from courses.models import APClasses, Courses

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

def fetch_requirements(request):
	return HttpResponse(json.dumps({'hi': 4}))

def question1(request):
	return render(request, 'question1.html')

def question2(request):
	return render(request, 'question2.html')