#-*- coding:utf-8 -*-
import time
def  now():
    print '2018-01-17'

f=now
print f.__name__
print \
    now.__name__

def log(func):
    def wrapper(*args,**kwargs):
        print 'call %s:'%func.__name__
        return func(*args,**kwargs)
    return wrapper