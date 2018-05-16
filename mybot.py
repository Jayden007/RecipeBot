# coding: utf-8
from __future__ import unicode_literals
from flask import Flask, render_template, request
from flask import jsonify
from flask import Response
from INTENTS import getWeather, getMovie, entities
import datetime
import codecs
import pickle
import re
import random
from initStack import initStack

import time
import konlpy

# for no-cache
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

# for context processor
import os

initStack()

app = Flask(__name__, static_url_path="/static")
f = open("ENTITIES/stack.txt", 'rb')
stack = pickle.load(f)

from gtts import gTTS
from io import BytesIO

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)

        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            print("url_for filename : %s %s",app.root_path, file_path)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


def greeting():
    GREETING_RESPONSES = ["안녕", "하이~~","안녕하세요~"]
    return random.choice(GREETING_RESPONSES)

@app.route('/message', methods=['POST'])
def reply():
    intent = 0
    userSay = request.form['msg']

        # Sentences we'll respond with if the user greeted us
    GREETING_KEYWORDS = ("하이", "안녕", "안뇽", "하잉",
                     "하이여","하이요","하이하이", "안녕하세요",)
    WEATHER_KEYWORDS = ("날씨", "예보", "기상")
    MOVIE_KEYWORDS = ("영화", "무비", "movie", "cinema")

    #words = re.sub("[^['가-힣']]", " ",  userSay).split()
    disintegrated_sentence = konlpy.tag.Twitter().pos(userSay, norm=True, stem=True)
    for word, t in disintegrated_sentence:
        if word.lower() in GREETING_KEYWORDS:
            intent = 1
        elif word.lower() in WEATHER_KEYWORDS:
            intent = 2
        elif word.lower() in MOVIE_KEYWORDS:
            intent = 3
            
    # 먼저 Intent 분석 후
    # 필요 엔티티 리스트 정의, 현재는 그냥 ['DATE']
    
    if intent == 1:
        reply = greeting()
    
    else:
    
        if stack['prompt'] > 0:
            # 되묻기가 트루인 경우
            # 의미있는 답변인지 체크 후
            # 의미 있다면 stack에 채워넣고
            stack['LOCATION'] = userSay
            intent = stack['prompt']

            stack['prompt'] = 0
            with open("ENTITIES/stack.txt", 'wb') as f:
                pickle.dump(stack, f, protocol=0)
            ent = stack

        else:
            _, ent = entities.disintegrate(disintegrated_sentence, userSay,['DATE'])
            # 필요 엔티티에 관련된 스택 업데이트
            if 'DATE' in ent.keys():
                stack['DATE'] = ent['DATE']

            with open("ENTITIES/stack.txt", 'wb') as f:
                pickle.dump(stack, f, protocol=0)

        if intent == 2: # Weather
            reply = getWeather.getWeather(ent,stack)

            if reply[:2] == 'ER':
                stack['prompt'] = True
                with open("ENTITIES/stack.txt", 'wb') as f:
                    pickle.dump(stack, f, protocol=0)

                print("reply is ER!")

                reply = getWeather.prompt(reply[2:])
            # add non response on error(?) - 처리하기 intent 없는 경우만
        
        elif intent == 3:  # Movie
            reply = getMovie.getMovie(ent, stack)

            if reply[:2] == 'ER':
                stack['prompt'] = intent
                with open("ENTITIES/stack.txt", 'wb') as f:
                    pickle.dump(stack, f, protocol=0)

                print("reply is ER!")

                reply = getMovie.prompt(reply[2:])
        else:
            print("intent is not correct!!!!")

            NONE_RESPONSES = [
                "네..?",
                "잘 모르겠어요.",
                "흠, 그렇군요.",
                "아하!",
                "몰라요 ㅠㅠ",
            ]
            reply = random.choice(NONE_RESPONSES)
            
    today = datetime.now()
    
    with codecs.open('log/chats.txt', 'a', encoding='utf-8') as f:
        f.write(str(today)+ '\'s chats\n')
        f.write('User says : ' + userSay + '\n')
        f.write('Bot  says : ' + reply + '\n')
        
    return jsonify( { 'text':  reply} )



@app.route("/")
def index():
    return render_template("index.html")




if (__name__ == "__main__"):
    app.debug = True
    app.run(host='localhost', port = 8000)
