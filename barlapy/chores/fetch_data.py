#!/usr/bin/python3

# Collect data (questions, MP profiles) from website and dump the results to a json file

import datetime
import json

from mp import MP
from question import Question
from parser import parse_questions_in_page, parse_all_mps

def populate_questions(type, f):
    if type == 'w':
        page = 666
        url = "https://www.chambredesrepresentants.ma/ar/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D9%83%D8%AA%D8%A7%D8%A8%D9%8A%D8%A9"
    else:
        page = 936
        url = "https://www.chambredesrepresentants.ma/ar/%D9%85%D8%B1%D8%A7%D9%82%D8%A8%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%88%D9%85%D9%8A/%D8%A7%D9%84%D8%A3%D8%B3%D9%80%D8%A6%D9%84%D8%A9-%D8%A7%D9%84%D8%B4%D9%81%D9%88%D9%8A%D8%A9"

    url += "?page="
    try: 
        with open(f, 'w') as outf:
            questions = []
            outf.write('[')
            while not page < 0:
                u = url + str(page)
                questions = parse_questions_in_page(u)
                for q in questions:
                    d = q.to_dict()
                    d['updated_at'] = datetime.datetime.now().isoformat()

                    json.dump(d, outf)

                    if not (page == 0 and q == questions[len(questions) - 1]):
                        outf.write(',')
                page -= 1
            outf.write(']')
            outf.close()
    except Exception as e:
        print('Exception: ', e)


def populate_mps(f):
    mps = parse_all_mps()
    print('MPs parsed')
    try:
        with open(f, 'w') as outf:
            outf.write('[')
            for mp in mps:
                d = mp.to_dict()
                d['updated_at'] =  datetime.datetime.now().isoformat()

                json.dump(d, outf)

                if not mp == mps[len(mps) - 1]:
                    outf.write(',')
            outf.write(']')
            outf.close()

    except Exception as e:
        print("Exception: ", e)
