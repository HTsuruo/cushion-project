#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template
from model import db
from model import Connection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hideking_user:hideking@mysql1.php.xdomain.ne.jp/hideking_arduinoinfo'
db.init_app(app)

@app.route('/')
def index():
    c = Connection.query.first()
    return render_template("content/index.html", data=c)

@app.route('/index2')
def index2():
    return render_template("content/index2.html")

@app.route('/index3')
def index3():
    return render_template("content/index3.html")

@app.route('/hello/<name>')
def hello(name):
    if name == '':
        name = '名無しさん'
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)