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
		course = ' '.join(title_and_course_number_split[4:])

		desc = result_div.find_all('div', class_='description')[0].text
		desc_end_index = desc.find('[')
		desc = desc[:desc_end_index].strip()

		output_data.append((
			title_number,
			course,
			desc
		))

	return output_data

r_a = hub_request('A')
output_a = fetch_hub_classes(r_a)
print(len(output_a))
for element in output_a:
	print(element)











