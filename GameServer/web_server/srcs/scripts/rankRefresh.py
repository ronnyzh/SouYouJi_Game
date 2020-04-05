# -*- coding:utf-8 -*-

"""
每日计算分数
"""
import sys
sys.path.insert(0, '../server_common')
sys.path.insert(0, '../mahjong')

from common import log_util
from web_db_define import *

import time
from datetime import datetime, timedelta, date
import redis
import traceback

REFRESH_TIMES = ['00:00', '06:00', '12:00', '18:00']
WAIT_SLEEP_TIME = 15
SLEEP_TIME = 5 * 60 * 60 + 30 * 60

def addLog(s):
    nowDay = datetime.now().strftime('%Y-%m-%d')
    nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f = file('./log/%s.log'%(nowDay), 'a')
    print s
    f.write('%s: '%nowTime)
    f.write(str(s))
    f.write('\n')
    f.close()

def getInst(dbNum):
    global redisdb
    redisdb = redis.ConnectionPool(host="127.0.0.1", port=6379, db='1', password='')
    return redis.Redis(connection_pool=redisdb)

if __name__ == '__main__':
    redis = getInst(1)
    while True:
        try:
            nowTime = datetime.now()
            nowHour = nowTime.strftime("%H:%M")
            nowDay = nowTime.strftime('%Y-%m-%d')
            addLog('on refresh time: %s %s'%(nowDay, nowHour))
            if nowHour in REFRESH_TIMES:
                time.sleep(WAIT_SLEEP_TIME) #等待入库完成
                lastRank = RANK_COUNT-1
                if nowHour == '00:00':
                    yesterday = date.today() - timedelta(days=1)
                    table = FORMAT_USER_COINDELTA_TABLE%(yesterday)
                else:
                    table = FORMAT_USER_COINDELTA_TABLE%(nowDay)
                redis.delete(TMP_FORMAT_USER_COINDELTA_TABLE)
                addLog('table:%s'%(table))
                lastPlayers = redis.zrevrange(table, lastRank, lastRank, True, int)
                if lastPlayers:
                    lastPlayers = redis.zrevrangebyscore(table, lastPlayers[0][1], lastPlayers[0][1], score_cast_func = int)
                    lastRank = redis.zrevrank(table, lastPlayers[0]) + len(lastPlayers) - 1
                players = redis.zrevrange(table, 0, lastRank, True, int)
                #更低排名玩家的还存不存在，不存在则屏蔽盈利0分玩家
                zeroPlayers = redis.zrevrangebyscore(table, 0, 0, score_cast_func = int)
                if zeroPlayers:
                    less0Rank = redis.zrevrank(table, zeroPlayers[-1])
                    less0RankPlayers = redis.zrevrange(table, less0Rank+1, less0Rank+1, False, int)
                else:
                    less0RankPlayers = None

                rank = prevRank = 1
                sameCount = 0
                prevCoinDelta = players[0][1] if players else 0
                selfRank = 0
                pipe  = redis.pipeline()
                for player in players:
                    if player[1] >= prevCoinDelta:
                        rank = prevRank
                        sameCount += 1
                    else:
                        rank = prevRank + sameCount
                        sameCount = 1
                    prevRank = rank
                    prevCoinDelta = player[1]
                    playerAccount = player[0]
                    addLog('on zadd: account:%s data:%s'%(playerAccount, prevCoinDelta))
                    pipe.zadd(TMP_FORMAT_USER_COINDELTA_TABLE, playerAccount, prevCoinDelta)
                pipe.execute()
                time.sleep(SLEEP_TIME)
            else:
                time.sleep(WAIT_SLEEP_TIME)
        except Exception as e:
            addLog(traceback.format_exc())
            break

