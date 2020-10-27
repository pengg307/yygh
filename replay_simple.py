#  -*- coding: utf-8 -*-
__author__ = 'pengg'

import pandas as pd
import math
from datetime import date
from tqsdk import TqApi, TqAuth, TqReplay
from tqsdk import TqSim, TqAccount
from tqsdk import TqBacktest
import sys
import time
#复盘模式示例: 指定日期行情完全复盘  2020-05-26 行情

# 在创建 api 实例时传入 TqReplay 就会进入复盘模式
api = TqApi(web_gui=":16666", backtest=TqReplay(date(2020, 10, 15)), auth=TqAuth("aimoons", "112411"))
quote = api.get_quote(symbol=sys.argv[2]) #quote

rvddata = pd.DataFrame()
malength=15
while malength>0:
  rvddata=rvddata.append(pd.Series(0, name="close"))
  malength=malength-1


#rvddata = api.get_kline_serial(sys.argv[2],int(sys.argv[1]))
up = -1
while True:
    api.wait_update()
    if api.is_changing(quote): #rvddata
        print("最新价", quote.datetime, quote.last_price)
        if(math.isnan(quote.last_price)):
          rvddata=rvddata.append(pd.Series(0, name="close"))
        else:
          rvddata=rvddata.append(pd.Series(quote.last_price, name="close"))

        print(rvddata)
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        print(rvddata[0].close)
        ma5s = sum(rvddata[0].close.iloc[-5:])
        ma15s = sum(rvddata[0].close.iloc[-15:])
        print("ma=",ma5s)
        print("ma=",ma15s)
        ma5 = ma5s/5
        ma15 = ma15s/15
        #ma5 = sum(rvddata.close.iloc[-5:])/5
        #ma15 = sum(rvddata.close.iloc[-15:])/15
        
        #print("最新价:", rvddata.close.iloc[-1], ",MA5:", ma5, ",MA15:", ma15)
        #print("UP:", up, "ma5-ma15:", ma5-ma15)
        #if rvddata.close.iloc[-1] > ma5:
        if ma5 - ma15 > 0 and up < 0:
            print("市价开仓")
            order=api.insert_order(symbol=sys.argv[2], direction="BUY", offset="OPEN", volume=1, limit_price=quote.bid_price1)
            while order.status != "FINISHED":
              api.wait_update()
            print("已开仓")
#            break
        #elif rvddata.close.iloc[-1] < ma15:
        elif ma5 - ma15 < 0 and up > 0:
            print("市价平仓")
            order=api.insert_order(symbol=sys.argv[2], direction="SELL", offset="CLOSETODAY", volume=1, limit_price=quote.bid_price1)
            while order.status != "FINISHED":
              api.wait_update()
            print("已平今")

#            break
        up = ma5 - ma15
