#!/usr/bin/python3

import unicodedata
from datetime import datetime
import re
from pyarabic import araby

BASE_URL = "https://www.chambredesrepresentants.ma"

def arabic_strip_all(s):
    araby.strip_tatweel(s)
    araby.strip_tashkeel(s)
    return s.lstrip().rstrip()

def arabic_string_eq(s1, s2):
    s1 = arabic_strip_all(s1)
    s2 = arabic_strip_all(s2)

    return unicodedata.normalize('NFKD', s1).casefold() == unicodedata.normalize('NFKD', s2).casefold()

def arabic_month_to_number(m):
    if arabic_string_eq(m, 'يناير'):
        return 1
    elif arabic_string_eq(m, 'فبراير'):
        return 2
    elif arabic_string_eq(m, 'مارس'):
        return 3
    elif arabic_string_eq(m, 'أبريل'):
        return 4
    elif arabic_string_eq(m, 'ماي'):
        return 5
    elif arabic_string_eq(m, 'يونيو'):
        return 6
    elif arabic_string_eq(m, 'يوليوز'):
        return 7
    elif arabic_string_eq(m, 'غشت'):
        return 8
    elif arabic_string_eq(m, 'شتمبر'):
        return 9
    elif arabic_string_eq(m, 'أكتوبر'):
        return 10
    elif arabic_string_eq(m, 'نونبر'):
        return 11
    elif arabic_string_eq(m, 'دجنبر'):
        return 12
    else:
        print("Unrecognized m: %s" % m)
        return -1

def format_raw_date_to_isoformat(str):
    """
    Example: الجمعة 11 غشت 2017 -> 2017-08-11T00:00:00
    """
    p = re.compile('(\w+) (\d+) (\w+) (\d+)')
    r = p.match(str)
    if r:
        d = int(r.group(2))
        m = arabic_month_to_number(r.group(3))
        y = int(r.group(4))
        dt =  datetime.strptime("%d/%d/%d" % (d, m, y), "%d/%m/%Y")
        return dt.isoformat()

    return ''

