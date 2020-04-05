#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    清除金币场统计数据
"""

from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, '..')
sys.path.insert(0, '../mahjong')
sys.path.insert(0, '../server_common')
import traceback
import redis
from tsconfig import get_pub_inst
from model.gold_db_define import MASTER_GAMEID
from web_db_define import GAME2REDIS


def getPrivateRedisInst(redisdb, gameid):
    """
        获取redis连接实例
    """
    try:
        if not redisdb.exists(GAME2REDIS % gameid):
            return None
        info = redisdb.hgetall(GAME2REDIS % gameid)
        ip = info['ip']
        passwd = info['passwd']
        port = int(info['port'])
        dbnum = int(info['num'])
        print info
        redisdb = redis.ConnectionPool(host=ip, port=port, db=dbnum, password=passwd)
        return redis.Redis(connection_pool=redisdb)
    except:
        traceback.print_exc()
        return None


def clear_gold_statis():
    redis = getPrivateRedisInst(get_pub_inst(), MASTER_GAMEID)
    pipe = redis.pipeline()
    for key in redis.keys('gold:*'):
        pipe.delete(key)
    return pipe.execute()

if __name__ == '__main__':
    clear_gold_statis()
