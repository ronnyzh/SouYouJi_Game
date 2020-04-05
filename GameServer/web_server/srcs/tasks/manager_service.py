#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
        web 通讯模块
        主要用于同游戏包通讯 定时查询等任务
"""
from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from threading import Timer
from tsconfig import *
sys.path.insert(0, '../mahjong')
sys.path.insert(0, '../server_common')
sys.path.insert(0, '..')
from model.niuniuModel import NIUNIU_ACTIVI_CONFIG_TABLE
from worker import SchedulerWorker, onFeedServiceStatus

# 睡眠时间
sleepingTime = 4
ActiveTable = NIUNIU_ACTIVI_CONFIG_TABLE
redis = get_inst()


def check_niuniu_active():
    """ 
        监听牛牛活动状态
    """
    log_debug('当前时间: %s' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if not redis.exists(ActiveTable):
        log_debug('当前没有牛牛活动')
        return
    info = redis.hgetall(ActiveTable)
    if not info:
        return

    start_time = str2timestamp2(info['start_date'])
    end_time = str2timestamp2(info['end_date'])
    if end_time <= start_time:
        return
    cur_time = time.time()
    status = info.get('status', '')
    if status == '0':
        log_debug('牛牛活动未开始')
    if cur_time - start_time > 0 and status == '0':
        redis.hset(ActiveTable, 'status', 1)
        log_debug('牛牛活动开始')
    if end_time - cur_time < 0 and status == '1':
        redis.hset(ActiveTable, 'status', 2)
        log_debug('牛牛活动结束')


def loopfunc(timeout):
    onFeedServiceStatus(redis, timeout+2)
    check_niuniu_active()
    Timer(timeout, loopfunc, (timeout,)).start()


def start():
    SchedulerWorker().run()
    timer = Timer(sleepingTime, loopfunc, (sleepingTime,))
    timer.start()


if __name__ == '__main__':
    init_log('manager')
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] not in ['active_start']):
        print 'usage: python manager_service.py [active_start]'
        print 'active_start: start niuniu active'
        exit(1)
    if len(sys.argv) == 1:
        start()
    else:
        redis.hmset(ActiveTable, config['niuniu_active'])
        print '活动信息:{0}'.format(redis.hgetall(ActiveTable))
