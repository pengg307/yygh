#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import sys
__author__ = "pengg"

#inarr = sys.argv[1].split(',')
#klines = inarr[::-1]
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
def v2(klines, rindex=0):
    return v1(klines, 1+rindex) and veven(klines, rindex)
def v3(klines, rindex=0):
    return v2(klines, 1+rindex) and vodd(klines, rindex)
def v4(klines, rindex=0):
    return v3(klines, 1+rindex) and veven(klines, rindex)
def v5(klines, rindex=0):
    return v4(klines, 1+rindex) and vodd(klines, rindex)
def v6(klines, rindex=0):
    return v5(klines, 1+rindex) and veven(klines, rindex)
def v7(klines, rindex=0):
    return v6(klines, 1+rindex) and vodd(klines, rindex)
def v8(klines, rindex=0):
    return v7(klines, 1+rindex) and veven(klines, rindex)
def v9(klines, rindex=0):
    return v8(klines, 1+rindex) and vodd(klines, rindex)
def va(klines, rindex=0):
    return v9(klines, 1+rindex) and veven(klines, rindex)
def vb(klines, rindex=0):
    return va(klines, 1+rindex) and vodd(klines, rindex)
def vc(klines, rindex=0):
    return vb(klines, 1+rindex) and veven(klines, rindex)
def u1(klines, rindex=0):
    return klines.iloc[cur-rindex].close < klines.iloc[cur-1-rindex].close \
            and klines.iloc[cur-rindex].close < klines.iloc[cur-2-rindex].close
def u2(klines, rindex=0):
    return u1(klines, 1+rindex) and vodd(klines, rindex)
def u3(klines, rindex=0):
    return u2(klines, 1+rindex) and veven(klines, rindex)
def u4(klines, rindex=0):
    return u3(klines, 1+rindex) and vodd(klines, rindex)
def u5(klines, rindex=0):
    return u4(klines, 1+rindex) and veven(klines, rindex)
def u6(klines, rindex=0):
    return u5(klines, 1+rindex) and vodd(klines, rindex)
def u7(klines, rindex=0):
    return u6(klines, 1+rindex) and veven(klines, rindex)
def u8(klines, rindex=0):
    return u7(klines, 1+rindex) and vodd(klines, rindex)
def u9(klines, rindex=0):
    return u8(klines, 1+rindex) and veven(klines, rindex)
def ua(klines, rindex=0):
    return u9(klines, 1+rindex) and vodd(klines, rindex)
def ub(klines, rindex=0):
    return ua(klines, 1+rindex) and veven(klines, rindex)
def uc(klines, rindex=0):
    return ub(klines, 1+rindex) and vodd(klines, rindex)
def usignal(klines):
    return v1(klines) and (u1(klines,1) or u2(klines, 1) or u3(klines, 1) or u4(klines, 1) or u5(klines, 1) or u6(klines, 1) or u7(klines, 1) or u8(klines, 1) or u9(klines, 1) or ua(klines, 1) or ub(klines, 1) or uc(klines, 1))
def vsignal(klines):
    return u1(klines) and (v1(klines, 1) or v2(klines, 1) or v3(klines, 1) or v4(klines, 1) or v5(klines, 1) or v6(klines, 1) or v7(klines, 1) or v8(klines, 1) or v9(klines, 1) or va(klines, 1) or vb(klines, 1) or vc(klines, 1))
us, vs = False, False
#us = usignal(klines)
#vs = vsignal(klines)
#print(float(klines.iloc[0].close)+float(klines.iloc[1].close))
#print("usignal:"+str(us)+", vsignal:"+str(vs))
'''
print("v1:"+str(v1(0)) \
+",u1:"+str(u1(1)) \
+",u2:"+str(u1(1) or u2(1)) \
+",u3:"+str(u1(1) or u2(1) or u3(1)) \
+",u4:"+str(u1(1) or u2(1) or u3(1) or u4(1)) \
+",u5:"+str(u1(1) or u2(1) or u3(1) or u4(1) or u5(1)) \
+",u6:"+str(u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1)) \
+",u7:"+str(u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1) or u7(1)) \
+",u8:"+str(u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1) or u7(1) or u8(1)) \
+",u9:"+str(u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1) or u7(1) or u8(1) or u9(1)) \
+",ua:"+str(u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1) or u7(1) or u8(1) or u9(1) or ua(1)) \
+",ub:"+str(u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1) or u7(1) or u8(1) or u9(1) or ua(1) or ub(1)) \
+",uc:"+str(u1(1) or u2(1) or u3(1) or u4(1) or u5(1) or u6(1) or u7(1) or u8(1) or u9(1) or ua(1) or ub(1) or uc(1)))
print("u1:"+str(u1(0)) \
+",v1:"+str(v1(1)) \
+",v2:"+str(v1(1) or v2(1)) \
+",v3:"+str(v1(1) or v2(1) or v3(1)) \
+",v4:"+str(v1(1) or v2(1) or v3(1) or v4(1)) \
+",v5:"+str(v1(1) or v2(1) or v3(1) or v4(1) or v5(1)) \
+",v6:"+str(v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1)) \
+",v7:"+str(v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1) or v7(1)) \
+",v8:"+str(v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1) or v7(1) or v8(1)) \
+",v9:"+str(v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1) or v7(1) or v8(1) or v9(1)) \
+",va:"+str(v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1) or v7(1) or v8(1) or v9(1) or va(1)) \
+",vb:"+str(v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1) or v7(1) or v8(1) or v9(1) or va(1) or vb(1)) \
+",vc:"+str(v1(1) or v2(1) or v3(1) or v4(1) or v5(1) or v6(1) or v7(1) or v8(1) or v9(1) or va(1) or vb(1) or vc(1)))
'''
