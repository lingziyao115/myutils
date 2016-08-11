# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012 Bo Zhu http://about.bozhu.me

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.


    RC4 加密算法（放弃使用）

    一种密钥长度可变的流加密算法簇。
    注意：RC4 加密算法已不再安全。比较容易被猜解，不应该再用于关键数据的加密。
    参考：RC4加密已不再安全，破解效率极高 (http://www.freebuf.com/news/72622.html)
"""

__all__ = ['encrypt', 'decrypt']


def KSA(key):
    ''' 初始化算法 '''
    keylength = len(key)

    S = range(256)

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap

    return S


def PRGA(S):
    ''' 伪随机子密码生成算法 '''
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap

        K = S[(S[i] + S[j]) % 256]
        yield K


def RC4(key):
    S = KSA(key)
    return PRGA(S)


def convert_key(s):
    return [ord(c) for c in s]


def crypt(key, data):
    ret = []
    key = convert_key(key)
    keystream = RC4(key)
    for c in data:
        one = chr(ord(c) ^ keystream.next())
        ret.append(one)
    return ''.join(ret)


SAMPLE_KEY = "hb3)u07632C1pUM:O3409?-L01gh=c>(L1$+,VpDZw363_7U6<n-%*cxTY&Zc5(}Db2[Zh)pYD<^T+`D,um@45*Eh`])pmy$p`4C58:v3|8tGpz^6F[Kbu$]`)`Kc<w>VZ"

def encrypt(data, key=SAMPLE_KEY):
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    return crypt(key, data)


def decrypt(data, key=SAMPLE_KEY):
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    return crypt(key, data)
