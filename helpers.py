# -*- coding: utf-8 -*-
"""
    Misc Tools
"""

import hashlib
import os
import random
import socket
import string
import struct
import time
from datetime import datetime
from hashlib import sha256
from hmac import HMAC


def convert_dict(args):
    ''' 将类字典对象转换为字典 '''
    return dict((k, v) for k, v in args.items())


def convert_human_num(num):
    ''' 将数字转换为更可读的形式，如 3.5k, 1w '''
    try:
        num = float(int(num))
    except:
        return ''

    if num < 1000:
        return str(int(num))
    elif num < 10000:
        num = str(round(num / 1000, 1))
        if num[-2:] == '.0':
            num = num[:-2]
        return '%sk' % num
    elif num < 100000:
        num = str(round(num / 10000, 1))
        if num[-2:] == '.0':
            num = num[:-2]
        return '%sw' % num
    else:
        num = str(round(num / 10000))
        if num[-2:] == '.0':
            num = num[:-2]
        return '%sw' % num


def ip2int(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]

def int2ip(i):
    return socket.inet_ntoa(struct.pack('!I', i))


def encrypt_password(password, salt=None):
    """加密密码
    产生 40 个字符长度的密码，其中前 8 个字符为加密时的盐值
    注意，加密时不要传 salt 参数
    """
    if not salt:
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    if isinstance(password, unicode):
        password = password.encode("utf-8")

    return salt + HMAC(password, salt, sha256).hexdigest()[:32]


def validate_password(hashed, password):
    """验证密码
    :param hashed: 加密后的密码
    :param password: 密码
    """
    return hashed == encrypt_password(password, salt=hashed[:8])


def filter_fields(args, filter_fields, exists=False):
    """过滤字典
    :param args: 被过滤的可迭代的类 dict 类型
    :param filter_fields: 过滤的字段列表
    :param exists: 若设置为 True, 则返回 args 中 value 为真值的项
    """
    if not exists:
        return dict((k, v) for k, v in args.iteritems() if k in filter_fields)
    return dict((k, v) for k, v in args.iteritems() if k in filter_fields and v)


def filter_dicts(data_ins, reserved_keys):
    """高级过滤字典方法
    根据保留字段，对输入的字典或者字典列表进行字段筛选，支持 2 级深度
    :param data_ins: 输入值，只能是字典或者相同结构字典的列表
    :param reserved_keys: 保留字段列表，输出的字典中只含有这些字段
    """
    if not data_ins or not isinstance(data_ins, (dict, list)) or not reserved_keys:
        return None

    if isinstance(data_ins, dict):
        data_out = dict()
        for key in reserved_keys:
            key_slices = key.split('.')

            if len(key_slices) == 1:
                if key in data_ins:
                    data_out[key] = data_ins.get(key)
            elif len(key_slices) == 2:
                key, sub_key = key_slices
                if not key in data_ins:
                    continue
                if not key in data_out:
                    data_out[key] = dict()
                if sub_key in data_ins[key]:
                    data_out[key][sub_key] = data_ins[key].get(sub_key)
        return data_out

    if isinstance(data_ins, list):
        data_outs = []
        for data_in in data_ins:
            data_out = filter_dicts(data_in, reserved_keys)
            data_outs.append(data_out)
        return data_outs


def get_start_end(offset, limit, is_redis=True):
    """获取数据开始和结束的位置
    :param offset: 开始位置
    :param limit: 数据条数
    :param is_redis: 是否为 redis
    """
    offset, limit = int(offset), int(limit)
    if offset == 0 and limit == -1:
        start = 0
        end = None if not is_redis else -1
        return start, end
    start = offset
    end = start + limit
    if is_redis and end > 0:
        end -= 1
    return start, end


def get_today_remaining_seconds():
    ''' 获取今天剩余的秒数时间 '''
    now_date_str = datetime.now().strftime("%Y-%m-%d")
    today_end_dt = datetime.strptime("%s 23:59:59" % now_date_str, "%Y-%m-%d %H:%M:%S")
    today_end_ts = int(time.mktime(today_end_dt.timetuple()))
    now_ts = int(time.time())
    return today_end_ts - now_ts


def get_file_suffix(file_name, default=None):
    '''获取文件名后缀
    参数说明:
        file_name    文件名(可包含路径)
        default      返回的默认值
    返回:
        不带点的文件名后缀
    '''
    ext = os.path.splitext(file_name)[1].lower()
    if ext:
        ext = ext[1:]
    if not ext and default:
        return default
    return ext


def calc_file_md5(file_path):
    ''' 计算文件的 md5 '''
    if not os.path.isfile(file_path):
        return False

    fo = open(file_path, 'rb')
    md5_hash = hashlib.md5()
    while True:
        bytes = fo.read(8096)
        if not bytes:
            break
        md5_hash.update(bytes)
    fo.close()

    return md5_hash.hexdigest()
