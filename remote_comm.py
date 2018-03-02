#!/usr/bin/env python
# -*- coding: utf8 -*-

import paramiko
import threading
import os
import sys
#远程并发连接主机实现命令的执行 给出参数，自动并发执行命令
def remote_comm(host, pwd, comm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    ) # 回答yes
    ssh.connect(host, username='root', password=pwd)
    stdin, stdout, stderr = ssh.exec_command(comm)
    out = stdout.read()
    err = stderr.read()
    if out:
        print "[%s]out:\n%s" % (host, out)
    if err:
        print "[%s]error:\n%s" % (host, err)
    ssh.close()

if __name__ == '__main__':   #判断是否是脚本自己执行的命令 如果是脚本自己执行则做如下操作  
    if len(sys.argv) != 4:
        print "Usage: %s ipfile password 'comm'" % sys.argv[0]
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print "No such file:", sys.argv[1]
        sys.exit(2)

    ipfile = sys.argv[1]
    pwd = sys.argv[2]
    comm = sys.argv[3]

    with open(ipfile) as fobj:
        for line in fobj:
            ip = line.strip() # 去除字符串两端空白
            t = threading.Thread(
                target=remote_comm, args=(ip, pwd, comm)
            )
            t.start()
