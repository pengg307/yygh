#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "pengg"
import logging
from datetime import date, datetime
logfile = open("logreport-"+datetime.now().strftime("%Y%m%d-%H%M%S"), encoding="utf-8", mode="w")
LOG_FORMAT = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s"
logging.basicConfig(level = logging.INFO, stream = logfile, datefmt = '%a %d %b %Y %H:%M:%S', format = LOG_FORMAT)
#logging.getLogger().setLevel(logging.INFO) 

from tqsdk import TqApi, TqAuth, TargetPosTask, TqReplay, TqBacktest
from tqsdk.ta import MA, BOLL
from datetime import date
import time, sys
from tickersalgo import bolledge_crossout, bias_crossout
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
bollup, bolldown = False, False
cur = -2
us, vs = False, False
while True:
    api.wait_update()
    #draw
    boll = BOLL(klines, 26, 2)
    # 将画图代码放在循环中即可使图像随着行情推进而更新
    #ma = MA(klines, 30)  # 使用tqsdk自带指标函数计算均线

    # 示例1: 在附图中画一根绿色的ma指标线
    klines["ma_B2"] = boll.top
    klines["ma_B2"] = boll.mid
    klines["ma_B2"] = boll.bottom
    klines["ma_B2.board"] = "B2"  # 设置附图: 可以设置任意字符串,同一字符串表示同一副图
    klines["ma_B2.color"] = "green"  # 设置为绿色. 以下设置颜色方式都可行: "green", "#00FF00", "rgb(0,255,0)", "rgba(0,125,0,0.5)"



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
        #biasup, biasdown = bias_crossout(klines) 
        #bollup, bolldown = bolledge_crossout(klines)
        if not bollup or not bolldown:
            bollup, bolldown = bollegde_crossout(klines) 

        if us :
            if position.pos_long == 0 and bolldown:   # 开多头判断
                bolldown = False
                logging.info("最新BOLLDOWN为:%.2f 开多头" % bolldown)
                print("最新价为:%.2f 开多头" % quote.last_price)
                orderbuy=api.insert_order(symbol=SYMBOL, direction="BUY", offset="OPEN", volume=1, limit_price=quote.ask_price1)
            if position.pos_short > 0:
                print("最新价为:%.2f 进行空头止win" % quote.last_price)
                orderbuy=api.insert_order(symbol=SYMBOL, direction="BUY", offset="CLOSETODAY", volume=1, limit_price=quote.ask_price1)
        if vs :
            if position.pos_short == 0 and bollup:    # 开空头判断
                bollup = False
                logging.info("最新BOLLUP为:%.2f 开空头" % bollup)
                print("最新价为:%.2f 开空头" % quote.last_price)
                ordersell=api.insert_order(symbol=SYMBOL, direction="SELL", offset="OPEN", volume=1, limit_price=quote.bid_price1)
            if position.pos_long > 0:
                print("最新价为:%.2f,进行多头止win" % (quote.last_price))
                ordersell=api.insert_order(symbol=SYMBOL, direction="SELL", offset="CLOSETODAY", volume=1, limit_price=quote.bid_price1)

