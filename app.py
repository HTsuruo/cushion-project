#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, jsonify, redirect, url_for, request
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
        data["connected_id"] = item.connect
        data["latest_date"] = latest_date
        if Connection.query.filter_by(connect=item.id).first() is not None:
            data["connected_name"] = Connection.query.filter_by(connect=item.id).first().name

        item_list.append(data)
    return render_template("content/index.html", item_list=item_list, connection_list=Connection.query.all())


@app.route('/sensor_data/<cushion_id>')
def sensor_data(cushion_id):
    return render_template("content/sensor_data.html", cushion_id=cushion_id)


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
    id = request.form.get("id")
    connected_id = request.form.get("connected_id")
    if id is None or connected_id is None:
        return

    # 接続先が既に存在する場合は空にします.
    conn_old = Connection.query.filter_by(connect=connected_id).first()
    if conn_old is not None:
        conn_old.connect = None
        db.session.add(conn_old)
        db.session.commit()

    conn = Connection.query.filter_by(id=id).first()
    conn.connect = connected_id
    db.session.add(conn)
    db.session.commit()

    conn_old = Connection.query.filter_by(connect=id).first()
    if conn_old is not None:
        conn_old.connect = None
        db.session.add(conn_old)
        db.session.commit()

    target_conn = Connection.query.filter_by(id=connected_id).first()
    target_conn.connect = id
    db.session.add(target_conn)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/api/cushion/all')
def get_cushion_all():
    conn_list = Connection.query.order_by(Connection.id)
    cushion_list = list()
    for item in conn_list:
        if item is None:
            continue
        data = {}
        data["id"] = item.id
        data["name"] = item.name
        cushion_list.append(data)

    return jsonify(data=cushion_list)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)
