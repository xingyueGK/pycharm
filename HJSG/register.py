import requests
import sys
import time
import json

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
    # 'Accept-Encoding':'gzip, deflate',
    # 'Accept-Language':'zh-CN,zh;q=0.8',
    # 'Connection':'keep-alive',
    'Host':'uc.game.hanjiangsanguo.com',
    # 'Upgrade-Insecure-Requests':'1',
    # 'Content-Type':'application/json',
    # 'DNT':'1',
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
proxies = {
            "http": "http://163.125.233.27:8118",
}
userlist= ['zhu  '  ,
'qin  '  ,
'you  '  ,
'xu   '  ,
'he   '  ,
'lv   '  ,
'shi  '  ,
'zhang'  ,
'kong '  ,
'cao  '  ,
'yan  '  ,
'hua  '  ,
'jin  '  ,
'tao  '  ,
'jiang'  ,
'qi   '  ,
'xie  '  ,
'zou  '  ,
'yu   '  ,
'bai  '  ,
'shui '  ,
'dou  '  ,
'yun  '  ,
'su   '  ,
'pan  '  ,
'ge   '  ,
'fan  '  ,
'peng '  ,
'lang '  ,
'miao '  ,
'fang '  ,
'ren  '  ,
'yuan '  ,
'liu  '  ,
'bao  '  ,]
for i in userlist:
    str = i.strip()
    name = str + 'yue123a'
    print name
    url = 'http://uc.game.hanjiangsanguo.com/index.php?c=register&m=reg&u=%s&p=413728161&mobile=18910598793&mac=00:FF:7B:F0:5D:DD&32d7d8f515a95064d2d36ce16330a846=c5e55009d72507b33ba7beecbf680550&v=2017111501&channel=11&imei=NoDeviceId&platform=android&token_uid=&token=&mac=00:FF:7B:F0:5D:DD&gps_adid=&android_id=00ff7bf05ddd9502&rand=1511767171 HTTP/1.1' % name
    print requests.get(url).text
    time.sleep(1)




# for  i in  'abcdefghijklmnopqrstuvwxyz':
#     str = i + 'a'
#     url = 'http://uc.game.hanjiangsanguo.com/index.php?c=register&m=reg&u=%s&p=413728161&mobile=18910598793&mac=00:FF:7B:F0:5D:DD&32d7d8f515a95064d2d36ce16330a846=c5e55009d72507b33ba7beecbf680550&v=2017111501&channel=11&imei=NoDeviceId&platform=android&token_uid=&token=&mac=00:FF:7B:F0:5D:DD&gps_adid=&android_id=00ff7bf05ddd9502&rand=1511767171 HTTP/1.1' % str
#     print requests.get(url).text
#     time.sleep(1)