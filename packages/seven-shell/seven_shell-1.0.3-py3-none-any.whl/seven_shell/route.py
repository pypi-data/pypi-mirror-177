# -*- coding: utf-8 -*-
"""
:Author: Kangwenbin
:Date: 2022-11-17 17:44:57
:LastEditTime: 2022-11-18 11:04:43
:LastEditors: ChenXiaolei
:Description: 
"""
# 框架引用
import seven_shell.handlers.integral as integral

def seven_studio_route():
    return [
        (r"/shell/exchange_list", integral.ExchangeListHandle), # 兑换列表 
        (r"/shell/goods_detail", integral.GoodsDetailHandle), # 商品详情 
        (r"/shell/goods_exchange", integral.GoodsExchangeHandle), # 商品兑换 
        (r"/shell/goods_list", integral.GoodsListHandle), # 积分商品列表 
    ]
