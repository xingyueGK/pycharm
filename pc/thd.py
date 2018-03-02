#-*- coding:utf-8 -*-

import  time
now_time = time.strftime('%H:%M:%S')
while True:
    now_time = time.strftime('%H:%M:%S')
    if now_time >= '10:23:00':
        print now_time
        exit(1)
    else:
        print '1'
