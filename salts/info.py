#!/usr/bin/env python
import  commands
import json
import requests

def role():
    information={}
    information['disk_num']=commands.getoutput('fdisk -l|grep Disk|wc -l')
    with open('/etc/sysconf/network') as f:
        for i in f.readlines():
            if i.split('=')[0]=='HOSTNAME':
                information['hostname'] = i.split('=')[1]

    return information