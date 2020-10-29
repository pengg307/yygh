#!usr/bin/env python3
#-*- coding:utf-8 -*-
#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'pengg'

from datetime import date
from tqsdk import TqApi, TqAuth, TqReplay, TargetPosTask
from tqsdk.ta import MA
'''
复盘 2020-05-26
如果当前价格大于5分钟K线的MA15则开多仓,如果小于则平仓
'''
# 在创建 api 实例时传入 TqReplay 就会进入复盘模式, 同时打开 web_gui
api = TqApi(web_gui=":16666", backtest=TqReplay(date(2020, 10, 15)), auth=TqAuth("aimoons", "112411"))
# 获得 cu2009 5分钟K线的引用
klines = api.get_kline_serial("SHFE.cu2102", 5 * 60, data_length=15)
# 创建 cu2009 的目标持仓 task，该 task 负责调整 m1901 的仓位到指定的目标仓位
target_pos = TargetPosTask(api, "SHFE.cu2102")

while True:
    ma3 = MA(klines, 3)  # 使用 tqsdk 自带指标函数计算均线
    ma5 = MA(klines, 5)  # 使用 tqsdk 自带指标函数计算均线

    klines["ma3_MAIN.board"] = "MA3"
    klines["ma3_MAIN"] = ma3.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma3_MAIN.color"] = 0x00FF00  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma5_MAIN.board"] = "MA5"
    klines["ma5_MAIN"] = ma5.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma5_MAIN.color"] = "blue"  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma5_MAIN.width"] = 4  # 设置宽度为4，默认为1


    api.wait_update()
    if api.is_changing(klines):
        ma = sum(klines.close.iloc[-15:]) / 15
        print("最新价", klines.close.iloc[-1], "MA", ma)
        if klines.close.iloc[-1] > ma:
            print("最新价大于MA: 目标多头5手")
            # 设置目标持仓为多头5手
            target_pos.set_target_volume(5)
        elif klines.close.iloc[-1] < ma:
            print("最新价小于MA: 目标空仓")
            # 设置目标持仓为空仓
            target_pos.set_target_volume(0)
