import csv
from os import listdir
from os.path import isfile, join

from courses.models import HubCourse

def fetch_csv(path):
	return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

def populate_database(csv_file):
	with open(csv_file, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			area = row[0]
			subarea = row[1]
			title  = row[3]
			course_number = row[2]
			description = row[4]

			HubCourse.objects.create(
				area = area,
				subarea = subarea,
				title = title,
				course_number = course_number,
				description = description
			)

csv_files = fetch_csv('hub_data')
for csv_file in csv_files:
	populate_database(csv_file)

