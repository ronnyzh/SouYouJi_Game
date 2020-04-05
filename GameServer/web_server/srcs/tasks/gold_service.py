#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    金币场
"""

from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
from tsconfig import *
sys.path.insert(0, '..')
sys.path.insert(0, '../mahjong')
sys.path.insert(0, '../server_common')
from gold_worker import GoldWorker, onFeedServiceStatus, self_check, clear_on_gold_room_players

sleepingTime = 1
redis = get_inst()


def loopfunc(timeout):
    while True:
        prevtime = time.time()
        try:
            onFeedServiceStatus(redis, timeout + 2)
            self_check(redis)
        except:
            traceback.print_exc()
            break
        elapsetime = time.time() - prevtime
        sleeptime = max(sleepingTime - elapsetime, 0)
        time.sleep(sleeptime)


def start():
    worker = GoldWorker()
    worker.run()
    loopfunc(sleepingTime)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'clean_db':
            clear_on_gold_room_players()
            exit(1)
        print 'usage: python gold_service.py [clean_db]'
        exit(1)
    if len(sys.argv) == 1:
        start()
