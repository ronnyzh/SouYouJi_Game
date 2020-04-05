# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description: Timer
"""

import time
from threading import RLock
import traceback
import logging
import logging.handlers

import logger_mgr

t_logger = logger_mgr.getLogger('Timer')


class log(object):
    def info(self, str, *args, **kwargs):
        try:
            t_logger.info(str)
        except:
            traceback.print_exc()

    def error(self, str, *args, **kwargs):
        try:
            t_logger.error(str)
        except:
            traceback.print_exc()


Tlogger = log()


def get_nowTime():
    return int(time.time() * 1000)


class TimersMgr(object):
    def __init__(self, Game=None):
        self.timer = None
        self.timerId = 0
        self.timerList = []
        self.timerListId = 0
        if Game:
            self.game = Game
        self.lock = RLock()

    def reset_timer(self):
        self.__init__()

    def get_nextId(self, type=0):
        self.lock.acquire()
        if type == 0:
            self.timerId += 1
            self.lock.release()
            return self.timerId
        elif type == 1:
            self.timerListId += 1
            self.lock.release()
            return self.timerListId
        else:
            self.lock.release()

    def add_Timer(self, Timer, type=0):
        Timer.ID = self.get_nextId(type)
        Tlogger.info(Timer.__str__(Note='增加(%s)' % type))
        self.lock.acquire()
        if type == 0:
            self.timer = Timer
        elif type == 1:
            self.timerList.append(Timer)
        self.lock.release()

    def get_nowtime(self):
        return int(time.time() * 1000)

    def check_timer(self):
        timestamp = self.get_nowTime()
        if self.timer:
            if timestamp - self.timer.startTime >= self.timer.overTime:
                _timer = self.timer
                self.timer = None
                try:
                    _timer.do_job()
                except:
                    traceback.print_exc()
                    Tlogger.info(_timer.__str__(Note='发生错误'))
                finally:
                    self.del_timer(_timer, type=0)

        if self.timerList:
            for _timer in self.timerList:
                if timestamp - _timer.startTime >= _timer.overTime:
                    try:
                        _timer.do_job()
                    except:
                        traceback.print_exc()
                        Tlogger.info(_timer.__str__(Note='发生错误'))
                    finally:
                        self.del_timer(_timer, type=1)

    def del_timer(self, Timer, type=0):
        self.lock.acquire()
        if type == 0:
            try:
                Timer.__del__(isPrint=True)
                del Timer
            except:
                pass
        elif type == 1:
            if Timer in self.timerList:
                self.timerList.remove(Timer)
                try:
                    Timer.__del__(isPrint=True)
                    del Timer
                except:
                    pass
        self.lock.release()

    def get_nowTime(self):
        return int(time.time() * 1000)

    def getTimer(self, callback, params=(), startTime=0, overTime=0, note='默认'):
        return Timer(callback, params, startTime, overTime, note, self.game.getTimerNum() if self.game else '000000')


class Timer(object):
    def __init__(self, callback, params=(), startTime=0, overTime=0, note='默认', num='000000'):
        self.callback = callback
        self.params = params
        self.startTime = startTime if startTime else int(time.time() * 1000)
        self.overTime = overTime
        self.note = note
        self.action = 0
        self.ID = 0
        self.num = num
        self.isDelete = False
        Tlogger.info(self.__str__('设置'))

    def __str__(self, Note='打印'):

        try:
            return 'num[%s] [%s] Timer[%s] ID[%s] callback[%s] params%s startTime[%s] overTime[%s] isDelete[%s]' % \
                   (self.num, Note, self.note, self.ID or '未知', self.callback.__name__, list(self.params),
                    self.startTime, self.overTime, self.isDelete)
        except:
            traceback.print_exc()
            return 'Error'

    def do_job(self):
        if not self.checkLive():
            Tlogger.info(self.__str__('已经销毁,忽略执行'))
        if self.action:
            Tlogger.info(self.__str__('已经执行,忽略执行'))
            return
        Tlogger.info(self.__str__('执行'))
        self.callback(*self.params)
        self.action += 1

    def get_SurplusMS(self, timestamp=0):
        if not timestamp:
            timestamp = get_nowTime()
        interval = self.overTime - (timestamp - self.startTime)
        return interval

    def checkLive(self):
        if self.isDelete:
            return False
        return True

    def __del__(self, isPrint=False):
        try:
            self.isDelete = True
            if isPrint:
                Tlogger.info(self.__str__(Note='主动销毁'))
        except:
            pass
