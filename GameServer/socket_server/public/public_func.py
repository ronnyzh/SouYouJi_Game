# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
import hashlib
import json
import time
import traceback
import urllib.parse
from datetime import datetime, date
from functools import wraps
import tornado.util
import platform


def dict_to_obj(dictData):
    obj = tornado.util.ObjectDict(dictData)
    return obj


def dictList_to_obj(dictList):
    objs = []
    for _dict in dictList:
        objs.append(dict_to_obj(_dict))
    return objs


def getNowStamp(millisecond=False):
    precision = 1
    if millisecond:
        precision = 1000
    return int(time.time() * precision)


def timeStampTo_Second(timeStamp):
    timeStamp = int(str(timeStamp)[:10])
    return timeStamp


def toJsStr(msg):
    return urllib.parse.quote(msg)


def listStrToInt(strList, isSorted=False, *args, **kwargs):
    result = list(map(int, strList))
    if isSorted:
        return sorted(result, *args, **kwargs)
    return result


def get_nowtime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def md5_encode(str):
    return hashlib.md5(str.encode(encoding='utf-8')).hexdigest()


def getSessionId(account):
    hash = hashlib.md5()
    hash.update(str(getNowStamp()).encode(encoding='utf-8'))
    hash.update(account.encode(encoding='utf-8'))
    return hash.hexdigest()


# 同时被多个方法装饰
def decorator(*func):
    def deco(f):
        for fun in reversed(func):
            f = fun(f)
        return f

    return deco


# tornado支持跨域
def allow_Origin(object):
    @wraps(object)
    class __waper__(object):
        def __init__(self, *args, **kwargs):
            super(__waper__, self).__init__(*args, **kwargs)
            self.set_header("Access-Control-Allow-Origin", '*')
            self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    __waper__.__name__ = object.__name__
    return __waper__


# python转json,支持datetime等格式
class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super(CJsonEncoder, self).default(obj)


def pretty_dict(obj, indent=' '):
    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            # 如果是字符串则拼上""
            if isinstance(k, str):
                k = '"%s"' % k
            if isinstance(v, str):
                v = '"%s"' % v
            # 如果是字典则递归
            if isinstance(v, dict):
                v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))  # 计算下一层的indent
            # case,根据(k,v)对在哪个位置确定拼接什么
            if i == 0:  # 开头,拼左花括号
                if len(obj) == 1:
                    yield '{%s: %s}' % (k, v)
                else:
                    yield '{%s: %s,\n' % (k, v)
            elif i == len(obj) - 1:  # 结尾,拼右花括号
                yield '%s%s: %s}' % (indent, k, v)
            else:  # 中间
                yield '%s%s: %s,\n' % (indent, k, v)

    return ''.join(_pretty(obj, indent))


def record_http_request(func):
    @wraps(func)
    def record(self, *args, **kwargs):
        request_time = str(datetime.now())
        response = func(self, *args, **kwargs)
        http_request = dict(
            request_time=request_time,
            expend_time=self.request.request_time(),
            response_time=str(datetime.now()),
            request_ip=self.request.remote_ip,
            method=self.request.method,
            url=self.request.uri,
            request_params=self.request.arguments,
            response_code=self.get_status(),
            response_text=self.response_value,
        )
        print(http_request)
        return response

    return record


def dictParseValue(parserObj, onlyParseKey=True, **kwargs):
    arguments = {}
    if not onlyParseKey:
        arguments = kwargs.copy()
    defaultMap = {
        int: 0,
        str: '',
        float: 0.0,
    }
    defaultFiter = [None, '', 0, 0.0, ' ']
    for _key, _value in parserObj.items():
        filter = defaultFiter.copy()  # 过滤器,如果不是必需,会过滤按条件删除key
        isMust = False  # 是否必需的,true时,key一定会有,无传入值会设置默认值

        if isinstance(_value, dict):
            val_type = _value.get('type', str)
            defaultVal = _value.get('default', defaultMap.get(val_type, None))
            filter = _value.get('filter', filter)
            isMust = _value.get('isMust', isMust)
        else:
            val_type = _value
            defaultVal = defaultMap.get(val_type, None)
        try:
            if isMust:
                theKeyVal = kwargs.get(_key, defaultVal)
                try:
                    theKeyVal = val_type(theKeyVal)
                except:
                    print('[Error][dictParseValue] <%s> cant not to [%s]' % (theKeyVal, val_type))
                    traceback.print_exc()
                    theKeyVal = defaultVal
            else:
                if _key not in kwargs:
                    continue
                try:
                    theKeyVal = val_type(kwargs[_key])
                    if filter:
                        if isinstance(filter, list):
                            if theKeyVal in filter:
                                continue
                        elif callable(filter):
                            if filter(theKeyVal):
                                continue
                except:
                    traceback.print_exc()
                    continue
            arguments[_key] = theKeyVal
        except:
            traceback.print_exc()
            continue
    return arguments


system_None = 0
system_Windows = 1
system_Linux = 2


def getCurSystem():
    if platform.system() == 'Windows':
        return system_Windows
    elif platform.system() == 'Linux':
        return system_Linux
    else:
        return system_None
