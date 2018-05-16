# coding: utf-8
from __future__ import unicode_literals
import pickle
import datetime
import random

import konlpy
from konlpy.utils import pprint

import re

def disintegrate(disintegrated_sentence, sentence, needThese):
    """sentence는 input문장, needThese 그 Intent에서 필요하는 ENTITIES 리스트"""
    #disintegrated_sentence = konlpy.tag.Twitter().pos(sentence, norm=True, stem=True)
    result = []
    entities = {}
    numflag = 0 # 1 7 30
    # needThese에 명시된 엔터티 딕셔너리 불러오기
    # entities 검사기는 needThese에 따라 on/off 하듯이?
    for w, t in disintegrated_sentence: 
        numflag, entities = ent_date(w,t,numflag,entities,sentence) #임시
        entities = ent_location(w, t, entities, sentence)  # 임시
        
        if t not in ['Eomi', 'Josa', 'Number', 'KoreanParticle', 'Punctuation']:            
            result.append(w) 
    
    return ' '.join(result), entities


def ent_date(w,t,numflag,entities,sentence):

    nday = re.compile('[가-힣\s\d]+일')
    nweek = re.compile('[가-힣\s\d]+주')
    nmonth = re.compile('[가-힣\s\d]+달')
    ndate = re.compile('[가-힣\s\d]+월 [가-힣\s\d]+일')
    TIME={'지금':0, '오늘':0, '어제':-1,'내일':1,'내일모레':2,'모레':2,'그저께':-2}

    if (t == 'Noun') & (w in TIME.keys()):
            entities['DATE'] = TIME[w]

    if (t == 'Number'):
        if(ndate.match(sentence)!= None):
            findMonth = re.compile('[\d]+월')
            findDay = re.compile('[\d]일')
            month = findMonth.findall(sentence)[0][:-1]
            day = findDay.findall(sentence)[0][:-1]
            timevalue = datetime.date.today()-datetime.date.today().replace(month=int(month),day=int(day))
            if datetime.date.today() > datetime.date.today().replace(month=int(month),day=int(day)):
                entities['DATE'] = timevalue.days*-1
            else: entities['DATE'] = timevalue.days
        elif(nday.match(sentence) != None):
            numflag = 1
            findDay = re.compile('[\d]+일')
            day = findDay.findall(sentence)[0][:-1]
            entities['DATE'] = numflag*int(day)
        elif(nweek.match(sentence) != None):
            numflag = 7
            findWeek = re.compile('[\d]+주')
            week = findWeek.findall(sentence)[0][:-1]
            entities['DATE'] = numflag*int(week)
        elif(nmonth.match(sentence) != None):
            numflag = 30
            findMonth = re.compile('[\d]+달')
            month = findMonth.findall(sentence)[0][:-1]
            entities['DATE'] = numflag*int(month)
        else: entities['DATE'] = 0

    if w =='저번':
        if (re.compile('저번주').match(sentence) != None) | (re.compile('저번 주').match(sentence) != None): entities['DATE'] = -7
        elif (re.compile('저번달').match(sentence) != None) | (re.compile('저번 달').match(sentence) != None): entities['DATE'] = -30

    if (w=='다음주'): entities['DATE'] = 7

    if (w =='다음') | (w=='담다'):
        # special token
        if  (re.compile('다음 주').match(sentence) != None): entities['DATE'] = 7
        elif (re.compile('담주').match(sentence) != None): entities['DATE'] = 7
        elif (re.compile('담달').match(sentence) != None): entities['DATE'] = 30
        elif (re.compile('다음달').match(sentence) != None) | (re.compile('다음 달').match(sentence) != None): entities['DATE'] = 30

    if w =='이번':
        # special token
        if (re.compile('이번주').match(sentence) != None) | (re.compile('이번 주').match(sentence) != None): entities['DATE'] = 'WEEK'
        elif (re.compile('저번달').match(sentence) != None) | (re.compile('저번 달').match(sentence) != None): entities['DATE'] = 'MONTH'


    if (numflag>0) & (w == '전'):
        entities['DATE'] = entities['DATE']*-1

    return numflag, entities


def ent_location(w, t, entities, sentence):
    CITY = {'서울', '대전', '대구', '부산', '광주', '용인', '수원', '청주'}
    PROVINCE = {'경기도', '충청북도', '충청남도', '강원도', '경상북도', '경상남도', '전라북도', '전라남도'}

    if (t == 'Noun'):
        if w in CITY or w in PROVINCE:
            entities['LOCATION'] = w
            print('ent_location - w : %s' % w)

    return entities