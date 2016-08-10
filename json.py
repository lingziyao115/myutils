# -*- coding: utf-8 -*-
"""
    升级版 JSON 序列化方法
"""

from datetime import datetime, date
from simplejson import dumps, loads, dump, load


def _default(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    raise TypeError("%r is not JSON serializable" % obj)


def jsonify(args):
    return dumps(args, default=_default)
