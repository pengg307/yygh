#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import sys
__author__ = "pengg"

inarr = sys.argv[1].split(',')
klines = inarr[::-1]
cur = -2
def vodd(rindex=0):
    return klines[cur-rindex] >= klines[cur-1-rindex] \
            and klines[cur-rindex] <= klines[cur-2-rindex]
def veven(rindex=0):
    return klines[cur-rindex] <= klines[cur-1-rindex] \
            and klines[cur-rindex] >= klines[cur-2-rindex]
def v1(rindex=0):
    return klines[cur-rindex] > klines[cur-1-rindex] \
            and klines[cur-rindex] > klines[cur-2-rindex]
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
    return klines[cur-rindex] < klines[cur-1-rindex] \
            and klines[cur-rindex] < klines[cur-2-rindex]
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
print(float(klines[0])+float(klines[1]))
us = usignal(0)
vs = vsignal(0)
print("usignal:"+str(us)+", vsignal:"+str(vs))
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
