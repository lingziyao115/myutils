# -*- coding: utf-8 -*-
"""
    七牛云存储文件 hash 算法
    ~~~~~~~~~~~~~~~~~~~~~

    算法如下：
    1. 如果文件 <= 4M，那么 hash = UrlsafeBase64([0x16, sha1(FileContent)])。
    也就是，文件的内容的sha1值（20个字节），前面加一个byte（值为0x16），
    构成 21 字节的二进制数据，然后对这 21 字节的数据做 urlsafe 的 base64 编码。
    2. 如果文件 > 4M，则 hash = UrlsafeBase64([0x96, sha1([sha1(Block1), sha1(Block2), ...])])，
    其中 Block 是把文件内容切分为 4M 为单位的一个个块，也就是 BlockI = FileContent[I*4M:(I+1)*4M]。

    为何在 sha1 值前面加一个byte的标记位(0x16或0x96）？
    0x16 = 22，而 2^22 = 4M。所以前面的 0x16 其实是文件按 4M 分块的意思。
    0x96 = 0x80 | 0x16。其中的 0x80 表示这个文件是大文件（有多个分块），
    hash 值也经过了2重的 sha1 计算。
"""

import os
import sys
import base64
import hashlib
try:
    from cStringIO import StringIO as BytesIO  # py2
    bytes_chr = chr
except ImportError:
    from io import BytesIO  # py3
    bytes_chr = lambda c: bytes([c])


CHUNK_BITS = 22
CHUNK_SIZE = 1 << CHUNK_BITS  # == 2 ** 22 == 4 * 1024 * 1024 == 4MiB


def get_io_size(fio):
    """get file size from fio"""
    fio.seek(0, os.SEEK_END)
    fsize = fio.tell()
    fio.seek(0)
    return fsize


def get_io_qetag(fio):
    """Caculates qetag from file object

    Parameters:
        - fio: file-like object to the file

    Usage:
    >>> data = bytes_chr(0) * (CHUNK_SIZE + 42) * 42
    >>> fio = BytesIO(data)
    >>> print(get_io_qetag(fio))
    lnmoz9lrkr6HWgZyTqu2vD0XUj6R

    Returns qetag

    """
    size = get_io_size(fio)
    flag = CHUNK_BITS
    sha1 = hashlib.sha1
    buf = []
    while size > 0:
        size -= CHUNK_SIZE
        buf.append(sha1(fio.read(CHUNK_SIZE)).digest())
    buf = b''.join(buf)
    if len(buf) > 20:  # more than 1 chunk
        flag |= 0x80
        buf = sha1(buf).digest()
    fio.seek(0)
    return base64.urlsafe_b64encode(bytes_chr(flag) + buf).decode('ASCII')


def get_qetag(filename):
    """Caculates qetag

    Parameters:
        - filename: string, file name

    Returns qetag

    """
    with open(filename, 'rb') as fp:
        return get_io_qetag(fp)


if __name__ == '__main__':
    assert len(sys.argv) > 1
    print(get_qetag(sys.argv[1]))
