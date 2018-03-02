# -*- coding:utf-8 -*-

import requests
import sys
import time
import json
import threading

reload(sys)
sys.setdefaultencoding('utf-8')
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
def peiyang():
    '''gid:210000385950#需要培养的武将角色id
        c:cultivate 培养
        m:roll #培养开始
        mode:1 #模式为金钱
        '''
    '''c:cultivate
    m:save
    gid:210000385950
    '''
class fuben(object):
    def __init__(self,username, password):
        self.username = username
        self.password = password
        def get_html():
            # 获取首页html
            url = 'http://uc.game.hanjiangsanguo.com/index.php?&c=user&m=login&&token=&channel=150&lang=zh-cn&rand=150959328607564&u=%s&p=%s'%(self.username,self.password)
            r = requests.session()
            return r.get(url).text
        self.rand = int(time.time()*1000)
        self.token_uid = '210000353508'
        self.addr_info = json.loads(get_html())['serverlist']
        for v in self.addr_info:
            if v['selected'] == 1:
                self.addr = v['addr']
                break
        #自定义等级位置
        self.addr = "s21.game.hanjiangsanguo.com"
        def get_token():
            url = 'http://%s/index.php?v=0&c=login&&m=user&&token=&channel=150&lang=zh-cn&rand=150959405499450&u=%s&p=%s' % (
            self.addr, self.username, self.password)
            token = requests.session().get(url).text
            tokens = json.loads(token)
            return tokens['token']
        self.token = get_token()
    def post_url(self,data):
        #url拼接数据
        self.url = 'http://%s/index.php?v=2017111501&v=2017111501&channel=11&imei=NoDeviceId&platform=android&lang=zh-cn&token=%s&token_uid=%s&rand=%s&' % (self.addr,self.token, self.token_uid, self.rand)
        for k,v in data.items():
            self.url += '&%s=%s'%(k,v)
        r = requests.post(self.url,headers=headers)
        return r.text
    def action(self,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        self.action_data = kwargs
        self.serverinfo = self.post_url(self.action_data)
        #self.serverinfo
        try:
            return json.loads(self.serverinfo)
        except ValueError as e:
            print e

    def level(self):
        level = self.action(c='member', m='index')
        levelinfo = int(level['level'])
        return levelinfo
    def muster(self):#添加武将并出征
        # gid武将id，pid那个槽位训练获取
        caiid=''
        liaoid=''
        gid=''
        practtice_info = self.action(c='practice', m='index')
        # 初期都是两个训练槽位，
        pid = practtice_info['place']['1']['id']
        self.action(c = 'practice' , m = 'practice_stop ',pid = pid)#终止训练
        #获取武将
        self.action(c='levelgift',m='index')
        wujiang_index = self.action(c='muster',m='index',page=1,perpage=999)['list']
        for  k,v in wujiang_index.items():
            if v['name']=='孙权':#蔡文姬
                print '孙权出战'
                gid = v['id']
                self.action(c='muster',m='go_battle',gid=v['id'])
                self.action(c='matrix',m='index')
                caiid =  v['id']
            elif v['name']=='蔡文姬':
                liaoid = v['id']
        lists = '0,%s,0,%s,0,0,0,0,0'%(caiid,liaoid)
        self.action(c='matrix',m='update_matrix',list=lists,mid=1)
        #训练武将，
        self.action(c='practice',m='practice_start',gid= gid,pid=pid,type=2)
        #队武将突飞
        status=1
        index_info = self.action(c='practice',m='index')
        freetimes = index_info['freetimes']#突飞卡
        isturn = index_info['list']['1']['isturn']#武将师是否到转生级别
        wjlevel = index_info['list']['1']['level']
        print wjlevel
        while status == 1 and freetimes != '0':#队伍将进行突飞
            if int(isturn) == 1 and int(wjlevel) < 60:
                print '武将转生'
                print self.action(c='practice',m='turn',gid=gid)
            self.action(c='practice', m='mop', times = 100,gid=gid)
            self.action(c='practice', m='mop', times=50, gid=gid)
            self.action(c='practice', m='mop', times=10, gid=gid)
            self.action(c='practice', m='mop', times=5, gid=gid)
            index_info = self.action(c='practice', m='index')
            freetimes = index_info['freetimes']
            info = self.action(c = 'practice',m='go_leap',gid=gid)#武将突飞一次
            status = info['status']
    def zhengshou(self):#征收
        cishu = self.action(c='city',m='index')#获取银币征收次数,m=impose,执行征收
        cishu_count = cishu['times']
        if cishu_count != '0':#判断征收次数是否为0，不为0则进行全部征收
            for count in range(1,int(cishu_count)+1):
                print '开始征收第 %d 次'%count
                time.sleep(0.5)
                self.action(c='city',m='impose')
        else:
            print '次数为0次'
    def join(self):#申请加入你是学姐国家
        print self.action(c='country',m='search',name='%E6%98%AF%E4%BD%A0%E5%AD%A6%E5%A7%90')
        print self.action(c='country',m='apply',id=250000000286,page=1)
    def overseastrade(self):  # 海外贸易
        self.action(c='message',m='index')
        self.action(c='overseastrade',m='index')
        # 购买粮食，花费银币的，id=1为粮食，id2-5为花费元宝的玛瑙等
        self.action(c='overseastrade', m='buy_item', id=1)
        # 组队 ，检查是否有对， 有则加入，没有则创建 ，开始贸易
        # 1获取组队列表
        list_country = self.action(c='overseastrade', m='get_list_by_country', p=1)['list']
        if list_country:  # 如果列表不为空，说明有组
            # 自动加组贸易
            for k, v in list_country.items():  # 判断第一个角色有值没有，有责加入第二个，没有则加入第一个#需要time_id
                if v['member1'] != '0':  # 如果不为0 则说明角色有人，加入另一个，
                    print '加入2'
                    self.id = v['id']
                    print self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=2, page=1)
                else:
                    print '加入1'
                    self.id = v['id']
                    print self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=1, page=1)
                    # print list_country[k]['member1']
        else:
            # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
            print self.action(c="overseastrade", m='join_team', id=0, place=4, site=2, page=1)
    def general(self,type):#获取武将id和装备id,并返回输入获取的等级
        #装备信息栏
        info = self.action(c='general', m='index')
        # print info
        gid = info['list']['1']['id']
        eid = []
        if info['list']['1']['eid1'] == 0 or info['list']['1']['eid1'] == "0":
            for k,v in  info['equipments'].items():#初期获得最高级装备为2级别
                if v['needlevel'] == str(type) and v['etype']== 1:
                    eid.append(v['id'])
        else:
            eid.append(info['list']['1']['eid1']['id'])
        if info['list']['1']['eid2'] == 0 or info['list']['1']['eid2'] == "0":
            for k,v in  info['equipments'].items():#初期获得最高级装备为2级别
                if v['needlevel'] == str(type) and v['etype']== 2:
                    eid.append(v['id'])
        else:
            eid.append(info['list']['1']['eid2']['id'])
        if info['list']['1']['eid3'] == 0 or info['list']['1']['eid3'] == "0":
            for k, v in info['equipments'].items():  # 初期获得最高级装备为2级别
                if v['needlevel'] == str(type) and v['etype']== 3:
                    eid.append(v['id'])
        else:
            eid.append(info['list']['1']['eid3']['id'])
        # if not eid:
        #     try:
        #         eid = [,info['list']['1']['eid2']['id'],info['list']['1']['eid3']['id']]
        #     except TypeError as e:
        #         print '获取装备错误',info,e
        return gid,eid
    def get_general(self):#获取武将信息
        general_index=self.action(c='general',m='index')
        return general_index
    def strengthen(self,id):#强化装备
        print id
        levelinfo = self.level()
        self.action(c='general',m='index')
        self.action(c='strengthen',m='index')
        id_info = self.action(c='strengthen',m='strengthen_info',id=id)
        newlevel = id_info['info']['level']#获取当前装备的强化等级
        print '当前等级',newlevel
        try:
            while int(newlevel) < levelinfo - 25 :
                strenthinfo = self.action(c='strengthen', m='strengthen_start', id=id, ratetype=0)
                newlevel = strenthinfo['newlevel']
        except KeyError as e:
            print '已经强化到最高级',e
    def eqip(self,gid,eid):#给武将穿戴装备
        self.action(c='general',m='equip',gid=gid,eid=eid)
    def levelgift(self,level):#获取等级奖励
        self.action(c = 'levelgift' , m = 'index')#打开奖励页面
        self.action(c='levelgift',m='get_reward',level=level)#获取30级奖励
    def saodang(self,num):#攻击小兵
        exit_code = 1
        if exit_code == 1 :
            for level in range(num,12):#遍历每一个图
                print '开始攻击第 %s 个图'%level
                print  self.action(c='map',m='get_scene_list',l=level)
                site = len(self.action(c='map',m='get_scene_list',l=level)['list'])
                for i in range(0,site):#遍历关卡图次数
                    print '关卡',i
                    status = 1
                    for id in range(1,11):  # 遍历10个小兵
                        try:
                            #获取首杀状态，1为首杀，-1为已经击杀
                            first = self.action(c='map', m='mission', l=level, s=i+1, id=id)['info']['first']
                        except KeyError as e :
                            continue
                        if first == 1 and status == 1:#
                            status = self.action(c='map',m='action',l=level,s=i+1,id=id)['status']
                            print status
                            if  first == 1 and status == -5:
                                print '退出'
                                exit_code = 2
                                return exit_code
                        else:
                            print '已经击杀'
        else:
            print 'dabuduole'
            return
    def herothrone(self):#
        self.action(c='herothrone',m='index')
        for i in range(3):
            print self.action(c='herothrone',m='start')#开始王座
            #攻击:
            while True:
                flag = self.action(c='herothrone', m='action')['status']
                print  '攻击王座副本'
                if flag == -2:
                    break
    def act_steadily(self):#节节高
        info = self.action(c='act_steadily',m='index')
        status  = info['status']
        reward_cd = info['reward_cd']
        t = info['reward']['time']
        if reward_cd == 0 and status == 1:
            self.action(c='act_steadily',m='get_online_reward',t=t)
        elif reward_cd == 0 and status != 1:
            exit(2)
        else:
            print '%s分钟后领取,%s'%(reward_cd/60,reward_cd)

            time.sleep(reward_cd+1)
            self.action(c='act_steadily', m='get_online_reward', t=t)
    def morra(self):#节节高奖券
        status =1
        while status == 1:
            info=self.action(c='act_steadily',m='morra',type=1)
            status= info['status']
        #买突飞卡
        print self.action(c='act_steadily',m='get_score_reward',id=1)
    def mainquest(self):#领取所有活动奖励
            mainquest_info =self.action(c='mainquest',m='index')
            print '领奖'
            for i in mainquest_info['list']:
                if int(i['status'])==1:#获取奖励
                    self.action(c='mainquest',m='get_task_reward',id=i['task_id'])
                    print '领取奖励',i['task_id']


    def soul(self):#武将将魂
        site = [1, 2, 3, 4]
        sid = []
        gid=''
        soulindex=self.action(c='soul',m='index')
        for i in soulindex['pack']['list']:
            sid.append(int(i['id']))
        for k,v in soulindex['general'].items():
            if v['name'] == '孙权':
                gid = int(v['id'])
        for i in range(4):
            self.action(c='soul',m='equip',gid=gid,sid=sid[i],site=site[i])
if __name__ == '__main__':
    def act(user,apass):
        while True:
            action = fuben(user,apass)
            action.act_steadily()
           # action.saodang(9)
    with open('user.txt', 'r') as f:
        for i in f:
            str = i.strip()
            name = str + 'yue123a'
            t1 = threading.Thread(target=act, args=(name,'413728161'))
            t1.start()