#-*- coding:utf-8 -*-
#!/usr/bin/env python

import json
import traceback
from threading import Thread, Lock
from tsconfig import *
from model.serviceModle import *
"""
     web 跟 game 之间通讯

"""


def onFeedServiceStatus(redis, timeout):
    """
        服务状态监听 喂狗
    """
    redis.set(SERVICE_STATUS_KEY, "")
    redis.expire(SERVICE_STATUS_KEY, timeout)
    return {'code': 0}


def onServiceClose():
    """
        关闭服务
    """
    redis = get_inst()
    redis.delete(PROTOCOL_KEY)
    redis.delete(SERVICE_STATUS_KEY)
    return {'code': 0}


class SchedulerWorker(object):
    def __init__(self, thread_num=5):
        self.mutex = Lock()
        self.thread_num = thread_num
        self.serviceProtocolTable = PROTOCOL_KEY
        self.serviceStatus = SERVICE_STATUS_KEY
        self.serviceProtoCalls = []
        self.registerServiceProtocols()

    def run(self):
        log_debug('SchedulerWorker ***************************')
        self.spawn_worker()

    def spawn_worker(self):
        t_list = []
        for th_i in range(self.thread_num):
            t_threading = Thread(target=self.spawn_handler, args=())
            t_list.append(t_threading)
        for th_i in t_list:
            th_i.setDaemon(True)
            th_i.start()

    def spawn_handler(self):
        while True:
            if self.mutex.acquire(1):
                self.readPartyServiceProtocol()
                self.mutex.release()
            time.sleep(0.1)

    def registerServiceProtocols(self):
        """
            注册协议
        """
        self.serviceProtoCalls = {
            'close': onServiceClose,
        }

    def appendServiceProtocols(self, params):
        """ 
            拓展协议
        """
        if not isinstance(params, dict):
            return
        self.serviceProtoCalls.update(params)


    def readPartyServiceProtocol(self):
        """ 
            协议处理
        """
        redis = get_inst()
        if not is_service_started(redis):
            return
        protoName = redis.lpop(self.serviceProtocolTable)
        while protoName:
            log_debug('protoName[%s]' % protoName)
            uuid = protoName[-32:]
            protoName = protoName[:-32]
            protoArgs = protoName.split('|')
            if protoArgs:
                protoHead = protoArgs[0]
                if protoHead in self.serviceProtoCalls:
                    try:
                        result = self.serviceProtoCalls[protoHead](*protoArgs[1:])
                        redis.set(PROTOCOL_RESULT % uuid, json.dumps(result))
                        redis.expire(PROTOCOL_RESULT % uuid, 5)
                    except:
                        traceback.print_exc()
            protoName = redis.lpop(self.serviceProtocolTable)