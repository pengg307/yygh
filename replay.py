#  -*- coding: utf-8 -*-
__author__ = 'pengg'

from datetime import date
from tqsdk import TqApi, TqAuth, TqReplay

'''
复盘模式示例: 指定日期行情完全复盘
复盘 2020-05-26 行情
'''
# 在创建 api 实例时传入 TqReplay 就会进入复盘模式
api = TqApi(backtest=TqReplay(date(2020, 10, 15)), auth=TqAuth("aimoons", "112411"))
quote = api.get_quote("SHFE.cu2101")

while True:
    api.wait_update()
    if api.is_changing(quote):
        print("最新价", quote.datetime, quote.last_price)
