# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/12/4
Revision: 1.0.0
Description: Description
"""
from model.model_asyn_mysql import *
from model.model_redis import *
from configs import CONFIGS
from public.public_logger import *
from public.public_sqlFormat import *
from define.define_mysql_key import *
from define.define_redis_key import *
import asyncio
from pprint import pprint, pformat


@wraps_getRedis
async def job(redis):
    mysql_logger = getHandlerLogger(loggerLabel='server', level=logging.DEBUG, handler_types=[Handler_Class.Stream])
    async_mysqlDb = Async_Mysql(CONFIGS['async_mysql'], logger=mysql_logger)
    await async_mysqlDb.createPool_async()
    sql, args = FormatSql_Select(
        **dict(
            tableName=Table_match_record,
            orderBy='start_time',
            columnNames=['match_number', 'balance_datas', 'id'],
            orderType='ASC'
        )
    ).getSqlStrAndArgs()
    mysql_logger.info(u'%s %s' % (sql, args))
    results = await async_mysqlDb.select(sql, args)

    for result in results:
        mysql_logger.info(u'%s' % (pformat(result)))

        match_number = result['match_number']
        redisKey = Key_Match_matchNumber_Hesh % match_number
        matchInfo = redis.hgetall(redisKey)
        mysql_logger.info(u'%s' % (pformat(matchInfo)))
        # userIds
        userIds = matchInfo.get('userIds', '')
        userIds = eval(userIds)
        userIds_str = ','.join(map(str, userIds))
        print('userIds_str', userIds_str)
        # serviceTag
        serviceTag = matchInfo.get('serviceTag', '')
        serviceTag = ':'.join(serviceTag.split(':')[1:])
        print('serviceTag', serviceTag)
        # BalanceDatas
        BalanceDatas = matchInfo.get('BalanceDatas', '{}')

        sql, args = FormatSql_Update(**dict(
            tableName=Table_match_record,
            datasDict={
                'user_ids': userIds_str,
                'serviceTag': serviceTag,
                'balance_datas': BalanceDatas,
            },
            whereParams={
                'data': {'match_number': match_number},
                'joinStr': 'AND',
                'sign': '=',
            },
        )).getSqlStrAndArgs()
        mysql_logger.info(u'%s %s' % (sql, args))
        result = await async_mysqlDb.update(sql, args)
        print('result', result)
        redis.expire(redisKey, 60 * 60)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(job())
