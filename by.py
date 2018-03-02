# -*- coding:utf-8 -*-
import urllib,re
#获取网页源码
def gethtml():
    papg = urllib.urlopen('http://www.wmpic.me/meinv')
    html = papg.read()
    return html
x = 0
#匹配图片下载
def getimg(html):
    imgre = re.compile(r' src="(.*?)" class=') #提高效率
    imglist = re.findall(imgre,html) #匹配，列表的形式返回
    for imgurl in imglist:
        print imgurl #打印图片地址
        global x #重新赋值
        urllib.urlretrieve(imgurl,'D:\\python\%s.jpg'%x) #下载
        x += 1
        print ("正在下载第%s张"%x)
html = gethtml()
getimg(html)



