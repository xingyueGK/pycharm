#-*- coding:utf-8 -*-
#爬虫参数设置

#四至，城市，中心经纬度
lng_min = 114.88
lat_max = 33.76
lng_max = 114.90
lat_min = 33.74



#爬取的间隔时间
sleeptime = 3600 #单位是秒，7200秒即为2小时

#下面这个表单是用来获取cookie的列表，最好多放一些QQ号
qq_list = [ ["534513394","houxinya302302"],
            ["413728161","xingyue(123"],
            ["995598502", "fyy7686935"],]
fre = 100
#每次爬取方格的边长（单位：km）
edge = 2.5


#下面的参数不用设置
lng_delta = 0.01167*edge
lat_delta = 0.009*edge
