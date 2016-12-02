#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template
from model import db
from model import Connection

app = Flask(__name__)

# Connect to MySQL DB
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'cushion'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' \
                                        + app.config['MYSQL_DATABASE_USER'] + ':' \
                                        + app.config['MYSQL_DATABASE_PASSWORD'] + '@' \
                                        + app.config['MYSQL_DATABASE_HOST'] + '/' + app.config['MYSQL_DATABASE_DB']
db.init_app(app)


@app.route('/')
def index():
    connectionList = Connection.query.order_by(Connection.id)
    itemList = list()
    for item in connectionList:
        data = {}
        data["name"] = item.name
        data["state"] = 0
        # data["connectedName"] = Connection.query.filter_by(Connection.connect == item.id).name
        data["latestDate"] = 'hgoe'
        itemList.append(data)
    return render_template("content/index.html", itemList=itemList)


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
