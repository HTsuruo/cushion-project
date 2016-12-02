#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'hideking_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hideking'
app.config['MYSQL_DATABASE_DB'] = 'hideking_arduinoinfo'
app.config['MYSQL_DATABASE_HOST'] = 'mysql1.php.xdomain.ne.jp'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template("content/index.html")

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