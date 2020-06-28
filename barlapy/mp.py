#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

from utils import BASE_URL
from question import Question

def parse_mp_questions(url):
    url = url + "?page="
    
    questions = []
    page = 0
    while True:
        u = url + str(page)
        r = requests.get(u)
        s = BeautifulSoup(r.text, 'html.parser')

        for elt in s.find_all(class_='q-block3'):
            question_url = BASE_URL + elt.find_all('a', href=True)[0]['href']
            q = Question.from_url(question_url)
            if q:
                questions.append(q)

        if s.find_all('li', class_='next') == []:
            break
        page += 1

    return questions

class MP:
    def __init__(self, url = None, name = None, image = None, party = None, team = None, district = None,
                 legislature = None, questions = None, law_props = None, missions = None, media = None):
        self.profile = url
        self.name = name
        self.image = image
        self.party = party
        self.team = team
        self.district = district
        self.legislature = legislature
        self.questions = questions or []
        self.law_props = law_props or []
        self.missions = missions or []
        self.media = media or []

    @staticmethod
    def from_url(url, parse_questions = False):
        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        try:
            image = s.find_all(class_='mhr-b1_img-wrp')[0].find('img')['src']

            info = s.find_all(class_='mhr-b1_info')[0]
            name = info.find_all(class_='section-title')[0].text.split(':')[1].lstrip().rstrip()

            subinfo = s.find_all(class_='mhr-b1_info-in')[0].find_all(class_='mhr-b1-info-l')[0].find_all('div')
            subinfo += s.find_all(class_='mhr-b1_info-in')[0].find_all(class_='mhr-b1-info-r')[0].find_all('div')

            party = ''
            team = ''
            district = ''
            legislature = ''
            for _ in subinfo:
                _ = _.text

                title = _.split(':')[0].lstrip().rstrip()

                if title == 'الحزب':
                    party = _.split(':')[1].lstrip().rstrip()
                if title == 'الفريق أو المجموعة':
                    team = _.split(':')[1].lstrip().rstrip()
                if title == 'الدائرة الإنتخابية':
                    district = _.split(':')[1].lstrip().rstrip()
                if title == 'الولاية التشريعية':
                    legislature = _.split(':')[1].lstrip().rstrip()

            q_slider = BASE_URL + s.find('a', class_='see-more-btn')['href']

            if parse_questions:
                mp_questions = parse_mp_questions(q_slider)
            else:
                mp_questions = None

            mp = MP(url,
                    name,
                    image,
                    party,
                    team,
                    district,
                    legislature,
                    mp_questions)

            # TODO : check for previous mandate button
            # TODO : parse media

            return mp

        # The only 'known-of' exception occurs when parsing the president's profile page,
        # which is not a standard MP profile page
        except Exception as e:
            print("There was an exception: %s" % e)
            return None

    def to_dict(self):
        return {
            'profile': self.profile,
            'name': self.name,
            'image': self.image,
            'party': self.party,
            'team': self.team,
            'district': self.district,
            'legislature': self.legislature
        }

    def __str__(self):
        return self.to_dict()

