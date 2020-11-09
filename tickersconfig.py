#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "pengg"



def get_tickers_list():
    #SHFE上海期货交易所 DCE#大连商品交易所    CZCE#郑州商品交易所
    markets = ["SHFE","DCE","CZCE"]
    tickers = [["au","ag","rb","cu"],
               ["m","i","p"],
               ["ta","ma"]]
    yrmons = ["2102","2103","2101"]
    tickerslist = ["SHFE.ag2102","DCE.m2101","SHFE.au2102","DCE.i2102"]#,"CZCE.ta101","CZCE.ma101"]
    
    #for i in markets:
    #    for j markets.index(i)
    return tickerslist

print("tickers:", get_tickers_list())
