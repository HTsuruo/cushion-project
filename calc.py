# coding: utf-8

from model import *
import math

SENSOR_NUM = 6
SITTING_THRESHOLD = 100
WORKING_THRESHOLD = 300


def do_calibration(cushion_id, rand_id, raw_data):
    # get oldest base data for calibration.
    base = SensorData.query.filter_by(cushion_id=cushion_id).filter_by(rand_id=rand_id).order_by(SensorData.timestamp).first()
    base_data = []
    if base is None:
        for i in range(SENSOR_NUM):
            base_data.append(raw_data[i])
    else:
        base_data.append(base.sensor_1)
        base_data.append(base.sensor_2)
        base_data.append(base.sensor_3)
        base_data.append(base.sensor_4)
        base_data.append(base.sensor_5)
        base_data.append(base.sensor_6)

    print("raw_data[do_calibration]:" + str(raw_data))
    print("base_data[do_calibration]: " + str(base_data))

    cali_data = []
    for i in range(SENSOR_NUM):
        cali_data.append(raw_data[i] - base_data[i])
        if cali_data[i] < 0:
            cali_data[i] = 0
    return cali_data


def calc_working_state(cushion_id, raw_data, cali_data):

    # not sitting state.
    if cali_data[0] < SITTING_THRESHOLD and cali_data[1] < SITTING_THRESHOLD:
        return 0

    # sitting state.
    p_val = get_posture_value(cali_data)
    m_val = get_movement_value(cushion_id, raw_data)
    return p_val * m_val


def get_posture_value(data):
    filter_num = (data[2] + data[3])/2

    if filter_num < WORKING_THRESHOLD:
        return 2  # working.
    return 1  # not working.


def get_movement_value(cushion_id, raw_data):
    diff = get_movement_diff(cushion_id, raw_data)
    if diff < 10:
        return 5
    if diff < 20:
        return 4
    if diff < 30:
        return 3
    if diff < 40:
        return 2
    return 1


def get_movement_diff(cushion_id, raw_data):
    pre_data_all = SensorData.query.filter_by(cushion_id=cushion_id).order_by(SensorData.timestamp.desc()).first()
    pre_data = []
    if pre_data_all is None:
        for i in range(SENSOR_NUM):
            pre_data.append(raw_data[i])
    else:
        pre_data.append(pre_data_all.sensor_1)
        pre_data.append(pre_data_all.sensor_2)
        pre_data.append(pre_data_all.sensor_3)
        pre_data.append(pre_data_all.sensor_4)
        pre_data.append(pre_data_all.sensor_5)
        pre_data.append(pre_data_all.sensor_6)

    diff_data = []
    for i in range(SENSOR_NUM):
        diff_data.append(raw_data[i] - pre_data[i])
        if diff_data[i] < 0:
            diff_data[i] *= -1
    diff = sum(diff_data)/SENSOR_NUM
    return math.floor(diff)


def get_working_state_average(cushion_id):
    data_num = 5  # 最新5個のデータを取得します.
    data_list = WorkingStates.query.filter_by(cushion_id=cushion_id).order_by(WorkingStates.id.desc()).limit(data_num)
    values = []
    for data in data_list:
        values.append(data.value)
    return math.floor(sum(values)/data_num)
