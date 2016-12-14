#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, jsonify, redirect, url_for
from model import db
from model import Connection
import util

app = Flask(__name__)

# Connect to MySQL DB
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'cushion'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'hideking_user'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'hideking'
# app.config['MYSQL_DATABASE_DB'] = 'hideking_arduinoinfo'
# app.config['MYSQL_DATABASE_HOST'] = 'mysql1.php.xdomain.ne.jp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' \
                                        + app.config['MYSQL_DATABASE_USER'] + ':' \
                                        + app.config['MYSQL_DATABASE_PASSWORD'] + '@' \
                                        + app.config['MYSQL_DATABASE_HOST'] + '/' + app.config['MYSQL_DATABASE_DB']
db.init_app(app)


@app.route('/')
def index():
    connection_list = Connection.query.order_by(Connection.id)
    item_list = list()
    for item in connection_list:
        if item is None:
            continue
        data = {}
        latest_date = util.get_latest_date(item.id)
        data["id"] = item.id
        data["name"] = item.name
        data["status"] = util.is_active(latest_date)
        data["connected_name"] = Connection.query.filter_by(connect=item.id).first().name
        data["connected_id"] = item.connect
        data["latest_date"] = latest_date
        item_list.append(data)
    return render_template("content/index.html", item_list=item_list, connection_list=Connection.query.all())


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


@app.route('/api/change_connection_pair', methods=['POST'])
def change_connection_pair():
    connection = Connection.query.filter_by(id=1).first()
    connection.connect = 3
    db.session.add(connection)
    db.session.commit()

    target_connection = Connection.query.filter_by(id=3).first()
    target_connection.connect = 1
    db.session.add(target_connection)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)
