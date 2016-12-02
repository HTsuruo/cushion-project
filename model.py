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


#
# # クッション1のセンサデータ
# class Cushion1(db.Model):
#     __tablename__ = 'cushion1'
#
#     def __init__(self):
#
#     def __repr__(self):
#         return 'Cushion1'
#
#
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