#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "pengg"
#参考: https://www.shinnytech.com/blog/escalator/
from tqsdk import TqApi, TqAuth, TargetPosTask, TqReplay, TqBacktest
from tqsdk.ta import MA, BOLL
from datetime import date
import time, sys

# 设置合约
SYMBOL = "SHFE.ag2102"
# 设置均线长短周期
MA_SLOW, MA_FAST = 3, 5
#replay block
#replay = TqReplay(date(2020, 11, int(sys.argv[1])))
#replay.set_replay_speed(2000.0)
#api = TqApi(web_gui=":16666", backtest=replay, auth=TqAuth("aimoons", "112411"))

#prof...api = TqApi(web_gui=":16666", backtest=TqBacktest(start_dt=date(2020, 10, 12), end_dt=date(2020, 10, 16)), auth=TqAuth("aimoons", "112411"))

api = TqApi(web_gui=":26789", auth=TqAuth("aimoons", "112411"))
klines = api.get_kline_serial(SYMBOL, 60)
quote = api.get_quote(SYMBOL)
account = api.get_account()
position = api.get_position(SYMBOL)
target_pos = TargetPosTask(api, SYMBOL)
orderbuy={}
ordersell={}
limitwinlose=[2,5]

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
#print("慢速均线为%.2f,快速均线为%.2f" % (ma_slow, ma_fast))

cur = -2
def vodd(rindex=0):
    return klines.iloc[cur-rindex].close >= klines.iloc[cur-1-rindex].close \
            and klines.iloc[cur-rindex].close <= klines.iloc[cur-2-rindex].close
def veven(rindex=0):
    return klines.iloc[cur-rindex].close <= klines.iloc[cur-1-rindex].close \
            and klines.iloc[cur-rindex].close >= klines.iloc[cur-2-rindex].close
def v1(rindex=0):
    return klines.iloc[cur-rindex].close > klines.iloc[cur-1-rindex].close \
            and klines.iloc[cur-rindex].close > klines.iloc[cur-2-rindex].close
def v2(rindex=0):
    return v1(1+rindex) and veven(rindex)
def v3(rindex=0):
    return v2(1+rindex) and vodd(rindex)
def v4(rindex=0):
    return v3(1+rindex) and veven(rindex)
def v5(rindex=0):
    return v4(1+rindex) and vodd(rindex)
def v6(rindex=0):
    return v5(1+rindex) and veven(rindex)
def v7(rindex=0):
    return v6(1+rindex) and vodd(rindex)
def v8(rindex=0):
    return v7(1+rindex) and veven(rindex)
def v9(rindex=0):
    return v8(1+rindex) and vodd(rindex)
def va(rindex=0):
    return v9(1+rindex) and veven(rindex)
def vb(rindex=0):
    return va(1+rindex) and vodd(rindex)
def vc(rindex=0):
    return vb(1+rindex) and veven(rindex)
def u1(rindex=0):
    return klines.iloc[cur-rindex].close < klines.iloc[cur-1-rindex].close \
            and klines.iloc[cur-rindex].close < klines.iloc[cur-2-rindex].close
def u2(rindex=0):
    return u1(1+rindex) and vodd(rindex)
def u3(rindex=0):
    return u2(1+rindex) and veven(rindex)
def u4(rindex=0):
    return u3(1+rindex) and vodd(rindex)
def u5(rindex=0):
    return u4(1+rindex) and veven(rindex)
def u6(rindex=0):
    return u5(1+rindex) and vodd(rindex)
def u7(rindex=0):
    return u6(1+rindex) and veven(rindex)
def u8(rindex=0):
    return u7(1+rindex) and vodd(rindex)
def u9(rindex=0):
    return u8(1+rindex) and veven(rindex)
def ua(rindex=0):
    return u9(1+rindex) and vodd(rindex)
def ub(rindex=0):
    return ua(1+rindex) and veven(rindex)
def uc(rindex=0):
    return ub(1+rindex) and vodd(rindex)
def usignal(z=0):
    return v1 and (u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1) or u7(1) or u8(1) or u9(1) or ua(1) or ub(1) or uc(1))
def vsignal(z=0):
    return u1 and (v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1) or v7(1) or v8(1) or v9(1) or va(1) or vb(1) or vc(1))
us, vs = False, False
while True:
    api.wait_update()
    # 每次k线更新，重新计算快慢均线
    if api.is_changing(klines.iloc[-1], "datetime"):
        print("iloc[-1:-10]:", klines.iloc[-1].close,",",klines.iloc[-2].close,",",klines.iloc[-3].close,",", \
                               klines.iloc[-4].close,",",klines.iloc[-5].close,",",klines.iloc[-6].close,",", \
                               klines.iloc[-7].close,",",klines.iloc[-8].close,",",klines.iloc[-9].close,",", \
                               klines.iloc[-10].close,",",klines.iloc[-11].close,",",klines.iloc[-12].close)
        us = usignal(0)
        vs = vsignal(0)
        #print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        print("us:"+str(us)+", vs:"+str(vs)+",最新价", str(quote.datetime), str(quote.last_price),",profit:"+str(position.float_profit_long) + str(position.float_profit_short)+",acctprofit:"+str(account.float_profit))
        boll=BOLL(klines, 26, 2)
        bollmid = list(boll["mid"])[-2]
        booltop = list(boll["top"])[-2]
        boolbtm = list(boll["bottom"])[-2]
        print("boll:", list(boll["top"])[-2], list(boll["mid"])[-2], list(boll["bottom"])[-2])
        if vs :
           api.draw_text(klines, "V", x=-1, y=klines.iloc[-1].close - 5, color=0xFFFF3333)
        if us :
           api.draw_text(klines, "U", x=-1, y=klines.iloc[-1].close + 5, color=0xAAAA6666)
    #if api.is_changing(quote, "last_price"):
        if api.is_changing(orderbuy):
            print("buy单状态: %s, 已成交: %d 手" % (orderbuy.status, orderbuy.volume_orign - orderbuy.volume_left))
        if api.is_changing(ordersell):
            print("sell单状态: %s, 已成交: %d 手" % (ordersell.status, ordersell.volume_orign - ordersell.volume_left))
        # 当行情有变化且当前挂单价格不优时，则撤单
        if orderbuy and api.is_changing(quote) and orderbuy.status == "ALIVE" and quote.bid_price1 > orderbuy.limit_price:
            print("价格改变，撤单重下")
            api.cancel_order(orderbuy)
        if ordersell and api.is_changing(quote) and ordersell.status == "ALIVE" and quote.ask_price1 < ordersell.limit_price:
            print("价格改变，撤单重下")
            api.cancel_order(ordersell)
        # 开仓判断
        if position.pos_long == 0 and position.pos_short == 0:
            # 开多头判断
            if us and quote.last_price > bollmid :
                print("最新价为:%.2f 开多头" % quote.last_price)
                #target_pos.set_target_volume(10)
                orderbuy=api.insert_order(symbol=SYMBOL, direction="BUY", offset="OPEN", volume=1, limit_price=quote.bid_price1)
                #while order.status != "FINISHED":
                #  api.wait_update()
                #print("已开多仓",quote.ask_price1)
            # 开空头判断，最近一根K线收盘价在短期均线和长期均线之下，前一根K线收盘价位于K线波动范围顶部25%，最近这根K线收盘价位于K线波动范围底部25%
            #elif klines.iloc[-2].close < min(ma_slow, ma_fast) and kl_range_pre >= 0.75 and kl_range_cur <= 0.25:
            elif vs and quote.last_price < bollmid :
                print("最新价为:%.2f 开空头" % quote.last_price)
                #target_pos.set_target_volume(-10)
                ordersell=api.insert_order(symbol=SYMBOL, direction="SELL", offset="OPEN", volume=1, limit_price=quote.ask_price1)
                #while order.status != "FINISHED":
                #  api.wait_update()
                #print("已开空仓",quote.bid_price1)
            else:
                #print("最新价位:%.2f ，未满足开仓条件" % quote.last_price)
                cur
        # 多头持仓止损策略
        elif position.pos_long > 0:
            # 在两根K线较低点减一跳，进行多头止损
            #kline_low = min(klines.iloc[-2].low, klines.iloc[-3].low)
            #if klines.iloc[-1].close <= kline_low - quote.price_tick:
            if vs and position.open_price_long < quote.last_price + limitwinlose[1]*2 :
                print("最新价为:%.2f,进行多头止win" % (quote.last_price))
                #target_pos.set_target_volume(0)
                ordersell=api.insert_order(symbol=SYMBOL, direction="SELL", offset="CLOSETODAY", volume=1, limit_price=quote.bid_price1)
                #while order.status != "FINISHED":
                #  api.wait_update()
                #print("已平多今",quote.bid_price1)
            elif position.open_price_long >  quote.last_price + limitwinlose[0]*2 :
                #print("多头持仓，当前价格 %.2f,多头离场价格%.2f" %
                  #    (quote.last_price, kline_low - quote.price_tick))
                print("最新价为:%.2f,进行多头止损" % (quote.last_price))
                ordersell=api.insert_order(symbol=SYMBOL, direction="SELL", offset="CLOSETODAY", volume=1, limit_price=quote.bid_price1)
                #while order.status != "FINISHED":
                #  api.wait_update()
                #print("已平多今to, from,",quote.bid_price1, position.open_price_long)
                  

        # 空头持仓止损策略
        elif position.pos_short > 0:
            # 在两根K线较高点加一跳，进行空头止损
            #kline_high = max(klines.iloc[-2].high, klines.iloc[-3].high)
            #if klines.iloc[-1].close >= kline_high + quote.price_tick:
            if us and position.open_price_short > quote.last_price + limitwinlose[1]*2 :
                print("最新价为:%.2f 进行空头止win" % quote.last_price)
                #target_pos.set_target_volume(0)
                orderbuy=api.insert_order(symbol=SYMBOL, direction="BUY", offset="CLOSETODAY", volume=1, limit_price=quote.ask_price1)
                #while order.status != "FINISHED":
                #  api.wait_update()
                #print("已平空今",quote.ask_price1)
            elif position.open_price_short < quote.last_price - limitwinlose[0]*2 :
                #print("空头持仓，当前价格 %.2f,空头离场价格%.2f" %
                 #     (quote.last_price, kline_high + quote.price_tick))
                print("最新价为:%.2f,进行空头止损" % (quote.last_price))
                orderbuy=api.insert_order(symbol=SYMBOL, direction="BUY", offset="CLOSETODAY", volume=1, limit_price=quote.ask_price1)
                #while order.status != "FINISHED":
                #  api.wait_update()
                #print("已平空今to, from,",quote.ask_price1, position.open_price_short)

