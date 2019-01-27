import json

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'index.html')

def fetch_requirements(request):
	return HttpResponse(json.dumps({'hi': 4}))

def question1(request):
	return render(request, 'question1.html')

def question2(request):
	return render(request, 'question2.html')