import csv
import urllib.request
from bs4 import BeautifulSoup

department_list = []

def scrape_page(url):
    #specify url
    quote_page = url

    #set page = website html
    page = urllib.request.urlopen(quote_page)

    #set soup = parsed html
    soup = BeautifulSoup(page, 'html.parser')

    dep_courses = soup.find('ul', attrs={'class': 'course-feed'})

    output = []
    
    course_list = dep_courses.find_all('li')

    for course in course_list:
        title_and_course_number = course.find('strong')
        if not title_and_course_number:
            continue
        title_and_course_number_split = title_and_course_number.text.split(' ')
        title_number = int(title_and_course_number_split[2][:-1])
        coursename = ' '.join(title_and_course_number_split[3:])
        print(course.text)
        course_desc = course.text[:course.text.index('<div')]

        output.append((title_number, coursename, course_desc))
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
    'core-curriculum', 'earth-environmenta', 'economics',
    'editorial-studies', 'english', 'first-year-experience',
    'modern-languages-french', 'modern-languages-german',
    'modern-languages-hebrew', 'modern-languages-hindi', 'history',
    'art-history', 'inte rnational-relations', 'internships',
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
    print(scrape_page(quote_url))
    break

