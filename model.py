# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# クッションの接続先情報
class Connections(db.Model):
    __tablename__ = 'connections'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String)
    connected_id = db.Column(db.INTEGER)

    def __init__(self, name, connected_id):
        self.name = name
        self.connected_id = connected_id

    def __repr__(self):
        return '<Connections %r>' % self.name


# クッションのセンサデータ
class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.INTEGER, primary_key=True)
    cushion_id = db.Column('cushion_id', db.INTEGER)
    sensor_1 = db.Column('sensor_1', db.INTEGER)
    sensor_2 = db.Column('sensor_2', db.INTEGER)
    sensor_3 = db.Column('sensor_3', db.INTEGER)
    sensor_4 = db.Column('sensor_4', db.INTEGER)
    sensor_5 = db.Column('sensor_5', db.INTEGER)
    sensor_6 = db.Column('sensor_6', db.INTEGER)
    rand_id = db.Column('rand_id', db.INTEGER)
    timestamp = db.Column('timestamp', db.DATETIME)

    def __init__(self, cushion_id, sensor_1, sensor_2, sensor_3, sensor_4, sensor_5, sensor_6, rand_id):
        self.cushion_id = cushion_id
        self.sensor_1 = sensor_1
        self.sensor_2 = sensor_2
        self.sensor_3 = sensor_3
        self.sensor_4 = sensor_4
        self.sensor_5 = sensor_5
        self.sensor_6 = sensor_6
        self.rand_id = rand_id

    def __repr__(self):
        return 'SensorData'


# 着座状態
class WorkingStates(db.Model):
    __tablename__ = 'working_states'
    id = db.Column(db.INTEGER, primary_key=True)
    cushion_id = db.Column('cushion_id', db.INTEGER)
    value = db.Column('value', db.INTEGER)
    diff = db.Column('diff', db.INTEGER)

    def __init__(self, cushion_id, value, diff):
        self.cushion_id = cushion_id
        self.value = value
        self.diff = diff

    def __repr__(self):
        return 'WorkingStates'