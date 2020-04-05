# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/23
Revision: 1.0.0
Description: Description
"""
import aiomysql
import traceback
import re
from pprint import pformat


class Async_Mysql(object):
    PARAMERTS_REG = re.compile(r':([_0-9]*[_A-z]+[_0-9]*[_A-z]*)')

    def __init__(self, mysql_configs, logger=None):
        self._pool = None
        self.configs = mysql_configs
        self.logger = logger

    def log(self, msg='', level='info'):
        try:
            if self.logger:
                self.logger.info(u'[Async_Mysql] %s' % (pformat(msg)))
            else:
                print(u'[Async_Mysql][%s] %s' % (level, pformat(msg)))
        except:
            traceback.print_exc()

    def checkPool(self):
        return self._pool

    async def createPool_async(self, mautocommit=True):
        pool = await aiomysql.create_pool(cursorclass=aiomysql.DictCursor, autocommit=mautocommit, **self.configs)
        self._pool = pool
        self.log(u'mysql连接池已经建立')

    async def close(self):
        self._pool.close()
        await self._pool.wait_closed()
        self.log(u'mysql连接池已经关闭')
        self._pool = None

    async def execute(self, sql, args=None):
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                self.log(u'[execute] sql[%s] args => %s' % (sql, args))
                await cursor.execute(sql, args)

    async def query(self, sql, args=None):
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                self.log(u'[query] sql[%s] args => %s' % (sql, args))
                await cursor.execute(sql, args)
                return await cursor.fetchall()

    async def queryOne(self, sql, args=None):
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                self.log(u'[queryOne] sql[%s] args => %s' % (sql, args))
                await cursor.execute(sql, args)
                return await cursor.fetchone()

    select = query
    selectOne = queryOne

    async def insert(self, sql, args=None):
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                self.log(u'[insert] sql[%s] args => %s' % (sql, args))
                await cursor.execute(sql, args)
                return cursor.lastrowid

    async def update(self, sql, args=None):
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                self.log(u'[update] sql[%s] args => %s' % (sql, args))
                await cursor.execute(sql, args)
                return cursor.rowcount

    async def delete(self, sql, args=None):
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cursor:
                self.log(u'[delete] sql[%s] args => %s' % (sql, args))
                await cursor.execute(sql, args)
                return cursor.rowcount


if __name__ == '__main__':
    import asyncio

    mysql_configs = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "root",
        "db": "game_db",
    }


    async def test():
        mysql_db = Async_Mysql(mysql_configs)
        await mysql_db.createPool_async()
        result = await mysql_db.insert(
            '''INSERT INTO match_player (user_id,game_id,match_id,match_number,fee_type,fee,score,rank,reward_type,reward_fee,create_time) VALUES (%(value_1)s,%(value_2)s,%(value_3)s,%(value_4)s,%(value_5)s,%(value_6)s,%(value_7)s,%(value_8)s,%(value_9)s,%(value_10)s,%(value_11)s)''',
            args={'value_1': 119, 'value_2': 704, 'value_3': 2, 'value_4': '704-2-1575019543204', 'value_5': 1,
                  'value_6': 1, 'value_7': 92, 'value_8': 1, 'value_9': 3, 'value_10': 5, 'value_11': 1575097645}
        )
        print(result)


    asyncio.get_event_loop().run_until_complete(test())
