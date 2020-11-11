#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "pengg"
#参考: https://www.shinnytech.com/blog/escalator/
from tqsdk import TqApi, TqAuth, TargetPosTask, TqReplay, TqBacktest
from tqsdk.ta import MA, BOLL
from datetime import date
import time, sys
from tickersalgo import bias_crossout
from uvsignal import usignal, vsignal

# 设置合约
SYMBOL = "SHFE.ag2102"
# 设置均线长短周期
MA_SLOW, MA_FAST = 3, 5
#replay block
#replay = TqReplay(date(2020, 11, 6))#int(sys.argv[1])))
#replay.set_replay_speed(2000.0)
#api = TqApi(web_gui=":16666", backtest=replay, auth=TqAuth("aimoons", "112411"))

#prof...api = TqApi(web_gui=":16666", backtest=TqBacktest(start_dt=date(2020, 10, 12), end_dt=date(2020, 10, 16)), auth=TqAuth("aimoons", "112411"))

api = TqApi(web_gui=":19876", auth=TqAuth("aimoons", "112411"))
klines = api.get_kline_serial(SYMBOL, 30)
quote = api.get_quote(SYMBOL)
account = api.get_account()
position = api.get_position(SYMBOL)
target_pos = TargetPosTask(api, SYMBOL)
orderbuy={}
ordersell={}
limitwinlose=[3,7]

biasup, biasdown = False, False
cur = -2
us, vs = False, False
while True:
    api.wait_update()
    # 每次k线更新，重新计算快慢均线
    if api.is_changing(klines.iloc[-1], "datetime"):
        print("iloc[-1:-N]:", klines.iloc[-1].close,",",klines.iloc[-2].close,",",klines.iloc[-3].close,",", \
                               klines.iloc[-4].close,",",klines.iloc[-5].close,",",klines.iloc[-6].close,",", \
                               klines.iloc[-7].close,",",klines.iloc[-8].close,",",klines.iloc[-9].close,",", \
                               klines.iloc[-10].close,",",klines.iloc[-11].close,",",klines.iloc[-12].close,",", \
                               klines.iloc[-13].close,",",klines.iloc[-14].close,",",klines.iloc[-15].close,",", \
                               klines.iloc[-16].close,",",klines.iloc[-17].close,",",klines.iloc[-18].close)
        us = usignal(klines)
        vs = vsignal(klines)
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
        biasup, biasdown = bias_crossout(klines) 
        if not biasup or not biasdown:
            biasup, biasdown = bias_crossout(klines) 

        if us :
            if position.pos_long == 0 :# and biasdown:   # 开多头判断
                biasdown = False
                print("最新价为:%.2f 开多头" % quote.last_price)
                orderbuy=api.insert_order(symbol=SYMBOL, direction="BUY", offset="OPEN", volume=1, limit_price=quote.ask_price1)
            if position.pos_short > 0:
                print("最新价为:%.2f 进行空头止win" % quote.last_price)
                orderbuy=api.insert_order(symbol=SYMBOL, direction="BUY", offset="CLOSETODAY", volume=1, limit_price=quote.ask_price1)
        if vs :
            if position.pos_short == 0 :#and biasup:    # 开空头判断
                biasup = False
                print("最新价为:%.2f 开空头" % quote.last_price)
                ordersell=api.insert_order(symbol=SYMBOL, direction="SELL", offset="OPEN", volume=1, limit_price=quote.bid_price1)
            if position.pos_long > 0:
                print("最新价为:%.2f,进行多头止win" % (quote.last_price))
                ordersell=api.insert_order(symbol=SYMBOL, direction="SELL", offset="CLOSETODAY", volume=1, limit_price=quote.bid_price1)

