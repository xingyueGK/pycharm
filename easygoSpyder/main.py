#! /usr/local/bin/python3
#-*- coding: utf-8 -*-
# __author__ = "Brady Hu"
# __date__ = 2017/10/16 16:11

from selenium import webdriver
import requests
import json
import time
import os
import settings
import transCoordinateSystem
import sys

#创建一个异常类，用于在cookie失效时抛出异常
class CookieException(Exception):
    def __init__(self):
        Exception.__init__(self)

def main():
    """爬虫主程序，负责控制时间抓取"""
    qq_number_sides = 0
    while True:
        time_now = time.time()
        time_now_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time_now))
        print("此轮抓取开始")
        cookie = get_cookie(qq_number_sides)
        i = 1
        qq_number_sides += 1
        spyder_list = spyder_list_all()
        for item in spyder_list:

            """这部分负责每个qq号码抓取的次数"""
            if i% settings.fre == 0:
                cookie = get_cookie(qq_number_sides)
                qq_number_sides += 1


            params = spyder_params(item)
            try:
                text = spyder(cookie, params)
                save(text, time_now_str, file_name="淮阳" + time_now_str+".txt")
            except CookieException as e:
                cookie = get_cookie(qq_number_sides)
                qq_number_sides += 1
                text = spyder(cookie, params)
                save(text, time_now_str, file_name="淮阳" + time_now_str+".txt")
            i+=1
            view_bar(i,len(spyder_list))
        print("此轮抓取完成")
        time.sleep(settings.sleeptime-int(time.time()-time_now))
        qq_number_sides += 1




def get_cookie(num):
    """负责跟据传入的qq号位次，获得对应的cookie并返回，以便用于爬虫"""
    chromedriver = r'C:\Users\Administrator\Desktop\chromedriver.exe'
    os.environ["webdriver.chrme.driver"] = chromedriver
    chrome_login = webdriver.Chrome(chromedriver)
    chrome_login.get(
        "http://c.easygo.qq.com/eg_toc/map.html?origin=csfw&cityid=110000")
    chrome_login.find_element_by_id("u").send_keys(settings.qq_list[num][0])
    chrome_login.find_element_by_id("p").send_keys(settings.qq_list[num][1])
    chrome_login.maximize_window()
    chrome_login.find_element_by_id("go").click()
    time.sleep(5)
    cookies = chrome_login.get_cookies()
    chrome_login.quit()
    user_cookie = {}
    for cookie in cookies:
        user_cookie[cookie["name"]] = cookie["value"]

    return user_cookie


def spyder(user_cookie, params):
    """根据传入的表单，利用cookie抓取宜出行后台数据"""
    user_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Referer": "http://c.easygo.qq.com/eg_toc/map.html?origin=csfw"
    }
    url = "http://c.easygo.qq.com/api/egc/heatmapdata"
    while True:
        try:
            r = requests.get(url, headers=user_header,
                             cookies=user_cookie, params=params)
            # print(r.status_code)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print(e.args)
        break

def spyder_params(item):
    """将传入的块转化为网页所需的表单"""
    lng_min,lng_max,lat_min,lat_max = item
    lng_min,lat_min = transCoordinateSystem.wgs84_to_gcj02(lng_min,lat_min)
    lng_max,lat_max = transCoordinateSystem.wgs84_to_gcj02(lng_max,lat_max)
    lng = (lng_min+lng_max)*0.5
    lat = (lat_min+lat_max)*0.5
    params = {"lng_min": lng_min,
                "lat_max": lat_max,
                "lng_max": lng_max,
                "lat_min": lat_min,
                "level": 16,
                "city": "%E9%A9%AC%E9%9E%8D%E5%B1%B1",
                "lat": lat,
                "lng": lng,
                "_token": ""}
    return params

def save(text, time_now,file_name):
    """将抓取下来的流数据处理保存到文本文件"""

    #判断文件是否存在，若不存在则创建文件并写入头
    try:
        with open(file_name,'r') as f:
            f.readline()
    except FileNotFoundError as e:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write('count,wgs_lng,wgs_lat,time\n')
    #写入数据
    with open(file_name, "a", encoding="utf-8") as f:
        node_list = json.loads(text)["data"]
        try:
            min_count = node_list[0]["count"]
            for i in node_list:
                min_count = min(i['count'],min_count)
            for i in node_list:
                i['count'] = i['count']/min_count
                gcj_lng = 1e-6 * (250.0 * i['grid_x'] + 125.0) #此处的算法在宜出行网页后台的js可以找到，文件路径是http://c.easygo.qq.com/eg_toc/js/map-55f0ea7694.bundle.js
                gcj_lat = 1e-6 * (250.0 * i['grid_y'] + 125.0)
                lng, lat = transCoordinateSystem.gcj02_to_wgs84(gcj_lng, gcj_lat)
                f.write(str(i['count'])+","+str(lng)+","+str(lat)+","+time_now+"\n")
        except IndexError as e:
            pass
            # print("此区域没有点信息")
        except TypeError as e:
            print(node_list)
            raise CookieException

def spyder_list_all():
    """获取所需爬取的所有块"""
    spyder_list_all = []
    templng = settings.lng_min
    while templng < settings.lng_max:
        templat = settings.lat_min
        while templat < settings.lat_max:
            spyder_list_all.append([round(templng,5),round(templng+settings.lng_delta,5),round(templat,5),round(templat+settings.lat_delta,5)])
            templat += settings.lat_delta
        templng += settings.lng_delta
    return spyder_list_all

def view_bar(num, total):
    rate = float(num) / float(total)
    rate_num = int(rate * 100)
    r = '\r[%s%s]%d%%' % ("="*(rate_num+1), " "*(100-rate_num-1), rate_num+1, )
    sys.stdout.write(r)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
