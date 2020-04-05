# -*- coding:utf-8 -*-

"""
用来设置房间号
"""

import random
from redis_instance import getInst

'''无配置'''


def do():
    MAX_COUNT = 999999 + 1  # 限制
    maxRoomCount = 100000  # 最大房间数
    GAME_ROOM_SET = 'gameNnm:set'
    redis = getInst(1)
    if maxRoomCount > MAX_COUNT:
        print 'more than %s' % (MAX_COUNT)
    numSet = random.sample(range(MAX_COUNT), maxRoomCount)
    redis.delete(GAME_ROOM_SET)
    redis.sadd(GAME_ROOM_SET, *numSet)
    print redis.scard(GAME_ROOM_SET)


if __name__ == '__main__':
    do()
