# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/26
Revision: 1.0.0
Description: Description
"""
from twisted.enterprise import adbapi
from twisted.internet import reactor, defer, task
import pymysql
import traceback
import sys
import random

from configs import CONFIGS
from sqlFormat import *
from publicCommon.logger_mgr import getLogger

sql_logger = getLogger('mysql')

from twisted.enterprise import adbapi
from twisted.python import log, compat

log.startLogging(sys.stdout)


class AdbApi_ConnectionPool(adbapi.ConnectionPool):
    def _runInteraction(self, interaction, *args, **kwargs):
        conn = self.connectionFactory(self)
        conn.ping()
        trans = self.transactionFactory(self, conn)
        try:
            result = interaction(trans, *args, **kwargs)
            trans.close()
            conn.commit()
            return result
        except:
            excType, excValue, excTraceback = sys.exc_info()
            try:
                conn.rollback()
            except:
                log.err(None, "Rollback failed")
            compat.reraise(excValue, excTraceback)


class mysql_twisted(object):
    def __init__(self, init_command='', **configs):
        self._pool = None
        self.configs = configs
        self.init_command = init_command
        self.initPool()

    def check_pool(self):
        if self._pool:
            sql_logger.info(u'[check_pool] %s' % self._pool.connections)
        return self._pool

    def initPool(self):
        try:
            _pool = AdbApi_ConnectionPool(
                cp_reconnect=True,
                cp_noisy=True,
                dbapiName='pymysql',
                cursorclass=pymysql.cursors.DictCursor,
                **self.configs
            )
            if self.init_command:
                d = self.execute(self.init_command, _pool=_pool)
                d.addCallbacks(
                    callback=self.connect_pool_suc, callbackKeywords={'_pool': _pool},
                    errback=self.connect_pool_fail,
                )
        except:
            traceback.print_exc()
            raise

    def connect_pool_suc(self, _, _pool, *args, **kwargs):
        sql_logger.info(u'[connect_pool_suc] 连接成功 %s' % _pool)
        self._pool = _pool

    def connect_pool_fail(self, failure, *args, **kwargs):
        sql_logger.info(u'[connect_pool_fail] 连接失败 %s' % failure.getErrorMessage())

    def del_pool(self, msg=u'未知'):
        sql_logger.info(u'[del_pool] 原因[%s]' % msg)
        self._pool = None

    @defer.inlineCallbacks
    def default_action(self, sql, args=None, callBack=None, actionName='None'):
        number = random.randint(100000, 999999)
        try:
            sql_logger.info(u'[%s:%s] sql[%s]' % (actionName, number, sql))
            sql_logger.info(u'[%s:%s] args => %s' % (actionName, number, args))
            result = yield self.execute(sql, args, callBack=callBack, number=number)
            sql_logger.info(u'[%s:%s] result => %s' % (actionName, number, result))
        except:
            for tb in traceback.format_exc().splitlines():
                sql_logger.error(u'[Error][%s:%s] %s' % (actionName, number, tb))
            sql_logger.error(u'[Error][%s:%s] sql[%s]' % (actionName, number, sql))
            sql_logger.error(u'[Error][%s:%s] args => %s' % (actionName, number, args))
            traceback.print_exc()
            raise
        else:
            defer.returnValue(result)

    def select(self, *args, **kwargs):
        return self.default_action(callBack=lambda cursor: cursor.fetchall(), actionName='select', *args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.default_action(callBack=lambda cursor: cursor.lastrowid, actionName='insert', *args, **kwargs)

    def update(self, *args, **kwargs):
        return self.default_action(callBack=lambda cursor: cursor.rowcount, actionName='update', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.default_action(callBack=lambda cursor: cursor.rowcount, actionName='update', *args, **kwargs)

    def execute(self, sql, args=None, callBack=None, _pool=None, number=0):
        if not _pool:
            _pool = self._pool
        d = _pool.runInteraction(self._execute, sql=sql, args=args, callBack=callBack, number=number)
        return d

    def _execute(self, cursor, sql, args=None, callBack=None, number=0):
        sql_logger.info(u'[_execute:%s] [%s]' % (number, cursor.connection))
        cursor.execute(sql, args)
        result = callBack(cursor) if callBack else cursor
        return result


if __name__ == '__main__':
    import logging
    import logging.handlers

    sql_logger = logging.getLogger('mysql')
    sql_logger.addHandler(logging.StreamHandler())


    @defer.inlineCallbacks
    def asb(mysql_db):
        try:
            sql, args = FormatSql_Update(**dict(
                tableName='match_record',
                datasDict={
                    'game_id': random.randint(1, 100),
                },
                whereParams={
                    'data': {'match_number': '0'}
                },

            )).getSqlStrAndArgs()
            result = yield mysql_db.update(sql, args)
        except:
            traceback.print_exc()
        else:
            print(result)
            defer.returnValue(result)


    def abc(mysql_db):
        sql, args = FormatSql_Update(**dict(
            tableName='match_record',
            datasDict={
                'game_id': random.randint(1, 100),
            },
            whereParams={
                'data': {'match_number': '0'}
            },

        )).getSqlStrAndArgs()
        if mysql_db.check_pool():
            for x in xrange(10):
                d = mysql_db.update(sql, args)
                d.addCallbacks(callback=suc, callbackKeywords={'1': 1},
                    errback=errPrint,errbackArgs=(1, 2, 3))

    def suc(*args,**kwargs):
        print('[suc]',args)
        print('[suc]',kwargs)

    def errPrint(failure, *args, **kwargs):
        # print('[errPrint]', str(failure))
        print('[errPrint]', args)
        print('[errPrint]', kwargs)
        print(failure.getErrorMessage())


    db_settings = dict(
        db='game_db',
        host='192.168.50.2',
        port=3306,
        user='root',
        passwd='root',
        charset='utf8',
        init_command='select count(*) from match_record',
        cp_min=5,
        cp_max=10,
    )
    mysql_db = mysql_twisted(**db_settings)
    task.LoopingCall(abc, mysql_db).start(1, False)
    # task.LoopingCall(asb, mysql_db).start(5, False)
    # abc(mysql_db)
    # asb(mysql_db)
    reactor.run()
