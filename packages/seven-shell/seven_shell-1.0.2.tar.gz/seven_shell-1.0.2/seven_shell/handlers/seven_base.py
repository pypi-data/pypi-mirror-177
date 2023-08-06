# -*- coding: utf-8 -*-
"""
:Author: Kangwenbin
:Date: 2022-11-16 19:28:38
:LastEditTime: 2022-11-17 16:32:26
:LastEditors: Kangwenbin
:Description: 
"""

# -*- coding: utf-8 -*-

from seven_framework.web_tornado.base_handler.base_api_handler import *
import random

class SevenBaseHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_order_number(self):
        # 获取当前时分秒
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))
        # 获取8位随机数
        random_str = random.randint(10000000, 99999999)
        order_number = f"E{time_str}{random_str}"
        return order_number
