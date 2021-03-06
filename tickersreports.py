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
import time, sys
from tickersconfig import get_tickers_list
from tickersalgo import ma_multiup, ma_multidown, ma_calculate
from uvsignal import usignal, vsignal

import asyncio
import datetime
import json
import random
import websockets

#replay block
#replay = TqReplay(date(2020, 11, 5))#int(sys.argv[1])))#date of replay
#replay.set_replay_speed(2000.0)
#api = TqApi(web_gui=":16666", backtest=replay, auth=TqAuth("aimoons", "112411"))

#prof...api = TqApi(web_gui=":16666", backtest=TqBacktest(start_dt=date(2020, 10, 12), end_dt=date(2020, 10, 16)), auth=TqAuth("aimoons", "112411"))

api = TqApi(web_gui=":26789", auth=TqAuth("aimoons", "112411"))
tickers = get_tickers_list()

async def tqdata_live(websocket, path):
    while True:
        for i in tickers:
            for j in [1,5,30,240]:
                logging.info("<<<curticker>>>:"+str(i)+"curcycle:"+str(j))
                klines = api.get_kline_serial(i, j*60, 200)
                #quote = api.get_quote(i)
                #logging.info("最新time/quote:"+str(quote.datetime)+":"+str(quote.last_price))
                logging.info("最新time/kline:"+str(klines.iloc[-1].close)+","+str(klines.iloc[-2].close)+","+str(klines.iloc[-3].close))
                '''
                logging.info("[-1:-N]:"+ str(klines.iloc[-1].close)+","+str(klines.iloc[-2].close)+","+str(klines.iloc[-3].close)+","+ \
                                         str(klines.iloc[-4].close)+","+str(klines.iloc[-5].close)+","+str(klines.iloc[-6].close)+","+ \
                                         str(klines.iloc[-7].close)+","+str(klines.iloc[-8].close)+","+str(klines.iloc[-9].close)+","+ \
                                         str(klines.iloc[-10].close)+","+str(klines.iloc[-11].close)+","+str(klines.iloc[-12].close)+","+ \
                                         str(klines.iloc[-13].close)+","+str(klines.iloc[-14].close)+","+str(klines.iloc[-15].close)+","+ \
                                         str(klines.iloc[-16].close)+","+str(klines.iloc[-17].close)+","+str(klines.iloc[-18].close))
                '''
                #maslow, mafast = ma_calculate(klines)
                #logging.info(str(i)+"最新ma价@"+str(j)+",:"+str(maslow)+","+str(mafast))
                ismaup = ma_multiup(klines)
                ismadown = ma_multidown(klines)
                logging.info(str(i)+"最新@"+str(j)+",maup:"+str(ismaup)+",madown:"+str(ismadown))
                us = usignal(klines)
                vs = vsignal(klines)
                logging.info(str(i)+"最新UV价@"+str(j)+",:"+"us:"+str(us)+", vs:"+str(vs))

                #now = datetime.datetime.utcnow().isoformat() + "Z"
                now = datetime.datetime.utcnow().isoformat() + "Z" + "us:"+str(us)+", vs:"+str(vs)
                await websocket.send(now)
    api.close

start_server = websockets.serve(tqdata_live, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
