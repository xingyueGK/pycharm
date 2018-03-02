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
import os,sys


TestLoadBalancerId="lb-2zexi1mi1kkit6b4****"


# 创建 AcsClient 实例，线上阿里云key
client = AcsClient(
    "********",
    "************",
    "cn-beijing"
)

# 创建 request，并设置参数
# request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
# request.set_LoadBalancerId('lb-2zexi1mi1kkit6b4dv4ig')
# # 发起 API 请求并打印返回
# response = client.do_action_with_exception(request)
# print  response

def set_back_weight(loadbalancerid,serverid,weight):
    #设置后端服务器权重
    #LoadBalancerId	String	是	负载均衡实例的唯一标识
    #BackendServers	String	是	需要添加的后端服务器列表。
    #取值：是一个Json string，其结构是一个JsonList。一次请求中，List中的元素个数最多20个。List元素的结构详见下表和调用示例。
    #后端服务器信息BackendServers
    # 名称	类型	描述
    # ServerId	String	后端服务器名称ID，为ECS实例ID。
    # Weight	Integer	后端服务器的权重，范围为0-100，默认值100。
    #实例：BackendServers=[{"ServerId":"i-2zecsh1i1b8c04fswi55","Weight":"20"}]
    BackendServers = [{"ServerId": "%s", "Weight": "%s"}] %(serverid,int(weight))
    setquest=SetBackendServersRequest.SetBackendServersRequest()
    setquest.set_LoadBalancerId(loadbalancerid)
    setquest.set_BackendServers(BackendServers)
    response = client.do_action_with_exception(setquest)
    print  response



def getbackstatus(LoadBalancerId):
    #获取后端ECS健康状态
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

def addbackserver(LoadBalancerId,backendservers):
    request=AddBackendServersRequest.AddBackendServersRequest()
    request.set_LoadBalancerId(LoadBalancerId)
    request.set_BackendServers(backendservers)
    response = client.do_action_with_exception(request)

def  getDescribeZones():
    request = DescribeZonesRequest.DescribeZonesRequest()
    response = client.do_action_with_exception(request)
    print response
def  get_backserver(id):
    request=DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
    request.set_LoadBalancerId(id)
    response = client.do_action_with_exception(request)
    serverid = json.loads(response)['BackendServers']['BackendServer']
    print serverid
def  getserverlist():
    request=DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
    response = client.do_action_with_exception(request)
    test=json.loads(response)['LoadBalancers']['LoadBalancer']
    if type(test)is list:
        lens=len(test)
        name_list={}
        for i in range(lens):
            print  u'名字 : %sid : %s'%(test[i]['LoadBalancerName'].ljust(20),test[i]['LoadBalancerId'])
            name_list[test[i]['LoadBalancerName']]=test[i]['LoadBalancerId']
        #print name_list
if __name__ == '__main__':
    getserverlist()
