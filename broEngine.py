# coding: utf-8
from __future__ import unicode_literals
from flask import Flask, render_template, request
from flask import jsonify
from brobot import respond

app = Flask(__name__, static_url_path="/static")


@app.route('/message', methods=['POST'])
def reply():
    userSay = request.form['msg']
    reply = respond(userSay)

    return jsonify( { 'text':  reply} )



@app.route("/")
def index():
    return render_template("index.html")




if (__name__ == "__main__"):
    app.run(port = 5001)