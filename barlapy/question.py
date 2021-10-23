#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re
from pyarabic import araby

from utils import format_raw_date_to_isoformat, arabic_string_eq

class Question:
    def __init__(self, id = None, page_url = None, qtype = None, topic = None, 
                qdate = None, qtext = None, authors = None, status = None, 
                answer_date = None, answer_url = None, designated_min = None):
        self.id = id
        self.page_url = page_url
        self.qtype = qtype
        self.topic = topic
        self.qdate = qdate
        self.qtext = qtext
        self.authors = authors or []
        self.status = status
        self.answer_date = answer_date
        self.answer_url = answer_url
        self.min = designated_min
        self.legislature = '2016-2021'

    @staticmethod
    def from_url(url):
        """ Initialize a Question (written or oral) from its public URL
        e.g.: https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9/%D8%A7%D9%86%D8%AA%D8%B4%D8%A7%D8%B1-%D8%A7%D9%84%D8%AD%D8%B4%D8%B1%D8%A9-%D8%A7%D9%84%D9%82%D8%B1%D9%85%D8%B2%D9%8A%D8%A9-%D8%A8%D9%86%D8%A8%D8%A7%D8%AA-%D8%A7%D9%84%D8%B5%D8%A8%D8%A7%D8%B1
        Note: only the arabic version is currently supported."""

        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')

        try:
            # Note : strip_tatweel below is mandatory, it took me several hours of scratching
            title = araby.strip_tatweel(s.find_all('h1', class_='section-title title-global lang_ar')[0].text)
            title.lstrip().rstrip()

            qtype = 'undefined'
            if arabic_string_eq(title, "الأسئلة الكتابية"):
                qtype = 'written'
            elif arabic_string_eq(title, "الأسئلة الشفوية"):
                qtype = 'oral'

            spans = s.find_all(class_='q-b1-1')[0].find_all('span')
            status = 'unknown'
            if 'q-st-red' in spans[4]['class']:
                status = 'unanswered'
            elif 'q-st-green' in spans[4]['class']:
                status = 'answered'

            if status == 'unanswered':
                content = s.find_all(class_='q-block1-na')[0]
            elif status == 'answered':
                content = s.find_all(class_='q-block1')[0]
            else:
                raise ValueError("Malformed HTML")

            qb11 = content.find_all(class_='q-b1-1')[0].find_all('span')

            # XXX How do we handle RE faulty cases ?
            p = re.compile('رقم السؤال : ([0-9]+)')
            res = p.match(qb11[0].text.lstrip().rstrip())
            id = int(res.group(1))

            p = re.compile('الموضوع : (.*)')
            res = p.match(qb11[1].text.lstrip().rstrip())
            topic = res.group(1)

            answer_date_raw = ''
            if arabic_string_eq(qb11[2].text.split(':')[0].lstrip().rstrip(), 'تاريخ الجواب'):
                answer_date_raw = qb11[3].text.lstrip().rstrip()
            answer_date = format_raw_date_to_isoformat(answer_date_raw)
            
            qb12 = content.find_all(class_='q-b1-2 row')[0]
            team = qb12.find_all(class_='col-md-5')[0].find_all('a')[0].text
            questioners = []
            for q in qb12.find_all(class_='col-md-7')[0].find_all(class_='q-b1-2-s-item'):
                questioners.append(q.find_all(class_='q-name')[0].find('a').text.lstrip().rstrip())

            qb13 = content.find_all(class_='q-b1-3')[0]

            offset = 0
            designated_ministry = ''
            # XXX : are there cases where there are multiple ministries involved?
            if arabic_string_eq(qb13.find_all('div')[0].text.split(':')[0].lstrip().rstrip(), 'الوزارة المختصة'):
                designated_ministry = qb13.find_all('div')[0].text.split(':')[1].replace('\n', '').lstrip().rstrip()
                offset = 1

            question_date_raw = ''
            question_text = ''
            if qtype == "written":
                if arabic_string_eq(qb13.find_all('div')[offset].text.split(':')[0].lstrip().rstrip(), 'تاريخ السؤال'):
                    question_date_raw = qb13.find_all('div')[offset].text.split(':')[1].replace('\n', '').lstrip().rstrip()

                if arabic_string_eq(qb13.find_all('div')[offset + 1].text.split(':')[0].lstrip().rstrip(), 'السؤال'):
                    question_text = qb13.find_all('div')[offset + 1].find('p').text.lstrip().rstrip()
            elif qtype == "oral":
                # TODO: check if  there are cases where the date is given
                if arabic_string_eq(qb13.find_all('div')[offset].text.split(':')[0].lstrip().rstrip(), 'السؤال'):
                    question_text = qb13.find_all('div')[offset].find('p').text.lstrip().rstrip()

            question_date = format_raw_date_to_isoformat(question_date_raw)

            answer_doc = ''
            answer_content = s.find_all(class_='q-block2')
            if answer_content != []:
                answer_doc = answer_content[0].find_all('a', href=True)[0]['href']

            q = Question(id,
                         url,
                         qtype,
                         topic,
                         question_date,
                         question_text,
                         questioners,
                         status,
                         answer_date,
                         answer_doc,
                         designated_ministry)
            return q

        except Exception as e:
            print('There was an exception: %s' % e)
            return None

    def get_id(self):
        return self.id

    def get_text(self):
        return self.qtext

    def get_url(self):
        return self.page_url

    def get_authors(self):
        return self.authors

    def get_type(self):
        return self.qtype

    def get_answer(self):
        return {"url": self.answer_url, "date": self.answer_date}

    def get_date(self):
        return self.qdate

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.page_url,
            'type': self.qtype,
            'topic': self.topic,
            'date': self.qdate,
            'text': self.qtext,
            'authors': self.authors,
            'status': self.status,
            'answer': {
                'date': self.answer_date,
                'url': self.answer_url
            } if self.status == 'answered' else {},
            'ministry': self.min,
            'legislature': self.legislature
        }

