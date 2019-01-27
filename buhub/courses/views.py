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

# SCI-IISOC-II EITHER
subareas_to_indices = {
	'AE': 0, 'CI': 1, 'CT': 2,
	'DME': 3, 'ER': 4, 'FYWS': 5,
	'GCIL': 6, 'HC': 7, 'IC': 8,
	'OSC': 9, 'PILM': 10, 'QR I': 11,
	'QR-I': 11, 'QR II': 12, 'QR-II': 12,
	'RIL': 13, 'SCI I': 14, 'SCI-I': 14,
	'SCI II': 15, 'SCI-II': 15, 'SOC I': 16, 
	'SOC-I': 16, 'SOC II': 17, 'SOC-II': 17,
	'TC': 18, 'WIC': 19, 'WRI': 20
}

# def find_set_of_vectors(hub_vector):
# 	course_to_subareas = dict()
# 	hub_courses = ActualHubCourse.objects.all()
# 	for hub_course in hub_courses:
# 		subareas = hub_course.subareas.split(',')
# 		course_vector = [0 for _ in range(21)]
# 		for subarea in subareas:
# 			course_vector[subareas_to_indices[subarea]] = 1
# 		course_to_subareas[hub_course.title_course_name] = course_vector
# 	output = []
# 	for hub_course_name in course_to_subareas:
# 		curr_vector = course_to_subareas[hub_course_name]
# 		vector_sum = sum([curr_vector[i] * hub_vector[i] for i in range(21)])
# 		output.append((hub_course_name, vector_sum))
# 	sorted_output = sorted(output, key = lambda x: x[1], reverse=True)
# 	print(sorted_output)
# 	current_sum = [0 for _ in range(21)]
# 	index = 0
# 	while True:
# 		curr_course = sorted_output[index][0]
# 		curr_course_vector = course_to_subareas[curr_course]
# 		current_sum = [current_sum[i] + curr_course_vector[i] for i in range(21)]
# 		print("{} CURRENT SUM".format(current_sum))
# 		print("{} HUB VECTOR".format(hub_vector))
# 		if all([current_sum[i] - hub_vector[i] >= 0 for i in range(21)]):
# 			break
# 		index += 1
# 	print("\n\n\nWhat is index {}".format(index))
# 	return sorted_output[:index + 1]

def find_set_of_vectors(hub_vector):
	course_to_subareas = dict()
	hub_courses = ActualHubCourse.objects.all()
	for hub_course in hub_courses:
		subareas = hub_course.subareas.split(',')
		course_vector = [0 for _ in range(21)]
		for subarea in subareas:
			course_vector[subareas_to_indices[subarea]] = 1
		course_to_subareas[hub_course.title_course_name] = course_vector
	
	classes = []
	current_sum = [0 for _ in range(21)]
	while True:
		if all([current_sum[i] - hub_vector[i] >= 0 for i in range(21)]):
			break
		difference = [hub_vector[i] - current_sum[i] for i in range(21)]
		difference = [x if x > 0 else 0 for x in difference]
		best_vector_sum = 0
		best_vector = []
		best_vector_name = ''
		for hub_course_name in course_to_subareas:
			curr_vector = course_to_subareas[hub_course_name]
			vector_sum = sum([curr_vector[i] * difference[i] for i in range(21)])
			if vector_sum > best_vector_sum:
				best_vector = curr_vector
				best_vector_sum = vector_sum
				best_vector_name = hub_course_name
		classes.append(best_vector_name)
		current_sum = [current_sum[i] + best_vector[i] for i in range(21)]
	return classes

def fetch_hub_classes(request):
	hub_vector = [0 for _ in range(21)]

	dont_touch = set({'SCI II', 'SCI-II', 'SOC II', 'SOC-II'})
	for subarea in subareas_to_indices:
		if '-' in subarea or subarea in dont_touch:
			continue
		post_key = 'units_left[{}]'.format(subarea)
		hub_vector[subareas_to_indices[subarea]] = int(request.POST.get(post_key))

	scisoc_key = 'units_left[{}]'.format('SCI-IISOC-II')
	hub_vectors = []
	if int(request.POST.get(scisoc_key)) > 0:
		hub_vector_soc_copy = [_ for _ in hub_vector]
		hub_vector_soc_copy[17] += 1
		hub_vector_sic_copy = [_ for _ in hub_vector]
		hub_vector_sic_copy[15] += 1
		hub_vectors.append(hub_vector_sic_copy)
		hub_vectors.append(hub_vector_soc_copy)
	else:
		hub_vectors.append(hub_vector)

	hub_classes = find_set_of_vectors(hub_vectors[0])
	return HttpResponse(json.dumps({'hub_classes': hub_classes}))








