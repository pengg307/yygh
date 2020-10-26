#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from tqsdk import TqApi, TqSim, TqAccount
from tqsdk import TqBacktest
import sys
import time
from datetime import date

#api = TqApi(web_gui=True)
#api = TqApi(web_gui=":16789",backtest=TqBacktest(start_dt=date(2020, 1, 6), end_dt=date(2020, 1, 7)))
api = TqApi(web_gui=":16789")
rvddata = api.get_kline_serial(sys.argv[2],int(sys.argv[1]))
#rvddata = api.get_kline_serial(sys.argv[3],int(sys.argv[1]),int(sys.argv[2]))
#rvddata = api.get_kline_serial("SHFE.cu2102",5)
up = -1
while True:
    api.wait_update()
    if api.is_changing(rvddata):
#        print(rvddata)
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        ma5 = sum(rvddata.close.iloc[-5:])/5
        ma15 = sum(rvddata.close.iloc[-15:])/15
        #print("最新价:", rvddata.close.iloc[-1], ",MA5:", ma5, ",MA15:", ma15)
        #print("UP:", up, "ma5-ma15:", ma5-ma15)
        #if rvddata.close.iloc[-1] > ma5:
        if ma5 - ma15 > 0 and up < 0:
            print("市价开仓")
            order=api.insert_order(symbol=sys.argv[2], direction="BUY", offset="OPEN", volume=1)
            while order.status != "FINISHED":
              api.wait_update()
            print("已开仓")
#            break
        #elif rvddata.close.iloc[-1] < ma15:
        elif ma5 - ma15 < 0 and up > 0:
            print("市价平仓")
            order=api.insert_order(symbol=sys.argv[2], direction="SELL", offset="CLOSE", volume=1)
            while order.status != "FINISHED":
              api.wait_update()
            print("已平今")

#            break
        up = ma5 - ma15
#
"""
while True:
    api.wait_update()
    if api.is_changing(rvddata):
        ma = sum(rvddata.close.iloc[-15:]) / 15
#        print("最新价", rvddata.close.iloc[-1], "MA", ma)
        if rvddata.close.iloc[-1] < ma:
            print("市价平仓")
            api.insert_order(symbol=sys.argv[3], direction="SELL", offset="CLOSE", volume=1)
            break
"""
api.close()
