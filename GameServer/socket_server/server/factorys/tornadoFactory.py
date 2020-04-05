# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
import traceback

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web
from typing import *

from define.define_redis_key import *
from define.define_consts import *
from public.public_logger import *


class baseFactory(object):
    def __init__(self, address='127.0.0.1', port=9797, debug=False, *args, **kwargs):
        self.address = address
        self.port = port
        self.serverTag = '%s:%s' % (self.address, self.port)
        self.debug = debug
        self.runtime = int(time.time())
        self.OrderJob = {}
        self._logger_ = None
        self.curServerStage = ServerStage.none
        self.setServerOrderJob()

    def getLogger(self):
        logger = getHandlerLogger(fileLabel='%s_%s_server' % (self.address, self.port), loggerLabel='server',
                                  level=logging.DEBUG, handler_types=[Handler_Class.HourFile], when='H')
        logger.setLevel(logging.DEBUG)
        return logger

    def log(self, msg='', level='info'):
        if not self._logger_:
            self._logger_ = self.getLogger()
        try:
            if level in ['warn', 'warning']:
                self._logger_.warning(msg)
            elif level == 'error':
                self._logger_.error(msg)
            else:
                self._logger_.info(msg)
        except:
            traceback.print_exc()
            print(msg)

    def setServerOrderJob(self):
        self.OrderJob['closeServer'] = self.closeServer

    def closeServer(self, waitSecond: int = 60, *args, **kwargs):
        waitSecond = int(waitSecond)
        if self.curServerStage == ServerStage.readyClose:
            return
        self.curServerStage = ServerStage.readyClose
        self.log('服务器[%s]正在关闭,将在[%s]秒后关闭' % (self.serverTag, waitSecond))
        self.add_timeLater_callFunc(delay=waitSecond, callback=self.doCloseServer)

    def doCloseServer(self, *args, **kwargs):
        self.curServerStage = ServerStage.Closed
        tornado.ioloop.IOLoop.current().stop()
        self.log('服务器[%s]已经关闭' % (self.serverTag))

    def onHeartbeat(self):
        timeStamp = int(time.time() * 1000)
        try:
            self.onTick(timeStamp)
        except:
            traceback.print_exc()

    def onTick(self, timeStamp):
        self.checkOrderJobs()

    def checkOrderJobs(self):
        orderServices = self.getOrderServices()
        for _order in orderServices:
            _orderArgs = _order.split('|')
            jobKey = _orderArgs.pop(0)
            jobFunc = self.OrderJob.get(jobKey, None)
            if jobFunc:
                self.doOrderJobs_before(jobFunc, _orderArgs, _order)
                doResult, err = self.doOrderJobs_doing(jobFunc, _orderArgs, _order)
                if doResult:
                    self.doOrderJobs_afterSuc(jobFunc, _orderArgs, _order)
                else:
                    self.doOrderJobs_afterFaild(jobFunc, _orderArgs, _order, err)

    def getOrderServices(self):
        return []

    def notFoundOrderJob(self, jobKey, orderArgs):
        self.log('[notFoundOrderJob] 未知任务[%s]=> %s' % (jobKey, orderArgs))

    def doOrderJobs_before(self, jobFunc, orderArgs, order):
        pass

    def doOrderJobs_doing(self, jobFunc, orderArgs, order):
        self.log('将要执行[%s]' % (order))
        try:
            jobFunc(*orderArgs)
        except Exception as err:
            traceback.print_exc()
            self.log('[ERROR][doOrderJobs_doing]执行[%s]失败' % (order), level='error')
            return False, err
        else:
            return True, ''

    def doOrderJobs_afterSuc(self, job, _orderArgs, _order):
        pass

    def doOrderJobs_afterFaild(self, job, _orderArgs, _order, err=''):
        pass

    def add_timeLater_callFunc(self, delay: float = 0, callback=None, **kwargs):
        if not callback:
            return
        tornado.ioloop.IOLoop.current().call_later(delay=delay, callback=callback, **kwargs)

    def add_callAt_callFunc(self, when: float, callback=None, **kwargs):
        if not callback:
            return
        return tornado.ioloop.IOLoop.current().call_at(when=when, callback=callback, **kwargs)

    def add_PeriodicCallback(self, callback: Callable, callback_time: float, rightAwayDo: bool = False,
                             jitter: float = 0):
        if rightAwayDo:
            callback()
        periodicClass = tornado.ioloop.PeriodicCallback(callback, callback_time, jitter=jitter)
        periodicClass.start()
        return periodicClass


class TornadoFactory(baseFactory):
    def __init__(self, *args, **kwargs):
        super(TornadoFactory, self).__init__(*args, **kwargs)
        self.httpServer = None

    def getAppRouterHandler(self):
        return []

    def getApplicationConfigs(self):
        return dict(
            static_path=os.path.join(os.path.dirname(__file__), "..\\static"),
            template_path=os.path.join(os.path.dirname(__file__), "..\\template"),
            debug=self.debug,
            compiled_template_cache=False
        )

    def initApplication(self):
        app = tornado.web.Application(self.getAppRouterHandler(), **self.getApplicationConfigs())
        app.factory = self
        return app

    def doBeforeServerStart(self):
        self.curServerStage = ServerStage.readyStart

    def doAfterServerStart(self):
        self.curServerStage = ServerStage.doing

    def run_server(self):
        self.log('服务器[%s]正在启动' % (self.serverTag))
        self.doBeforeServerStart()
        app = self.initApplication()
        self.httpServer = tornado.httpserver.HTTPServer(app)
        self.httpServer.listen(self.port, '0.0.0.0')
        self.httpServer.address = self.address
        self.httpServer.port = self.port
        self.httpServer.factory = self
        tornado.ioloop.PeriodicCallback(self.onHeartbeat, 3000).start()
        self.log('服务器[%s]已启动' % (self.serverTag))
        self.doAfterServerStart()
        tornado.ioloop.IOLoop.current().start()
