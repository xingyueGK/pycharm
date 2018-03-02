#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
header = {
    'Host':'movie.douban.com',
    'Referer':'https://movie.douban.com/top250',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
for i in range(0,10):
    url = 'https://movie.douban.com/top250?'+str(i*25)
    r=requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    div_list = soup.find_all('div',class_='item')
    #print(div_list)
    for each in div_list:
        top = each.div.em.text


        #print(each.div)
import requests
import json


def single_page_comment(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(link, headers=headers)
    # 获取 json 的 string
    json_string = r.text
    json_string = json_string[json_string.find('{'):-2]
    json_data = json.loads(json_string)
    comment_list = json_data['results']['parents']

    for eachone in comment_list:
        message = eachone['content']
        print (message)


for page in range(1, 4):
    link1 = "https://api-zero.livere.com/v1/comments/list?callback=jQuery112407875296433383039_1506267778283&limit=10&offset="
    link2 = "&repSeq=3871836&requestPath=%2Fv1%2Fcomments%2Flist&consumerSeq=1020&livereSeq=28583&smartloginSeq=5154&_=1506267778285"
    page_str = str(page)
    link = link1 + page_str + link2
    print (link)
    single_page_comment(link)