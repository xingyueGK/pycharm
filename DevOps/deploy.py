#!/usr/bin/env python
#-*- coding:utf-8 -*-

import  os
import sys
import getopt

dict_dir = {
    "appserver":"tomcat-appserver-8080",
    "trade":"tomcat-trade-8085",
    "umps":"tomcat-upms-8082",
    "yunying":"tomcat-yunying-8086",
    "fk":"tomcat-fk-8084",
    "yyserver":"tomcat-yyserver-8083",
            }

def update_package(package):
    sdir = '/home/mmuu/webapps'
    try :
        s_war_dir = os.path.join(sdir, package)
        packname = os.listdir(s_war_dir)[0]
        productdir = '/opt/'+dict_dir[package]+'/webapps/'+packname
        if packname.endswith('war'):
                cmd = '\cp {} {}'.format(s_war_dir+"/"+packname,productdir)
                os.system(cmd)
        else:
            print '文件不存在'
    except OSError as e:
        print  e
        sys.exit(1)
    except IOError as io:
        print io
        sys.exit(2)

def usage():
    usages='''usage:
    -h ,--help  帮助信息
    -stop        停止tomcat
    -start       启动tomcat
    -stauts      查看状态信息
    -d,--dirs  name        输入目录        
    '''
    print usages


if __name__ == '__main__':
    action=''
    package=''
    try:
        options, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "stop", "start", "status"])
    except getopt.GetoptError:
        print usage()
        sys.exit(2)
    for name, value in options:
        if name in ("-h", "--help"):
            usage()
        if name in ("--stop"):
            action = 'stop'
        if name in ("--start"):
            action = 'start'
        if name in ("--status"):
            action = 'status'
        if name in ("-d"):
            package = value
    print package, action
    try:
        web='/opt/'+dict_dir[package]
        os.system('/usr/bin/sh tomcat.sh {} {}'.format(web,action))
    except KeyError as e:
        print e
        sys.exit(3)

    #update_package(package)