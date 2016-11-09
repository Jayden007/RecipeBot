#coding: utf-8
from __future__ import unicode_literals
import os
import pickle
import time
import datetime
from entities import disintegrate, ent_date
from konlpy.utils import pprint
import random
import sys
import math
from xml.dom import minidom
import urllib
import json
import urllib2

def prompt(entType):
    """필요한 entities를 물어보기 위한 프롬프트 질문"""
    if entType == 'LOCATION':
        templates = ['어디요?', '위치를 말씀해주세요!', '위치는요?']
        promptMessage = random.choice(templates)

        # 이 result를 보내고 답이 올 때까지 대기한다?
        # 그렇다면 이 대답을 기다릴 때는 IntentClassifier 안거치고 일로 바로 오도록 해야하네?
        
# 엔티티 객체가 아니라면 대답인걸로 간주! (stack 메모리 뒤져서 일로 답을 보낸다)

        
    
    return promptMessage

def gridxy(location):
    location = urllib.pathname2url(location.encode('utf8'))

    url =  "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address=" + location

    data = urllib2.urlopen(url)
    jsonx = json.loads(data.read())
    
    try:
        latitude = jsonx["results"][0]["geometry"]["location"]["lat"]
        longitude = jsonx["results"][0]["geometry"]["location"]["lng"]
    except:
        latitude = 'ERROR'
        longitude = 'ERROR'
    
    return latitude, longitude


RE = 6371.00877 # 지구 반경(km)
GRID = 5.0 # 격자 간격(km)
SLAT1 = 30.0 # 투영 위도1(degree)
SLAT2 = 60.0 # 투영 위도2(degree)
OLON = 126.0 # 기준점 경도(degree)
OLAT = 38.0 # 기준점 위도(degree)
XO = 43 # 기준점 X좌표(GRID)
YO = 136 # 기준점 Y좌표(GRID)
DEGRAD = math.pi / 180.0
RADDEG = 180.0 / math.pi
re = RE / GRID
slat1 = SLAT1 * DEGRAD
slat2 = SLAT2 * DEGRAD
olon = OLON * DEGRAD
olat = OLAT * DEGRAD
sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
sf = math.pow(sf, sn) * math.cos(slat1) / sn
ro = math.tan(math.pi * 0.25 + olat * 0.5)
ro = re * sf / math.pow(ro, sn)
rs = {}

def dfs_xy2ll(x, y):
    rs['x'] = x
    rs['y'] = y
    xn = x - XO
    yn = ro - y + YO
    ra = math.sqrt(xn * xn + yn * yn)
    if (sn < 0.0): ra = -ra
    alat = math.pow((re * sf / ra), (1.0 / sn))
    alat = 2.0 * math.atan(alat) - math.pi * 0.5
     
    if (math.abs(xn) <= 0.0):
        theta = 0.0;
    else:
        if (math.abs(yn) <= 0.0):
            theta = math.pi * 0.5
            if (xn < 0.0): theta =  -theta
        else:
            theta = math.atan2(xn, yn)

    alon = theta / sn + olon
    rs['lat'] = alat * RADDEG
    rs['lng'] = alon * RADDEG
    return rs

def dfs_ll2xy(lat, lon):
    rs['lat'] = lat
    rs['lng'] = lon
    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)
    theta = lon * DEGRAD - olon
    if (theta > math.pi): theta -= 2.0 * math.pi
    if (theta < -math.pi): theta += 2.0 * math.pi
    theta *= sn
    rs['x'] = int(math.floor(ra * math.sin(theta) + XO + 0.5))
    rs['y'] = int(math.floor(ro - ra * math.cos(theta) + YO + 0.5))
    return rs

def parseWeather(lat, lon):
    base_url = "http://www.kma.go.kr/wid/queryDFS.jsp"
    rsd = dfs_ll2xy(lat, lon)
    url = base_url + '?gridx=' + str(rsd['x']) + '&gridy=' + str(rsd['y'])
    u = urllib2.urlopen(url)
    wdata = []
    try:
        data = u.read()
        dom = minidom.parseString(data)
        items = dom.getElementsByTagName("data")
        for item in items:
            hour = item.getElementsByTagName("hour")[0]   # 시간 3시간 단위
            day = item.getElementsByTagName("day")[0]     # 번째날
            temp = item.getElementsByTagName("temp")[0]   # 온도
            sky = item.getElementsByTagName("sky")[0]     # 하늘상태코드
            pty = item.getElementsByTagName("pty")[0]     # 강수상태코드
            wfKor = item.getElementsByTagName("wfKor")[0] # 날씨
            pop = item.getElementsByTagName("pop")[0]     # 강수확률%

            wdata.append([ hour.firstChild.data.strip(), \
                day.firstChild.data.strip(), \
                temp.firstChild.data.strip(), \
                sky.firstChild.data.strip(), \
                pty.firstChild.data.strip(), \
                wfKor.firstChild.data.strip(), \
                pop.firstChild.data.strip() ])
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]

    return wdata

def getWeather(entities,stack,location='',_date=datetime.datetime.now()):
    """필요 ENTITIES : Location, DATE"""
    
    if stack['DATE'] != 0:
        temp_date = stack['DATE']
    
    elif 'DATE' in entities.keys():
        temp_date = entities['DATE']
    
    if stack['LOCATION'] != None:
        location = stack['LOCATION']
    
    elif 'LOCATION' in entities.keys():
        location = entities['LOCATION']
        
    else:
        return 'ERLOCATION'
       # location = '수지구' # 쓰레드의 조인 기능? 그런거 이용해야 하나... 어떻게 하지
        # 로케를 입력받아 정확히 입력받았는지 확인하는 과정 필요
        # 만약 로케가 아니라면 다시 되 물어야 할듯,,,? prompt 함수에 되묻기 옵션으로!
        # 계속 엉뚱한 대답해대면 예를 들어 3번동안, 모르겠다고 출력하고 종료
        
    gridX, gridY = gridxy(location)
    if gridX =='ERROR': return '그곳이 어디죠..?'
    else: 
        weather = parseWeather(gridX,gridY)

    try: 
        int(temp_date)
        if temp_date > 0: 
            _date+=datetime.timedelta(days=temp_date)
            if temp_date == 1:
                weather = [x for x in weather if x[1]=='1']
            elif temp_date >= 2:
                weather = [x for x in weather if x[1]=='2']
                
        else: 
            _date-=datetime.timedelta(days=abs(temp_date))
             #   weather = weather[0]
    except:
        "아직 구현 안됌.. 특정 기간동안의 날씨"
        
    templates=["%s의 %s 날씨는 %s이고 기온은 %s, 강수확률은 %s 퍼센트 입니다."] # 이것도 구현 필요(날씨 api)
        
    result = random.choice(templates)

    return result % (location, _date.strftime('%Y-%m-%d'),weather[0][5], weather[0][2], weather[0][6])