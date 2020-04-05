#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
        娱乐模式 & 竞技场模式
"""

from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
from tsconfig import *
sys.path.insert(0, '..')
from party_worker import SchedulerWorker, onFeedServiceStatus, self_check
sleepingTime = 1
redis = get_inst()


def loopfunc(timeout):
    while True:
        onFeedServiceStatus(redis, timeout + 2)
        prevtime = time.time()
        try:
            self_check(redis)
        except:
            traceback.print_exc()
        elapsetime = time.time() - prevtime
        sleeptime = max(sleepingTime - elapsetime, 0)
        time.sleep(sleeptime)


def start():
    SchedulerWorker().run()
    loopfunc(sleepingTime)


if __name__ == '__main__':
    init_log('party')
    if len(sys.argv) > 2:
        print 'usage: python party_service.py'
        exit(1)
    if len(sys.argv) == 1:
        start()