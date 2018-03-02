#!/usr/bin/evn python3
#-*- coding:utf-8 -*-

import requests
from  bs4 import  BeautifulSoup
url = 'http://www.santostang.com/'

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}

html = requests.get(url,headers=headers)

soup = BeautifulSoup(html.text,'lxml')

title = soup.find('h1',class_="post-title").a.text.strip()
with open(r'title.txt','a') as  f:
    f.write(title)
    f.close()