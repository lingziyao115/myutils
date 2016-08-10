# -*- coding: utf-8 -*-
"""
    封装的 URL 请求方法
"""

import requests
import logging

from .json import jsonify


HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_DELETE = "DELETE"
REQUEST_TIMEOUT = 60


class RestRequest(object):

    def __init__(self, host='', method=HTTP_GET, json_encode=False,
                timeout=REQUEST_TIMEOUT):
        """
        :param host: 必须以 http(s) 开头 
        """
        if not host.startswith('http'):
            raise ValueError('host invalid')

        method = method.upper()
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise ValueError('method invalid')

        self.host = host.rstrip('/')
        self.method = method
        self.resp = None
        self.json_encode = json_encode
        self.timeout = timeout

    def get_url(self, uri='/'):
        return self.host + uri

    def fetch(self, uri, headers={}, **data):
        """
        :param uri: 必须以 / 开头
        """
        if not uri.startswith('/'):
            raise ValueError('uri invalid')
        url = self.get_url(uri)
        kwargs = dict(headers=headers, allow_redirects=True, timeout=self.timeout)

        if self.method == HTTP_GET:
            kwargs.update(params=data)
        elif self.method == HTTP_POST or self.method == HTTP_PUT:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            if self.json_encode:
                headers["Content-Type"] = "application/json"
                data = jsonify(data)
            kwargs.update(data=data)
        elif self.method == HTTP_DELETE:
            pass

        resp = requests.request(self.method, url, **kwargs)

        msg = "[%s] %s %s %d" % (self.method, resp.url, data, resp.status_code)
        logging.debug(msg)

        self.resp = resp

    @property
    def ok(self):
        if self.resp is not None:
            return self.resp.status_code == 200

    @property
    def data(self):
        if self.resp is not None:
            try:
                data = self.resp.json()
            except:
                data = self.resp.text
            return data

    @property
    def status_code(self):
        if self.resp is not None:
            return self.resp.status_code
