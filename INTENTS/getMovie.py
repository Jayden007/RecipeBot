#coding: utf-8
from __future__ import unicode_literals
import os
import pickle
import time
import datetime
#from entities import disintegrate, ent_date
from konlpy.utils import pprint
import random
import sys
import math
from xml.dom import minidom
#import urllib
import json
import urllib

import json
import math
from urllib.request import urlopen
#from urllib.parse import urlencode
from datetime import datetime
from datetime import timedelta

def prompt(entType):
    """필요한 entities를 물어보기 위한 프롬프트 질문"""
    if entType == 'LOCATION':
        templates = ['어디요?', '위치를 말씀해주세요!', '위치는요?']
        promptMessage = random.choice(templates)

        # 이 result를 보내고 답이 올 때까지 대기한다?
        # 그렇다면 이 대답을 기다릴 때는 IntentClassifier 안거치고 일로 바로 오도록 해야하네?
        
# 엔티티 객체가 아니라면 대답인걸로 간주! (stack 메모리 뒤져서 일로 답을 보낸다)

        
    
    return promptMessage

class BoxOffice(object):
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/'\
               'searchDailyBoxOfficeList.json'
    def __init__(self, api_key):
        self.api_key = api_key

    def get_movies(self):
        target_dt = datetime.now() - timedelta(days=1)
        target_dt_str = target_dt.strftime('%Y%m%d')
        query_url = '{}?key={}&targetDt={}'.format(self.base_url, self.api_key, target_dt_str)

        fin = urlopen(query_url)
        return json.loads(fin.read().decode('utf-8'))

    def simplify(self, result):
        return [
           {
              'rank': entry.get('rank'),
              'name': entry.get('movieNm'),
              'code': entry.get('movieCd')
           }
           for entry in result.get('boxOfficeResult').get('dailyBoxOfficeList')
        ]

def getMovie(entities,stack,location='',_date=datetime.now()):
    """필요 ENTITIES : Location, DATE"""
    API_KEY = '96c72f19172f1117e343285fc7bdea35'

    if stack['DATE'] != 0:
        temp_date = stack['DATE']
    
    elif 'DATE' in entities.keys():
        temp_date = entities['DATE']

    if 'LOCATION' in entities.keys():
        location = entities['LOCATION']
        stack['LOCATION'] = location

    elif stack['LOCATION'] != None:
        location = stack['LOCATION']

    else:
        print("ERLOCATION!!!!!")
        #return 'ERLOCATION'

    box = BoxOffice(API_KEY)
    movies = box.get_movies()

    movies_simple_list = box.simplify(movies)
    print(movies_simple_list)

    if len(movies_simple_list) < 2:
        return "죄송해요. 영화 정보를 가져오지 못했어요."

    templates=["%s 영화 순위 1위는 %s, 2위는 %s 입니다."]
        
    result = templates[0]

    # format string 한글 입력 시 인코딩 문제로 강제 replace
    date_str = _date.strftime('%Y-%m-%d').replace('-','년 ',1).replace('-','월 ',1) + '일'

    return result % (date_str, movies_simple_list[0]['name'], movies_simple_list[1]['name'])
