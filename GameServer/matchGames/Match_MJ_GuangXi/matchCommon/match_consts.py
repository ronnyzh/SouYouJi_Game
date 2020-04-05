# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/22
Revision: 1.0.0
Description: Description
"""


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


class Disconnected_actionType():
    # 1: 重新登录, 2: 重连, 3: 断开
    relogin = 1
    reconnect = 2
    disconnect = 3


class Email_Type():
    '''邮件类型'''
    none = 0  # 未知类型
    notice = 1  # 通知无附件
    compensateNotice = 2  # 补偿通知(含附件)
    matchAward = 11  # 比赛场奖品
    returnEnrollFee = 12  # 比赛场报名费返还
