#!/bin/env python
# coding: utf-8

from model import *
from datetime import datetime
import time


def get_latest_date(cushion_id):
    if cushion_id == 1:
        return Cushion1.query.order_by(Cushion1.id.desc()).first().timestamp
    else:
        return datetime.now().date()


# クッションが稼働中か否かを返します.
# 現在時刻と比較して30秒以内をみます.
def is_active(latest_date_str):
    # latest_date_time = datetime.strftime(latest_date_str, '%Y-%m-%d %H:%M:%S')
    # epo_time_latest = datetime_to_epoch(latest_date_time)
    # epo_time_now = datetime_to_epoch(datetime.now().date())
    # diff = epo_time_latest - epo_time_now
    return True


def datetime_to_epoch(d):
    return int(time.mktime(d.timetuple()))


def epoch_to_datetime(epoch):
    return datetime(*time.localtime(epoch)[:6])