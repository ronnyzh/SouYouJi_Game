# -*- coding:utf-8 -*-
'''
语音数据
'''
import json
import md5

import time

import urllib2
import socket

WAIT_WEB_TIME = 10 #访问网页超时时间

PATH = "http://api.voice.gcloud.qq.com:19988"
BUSINESS_ID = "gcloud.1696859158"
BUSINESS_KEY = "cfdd9d7f6aa542673f33b88cf49cd553"
OPEN_ID = "nimeideopenid"
IP = "127.0.0.1"
NET_TYPE = 1

def packTalkBusinessData(packTime):
    data = "[business_id:%s][open_id:%s][ip:%s][time:%d][business_key:%s]"%(BUSINESS_ID, OPEN_ID, IP, packTime,BUSINESS_KEY)
    data4md5 = md5.new(data).hexdigest()
    return data4md5

def packTalkData():
    packTime = int(time.time())
    businessData = packTalkBusinessData(packTime)
    packStr = "[1, \"gcloudVoiceService:GetAuthkey\", 1, 1, {\"req\": {\"rec\": {\"m_sigiture\": {\"str\": \"%s\"}, \"m_client_net_type\": {\"i32\": %d}, \"m_client_ip\": {\"str\": \"%s\"}, \"m_currenttime_since_1970_s\": {\"i32\": %d}, \"m_openid\": {\"str\": \"%s\"}, \"m_businessid\": {\"str\": \"%s\"}}}}]"\
        %(businessData, NET_TYPE, IP, packTime, OPEN_ID, BUSINESS_ID)
    return packStr

def sendTalkData():
    packStr = packTalkData()
    socket.setdefaulttimeout(WAIT_WEB_TIME)
    errorCode = 0
    errorStr = ''
    message = ''
    try:
        req = urllib2.Request(url = PATH, headers={'Content-Type':'text/xml'},data = packStr )
        Message = urllib2.urlopen(req)
        data = Message.read()
        dataDict = json.loads(data)[-1]
        if not dataDict['success']['rec']['m_error_code']['i32']:
            message = dataDict['success']['rec']['m_authkeystr']['str']
        else:
            errorCode = dataDict['success']['rec']['m_error_code']['i32']
            errorStr = dataDict['success']['rec']['m_error_str']['str']
    except Exception,e:
        print 'get talk data error:', e
        errorCode = 233
        errorStr = 'e'
    return message, errorCode, errorStr

