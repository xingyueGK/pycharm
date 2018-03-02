#!/usr/bin/env python

import urllib2
import urllib
import re
import os

def GetHtml(url):
    page = urllib2.urlopen(url)
    html = page.read().decode(encoding = 'Gb2312')
    return html
def GetImager(html):
    reg = r'(//.+?\.[pjPJ][npNP]e?[gG])'
    img = re.compile(reg)
    imglist = list(set([item.split('//')[-1] for item in  re.findall(img, html)]))
    x = 0
    path = "D:\\test\\"
    if not os.path.isdir(path):
        os.mkdir(path)
    for imgurl in imglist:
        urllib.urlretrieve('http://'+imgurl, '{}{}.jpg'.format(path, x))
        x = x + 1
    return imglist

html = GetHtml("https://item.taobao.com/item.htm?spm=a1z10.5-c-s.w4002-16391852180.15.5dba28bdI28h4Q&id=540918935842")
print(html)
print(GetImager(html))
