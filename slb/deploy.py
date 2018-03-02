#!/usr/bin/python
#  -*- coding: utf-8 -*-

#运营平台部署

import os,sys,getopt
import paramiko
import  time
WEB_DIR='/opt/tomcat-7.0.77-A'
mifeng_web='/opt/tomcat-7.0.77-A/webapps/mifeng'
system_dir='/home/mmuu'
back_dir='/opt/backup'
hostname = '10.27.218.193'
port = 4513
username = 'usernamd'
password = 'password'
local_path = '/home/mmuu/system.war'
remote_path = '/home/mmuu/system.war'
#获取tomcat进程ID
pid=os.popen("ps aux |grep logging.config.file=/opt/tomcat-7.0.77-A |grep -v grep  |awk '{print $2}'").read()
def getfile(username,hostname,password,port,remote_path,local_path):
    try:
        s = paramiko.Transport((hostname,port))
        s.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(s)
    except Exception as e:
        print e
        sys.exit(1)
    try:
        # 判断远程服务器是否有这个文件
        sftp.file(remote_path)
        # 使用get()方法从远程服务器拉去文件
        sftp.get(remote_path, local_path)
    except IOError as e:
            print e
            print remote_path + "remote file not exist!"
            sys.exit(1)
    finally:
            s.close()
    # 测试是否下载成功
    if os.path.isfile(local_path):
        print "下载成功."
    else:
        print "下载失败!"

def  stop():
    if pid :
        os.system('%s/bin/shutdown.sh'%WEB_DIR)
        if pid:
            os.system('kill %s'%pid)
    else:
        print 'tomcat not runing'
def start():
    os.system('%s/bin/startup.sh'%WEB_DIR)

def deploy(version):
    os.system("mv %s/system.war  %s/system.$s.war"%(system_dir,back_dir,version)) #备份上次war包
    getfile(username, hostname, password, port,remote_path, local_path)#从测试环境拉去war包
    print '关闭tomcat'
    stop()
    time.sleep(3)
    os.chdir(mifeng_web)
    os.system("rm  -rf *")
    print  '正在部署system'
    os.system('cp /home/mmuu/system.war .;jar -xf system.war;rm -rf system.war')
    os.system('\cp /opt/config/*  %s/WEB-INF/classes/;\cp /opt/js/* %s/system/js/filter/'%(mifeng_web,mifeng_web))
    start()
    print  '部署完成'
def usage():
    print '''usage:
    -h ,--help   帮助信息
    -id          服务器id信息
    -w           后端服务器权重值    
    '''

try:
    options,args = getopt.getopt(sys.argv[1:],"hw:id:",["help","id=","weight="])
except getopt.GetoptError:
    sys.exit(2)

print  options,args
for name,value in options:
    if name in ("-h","--help"):
        usage()
    if name in ("-id","--ip"):
        print 'ip is----',value
    if name in ("-w","--weight"):
        pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s deploy" % sys.argv[0]
        sys.exit(1)
    version=sys.argv[1]
