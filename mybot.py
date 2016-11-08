# coding: utf-8
from __future__ import unicode_literals
from flask import Flask, render_template, request
from flask import jsonify
from INTENTS import getWeather, entities
import datetime
import codecs

app = Flask(__name__, static_url_path="/static")

@app.route('/message', methods=['POST'])
def reply():
    userSay = request.form['msg']
    _, ent = entities.disintegrate(userSay ,['DATE']) # DAY 단위로만,,,,
    reply = getWeather.getWeather(ent)
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