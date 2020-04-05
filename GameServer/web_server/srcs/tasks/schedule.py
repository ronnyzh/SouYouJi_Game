#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
        web 的定时任务
"""
from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, '../mahjong')
sys.path.insert(0, '../server_common')
sys.path.insert(0, '..')
from threading import Timer
from server_common.web_db_define import *
from mahjong.model.activeModel import rm_online_activice,add_online_activice,init_all_user_schedule
from config.config import *
from tsconfig import *

redis = get_inst()
last_save_time_str = ""


def get_activices():
    log_debug('当前时间: %s' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    global last_save_time_str
    if not last_save_time_str:
        last_save_time_str = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d")
    if now != last_save_time_str:
        last_save_time_str = now
        init_all_user_schedule(redis)
    infos = []
    keys = redis.keys(ACTIVICE_LIST_TABLE % ('*'))
    for key in keys:
        tableIds = redis.lrange(key, 0, -1)
        agentId = key.split(':')[2]
        for _id in tableIds:
            table = ACTIVICE_TABLE % (_id)
            if not table:
                continue
            info = redis.hgetall(table)
            infos.append(info)
            cur_time = time.time()
            start_time = str2timestamp(info['startdate'])
            end_time = str2timestamp(info['enddate'])
            ts = cur_time - start_time
            last = end_time + ONE_DAY - cur_time
            log_debug('**************************starttimer {0}  last {1}  {2}'.format(ts,last,datetime.now().strftime("%Y-%m-%d")))
            if ts > 0 and info['status'] == STATUS_READY:
                add_online_activice(redis, agentId, _id)
            elif last < 0 and info['status'] == STATUS_STARTING:
                rm_online_activice(redis, agentId, _id)


def loopfunc(starttime):
    get_activices()
    Timer(5, loopfunc, (time.time(),)).start()


def clear_activice_db():
    pipe = redis.pipeline()
    key_list = ["activice:*","resource:*","reward:*","lotterys:*","rewardee:*"]
    for item in key_list:
        keys = redis.keys(item)
        for key in keys:
            pipe.delete(key)
    return pipe.execute()


def start():
    # clear_activice_db()
    timer = Timer(5, loopfunc, (time.time(),))
    timer.start()

if __name__ == '__main__':
    init_log('schedule')
    start()