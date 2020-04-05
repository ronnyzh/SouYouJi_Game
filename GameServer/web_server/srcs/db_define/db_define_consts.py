# -*- coding:utf-8 -*-
# !/usr/bin/python

class Define_Currency():
    Currency_roomCard = 1
    Currency_yyPoint = 2
    Currency_gamePoint = 3
    Currency_cyPoint = 4
    # KEY:货币名称=>货币ID
    # Currency
    Currency = CurrencyName_IdMap = {
        'roomCard': Currency_roomCard,
        'yyPoint': Currency_yyPoint,
        'gamePoint': Currency_gamePoint,
        'cyPoint': Currency_cyPoint,
    }
    Currency_Chinese = {
        Currency_roomCard: '钻石',
        Currency_yyPoint: '椰子积分',
        Currency_gamePoint: '游戏积分',
        Currency_cyPoint: '创盈积分',
    }
    # KEY:货币ID=>货币名称
    CurrencyId_nameMap = {value: key for key, value in Currency.items()}
    CurrencyIdList = CurrencyList = list(CurrencyName_IdMap.values())
    CurrencyNameList = list(CurrencyName_IdMap.keys())

    @classmethod
    def getCurrencyName(cls, currencyId):
        return cls.CurrencyId_nameMap.get(int(currencyId), '')

    @classmethod
    def getCurrencyId(cls, currencyName):
        return cls.CurrencyName_IdMap.get(currencyName, 0)

    @classmethod
    def getCurrencyChinese(cls, currencyId):
        return cls.Currency_Chinese.get(int(currencyId), '未知')


class Email_Type():
    '''邮件类型'''
    none = 0  # 未知类型
    notice = 1  # 通知无附件
    compensateNotice = 2  # 补偿通知(含附件)
    matchAward = 11  # 比赛场奖品
    returnEnrollFee = 12  # 比赛场报名费返还


class MatchOperate(object):
    State_None = 0  # 无状态(大厅状态)
    State_Enroll = 1  # 报完名,等待(大厅状态)
    State_WaitJoinRoom = 2  # 比赛满足,等待玩家进入房间(大厅状态)
    State_ReadyStart = 3  # 游戏已接管,等待比赛开始(倒计时)(游戏状态)
    State_Matching = 4  # 比赛进行中(游戏状态)
    State_Balance = 5  # 比赛结束,结算中(游戏状态)

    State_Ending = 10  # 比赛完美结束
    State_Dismissing = 11  # 比赛正在被解散
    State_Have_Dismiss = 12  # 比赛已解散


MatchGameIds = [701, 702, 703, 704, 705]
