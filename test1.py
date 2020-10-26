#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'pengg'

from tqsdk import TqApi, TqSim, TqAccount
from tqsdk import TqBacktest
import sys
import time
from datetime import date

'''
如果当前价格大于10秒K线的MA15则开多仓 (使用 insert_order() 函数)
如果小于则平仓
'''
api = TqApi(web_gui=":16789")
# 获得 ticker n秒K线的引用
klines = api.get_kline_serial(sys.argv[2],int(sys.argv[1]))
rvddata = klines
up = -1
# 判断开仓条件
while True:
    api.wait_update()
    if api.is_changing(klines):
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        ma5 = sum(rvddata.close.iloc[-5:])/5
        ma15 = sum(rvddata.close.iloc[-15:])/15
        print("最新价:", rvddata.close.iloc[-1], ",MA5:", ma5, ",MA15:", ma15)
        print("UP:", up, "ma5-ma15:", ma5-ma15)

        if ma5 - ma15 > 0 and up < 0: 
            print("最新价大于MA: 市价开仓")
            api.insert_order(symbol=sys.argv[2], direction="BUY", offset="OPEN", volume=5)
            break
# 判断平仓条件
while True:
    api.wait_update()
    if api.is_changing(klines):
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        ma5 = sum(rvddata.close.iloc[-5:])/5
        ma15 = sum(rvddata.close.iloc[-15:])/15
        print("最新价:", rvddata.close.iloc[-1], ",MA5:", ma5, ",MA15:", ma15)
        print("UP:", up, "ma5-ma15:", ma5-ma15)

        if ma5 - ma15 < 0 and up > 0:
            print("最新价小于MA: 市价平仓")
            api.insert_order(symbol=sys.argv[2], direction="SELL", offset="CLOSE", volume=5)
            break
# 关闭api,释放相应资源
api.close()

