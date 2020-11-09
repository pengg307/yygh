#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "pengg"
from tqsdk import TqApi, TqAuth, TargetPosTask, TqReplay, TqBacktest
from tqsdk.ta import MA, BOLL
from datetime import date
import time, sys

cur = -2
def vodd(klines, rindex=0):
    return klines.iloc[cur-rindex].close >= klines.iloc[cur-1-rindex].close \
            and klines.iloc[cur-rindex].close <= klines.iloc[cur-2-rindex].close
def veven(klines, rindex=0):
    return klines.iloc[cur-rindex].close <= klines.iloc[cur-1-rindex].close \
            and klines.iloc[cur-rindex].close >= klines.iloc[cur-2-rindex].close
def v1(klines, rindex=0):
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
def u1(klines, rindex=0):
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
    return v1(0) and (u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1) or u7(1) or u8(1) or u9(1) or ua(1) or ub(1) or uc(1))
def vsignal(z=0):
    return u1(0) and (v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1) or v7(1) or v8(1) or v9(1) or va(1) or vb(1) or vc(1))

