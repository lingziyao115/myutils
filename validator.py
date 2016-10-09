# -*- coding: utf-8 -*-
"""
    常用正则表达式
"""
from __future__ import print_function
import re


# 昵称（支持汉字）
nickname_validator = re.compile(r'^[\w]+$', re.UNICODE)

# 网址
# r'^https?://([A-Za-z\d-]+\.)+[A-Za-z]{2,20}(/\S*)?$'
url_validator = re.compile(r'''^
                        https?://
                        ([A-Za-z\d-]+\.)+    # 多级域名
                        [A-Za-z]{2,20}       # 最后的根限制为2~20个字母
                        (/\S*)?            # 只要求 / 后为非空字符即可
                        $''', re.X)

# 中国大陆手机号码
mobile_validator = r'^\+?(86)?1\d{10}$'

# 电子邮箱
# r'^[A-Za-z\d][\w\.-]*@([A-Za-z\d-]+\.)+[A-Za-z]{2,}$'
email_validator = re.compile(r'''^
                        [A-Za-z\d]           # 第一个字符只能是字母或数字
                        [\w\.-]*             # 后面的可以是字母、数字、下划线、点、中划线
                        @
                        ([A-Za-z\d-]+\.)+    # 支持多级域名
                        [A-Za-z]{2,20}       # 最后的根限制为2~20个字母
                        $''', re.X)

# IP 地址
ipv4_validator = re.compile(r'''^
                        ((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}  # 按数字位数分情况处理
                        (\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])
                        $''', re.X)


if __name__ == '__main__':
    # 测试代码
    test_yes_urls = [
        'http://www.jiandana.com',
        'http://www.jiandana.com/',
        'http://www.jiandana.com//',
        'http://www.jiandana.com/abc',
        'http://www.jiandana.com/abc/',
        'http://www.jiandana.com/abc/test.html',
        'http://www.jiandana.com/abc/test.html?name=eric&age=31#profile',

        'https://www.jiandana.com',
        'https://www.jiandana.com/',
        'https://www.jiandana.com//'
        'https://www.jiandana.com/abc',
        'https://www.jiandana.com/abc/',
        'https://www.jiandana.com/abc/test.html',
        'https://www.jiandana.com/abc/test.html?name=eric&age=31#profile'
    ]

    for url in test_yes_urls:
        print(url, end=" ... ")
        assert url_validator.match(url)
        print('[ok]')
