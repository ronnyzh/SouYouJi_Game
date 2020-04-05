# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
from functools import wraps


class EventClass(object):
    """
    事件驱动模块
    """
    # 主要是针对mothed方法,只要没有finish就继续执行下一层
    Type_not_finished = 1
    # 返回值为bool,result,如果bool为True就继续执行下一层
    Type_return_true = 2

    @staticmethod
    def execute(target):
        """装饰事件
        :params targer    :  必要。目标函数
        """

        def control(func, *args, **kwarg):
            result = lambda x: target(x)

            def __console(*ag, **kw):
                response = func(*ag, **kw)
                return result(response)

            return __console

        return control

    @staticmethod
    def defaultError_Http_cb(*args, **kwargs):
        print('[defaultError__Http_cb]', args, kwargs)
        return None

    @staticmethod
    def befor(target, keepOnType=Type_not_finished, toPayloadData=False, errorCallBackFunc=defaultError_Http_cb,
              **targetKW):
        """ 函数执行前函数
        """

        def control(func, *args, **kwarg):
            @wraps(func)
            def __console(*ag, **kw):
                self = ag[0]
                print("[befor][start][func: %s.%s][target: %s][payload: %s, %s, %s]" %
                      (self.__class__.__name__, func.__name__, target.__name__, ag, kw, targetKW))
                flag, response = target(*ag, **kw, **targetKW)
                print("[befor][doing][target: %s] flag[%s] response => %s" % (target.__name__, flag, response))
                if not flag:
                    kw["error"] = response
                    if keepOnType == EventClass.Type_not_finished:
                        if self._finished:
                            if errorCallBackFunc:
                                return errorCallBackFunc(*ag, **kw)
                            return response
                        else:
                            response['code'] = response.get('code', -1)
                            self.finish(response)
                    elif keepOnType == EventClass.Type_return_true:
                        if errorCallBackFunc:
                            return errorCallBackFunc(*ag, **kw)
                        return response
                    else:
                        assert False
                else:
                    if response:
                        if toPayloadData:
                            if "payload" in kw and isinstance(kw["payload"], dict):
                                kw["payload"].update(response)
                            else:
                                kw["payload"] = response
                        else:
                            print('[befor]', kw, response)
                            if response:
                                kw.update(response)
                    print("[befor][end][func: %s][args:%s,kw:%s]" % (func.__name__, ag, kw))
                    return func(*ag, **kw)

            return __console

        return control


class EventClassOld(object):
    """
    事件驱动模块
    """
    # 主要是针对mothed方法,只要没有finish就继续执行下一层
    Type_not_finished = 1
    # 返回值为bool,result,如果bool为True就继续执行下一层
    Type_return_true = 2

    @staticmethod
    def execute(target):
        """装饰事件
        :params targer    :  必要。目标函数
        """

        def control(func, *args, **kwarg):
            result = lambda x: target(x)

            def __console(*ag, **kw):
                response = func(*ag, **kw)
                return result(response)

            return __console

        return control

    @staticmethod
    def befor(target, keepOnType=Type_not_finished, toPayloadData=False, errorCallBackFunc=None, **targetKW):
        """ 函数执行前函数
        """

        def control(func, *args, **kwarg):
            @wraps(func)
            def __console(*ag, **kw):
                print("[befor][start][func: %s][target: %s][payload: %s, %s, %s]" %
                      (func.__name__, target.__name__, ag, kw, targetKW))
                if keepOnType == EventClass.Type_not_finished:
                    response = target(*ag, **kw, **targetKW)
                    self = ag[0]
                    if self._finished:
                        if errorCallBackFunc:
                            return errorCallBackFunc(response)
                        return response
                elif keepOnType == EventClass.Type_return_true:
                    flag, response = target(*ag, **kw, **targetKW)
                    if not flag:
                        if errorCallBackFunc:
                            return errorCallBackFunc(response)
                        return response
                else:
                    if errorCallBackFunc:
                        return errorCallBackFunc('未知')
                    return
                if response:
                    if toPayloadData:
                        if "payload" in kw and isinstance(kw["payload"], dict):
                            kw["payload"].update(response)
                        else:
                            kw["payload"] = response
                    else:
                        if response:
                            kw.update(response)
                print("[befor][end][func: %s][args:%s,kw:%s]" % (func.__name__, ag, kw))
                return func(*ag, **kw)

            return __console

        return control

    @staticmethod
    def after(target, *argsv, **kwargs):
        """ 函数执行之后是否执行某函数

        """

        def control(func, *args, **kwarg):
            result = lambda x: target(x)

            @wraps(func)
            def __console(*ag, **kw):
                response = func(*ag, **kw)
                print("[after][request][func: %s][payload: %s]" % (func.__name__, response))
                if not isinstance(response, dict) or not response:
                    if isinstance(response, tuple):
                        return response
                    return StatusCode.ERROR, StatusCode.ERROR['resultCode']
                if response.get("resultCode") and response.get("resultCode") != 200:
                    return response, response.get("resultCode", 400)
                if response.get("errStatus") and response.get("errStatus") != 200:
                    return response, response.get("resultCode", 200)

                return result(response)

            return __console

        return control
