# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
from configs import CONFIGS
from model.model_mysql import MySQLdb
from model.model_asyn_mysql import Async_Mysql
import tornado.ioloop
from public.public_logger import *

mysql_logger = getHandlerLogger(fileLabel='mysql', loggerLabel='mysql', level=logging.DEBUG,
                                handler_types=[Handler_Class.RotatingFile])
mysqlDB = MySQLdb(CONFIGS['mysql'])
async_mysqlDb = Async_Mysql(CONFIGS['async_mysql'], logger=mysql_logger)
tornado.ioloop.IOLoop.current().spawn_callback(async_mysqlDb.createPool_async)
