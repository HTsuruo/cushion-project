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
# 現在時刻と比較して60秒以内をみます.
def is_active(latest_date):
    epo_time_latest = datetime_to_epoch(latest_date)
    epo_time_now = datetime_to_epoch(datetime.now())
    diff = epo_time_now - epo_time_latest
    if diff < 0 or diff > 60:
        return False
    return True


def datetime_to_epoch(d):
    return int(time.mktime(d.timetuple()))


def epoch_to_datetime(epoch):
    return datetime(*time.localtime(epoch)[:6])