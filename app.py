#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, jsonify, redirect, url_for, request, make_response, send_file
from model import *
import util
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Connect to MySQL DB
app.config['MYSQL_DATABASE_USER'] = 'cushion_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cushion'
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
    connection_list = Connections.query.order_by(Connections.id)
    item_list = list()
    for item in connection_list:
        if item is None:
            continue
        data = {}
        latest_date = util.get_latest_date(item.id)
        data["id"] = item.id
        data["name"] = item.name
        data["connected_id"] = item.connected_id

        if latest_date is not None:
            data["status"] = util.is_active(latest_date)
            data["latest_date"] = latest_date
        if Connections.query.filter_by(connected_id=item.id).first() is not None:
            data["connected_name"] = Connections.query.filter_by(connected_id=item.id).first().name

        item_list.append(data)
    return render_template("content/index.html", item_list=item_list, connection_list=Connections.query.all())


@app.route('/sensor_data/<cushion_id>')
def sensor_data(cushion_id):
    sensor_data_list = SensorData.query.filter_by(cushion_id=cushion_id)
    if sensor_data_list is None:
        return
    rand_ids = []
    for data in sensor_data_list:
        rand_ids.append(data.rand_id)
    rand_ids = list(set(rand_ids)) #重複を排除します.

    time_rand_map = {}
    for rand_id in rand_ids:
        data = sensor_data_list.filter_by(rand_id=rand_id)
        data_desc = data.order_by(SensorData.timestamp.desc())
        begin_time = data.first().timestamp
        end_time = data_desc.first().timestamp
        date_str = util.date_formatter(begin_time) + " ~ " + util.date_formatter(end_time) + "（識別子ID: " + str(rand_id) + "）"
        time_rand_map[rand_id] = date_str

    print(time_rand_map)

    return render_template("content/sensor_data.html", cushion_id=cushion_id, time_rand_map=time_rand_map)


@app.route('/csv/<cushion_id>/<rand_id>')
def download_csv(cushion_id, rand_id):
    data_list = SensorData.query.filter_by(cushion_id=cushion_id).filter_by(rand_id=rand_id)

    sensor_1 = pd.Series()
    sensor_2 = pd.Series()
    sensor_3 = pd.Series()
    sensor_4 = pd.Series()
    sensor_5 = pd.Series()
    sensor_6 = pd.Series()
    timestamp = pd.Series()

    for data in data_list:
        sensor_1.set_value(data.id, data.sensor_1),
        sensor_2.set_value(data.id, data.sensor_2),
        sensor_3.set_value(data.id, data.sensor_3),
        sensor_4.set_value(data.id, data.sensor_4),
        sensor_5.set_value(data.id, data.sensor_5),
        sensor_6.set_value(data.id, data.sensor_6),
        timestamp.set_value(data.id, data.timestamp)

    df = pd.DataFrame({
        'sensor_1': sensor_1,
        'sensor_2': sensor_2,
        'sensor_3': sensor_3,
        'sensor_4': sensor_4,
        'sensor_5': sensor_5,
        'sensor_6': sensor_6,
        'timestamp': timestamp
    })

    filename = "C" + cushion_id + "R" + rand_id + "_" + datetime.now().strftime("%Y%m%d")
    res = make_response(df.to_csv())
    res.headers["Content-Disposition"] = "attachment; filename=" + filename + ".csv"
    res.headers["Content-Type"] = "text/csv"
    return res


'''
---↓REST APIとして扱います---
'''


@app.route('/api/get/json/<cushion_id>', methods=['GET'])
def get_data(cushion_id):

    # クエリパラメータを取得します.
    SENSOR_NUM = 6
    sensors = []
    for i in range(SENSOR_NUM):
        sensors.append(request.args.get('sensor_'+str(i+1)))
    randId = request.args.get('randId')

    # DBにデータを書き込みます
    item = SensorData(cushion_id, sensors[0], sensors[1], sensors[2], sensors[3], sensors[4], sensors[5], randId)
    db.session.add(item)

    # キャリブレーションの基準値を取得します.
    base = SensorData.query.filter_by(cushion_id=cushion_id).order_by(SensorData.timestamp).first()

    working_state = 10
    diff = 5

    # DBに作業レベルデータを書き込みます.
    ws_item = WorkingStates(cushion_id, working_state, diff)
    db.session.add(ws_item)
    db.session.commit()

    #ペアリングしているクッションを取得
    # conn = Connections.query.filter_by(id=id).first()
    # if conn is None:
    #     return
    # connected_id = conn.connected_id

    # DBに格納してある自分と相手の最新10個の作業レベルデータを取得します.
    ws_self = 8
    ws_partner = 15

    # for json data.
    data = {}
    data["ws_self"] = ws_self
    data["ws_partner"] = ws_partner

    return jsonify(data=data)


@app.route('/api/data/post', methods=['POST'])
def post_data():
    '''
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400
    '''
    print(request.json)

    item = SensorData(1, 10, 20, 30, 40, 50, 60, 888)
    db.session.add(item)
    db.session.commit()

    return jsonify(res='success')


@app.route('/api/change_connection_pair', methods=['POST'])
def change_connection_pair():
    id = request.form.get("id")
    connected_id = request.form.get("connected_id")
    if id is None or connected_id is None:
        return

    # 接続先が既に存在する場合は空にします.
    conn_old = Connections.query.filter_by(connected_id=connected_id).first()
    if conn_old is not None:
        conn_old.connected_id = None
        db.session.add(conn_old)
        db.session.commit()

    conn = Connections.query.filter_by(id=id).first()
    conn.connected_id = connected_id
    db.session.add(conn)
    db.session.commit()

    conn_old = Connections.query.filter_by(connected_id=id).first()
    if conn_old is not None:
        conn_old.connected_id = None
        db.session.add(conn_old)
        db.session.commit()

    target_conn = Connections.query.filter_by(id=connected_id).first()
    target_conn.connected_id = id
    db.session.add(target_conn)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/api/cushion/all')
def get_cushion_all():
    conn_list = Connections.query.order_by(Connections.id)
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
