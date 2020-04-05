#!/usr/bin/env python
#-*-coding:utf-8 -*-

"""
@Author: $Author$
@Date: $Date$
@version: $Revision$

Description:
    微信支付模块函数
"""
import random
import xml.dom.minidom
import md5
import hashlib
import urllib2
import urllib
import socket
from wechat.wechatData import *

def wechat_order_nonce():
    """
    获取微信授权字符
    """
    nonceStr = ''
    for count in xrange(MAX_RANDOM_STR_COUNT):
        nonceStr += random.choice(RANDOM_STR_LIST)
    return nonceStr

def tx_wechat_order_nonce():
    nonceStr = ''
    for count in xrange(32):
        nonceStr += random.choice(RANDOM_STR_LIST)
    return nonceStr


def gen_sign4fish(params):
    """
    捕鱼微信支付签名生成函数

    :param params: 参数，dict 对象
    :param key: API 密钥
    :return: sign string
    """

    param_list = []
    for k in sorted(params.keys()):
        v = params.get(k)
        if not v:
            # 参数的值为空不参与签名
            continue
        param_list.append('{0}={1}'.format(k, v))

    # 在最后拼接 key
    param_list.append('key={}'.format(MCH_KEY_FISH))
    # 用 & 连接各 k-v 对，然后对字符串进行 MD5 运算
    return md5.new('&'.join(param_list)).hexdigest().upper()

def gen_sign4TX(params):
    """
    签名生成函数

    :param params: 参数，dict 对象
    :param key: API 密钥
    :return: sign string
    """

    param_list = []
    for k in sorted(params.keys()):
        v = params.get(k)
        if not v:
            # 参数的值为空不参与签名
            continue
        param_list.append('{0}={1}'.format(k, v))

    # 在最后拼接 key
    param_list.append('key={}'.format(MCH_KEY_TX))
    # 用 & 连接各 k-v 对，然后对字符串进行 MD5 运算
    return md5.new('&'.join(param_list)).hexdigest().upper()

def get_xml_message(url, data):
    """
    解析xml数据接口
    """
    socket.setdefaulttimeout(WAIT_WEB_TIME)
    xmlDict = {}
    req = urllib2.Request(url = url, headers={'Content-Type':'text/xml'},data = data )
    Message = urllib2.urlopen(req)
    data = Message.read()

    xmlDict = trans_xml_2_dict(data)
    return xmlDict

def trans_xml_2_dict(data):
    """
    解析微信返回的xml
    """
    dom = xml.dom.minidom.parseString(data)
    root = dom.documentElement
    xmlDict = {}
    for child in root.childNodes:
        print child
        result = dom.getElementsByTagName(child.nodeName)
        if result == []:
            continue
        result = result[0].childNodes[0].nodeValue
        xmlDict[child.nodeName] = result

    return xmlDict
