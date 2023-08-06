# -*- coding: utf-8 -*-
"""
:Author: Kangwenbin
:Date: 2022-11-21 15:30:46
:LastEditTime: 2022-11-21 15:34:33
:LastEditors: Kangwenbin
:Description: 
"""
from models.db_models.exchange.exchange_model import *

class ExchangeModelEx(ExchangeModel):
    def __init__(self, db_connect_key='db_seven_shell', sub_table=None, db_transaction=None, context=None):
        super().__init__(db_connect_key, sub_table, db_transaction, context)

    def get_exchange_page_list(self,where='',field='*',order_by='id desc',limit='',params=None):
        condition = ""
        if where:
            condition += f" where {where}"
        if order_by:
            order_by = f" order by {order_by}"
        if limit:
            limit = f"limit {limit}"
        
        sql = f"SELECT {field} FROM exchange_tb a JOIN goods_tb b ON a.goods_id = b.id {condition} {order_by} {limit}"
        ret_list = self.db.fetch_all_rows(sql,params)
        sql_count = f"SELECT count(a.id) as count FROM exchange_tb a JOIN goods_tb b ON a.goods_id = b.id {condition}"
        row = self.db.fetch_one_row(sql_count,params)
        if row and 'count' in row and int(row['count']) > 0:
            row_count = int(row["count"])
        else:
            row_count = 0
        return ret_list,row_count