#  -*- coding: utf-8 -*-
__author__ = 'pengg'

import pandas as pd
from datetime import date
from tqsdk import TqApi, TqAuth, TqReplay
from tqsdk import TqSim, TqAccount
from tqsdk import TqBacktest
import sys
import time
#复盘模式示例: 指定日期行情完全复盘  2020-05-26 行情

# 在创建 api 实例时传入 TqReplay 就会进入复盘模式
api = TqApi(web_gui=":16666", backtest=TqReplay(date(2020, 10, 15)), auth=TqAuth("aimoons", "112411"))
quote = api.get_quote("SHFE.cu2101") #quote

rvddata = pd.DataFrame()
listidata = ['Google', 'Runoob', 'Taobao']

#rvddata = api.get_kline_serial(sys.argv[2],int(sys.argv[1]))
up = -1
while True:
    api.wait_update()
    if api.is_changing(quote): #rvddata
r        print("最新价", quote.datetime, quote.last_price)
        rvddata=rvddata.append(quote);
#        print(rvddata)
        
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        ma5 = sum(rvddata.close.iloc[-5:])/5
        ma15 = sum(rvddata.close.iloc[-15:])/15
        #print("最新价:", rvddata.close.iloc[-1], ",MA5:", ma5, ",MA15:", ma15)
        #print("UP:", up, "ma5-ma15:", ma5-ma15)
        #if rvddata.close.iloc[-1] > ma5:

