#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

from utils import BASE_URL
from question import Question
from parser import parse_mp_questions

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
    def from_url(url):
        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        try:
            image = s.find_all(class_='mhr-b1_img-wrp')[0].find('img')['src']

            info = s.find_all(class_='mhr-b1_info')[0]
            name = info.find_all(class_='section-title')[0].text.split(':')[1].lstrip().rstrip()

            subinfo = s.find_all(class_='mhr-b1_info-in')[0].find_all(class_='mhr-b1-info-l')[0].find_all('div')
            subinfo += s.find_all(class_='mhr-b1_info-in')[0].find_all(class_='mhr-b1-info-r')[0].find_all('div')

            for _ in subinfo:
                _ = _.text

                title = _.split(':')[0].lstrip().rstrip()

                party = ''
                team = ''
                district = ''
                legislature = ''
                if title == 'الحزب':
                    party = _.split(':')[1].lstrip().rstrip() or None
                if title == 'الفريق أو المجموعة':
                    team = _.split(':')[1].lstrip().rstrip() or None
                if title == 'الدائرة الإنتخابية':
                    district = _.split(':')[1].lstrip().rstrip() or None
                if title == 'الولاية التشريعية':
                    legislature = _.split(':')[1].lstrip().rstrip() or None

            q_slider = BASE_URL + s.find('a', class_='see-more-btn')['href']
            mp_questions = parse_mp_questions(q_slider)

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
            'legislature': self.legislature,
            'questions': [q.to_dict() for q in self.questions]
        }

    def __str__(self):
        return self.to_dict()

