#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "pengg"
from tqsdk.ta import MA, BOLL, BIAS
import logging

cur = -1
CYCLE = [5,20,60]

def ma_multiup(klines):
    isup = True
    for i in range(len(CYCLE)) :
        if (i+1<len(CYCLE)) and isup :
            short_avg = MA(klines, CYCLE[i]).iloc[cur].ma
            long_avg = MA(klines, CYCLE[i+1]).iloc[cur].ma
            #logging.info("short_avg:"+str(CYCLE[i])+":"+str(short_avg))
            #logging.info("long_avg:"+str(CYCLE[i+1])+":"+str(long_avg))
            isup = isup and short_avg>long_avg
    return isup

def ma_multidown(klines):
    isdown = True
    for i in range(len(CYCLE)) :
        if (i+1<len(CYCLE)) and isdown :
            short_avg = MA(klines, CYCLE[i]).iloc[cur].ma
            long_avg = MA(klines, CYCLE[i+1]).iloc[cur].ma
            #logging.info("short_avg:"+str(CYCLE[i])+":"+str(short_avg))
            #logging.info("long_avg:"+str(CYCLE[i+1])+":"+str(long_avg))
            isdown = isdown and short_avg<long_avg
    return isdown

def crossdown(short_avg, long_avg):
    return long_avg.iloc[-2] < short_avg.iloc[-2] and long_avg.iloc[-1] > short_avg.iloc[-1]

def crossup(short_avg, long_avg):
    return short_avg.iloc[-2] < long_avg.iloc[-2] and short_avg.iloc[-1] > long_avg.iloc[-1]

def bollzone(klines):
    boll = BOLL(klines, 26, 2)
    upper = boll["top"] - boll["mid"]
    lower = boll["mid"] - boll["bottom"]
    logging.info("boll:upper:"+str(boll["top"])+",mid:"+str(boll["mid"])+",lower:"+str(boll["lower"]))
    return upper, lower, upper+lower

def bolledge_crossout(klines):
    upper, lower, height = bollzone(klines)
    crossup = klines.iloc[cur].close > upper
    crossdown = klines.iloc[cur].close < lower
    return crossup, crossdown

def bias_crossout(klines):
    bias = BIAS(klines, 20)
    crossup, crossdown = False, False
    #logging.info("bias:"+";".join(list(bias["bias"])))
    #print("bias--:",list(bias.iloc[-1:-5:-1].bias))
    if max(bias.iloc[-2:-20:-1].bias) <= bias.iloc[-1].bias:
        crossup = True
        logging.info("crossup:True")
        logging.info(str(bias.iloc[-2].bias)+"<="+str(bias.iloc[-1].bias))
    elif min(bias.iloc[-2:-20:-1].bias) >= bias.iloc[-1].bias:
        crossdown = True
        logging.info("crossdown:True")
        logging.info(str(bias.iloc[-2].bias)+"=>"+str(bias.iloc[-1].bias))
    return crossup, crossdown

def ma_calculate(klines):
    ma_slow = MA(klines, CYCLE[0]).iloc[-1].ma
    ma_fast = MA(klines, CYCLE[1]).iloc[-1].ma
    return ma_slow, ma_fast

