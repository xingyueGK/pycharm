#/usr/bin/env python
# -*- coding: utf8 -*-
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkslb.request.v20140515  import  DescribeLoadBalancerAttributeRequest
from  aliyunsdkslb.request.v20140515 import  SetBackendServersRequest
from   aliyunsdkslb.request.v20140515 import  SetLoadBalancerStatusRequest
from aliyunsdkslb.request.v20140515  import  DescribeHealthStatusRequest
from  aliyunsdkslb.request.v20140515  import  AddBackendServersRequest
from  aliyunsdkslb.request.v20140515 import  DescribeZonesRequest
from  aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
import json
import os,sys,getopt


# 创建 AcsClient 实例，线上阿里云key
client = AcsClient(
    #生产
    # "",
    # "",
    #测试
    "key",
    "scerkty",
    "cn-beijing"
)

class getEcsName(object):
    #获取ECS主机id和名字
    servername={}
    def __init__(self):
        self.request=DescribeInstancesRequest.DescribeInstancesRequest()
        self.request.set_PageSize(100)
        self.serverinfo=client.do_action_with_exception(self.request)
    def getEcsServerList(self):
        SERVER=json.loads(self.serverinfo)
        #print SERVER
        SLIST=SERVER['Instances']['Instance']
        for i in range(len(SLIST)):
            self.servername[SLIST[i]['InstanceName']]=SLIST[i]['InstanceId']
        #返回主机ID和名字

        return self.servername
class  slbSet(object):
    def setBackWeight(sefl,loadbalancerid,serverid,weight):
        #设置后端服务器权重
        #LoadBalancerId	String	是	负载均衡实例的唯一标识
        #BackendServers	String	是	需要添加的后端服务器列表。
        #取值：是一个Json string，其结构是一个JsonList。一次请求中，List中的元素个数最多20个。List元素的结构详见下表和调用示例。
        #后端服务器信息BackendServers
        # 名称	类型	描述
        # ServerId	String	后端服务器名称ID，为ECS实例ID。
        # Weight	Integer	后端服务器的权重，范围为0-100，默认值100。
        #实例：BackendServers=[{"ServerId":"i-2zecsh1i1b8c04fswi55","Weight":"20"}]
        BackendServers = '[{"ServerId": "%s", "Weight": "%s"}]' %(serverid,int(weight))
        setquest=SetBackendServersRequest.SetBackendServersRequest()
        setquest.set_LoadBalancerId(loadbalancerid)
        setquest.set_BackendServers(BackendServers)
        response = client.do_action_with_exception(setquest)
        print  response

    def getBackStatus(self,LoadBalancerId):
        #获取slb后端ECS健康状态
        #ListenerPort	Integer	是	负载均衡实例前端使用的端口。
        # 取值：1-65535。默认值：无。
        # 不设置该参数表示获取所有端口的健康检查状态。
        # LoadBalancerId	String	是	负载均衡实例的唯一标识。
        # 后端服务器的健康状况，normal,abnormal或unavailable。normal表示状态为健康；abnormal表示状态为不健康；unavailable表示未能完成健康检查，具体原因可能是：未开启健康检查、
        dhs=DescribeHealthStatusRequest.DescribeHealthStatusRequest()
        dhs.set_LoadBalancerId(LoadBalancerId)
        response = client.do_action_with_exception(dhs)
        status=json.loads(response)['BackendServers']['BackendServer']
        return  status

    def getDescribeZones(self):
        request = DescribeZonesRequest.DescribeZonesRequest()
        response = client.do_action_with_exception(request)
        print response
    def  getBackServer(self,id):
        #获取slb后端ECS实例状态
        request=DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(id)
        response = client.do_action_with_exception(request)
        serverid = json.loads(response)['BackendServers']['BackendServer']
        return serverid
    def  getSlbList(self):
        #获取SLB负载均衡实例
        request=DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        response = client.do_action_with_exception(request)
        text=json.loads(response)['LoadBalancers']['LoadBalancer']
        return text
def  FormatPrint(text,name,id):
    #阿里云名字输出格式
    if type(text)is list:
        lens=len(text)
        name_list={}
        for i in range(lens):
            print  u'名字 : %sid : %s'%(text[i][name].ljust(25),text[i][id])#等宽度输出
            name_list[text[i][name]]=text[i][id]
        return name_list
    elif type(text) is dict:
        #按k排序输出
        items=text.items()
        items.sort()
        for k,v in items:
            print  u'名字 : %sid : %s' % (k.ljust(25), v)  # 等宽度输出
def  main():
    #获取主机和负载均衡实例
    EcsList=getEcsName().getEcsServerList()#获取ECS主机列表
    FormatPrint(EcsList,'InstanceName','InstanceId')#格式化输出
    print u'共计ECS实例 %s 个'%len(EcsList)
    slblist = slbSet().getSlbList()
    FormatPrint(slblist, 'LoadBalancerName', 'LoadBalancerId')
    print u'共计SLB负载 %s 个' % len(slblist)

def usage():
    return u'''usage:    
    -h ,--help   帮助信息
    -slbid       负载均衡id
    -bsid        后端服务器id
    -w           后端服务器权重值
    '''


if __name__ == '__main__':
    main()
    #参数选项执行
    # bsid=''
    # slbid=''
    # weight=''
    # if  len(sys.argv) >= 2:
    #     try:
    #         options, args = getopt.getopt(sys.argv[1:], "hw:", ["help","setw","bsid=","slbid="])
    #     except getopt.GetoptError:
    #         sys.stdout.write(u'参数输入错误')
    #         sys.exit(2)
    #     for name, value in options:
    #         #print  options
    #         if name in ("-h", "--help"):
    #             print usage()
    #         if name in ("--slbid",):
    #             slbid=value
    #         if name in ("--bsid",):
    #             bsid = value
    #         if name in ("-w",):
    #             weight= value
    #     print slbid,bsid,weight
    # else:
    #     a=usage()
    #     sys.stdout.write(a)
    #     sys.exit(2)
    cls=slbSet()
    SERVERSTATUS=cls.getBackStatus('lb-2zexi1mi1kkit6b4dv4ig')
    print   SERVERSTATUS
    if SERVERSTATUS[0]['ServerHealthStatus'] == 'normal'and SERVERSTATUS[1]['ServerHealthStatus'] == 'normal':
        print 'ok'
