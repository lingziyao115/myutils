# -*- coding: utf-8 -*-
"""
    验证码
"""

import random
from cStringIO import StringIO
from PIL import Image, ImageDraw, ImageFont


class Captcha(object):

    # 验证码字符（去掉了容易混淆的字符）
    characters = '234578acdefhjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ'
    # 字体(名称, 大小)
    font = ('Arial.ttf', 36)


    def __init__(self, character_width=4):
        # 验证码采用几个字符
        self.character_width = character_width


    def _rand_char(self):
        return random.choice(self.characters)


    def _rand_color(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


    def _rand_color2(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


    def generate(self):
        captchas = []
        font = self.font

        font = ImageFont.truetype(font[0], font[1])
        size = (self.character_width * 40 + 20, 40 + 10)
        im = Image.new("RGB", size, "white")
        draw = ImageDraw.Draw(im)

        # 填充背景
        for x in range(size[0]):
            for y in range(size[1]):
                draw.point((x, y), fill=self._rand_color())

        # 写入字符
        for i in range(self.character_width):
            char = self._rand_char()
            captchas.append(char)
            draw.text((40 * i + 10, 5), char, font=font, fill=self._rand_color2())

        # 图片文件保存到 StringIO
        s = StringIO()
        im.save(s, "JPEG")
        img_buffer = s.getvalue()
        s.close()

        return (''.join(captchas), img_buffer)
