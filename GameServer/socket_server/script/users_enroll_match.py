# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/26
Revision: 1.0.0
Description: Description
"""
import requests

from model.model_redis import getInst

redis = getInst()

gameId = 701
matchId = 3
StartNum = 72
Num = 3


def enrollMatch():
    users = range(StartNum, StartNum + Num)

    for userId in users:
        print(userId)
        r = requests.post('http://127.0.0.1:9797/match/enroll', data=dict(uid=userId, gameId=gameId, matchId=matchId))
        if r.status_code == 200:
            print(r.json())
        else:
            print(r.text)


if __name__ == '__main__':
    enrollMatch()
