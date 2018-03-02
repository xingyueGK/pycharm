#-*- coding:utf-8 -*-
import os
import requests
import sys
import threading
import re
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
result = requests.get(headers=headers,url=url).text
print result