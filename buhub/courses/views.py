import json

from django.shortcuts import render
from django.http import HttpResponse

from courses.models import APClasses, Courses

# Create your views here.
def index(request):
	context = {
		'majors': Courses.objects.all().order_by('course'),
		'aps': APClasses.objects.all().order_by('examination')
	}
	return render(request, 'index.html', context)

def fetch_requirements(request):
	return HttpResponse(json.dumps({'hi': 4}))