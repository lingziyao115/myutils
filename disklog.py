# -*- coding: utf-8 -*-
"""
    写磁盘日志
"""

import os
import time
import fcntl
import os.path
import datetime
import traceback

from .json import jsonify


class MsgTypeRequiredError(Exception):
    pass


class DiskLog():

    def __init__(self, log_dir, server_ip, project_name, retry_count=3):
        """
        Args:
            log_dir       存储日志的目录，使用绝对路径
            server_ip     服务器IP
            project_name  项目名称
            retry_count   写失败的重试次数
        """
        self.log_dir = log_dir
        self.retry_count = retry_count
        self.server_ip = server_ip
        self.project_name = project_name

    def write(self, msg):
        """写磁盘日志
        Args:
            msg    日志内容，dict 类型
        """
        # 日志信息中必须包含 msg_type 字段
        if 'msg_type' not in msg:
            raise MsgTypeRequiredError

        msg_type = msg['msg_type']
        abs_dir = os.path.join(self.log_dir, msg_type)
        if not os.path.exists(abs_dir):
            os.makedirs(abs_dir)
        today = datetime.datetime.now().strftime("%Y%m%d")
        filename = '_'.join([self.project_name, msg_type.lower(), self.server_ip,  today]) + '.txt'
        file_path = os.path.join(abs_dir, filename)
        for i in range(self.retry_count):
            try:
                f = open(file_path, "a")
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write("{msg}\n".format(msg=jsonify(msg)))
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()
                break
            except:
                traceback.print_exc()
                time.sleep(0.0001)
