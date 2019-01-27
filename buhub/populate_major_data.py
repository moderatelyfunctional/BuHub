import csv
from os import listdir
from os.path import isfile, join

from courses.models import MajorCourse

def fetch_csv(path):
	return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

def populate_database(csv_file):
	with open(csv_file, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			department = row[0]
			course_number = row[1]
			title = row[2]
			description = row[3]

			MajorCourse.objects.create(
				department = department,
				course_number = course_number,
				title = title,
				description = description
			)

csv_files = fetch_csv('major_data')
for csv_file in csv_files:
	populate_database(csv_file)

