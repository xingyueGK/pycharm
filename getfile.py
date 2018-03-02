#!/usr/bin/python
#  -*- coding: utf-8 -*-
import os, sys
import paramiko
hostname = '10.28.57.122'
port = 4513
username = 'mmuu'
password = 'mmuu_root_!@#'
local_path = '/home/mmuu/system.war'
remote_path = '/home/mmuu/system.war'
try:
    s = paramiko.Transport((hostname, port))
    s.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(s)
except Exception as e:
    print e
    sys.exit(1)
try:
    # 判断远程服务器是否有这个文件
    sftp.file(remote_path)          # 使用get()方法从远程服务器拉去文件
    sftp.get(remote_path, local_path)
except IOError as e:
        print remote_path + "remote file not exist!"
        sys.exit(1)
finally:
        s.close()
# 测试是否下载成功
if os.path.isfile(local_path):
    print "下载成功."
else:
    print "下载失败!"