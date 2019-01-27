import csv
import requests
from bs4 import BeautifulSoup

department_list = []

def scrape_page(url):
    #specify url
    quote_page = url

    #set page = website html
    response = requests.get(url)

    #set soup = parsed html
    soup = BeautifulSoup(response.text, 'html.parser')

    dep_courses = soup.find('ul', attrs={'class': 'course-feed'})

    output = []
    
    course_list = dep_courses.find_all('li')

    for course in course_list:
        title_and_course_number = course.find('strong')
        if not title_and_course_number:
            continue
        title_and_course_number_split = title_and_course_number.text.split(' ')
        title_number = int(title_and_course_number_split[2][:-1])
        course_name = ' '.join(title_and_course_number_split[3:])
        
        string_course = str(course)
        desc_start = string_course.find('<br/>')

        string_course = string_course[desc_start + len('<br/>'):]
        next_potential_br = string_course.find('<br/>')
        if next_potential_br:
            string_course = string_course[next_potential_br + len('<br/>'):]

        desc_end = string_course.find('<div class="cf-hub-ind">')
        if desc_end < 0:
            desc_end = string_course.find('</li>')

        course_desc = string_course[desc_start:desc_end].strip().encode('utf-8')
        output.append((title_number, course_name, course_desc))
    return output

BASE_URL = 'http://www.bu.edu/academics/cas/courses'

departments = [
    'computer-science', 'african-american-studies',
    'african-studies-culture-in-english', 'swahili',
    'modern-languages-african-languages-linguistics', 'isixhosa',
    'wolof', 'modern-languages-hausa', 'american-studies',
    'anthropology', 'modern-languages-arabic', 'archaeology',
    'asian-studies', 'astronomy', 'biochemistry-molecular-biology',
    'biology', 'chemistry', 'modern-languages-chinese',
    'cinema-media-studies', 'classical-studies', 'comparative-literature',
    'core-curriculum', 'earth-environment', 'economics',
    'editorial-studies', 'english', 'first-year-experience',
    'modern-languages-french', 'modern-languages-german',
    'modern-languages-hebrew', 'modern-languages-hindi', 'history',
    'art-history', 'international-relations', 'internships',
    'modern-languages-italian', 'modern-languages-japanese',
    'modern-languages-korean', 'modern-languages-linguistics',
    'marine-science', 'mathematics-statistics', 'middle-east-studies',
    'natural-sciences', 'neuroscience', 'modern-languages-persian',
    'philosophy', 'physics', 'political-science',
    'modern-languages-portuguese', 'psychology', 'religion',
    'modern-languages-russian', 'sea-semester', 'senior-year-development',
    'sociology', 'modern-languages-spanish', 'modern-languages-turkish',
    'womens-studies', 'writing'
]

for department in departments:
    quote_url = '{}/{}'.format(BASE_URL, department)
    print(quote_url)
    output_data = scrape_page(quote_url)
    print('Writing {}'.format(department))
    with open('data/{}.csv'.format(department), 'w') as f:
        data_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in output_data:
            department_row = [department]
            data_row = [element for element in row]
            data_writer.writerow(department_row + data_row)









