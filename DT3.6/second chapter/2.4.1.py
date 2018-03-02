#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import re
#print(range(1,100,2))
str='你好$$$我正在学 python@#@#我需要*#*#*#修改字符串'
str2 = str.replace('$$$',' ').replace('@#@#',' ').replace("*#*#*#",' ')
print(str2)
a=1
def fun(a):
    a=2
fun(a)
print a
var = 1
def fun():
    print var
    var = 200
print fun()
