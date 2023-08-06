# -*- coding: utf-8 -*-
"""
:Author: Kangwenbin
:Date: 2022-11-21 17:46:56
:LastEditTime: 2022-11-22 16:51:41
:LastEditors: Kangwenbin
:Description: 
"""
import seven_shell_studio.handlers.api.integral as integral

def seven_shell_studio_route():
    return [
        (r"/api/integral/exchange_list", integral.ExchangeListHandler), # 兑换列表 
        (r"/api/integral/goods_list", integral.GoodsListHandler), # 商品列表 
        (r"/api/integral/goods_manage", integral.GoodsManageHandler), # 商品信息/商品添加/商品修改/商品删除/商品上下架 
    ]
