# -*- coding:utf-8 -*-
# !/bin/python

from common.common_player import CommonPlayer
from common.handle_manger import HandleManger


class PublicPlayer(CommonPlayer):
    def __init__(self):
        super(PublicPlayer, self).__init__()
        self.isReady = False
        self.isproxy = False  # 是否托管中
        self.Timer = None

    def logger(self, str, level='info'):
        try:
            tmp_str = u'%s ' % (self.getHeadTab())
            str = tmp_str + str
            self.game.logger(str, level)
        except:
            print u'[logger] str[%s] level[%s]' % (str, level)

    def getHeadTab(self):
        return '[%s:%s:%s]' % (self.nickname, self.account, self.chair)

    def resetPerGame(self):
        super(PublicPlayer, self).resetPerGame()
        self.isproxy = False  # 是否托管中
        self.Timer = None

    def __str__(self):
        return '(%s curScore[%s])' % (self.account, self.curGameScore)
