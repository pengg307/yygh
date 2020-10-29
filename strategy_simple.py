#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "pengg"
#参考: https://www.shinnytech.com/blog/escalator/
from tqsdk import TqApi, TqAuth, TargetPosTask, TqReplay
from tqsdk.ta import MA
from datetime import date

# 设置合约
SYMBOL = "SHFE.ag2102"
# 设置均线长短周期
MA_SLOW, MA_FAST = 3, 5

api = TqApi(web_gui=":16666", backtest=TqReplay(date(2020, 10, 15)), auth=TqAuth("aimoons", "112411"))
klines = api.get_kline_serial(SYMBOL, 60 * 5)
quote = api.get_quote(SYMBOL)
position = api.get_position(SYMBOL)
target_pos = TargetPosTask(api, SYMBOL)

# K线收盘价在这根K线波动范围函数
def kline_range(num):
    kl_range = (klines.iloc[num].close - klines.iloc[num].low) / \
               (klines.iloc[num].high - klines.iloc[num].low)
    return kl_range
# 获取长短均线值
def ma_caculate(klines):
    ma_slow = MA(klines, MA_SLOW).iloc[-1].ma
    ma_fast = MA(klines, MA_FAST).iloc[-1].ma
    return ma_slow, ma_fast
ma_slow, ma_fast = ma_caculate(klines)
print("慢速均线为%.2f,快速均线为%.2f" % (ma_slow, ma_fast))

cur = -2
def vodd(rindex=0):
    return klines.iloc(cur-rindex).close >= klines.iloc(cur-1-rindex).close \
            and klines.iloc(cur-rindex).close <= klines.iloc(cur-2-rindex).close
def veven(rindex=0):
    return klines.iloc(cur-rindex).close <= klines.iloc(cur-1-rindex).close \
            and klines.iloc(cur-rindex).close >= klines.iloc(cur-2-rindex).close
def v1(rindex=0):
    return klines.iloc(cur-rindex).close > klines.iloc(cur-1-rindex).close \
            and klines.iloc(cur-rindex).close > klines.iloc(cur-2-rindex).close
def v2(rindex=0):
    return v1(1) and veven(rindex)
def v3(rindex=0):
    return v2(1) and vodd(rindex)
def v4(rindex=0):
    return v3(1) and veven(rindex)
def v5(rindex=0):
    return v4(1) and vodd(rindex)
def v6(rindex=0):
    return v5(1) and veven(rindex)
def v7(rindex=0):
    return v6(1) and vodd(rindex)
def v8(rindex=0):
    return v7(1) and veven(rindex)
def v9(rindex=0):
    return v8(1) and vodd(rindex)
def va(rindex=0):
    return v9(1) and veven(rindex)
def vb(rindex=0):
    return va(1) and vodd(rindex)
def vc(rindex=0):
    return vb(1) and veven(rindex)
def u1(rindex=0):
    return klines.iloc(cur-rindex).close < klines.iloc(cur-1-rindex).close \
            and klines.iloc(cur-rindex).close < klines.iloc(cur-2-rindex).close
def u2(rindex=0):
    return u1(1) and vodd(rindex)
def u3(rindex=0):
    return u2(1) and veven(rindex)
def u4(rindex=0):
    return u3(1) and vodd(rindex)
def u5(rindex=0):
    return u4(1) and veven(rindex)
def u6(rindex=0):
    return u5(1) and vodd(rindex)
def u7(rindex=0):
    return u6(1) and veven(rindex)
def u8(rindex=0):
    return u7(1) and vodd(rindex)
def u9(rindex=0):
    return u8(1) and veven(rindex)
def ua(rindex=0):
    return u9(1) and vodd(rindex)
def ub(rindex=0):
    return ua(1) and veven(rindex)
def uc(rindex=0):
    return ub(1) and vodd(rindex)

while True:
    ma3 = MA(klines, MA_SLOW)  # 使用 tqsdk 自带指标函数计算均线
    ma5 = MA(klines, MA_FAST)  # 使用 tqsdk 自带指标函数计算均线

    klines["ma3_MAIN.board"] = "MA3"
    klines["ma3_MAIN"] = ma3.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma3_MAIN.color"] = 0x00FF00  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma5_MAIN.board"] = "MA5"
    klines["ma5_MAIN"] = ma5.ma  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma5_MAIN.color"] = "blue"  # 在主图中画一根默认颜色（红色）的 ma 指标线
    klines["ma5_MAIN.width"] = 4  # 设置宽度为4，默认为1

    api.wait_update()
    # 每次k线更新，重新计算快慢均线
    if api.is_changing(klines.iloc[-1], "datetime"):
        ma_slow, ma_fast = ma_caculate(klines)
        print("慢速均线为%.2f,快速均线为%.2f" % (ma_slow, ma_fast))

    if api.is_changing(quote, "last_price"):
        # 开仓判断
        if position.pos_long == 0 and position.pos_short == 0:
            # 计算前后两根K线在当时K线范围波幅
            kl_range_cur = kline_range(-2)
            kl_range_pre = kline_range(-3)
            # 开多头判断，最近一根K线收盘价在短期均线和长期均线之上，前一根K线收盘价位于K线波动范围底部25%，最近这根K线收盘价位于K线波动范围顶部25%
            if klines.iloc[-2].close > max(ma_slow, ma_fast) and kl_range_pre <= 0.25 and kl_range_cur >= 0.75:
                print("最新价为:%.2f 开多头" % quote.last_price)
                target_pos.set_target_volume(100)

            # 开空头判断，最近一根K线收盘价在短期均线和长期均线之下，前一根K线收盘价位于K线波动范围顶部25%，最近这根K线收盘价位于K线波动范围底部25%
            elif klines.iloc[-2].close < min(ma_slow, ma_fast) and kl_range_pre >= 0.75 and kl_range_cur <= 0.25:
                print("最新价为:%.2f 开空头" % quote.last_price)
                target_pos.set_target_volume(-100)
            else:
                print("最新价位:%.2f ，未满足开仓条件" % quote.last_price)

        # 多头持仓止损策略
        elif position.pos_long > 0:
            # 在两根K线较低点减一跳，进行多头止损
            kline_low = min(klines.iloc[-2].low, klines.iloc[-3].low)
            if klines.iloc[-1].close <= kline_low - quote.price_tick:
                print("最新价为:%.2f,进行多头止损" % (quote.last_price))
                target_pos.set_target_volume(0)
            else:
                print("多头持仓，当前价格 %.2f,多头离场价格%.2f" %
                      (quote.last_price, kline_low - quote.price_tick))

        # 空头持仓止损策略
        elif position.pos_short > 0:
            # 在两根K线较高点加一跳，进行空头止损
            kline_high = max(klines.iloc[-2].high, klines.iloc[-3].high)
            if klines.iloc[-1].close >= kline_high + quote.price_tick:
                print("最新价为:%.2f 进行空头止损" % quote.last_price)
                target_pos.set_target_volume(0)
            else:
                print("空头持仓，当前价格 %.2f,空头离场价格%.2f" %
                      (quote.last_price, kline_high + quote.price_tick))
