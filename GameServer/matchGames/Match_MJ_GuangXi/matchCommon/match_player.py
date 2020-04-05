# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/1
Revision: 1.0.0
Description: Description
"""
from publicCommon.public_player import PublicPlayer


class MatchPlayer(PublicPlayer):
    def __init__(self):
        self.state = 0
        super(MatchPlayer, self).__init__()
        self.userRecordMgr = None
        self.ip = self.ip or ''
        # 没在房间时,ping的次数
        self.notGamePingCount = 0

    def resetPerGame(self):
        super(MatchPlayer, self).resetPerGame()
