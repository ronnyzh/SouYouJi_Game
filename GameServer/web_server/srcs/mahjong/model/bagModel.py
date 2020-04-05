# -*- coding:utf-8 -*-
# !/usr/bin/python

"""

     背包道具模型

"""
from common.log import log_debug
from web_db_define import *
from datetime import *
from bag.bag_config import bag_redis
from red_envelope_db_define import *

import time
import json
import random

def getItemListInfo():
    item_ids = bag_redis.smembers(ITEM_ID_SET)
    data = []
    for item_id in item_ids:
        dic = bag_redis.hgetall(ITEM_ATTRS%item_id)
        data.append(dic)

    res = json.dumps({"count":len(data),"data":data})
    return res

def changeIsDelete(item_id,ci):
    bag_redis.hset(ITEM_ATTRS%item_id,'is_delete',ci)

def changeIsGoods(item_id,ig):
    bag_redis.hset(ITEM_ATTRS%item_id,'is_goods',ig)

def changeCanUse(item_id,cu):
    bag_redis.hset(ITEM_ATTRS%item_id,'can_use',cu)

def changeBagShow(item_id,bs):
    bag_redis.hset(ITEM_ATTRS%item_id,'bag_show',bs)

def getModifyItemInfo(item_id):
    return bag_redis.hgetall(ITEM_ATTRS%item_id)

def getItemTtileAndId():
    item_ids = bag_redis.smembers(ITEM_ID_SET)
    data = []
    for item_id in item_ids:
        title = bag_redis.hget(ITEM_ATTRS%item_id,'title')
        dic = {
            'title':title,
            'id':item_id
        }
        data.append(dic)

    return data


# 元宝当天信息
def get_redbag_info(redis,selfUid,startDate,endDate):
    try:
        startDate = datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.strptime(endDate, '%Y-%m-%d')
    except:
        weekDelTime = timedelta(7)
        weekBefore = datetime.now() - weekDelTime
        startDate = weekBefore
        endDate = datetime.now()
    deltaTime = timedelta(1)
    res = []
    while startDate <= endDate:
        dateStr = endDate.strftime('%Y-%m-%d')
        #if bag_redis.exists(RED_ENVELOPE_DAY_INFO % (dateStr,)):
        info1 = bag_redis.hgetall(RED_ENVELOPE_DAY_INFO % (dateStr,))
        info = {}

        info['date'] = dateStr
        info['day_join_num'] = info1.get('playerCount',0)
        info['day_round'] = info1.get('gameRound',0) if info1.get('gameRound',0) else 0
        info['day_send_redbag'] =round( ( int(info1.get('30',0)) + int(info1.get('60',0)) + int(info1.get('120',0)) ) / 100.0 , 2)
        info['day_send_vcoin'] = int(info1.get('3',0)) + int(info1.get('6',0)) + int(info1.get('12',0)) # 当天发放元宝
        #info['day_send_vcoin'] = bag_redis.get('vcoin:present:date:%s:sum'%dateStr)
        info['day_present_redbag'] = info1.get('baselive_goldingot',0)
        info['day_room_fee'] = info1.get('roomCharge',0) if info1.get('roomCharge',0) else 0
        info['b_robot_change'] = info1.get('B',0)
        info['d_robot_change'] = info1.get('D',0)
        info['diamond_to_vcoin_num'] = 0 #info1.get('playerCount',0)
        r2c = bag_redis.get("redbag2cash:date:%s"%dateStr)
        # vcn = bag_redis.get("buy:vcoin:date:%s"%dateStr)
        info['player_claim_redbag_cash'] = r2c if r2c else 0#info1.get('playerCount',0)
        # info['vcoin_charge_num'] = vcn if vcn else 0 #info1.get('playerCount',0)
        # info['charge_order_num'] = 0 #info1.get('playerCount',0)

        res.append(info)
        endDate -= deltaTime
    return {"count": 1, "data": res}

def get_redbag_sum_info():
    res = [bag_redis.hgetall("redbag:sum:info")]
    return json.dumps({"count": 1, "data": res})


def get_exchange_info():
    course_ids = bag_redis.smembers('currency:change:course:set')
    data = []
    for cid in course_ids:
        dic = bag_redis.hgetall("currency:change:course:%s:hesh"%cid)
        dic['cid'] = cid
        data.append(dic)
    return json.dumps({"count":len(data),"data":data})

def get_strftime(timeStamp, timeType="%Y-%m-%d %H:%M:%S"):
    timeStamp = int(str(timeStamp)[:10])
    timeStamp = float(timeStamp)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def get_bag_mail_list(redis, sesion, weekList, condition):
    """获取邮件列表"""
    res = []
    for date in weekList:
        uesr_email_date_table = USER_EMAIL_DATE_SET % date
        if bag_redis.exists(uesr_email_date_table):
            mail_list = bag_redis.smembers(uesr_email_date_table)
            for mail in mail_list:
                if condition.get('eid'):
                    if mail != condition.get('eid'):
                        continue
                mail_info = bag_redis.hgetall(EMAIL_HASH % mail)
                if not mail_info:
                    continue
                read_time, valid_time, userId = mail_info.get('read_time'), mail_info.get('valid_time'), mail_info.get('userId')
                if condition.get('userId'):
                    if userId != condition.get('userId'):
                        continue
                nickname, account = redis.hmget(FORMAT_USER_TABLE % userId, ('nickname', 'account'))
                awards = mail_info.get('awards', '')
                awardStr, enclosureNum, bagId = '', '', '0'
                if awards:
                    bagId, bagNum = awards.split(',')
                    bagName = MATCH_AWARDS_TYPE_TABLE[bagId]
                    bagName = MATCH_AWARDS_NAME_TABLE[bagName]
                    awardStr = '%s' % bagName
                    enclosureNum = '%s' % bagNum
                mail_info['awardStr'] = awardStr
                if condition.get('enclosureType'):
                    if bagId != condition.get('enclosureType'):
                        continue
                mail_info['enclosureNum'] = enclosureNum
                mail_info['user'] = '%s / %s / %s' % (userId, nickname, account)
                mail_info['eid'] = mail
                if mail_info.get('valid_time'):
                    timeStamp = int(read_time) + int(valid_time) * 86400 * 1000
                    mail_info['valid_time'] = get_strftime(timeStamp)
                if mail_info.get('read_time'):
                    mail_info['read_time'] = get_strftime(read_time)
                if condition.get('isRead'):
                    if mail_info['read'] != condition.get('isRead'):
                        continue
                if mail_info.get('is_get'):
                    award_time = mail_info.get('award_time')
                    mail_info['is_get'] = get_strftime(award_time)
                    if condition.get('isGet') == '0':
                        continue
                else:
                    mail_info['is_get'] = '尚未领取' if awardStr else '空'
                    if condition.get('isGet') == '1':
                        continue

                mail_info['op'] = [
                    {'url': '/admin/bag/look/mail', 'txt': '查看', 'method': 'GET'},
                    {'url':  '/admin/bag/mail/delete', 'txt': '删除', 'method': 'POST'},
                ]
                res.append(mail_info)
    return res

def get_bag_look_mail(redis, session, userId, eid):
    """获取邮件详情"""
    userId = userId.split(' ')[0]
    userId = userId.split(':')[-1]
    userTable = FORMAT_USER_TABLE % userId
    account, nickname = redis.hmget(userTable, ('account', 'nickname'))

    EnclosureList = {'1': 'roomCard', '3': 'gamePoint'}
    FeeTypeList = {'roomCard': '钻石', 'gamePoint': '积分'}

    mailInfo = bag_redis.hgetall(EMAIL_HASH % eid)
    if not mailInfo:
        return {}
    awards = mailInfo.get('awards', '')
    if awards:
        awards = awards.split(',')
        awardType = EnclosureList.get(awards[0], 'roomCard')
        awardType = FeeTypeList.get(awardType, '钻石')
        awards = '%s ：%s' % (awardType, awards[-1])
    mailInfo['awards'] = awards
    read_time = mailInfo.get('read_time', '')
    award_time = mailInfo.get('award_time', '')
    if read_time:
        greadTimeStamp = get_strftime(read_time)
        mailInfo['read_time'] = greadTimeStamp
    if award_time:
        awardTimeStamp = get_strftime(award_time)
        mailInfo['award_time'] = awardTimeStamp
    mailInfo['account'] = account
    mailInfo['nickname'] = nickname
    return mailInfo