#!/usr/bin/env python
# _*_ coding:utf-8 -*-
import  getopt,sys


def usage():
    print u'''usage:
    -h ,--help   帮助信息
    -slbid       负载均衡id
    -bsid        后端服务器id
    -w           后端服务器权重值
    '''

try:
    options,args = getopt.getopt(sys.argv[1:],"hw:",["help","bsids=","slbid="])
except getopt.GetoptError:
    sys.stdout.write(u'参数输入错误')
    sys.exit(2)
for name,value in options:
    print  options
    if name in ("-h","--help"):
        usage()
    if name in ("--slbid",):
        print 'ip is----',value
    if name in ("--bsid",):
        print 'port is----',value
    if name in ("-w",):
        print  'wehit is ----',value