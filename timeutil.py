# -*- coding: utf-8 -*-
"""
    日期时间处理方法
"""

import time
import datetime


DT_FORMAT = '%Y-%m-%d %H:%M:%S'


def dts_to_datetime(dts, format=DT_FORMAT):
    """将字符串日期时间转换为 datetime 类型
    :param dts: date time string
    :param format: 对应的格式
    """
    return datetime.datetime.strptime(dts, format)


def timestamp_to_dts(timestamp, format=DT_FORMAT):
    """ 将时间戳转换为字符串日期时间 """
    return time.strftime(format, time.localtime(timestamp))


def dts_to_timestamp(dts, format=DT_FORMAT):
    """ 将字符串日期时间转换为时间戳 """
    return int(time.mktime(time.strptime(dts, format)))


def datetime_to_timestamp(dt):
    return int(time.mktime(dt.timetuple()))


def timestamp_to_datetime(ts):
    return datetime.datetime.fromtimestamp(ts)


def _pretty_datetime(dt):
    """
    :param dt: datetime 类型的日期时间
    """
    now = datetime.datetime.now()
    diff = now - dt
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "刚刚"
        if second_diff < 60:
            return str(second_diff) + "秒前"
        if second_diff < 3600:
            return str(second_diff / 60) + "分钟前"
        if second_diff < 86400:
            return str(second_diff / 3600) + "小时前"
    if day_diff == 1:
        return "昨天"
    if day_diff < 7:
        return str(day_diff) + "天前"
    if day_diff < 31:
        return str(day_diff / 7) + "周前"
    if day_diff < 365:
        return str(day_diff / 30) + "月前"
    return str(day_diff / 365) + "年前"


def pretty_datetime(dt=''):
    """美化日期时间
    :param dt: (字符串)日期时间，或者时间戳
    """
    if not isinstance(dt, datetime.datetime):
        if isinstance(dt, basestring):
            dt = dts_to_datetime(dt)
        elif isinstance(dt, int):
            dt = timestamp_to_datetime(dt)
        else:
            return False

    return _pretty_datetime(dt).decode('utf-8')


def seconds_to_time(seconds):
    """ 将总秒数转换为时间格式，如 88 -> 01:28 """
    try:
        seconds = int(seconds)
    except:
        seconds = 0
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    ret = ''
    if h > 0:
        ret += '%02d:' % h
    ret += '%02d:%02d' % (m, s)
    return ret
