#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

from barlapy.utils import BASE_URL
from barlapy.question import Question
from barlapy.mp import MP

def parse_all_mps(legislature="2021-2026"):
    index_url = BASE_URL + "/ar/%D8%AF%D9%84%D9%8A%D9%84-%D8%A3%D8%B9%D8%B6%D8%A7%D8%A1-%D9%85%D8%AC%D9%84%D8%B3-%D8%A7%D9%84%D9%86%D9%88%D8%A7%D8%A8/%s?page=" % legislature

    mps = []
    page = 0
    while True:
        url = index_url + str(page)
        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        results = s.find_all(class_='f-result-list row')[0].find_all(class_='col-sm-6 col-lg-3 mb-5')

        for result in results:
            profile_url = BASE_URL + result.find_all('a', href=True)[0]['href']
            mp = MP.from_url(profile_url)
            mps.append(mp)

        if s.find_all('li', class_='next') == []:
            break

        page += 1
    return mps

def parse_questions_in_page(url):
    res = []
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')

    for elt in s.find_all(class_='q-block3'):
        q = Question.from_url(BASE_URL + elt.find_all('a', href=True)[0]['href'])
        if q:
            res.append(q)
    return res

# TODO : refactor, use parse_questions_in page
def parse_all_written_q():
    index_url = BASE_URL + "/ar/الأسـئلة-الكتابية?page="

    res = []
    page = 0
    while True:
        url = index_url + str(page)
        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        results = s.find_all(class_='q-block3')
        for result in results:
            question_url = BASE_URL + result.find_all('a', href=True)[0]['href']
            q = Question.from_url(question_url)
            if q:
                res.append(q)

        if s.find_all('li', class_='next') == []:
            break

        page += 1
    return res
