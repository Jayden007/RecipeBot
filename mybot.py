# coding: utf-8
from __future__ import unicode_literals
from flask import Flask, render_template, request
from flask import jsonify
from INTENTS import getWeather, entities
import datetime
import codecs
import pickle

app = Flask(__name__, static_url_path="/static")
f = open("ENTITIES/stack.txt", 'rb')
stack = pickle.load(f)



@app.route('/message', methods=['POST'])
def reply():
    userSay = request.form['msg']
    
    # 먼저 Intent 분석 후
    # 필요 엔티티 리스트 정의, 현재는 그냥 ['DATE']
    
    if stack['prompt'] == True:
        # 되묻기가 트루인 경우
        # 의미있는 답변인지 체크 후
        # 의미 있다면 stack에 채워넣고
        stack['LOCATION'] = userSay
        stack['prompt'] = False
        ent = stack
      
    else:
        _, ent = entities.disintegrate(userSay,['DATE']) 
        # 필요 엔티티에 관련된 스택 업데이트
        if 'DATE' in ent.keys():
            stack['DATE'] = ent['DATE']
    
    reply = getWeather.getWeather(ent,stack)
    today = datetime.datetime.now()
    
    if reply[:2] == 'ER':
        stack['prompt'] = True
        reply = getWeather.prompt(reply[2:])
            
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