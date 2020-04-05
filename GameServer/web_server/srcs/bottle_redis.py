# -*-coding:utf8-*-

#!/usr/bin/env python
#-*-coding:utf-8 -*-

"""
@Author: $Author$
@Date: $Date$
@version: $Revision$

Description:
     Description
"""
import redis
import inspect
from bottle import default_app
from common.log import *

class RedisPlugin(object):
    name = 'redis'

    def __init__(self,host="",port="",database="",keyword='redis',password=''):
        conf = default_app().config
        self.host = str(conf.get('redis.host', host))
        self.port = conf.get('redis.port', port)
        self.database = conf.get('redis.database', database)
        self.keyword = str(conf.get('redis.keyword', keyword))
        self.password = str(conf.get('redis.password', password))
        self.redisdb = None
        # salve setting
        self.read_host = str(conf.get('redisSalve.host', None))
        self.read_port = conf.get('redisSalve.port', None)
        self.read_database = conf.get('redisSalve.database', None)
        self.read_keyword = str(conf.get('redisSalve.keyword', None))
        self.read_password = str(conf.get('redisSalve.password', password))
        self.redisReadDb = None

    def setup(self,app):
        for other in app.plugins:
            if not isinstance(other,RedisPlugin): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another redis plugin with "\
                        "conflicting settings (non-unique keyword).")

        if self.redisdb is None:  #主库
            self.redisdb = redis.ConnectionPool(host=self.host, port=self.port, db=self.database, password=self.password)

        if self.redisReadDb is None:#从库,做读配置
            self.redisReadDb = redis.ConnectionPool(host=self.read_host, port=self.read_port, db=self.read_database, password=self.read_password)

    def apply(self,callback,context):
        args = inspect.getargspec(context['callback'])[0]
        if self.keyword not in args:
            return callback

        def wrapper(*args,**kwargs):
            kwargs[self.keyword] = redis.Redis(connection_pool=self.redisdb)
            kwargs[self.keyword].connection_read_pool = self.redisReadDb
            #log_debug('[redis][Instance] connection_read_pool[%s]'%(kwargs[self.keyword].connection_read_pool))
            rv = callback(*args, **kwargs)
            return rv
        return wrapper

Plugin = RedisPlugin
