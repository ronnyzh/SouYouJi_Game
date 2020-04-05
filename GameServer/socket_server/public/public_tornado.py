# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/20
Revision: 1.0.0
Description: Description
"""

import traceback
from datetime import datetime

import tornado.web
import tornado.websocket

from server.operate import UserOperate


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(BaseWebSocketHandler, self).__init__(*args, **kwargs)
        host = self.request.connection.context.address
        self.ip = host[0]
        self.port = host[1] if len(host) > 1 else 0
        self.isConnect = False
        self.connectTime = None
        self.factory = self.application.factory

    def log(self, msg='', level='info'):
        try:
            msg = '%s %s' % (self.__str__(), msg)
            self.factory.log(msg=msg, level=level)
        except:
            traceback.print_exc()

    def check_origin(self, origin):
        '''是否允许跨域'''
        return True

    def open(self, *args, **kwargs):
        super(BaseWebSocketHandler, self).open(*args, **kwargs)
        self.log('[open] %s:%s 已连接' % (self.ip, self.port))
        self.isConnect = True
        self.connectTime = datetime.now()

    def on_message(self, message):
        self.log('[on_message] %s' % message)

    def write_message(self, message, binary=False):
        super(BaseWebSocketHandler, self).write_message(message, binary)

    def on_close(self):
        super(BaseWebSocketHandler, self).on_close()
        self.log('[on_close] %s:%s 连接已断开 %s:%s' % (self.ip, self.port, self.close_code, self.close_reason))
        self.isConnect = False

    def parseArgs(self, parserObj=None, *args, **kwargs):
        arguments = {}

        for _key, _value in parserObj.items():
            _defaultVal = 'None'
            _required = False
            _notEmpty = False
            _verifyFunc = None
            if isinstance(_value, dict):
                _type = _value.get('type', str)
                _defaultVal = _value.get('default', _defaultVal)
                _required = _value.get('required', _required)
                _notEmpty = _value.get('notEmpty', _notEmpty)
                _verifyFunc = _value.get('verifyFunc', _verifyFunc)
            else:
                _type = _value
            if _defaultVal == 'None':
                defaultMap = {
                    int: 0,
                    str: '',
                    float: 0.0,
                }
                _defaultVal = defaultMap.get(_type, None)
            # print('_type=> %s ,_defaultVal=> %s ,_required=>%s ' % (_type, _defaultVal, _required))
            try:
                if _required:
                    argVal = kwargs[_key]
                else:
                    argVal = kwargs.get(_key, _defaultVal)
                if _notEmpty and not argVal:
                    return False, {'msg': '[%s]参数不可为空' % (_key)}
                if _verifyFunc and not _verifyFunc(_key, argVal):
                    return False, {'msg': '[%s]参数的值非法' % (_key)}
                arguments[_key] = _type(argVal)
            except KeyError:
                return False, {'msg': '[%s]参数不可缺省' % (_key)}
            except Exception as err:
                traceback.print_exc()
                return False, {'msg': '[%s]参数错误, %s' % (_key, err)}
        return True, arguments

    def getMatchMgr(self, gameId: int, matchId: int):
        return self.factory.getMatchMgr(gameId, matchId)


class BaseRequestHandler(tornado.web.RequestHandler):
    allowOrigin = True

    def __init__(self, *args, **kwargs):
        self.factory = None
        super(BaseRequestHandler, self).__init__(*args, **kwargs)
        if self.allowOrigin:
            self.set_header("Access-Control-Allow-Origin", '*')
            self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.response_value = None

    def finish(self, chunk=None):
        if isinstance(chunk, dict):
            chunk['code'] = chunk.get('code', 0)
        self.response_value = chunk
        super(BaseRequestHandler, self).finish(chunk)

    def initialize(self, *args, **kwargs):
        super(BaseRequestHandler, self).initialize()
        self.factory = self.application.factory

    def getMatchMgr(self, gameId: int, matchId: int):
        return self.factory.getMatchMgr(gameId, matchId)

    def parseArgs(self, parserObj=None, *args, **kwargs):
        arguments = {}
        if not parserObj:
            return True, arguments

        for _key, _value in parserObj.items():
            _defaultVal = 'None'
            _required = False
            _notEmpty = False
            _verifyFunc = None
            if isinstance(_value, dict):
                _type = _value.get('type', str)
                _defaultVal = _value.get('default', _defaultVal)
                _required = _value.get('required', _required)
                _notEmpty = _value.get('notEmpty', _notEmpty)
                _verifyFunc = _value.get('verifyFunc', _verifyFunc)
            else:
                _type = _value
            if _defaultVal == 'None':
                defaultMap = {
                    int: 0,
                    str: '',
                    float: 0.0,
                    bool: False,
                }
                _defaultVal = defaultMap.get(_type, None)
            # print('_type=> %s ,_defaultVal=> %s ,_required=>%s ' % (_type, _defaultVal, _required))
            try:
                if _required:
                    argVal = self.get_argument(_key)
                else:
                    argVal = self.get_argument(_key, _defaultVal)
                if _notEmpty and not argVal and argVal != False:
                    return False, {'msg': '[%s]参数不可为空' % (_key)}
                if _verifyFunc and not _verifyFunc(_key, argVal):
                    return False, {'msg': '[%s]参数的值非法' % (_key)}
                arguments[_key] = _type(argVal)
            except tornado.web.MissingArgumentError:
                return False, {'msg': '[%s]参数不可缺省' % (_key)}
            except Exception as err:
                return False, {'msg': '[%s]参数错误, %s' % (_key, err)}
        return True, arguments

    def checkSid(self, sid: str = None, *args, **kwargs):
        if not sid:
            sid = self.get_argument('sid', '')
        uid = self.get_argument('uid', '')
        return UserOperate.checkSid(self=self, sid=sid, uid=uid, *args, **kwargs)
