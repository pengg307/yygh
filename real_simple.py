#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'pengg'

from tqsdk import TqApi, TqSim, TqAccount, TqAuth
from tqsdk import TqBacktest
import sys
import time
from datetime import date
from tqsdk.ta import MA

'''
如果当前价格大于10秒K线的MA15则开多仓 (使用 insert_order() 函数)
如果小于则平仓
'''
api = TqApi(web_gui=":16789",auth=TqAuth("aimoons", "112411"))
quote = api.get_quote(sys.argv[2])
order = {}
# 获得 ticker n秒K线的引用
klines = api.get_kline_serial(sys.argv[2],int(sys.argv[1]))
rvddata = klines

cd = 10;
up = -1
while cd:
    # 画一次指标线
    ma7 = MA(klines, 7)  # 使用 tqsdk 自带指标函数计算均线
    ma20 = MA(klines, 20)  # 使用 tqsdk 自带指标函数计算均线
    ma50 = MA(klines, 50)  # 使用 tqsdk 自带指标函数计算均线

    klines["ma7_MAIN"] = ma7.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma7_MAIN.color"] = "green"  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma20_MAIN"] = ma20.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma7_MAIN.color"] = "yellow"  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma50_MAIN"] = ma50.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma7_MAIN.color"] = "blue"  # 在主图中画一根默认颜色（红色）的 ma 指标线

    # 示例2: 在另一个附图画一根比ma小4的宽度为4的紫色指标线
    klines["yy"] = ma7.ma - 4
    klines["yy.board"] = "YY"  # 设置为另一个附图
    klines["yy.color"] = 0xFF9933CC  # 设置为紫色, 或者 "#9933FF"
    klines["yy.width"] = 4  # 设置宽度为4，默认为1

    # 判断开仓条件
    while True:
        api.wait_update()
        if api.is_changing(klines):
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
            ma5 = sum(rvddata.close.iloc[-5:])/5
            ma15 = sum(rvddata.close.iloc[-15:])/15
            print("最新价:", rvddata.close.iloc[-1], ",MA5:", ma5, ",MA15:", ma15)
            print("UP:", up, "ma5-ma15:", ma5-ma15)
            position = api.get_position(sys.argv[2])
            print(position.float_profit_long + position.float_profit_short)
            if ma5 - ma15 > 0 and up < 0: 
                print("最新价大于MA: 市价开仓")
                api.insert_order(symbol=sys.argv[2], direction="BUY", offset="OPEN", volume=5, limit_price=quote.bid_price1)
                break
            up = ma5 - ma15
    # 判断平仓条件
    while True:
        api.wait_update()
        if api.is_changing(klines):
            print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
            ma5 = sum(rvddata.close.iloc[-5:])/5
            ma15 = sum(rvddata.close.iloc[-15:])/15
            print("最新价:", rvddata.close.iloc[-1], ",MA5:", ma5, ",MA15:", ma15)
            print("UP:", up, "ma5-ma15:", ma5-ma15)
            position = api.get_position(sys.argv[2])
            print(position.float_profit_long + position.float_profit_short)
            if ma5 - ma15 < 0 and up > 0:
                print("最新价小于MA: 市价平仓")
                api.insert_order(symbol=sys.argv[2], direction="SELL", offset="CLOSETODAY", volume=5, limit_price=quote.bid_price1)
                break
            up = ma5 - ma15
    cd=cd-1
# 关闭api,释放相应资源
api.close()

