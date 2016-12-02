# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# クッションの接続先情報
class Connection(db.Model):
    __tablename__ = 'connection'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String)
    connect = db.Column(db.INTEGER)

    def __init__(self, name, connect):
        self.name = name
        self.connect = connect

    def __repr__(self):
        return '<Connection %r>' % self.name


# クッション1のセンサデータ
class Cushion1(db.Model):
    __tablename__ = 'cushion1'
    id = db.Column(db.INTEGER, primary_key=True)
    data1 = db.Column('sensorData1', db.INTEGER)
    data2 = db.Column('sensorData2', db.INTEGER)
    data3 = db.Column('sensorData3', db.INTEGER)
    data4 = db.Column('sensorData4', db.INTEGER)
    data5 = db.Column('sensorData5', db.INTEGER)
    data6 = db.Column('sensorData6', db.INTEGER)
    rand_id = db.Column('randID', db.INTEGER)
    timestamp = db.Column('timeStamp', db.DATETIME)

    def __init__(self, data1, data2, data3, data4, data5, data6, rand_id, timestamp):
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.data4 = data4
        self.data5 = data5
        self.data6 = data6
        self.rand_id = rand_id
        self.timestamp = timestamp

    def __repr__(self):
        return 'Cushion1'


# # クッション2のセンサデータ
# class Cushion2(db.Model):
#     __tablename__ = 'cushion2'
#
#     def __init__(self):
#
#
# # クッション3のセンサデータ
# class Cushion3(db.Model):
#     __tablename__ = 'cushion3'
#
#     def __init__(self):
#
#
# # クッション4のセンサデータ
# class Cushion4(db.Model):
#     __tablename__ = 'cushion4'
#
#     def __init__(self):