#-*- coding:utf-8 -*-
from shujufenx import  fuben
import  threading
import time
import activity
import requests
"""竞速步骤
1、第一次扫荡攻击后16级失败
2、强化2级装备到16级，然后并穿戴，扫荡到16级后失败
3、再次强化装备到26级后攻击超过30级失败
4、领取蔡文姬武将，并出站"""
headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    # 'Host':'s148.game.hanjiangsanguo.com',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'DNT':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
# url = 'http://s21.game.hanjiangsanguo.com/index.php?v=0&c=matrix&&m=update_matrix&&token_uid=210000353508&token=lecgC5Roo2F5Irxdhm4KRVldIxoevEZ0DPz5QH1gsEde2zf-QIFMuA&channel=150&lang=zh-cn&rand=151434283111377'
# #a=fuben()
# body = {'list':'-1,210000385950,-1,0,-1,0,210000370154,-1,0',"mid":1}
# print requests.post(url,headers=headers,data=body).text
def act(username,passwd):
    action = fuben(username,passwd)
    try:
        print '账号：%s   等级为：%s' % (username, action.level())
    except :
        print 'zhanghao ######################################################################## ',username
    if  action.level() <10:
        action.saodang(1)#16级 失败退出
        action.levelgift(16)  # 领取16级奖励
    #扫荡失败以后获取2级别装备，然后强化后并穿戴上去
    if action.level() < 35:
        gid,uid = action.general(7)#第一次的都是2级装备
        for i in uid:
            action.strengthen(i)
            action.eqip(gid, i)
        action.saodang(1)#26级失败退出
        for i in uid:
            action.strengthen(i)
        action.saodang(2)#30级失败退出从第二个图开始
        action.levelgift(30)  # 领取30级奖励
        action.morra()#节节高
        action.muster()  # 武将出征并上阵，并突飞到30级
        gid, uid = action.general(25)#获取三级装备，再次强化，并给武将穿戴上
        for i in uid:
            action.strengthen(i)
            action.eqip(gid, i)
            action.saodang(2)  # 级失败退出
        for i in uid:
            action.strengthen(i)
    if action.level()<50:
        for i  in range(2):
            action.mainquest()#获取所有活动
        gid, uid = action.general(25)#获取25级需要穿戴的装备强化
        for i in uid:#遍历装备，强化并穿戴
            action.strengthen(i)
            action.eqip(gid, i)
        action.muster()  # 再次突飞
        action.saodang(2)
    if action.level()  <70:#领取前60次奖励
        #action.muster()#对武将突飞
        #action.morra()  # 节节高
        for i in range(3):#循环领取通过奖励
            action.mainquest()
        for i in range(4,13):
            action.levelgift(5*i)  # 领取60级奖励
        # #获取竞速元宝
        # # for i in range(10, 120, 10):
        # #     action.action(c='map',m='get_mission_reward',id=i)

                #action.strengthen(eid1_quality_equipments)#强化装备
        # action.strengthen(general_index_list['eid1']['id'])
        action.saodang(3)
    # if action.level()  <90:#领取前60次奖励
    #     # gid, uid = action.general(25)  # 获取三级装备，再次强化，并给武将穿戴上
    #     # for i in uid:
    #     #     action.strengthen(i)
    #     for i in range(3):#循环领取通过奖励
    #         action.mainquest()
    #     for i in range(4,13):
    #         action.levelgift(5*i)  # 领取60级奖励
    #     action.saodang(4)
    #     #获取竞速元宝
    #     for i in range(10, 120, 10):
    #         action.action(c='map',m='get_mission_reward',id=i)

def joi(username,passwd):
    #国家海外贸易
    action = fuben(username,passwd)
    #action.join()加入国家
    print '账号：%s   等级为：%s' % (username, action.level())
    action.overseastrade()
def fuka(username,passwd):
    #福卡活动
    action = fuben(username,passwd)
    action.fuka()
def infogroup(username,passwd):
    activity.userinfo(username,passwd)
    activity.heishi(username,passwd)
def haiyun(username,passwd):
    a=activity.activity(username,passwd)
    a.haiyun()
def wujiang(username,passwd):#武将训练信息
    action = fuben(username,passwd)
    action.action(c='muster',m='index')
    practiceinfo=action.action(c='practice',m='index')
    freetimes = practiceinfo['freetimes']#突飞卡
    turn = practiceinfo['list']['1']['turn']
    level = practiceinfo['list']['1']['level']
    print '剩余突飞卡 %s 武将等级 %s 转 %s 级'%(freetimes,turn,level)
def sign(username,passwd):
    a=activity.activity(username,passwd)
    a.sign()
def buy(username,passwd):
    action = fuben(username, passwd)
    action.action(c = 'tavern', m = 'get_list' ,page = 1 , perpage = 100 , tab = 4)
    action.action(c='tavern',m='buy',generalid=79)#购买孙权武将武将
def zhengshou(username,passwd):#武将训练信息
    action = fuben(username,passwd)
    practtice_info = action.soul()
    # # 初期都是两个训练槽位，
    # pid = practtice_info['place']['2']['id']
    # action.action(c='practice', m='practice_stop ', pid=pid)  # 终止训练
def uneq(username,passwd):#武将训练信息
    action = fuben(username,passwd)
    general_index = action.get_general()  # 获取装备列表信息
    general_index_list = general_index['list']['2']  # 穿戴装备列表
    print general_index
    eid2 = general_index_list['eid2']
    eid3 = general_index_list['eid3']
    gid=general_index_list['id']
    action.action(c='general', m='unequip', gid=gid, eid=eid2, position=0)
    action.action(c='general', m='unequip', gid=gid, eid=eid3, position=0)
def genarl(username,passwd):#装备穿戴3级别以上装备
    action = fuben(username,passwd)
    general_index = action.get_general()  # 获取装备列表信息
    general_index_list = general_index['list']['1']  # 穿戴装备列表
    general_index_equipments = general_index['equipments']  # 未穿戴装备列表
    gid = general_index_list['id']  # 获取武将id
    # eid1_quality = general_index_list['eid1']['quality']#佩戴武器的等级
    for k, equ in general_index_equipments.items():  # 遍历未穿戴装备列表
        if equ['quality'] == '3' or equ['quality'] == '4' or equ['quality'] == '5':
            eid1_quality_equipments = equ['id']  # 未穿戴的6级或是5级装备
            action.eqip(gid, eid1_quality_equipments)

def jinsu(username,passwd):
    """适用于有紫石头3500以上，可以购买孙权的"""
    action = fuben(username,passwd)
    action.saodang(3)#突飞出征

with open('1user.txt', 'r') as f:
    for i in f:
        str = i.strip()
        name = str + 'yue123a'
        t1 = threading.Thread(target=jinsu,args=(name, '413728161'))
        t1.start()
        time.sleep(0.2)

