# coding: utf-8
from __future__ import unicode_literals
from flask import Flask, render_template, request
from flask import jsonify
from INTENTS import getWeather, entities
import datetime
import codecs
import pickle
import re
import random
from initStack import initStack

initStack()

app = Flask(__name__, static_url_path="/static")
f = open("ENTITIES/stack.txt", 'rb')
stack = pickle.load(f)




def greeting():
    GREETING_RESPONSES = ["ㅎㅇ", "하이~~","안뇽하세요~"]
    return random.choice(GREETING_RESPONSES)
    


@app.route('/message', methods=['POST'])
def reply():
    intent = 0
    userSay = request.form['msg']
    
        # Sentences we'll respond with if the user greeted us
    GREETING_KEYWORDS = ("ㅎㅇ", "하이", "안녕", "안뇽", "하잉", 
                     "하이여","하이요","하이하이", "안녕하세요",)
    words = re.sub("[^['가-힣']]", " ",  userSay).split()
    for word in words:
        if word.lower() in GREETING_KEYWORDS:
            intent = 1
            
    # 먼저 Intent 분석 후
    # 필요 엔티티 리스트 정의, 현재는 그냥 ['DATE']
    
    if intent == 1:
        reply = greeting()
    
    else:
    
        if stack['prompt'] == True:
            # 되묻기가 트루인 경우
            # 의미있는 답변인지 체크 후
            # 의미 있다면 stack에 채워넣고
            stack['LOCATION'] = userSay
            stack['prompt'] = False
            with open("ENTITIES/stack.txt", 'wb') as f:
                pickle.dump(stack, f, protocol=0)
            ent = stack

        else:
            _, ent = entities.disintegrate(userSay,['DATE']) 
            # 필요 엔티티에 관련된 스택 업데이트
            if 'DATE' in ent.keys():
                stack['DATE'] = ent['DATE']

            with open("ENTITIES/stack.txt", 'wb') as f:
                pickle.dump(stack, f, protocol=0)

        reply = getWeather.getWeather(ent,stack)
        

        if reply[:2] == 'ER':
            stack['prompt'] = True
            with open("ENTITIES/stack.txt", 'wb') as f:
                pickle.dump(stack, f, protocol=0)

            reply = getWeather.prompt(reply[2:])
    
    today = datetime.datetime.now()
    
    with codecs.open('log/chats.txt', 'a', encoding='utf-8') as f:
        f.write(str(today)+ '\'s chats\n')
        f.write('User says : ' + userSay + '\n')
        f.write('Bot  says : ' + reply + '\n')
        
    return jsonify( { 'text':  reply} )



@app.route("/")
def index():
    return render_template("index.html")




if (__name__ == "__main__"):
    app.run(port = 5001)