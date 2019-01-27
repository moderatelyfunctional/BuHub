import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.bu.edu/phpbin/course-search/search.php'

colleges = [
	'CAS', 'CFA', 'CGS',
	'COM', 'ENG', 'EOP',
	'GMS', 'GRS', 'KHC',
	'LAW', 'MED', 'MET',
	'OTP', 'PDP', 'QST',
	'SAR', 'SDM', 'SED',
	'SHA', 'SPH', 'SSW',
	'STH', 'XRG',
]

hub_mapping = {
	'PAHI': ['A', 'B', 'C'],
	'SSI': ['D', 'F', 'E', 'P'],
	'QR': ['G', 'H'],
	'DCEGC': ['I', 'J', 'K'],
	'C': ['L', 'M', '6', 'N', 'O'],
	'IT': ['1', '2', '3', '4']
}

hub_subarea_mapping = {
	'A': 'PILM',
	'B': 'AE',
	'C': 'HC',
	'D': 'SCI-I',
	'F': 'SCI-II',
	'E': 'SOC-I',
	'P': 'SOC-II',
	'G': 'QR-I',
	'H': 'QR-II',
	'I': 'IC',
	'J': 'GCIL',
	'K': 'ER',
	'L': 'FYWS',
	'M': 'WRI',
	'6': 'WIC',
	'N': 'OSC',
	'O': 'DME',
	'1': 'CT',
	'2': 'RIL',
	'3': 'TC',
	'4': 'CI'
}

def hub_request(hub_area_subtype):
	r = requests.post(BASE_URL, data = {
		'page': 0,
		'pagesize': -1,
		'adv': 1,
		'yearsem_adv': '2019-SPRG',
		'credits': '*',
		'hub': hub_area_subtype,
		'colleges': colleges	
	})
	return r

def fetch_hub_classes(response):
	text = response.text
	parsed_html = BeautifulSoup(text, 'html.parser')
	result_divs = parsed_html.find_all('div', class_='result')

	output_data = []
	for result_div in result_divs:
		title_and_course_number = result_div.find_all('div', class_='title')[0]
		title_and_course_number_split = title_and_course_number.text.split(' ')
		title_number = int(title_and_course_number_split[2])
		course = ' '.join(title_and_course_number_split[4:]).encode('utf-8')

		desc = result_div.find_all('div', class_='description')[0].text
		desc_end_index = desc.find('[')
		desc = desc[:desc_end_index].strip().encode('utf-8')

		output_data.append((
			title_number,
			course,
			desc
		))

	return output_data

for hub_area in hub_mapping:
	for hub_area_subtype in hub_mapping[hub_area]:
		print('Working on {}'.format(hub_area_subtype))
		response = hub_request(hub_area_subtype)
		output = fetch_hub_classes(response)

		print('There are {} rows'.format(len(output)))
		data_filename = 'data/{}_{}.csv'.format(hub_area, hub_area_subtype)
		with open(data_filename, mode='w') as f:
			data_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for output_line in output:
				area_subarea_row = [hub_area, hub_subarea_mapping[hub_area_subtype]] 
				data_row = [output_element for output_element in output_line]
				data_writer.writerow(area_subarea_row + data_row)

