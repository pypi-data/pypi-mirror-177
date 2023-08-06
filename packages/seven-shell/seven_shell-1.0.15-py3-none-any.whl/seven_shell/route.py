# -*- coding: utf-8 -*-
"""
:Author: Kangwenbin
:Date: 2022-11-17 17:44:57
:LastEditTime: 2022-11-22 17:32:39
:LastEditors: Kangwenbin
:Description: 
"""
# 框架引用
import seven_shell.handlers.integral as integral

def seven_shell_route():
    return [
        (r"/shell/exchange_list", integral.ExchangeListHandler), # 兑换列表 
        (r"/shell/goods_detail", integral.GoodsDetailHandler), # 商品详情 
        (r"/shell/goods_exchange", integral.GoodsExchangeHandler), # 商品兑换 
        (r"/shell/goods_list", integral.GoodsListHandler), # 积分商品列表 
    ]
