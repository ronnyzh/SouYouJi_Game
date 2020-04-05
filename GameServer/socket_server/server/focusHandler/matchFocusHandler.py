# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/5
Revision: 1.0.0
Description: Description
"""
import copy
from typing import *
from datetime import datetime
import uuid
import time

from define.define_consts import *
from server.operate import MatchOperate
from define.define_redis_key import *
from model.model_redis import getInst


class MatchFocusHandler(object):
    @classmethod
    def infoList(cls, self, uid, gameId=None, *args, **kwargs):
        flag, cb_data = MatchOperate.existMatchGame(self=self, gameId=gameId)
        if flag:
            _, cb_data = MatchOperate.getUserMatchEnrollInfo(self=self, uid=uid)
            enrollInfo = cb_data.get('enrollInfo', {})
            matchInfoMap = copy.deepcopy(self.factory.matchInfoMap)
            if gameId:
                if gameId not in matchInfoMap:
                    return False, {'msg': '获取失败,没有该游戏的相关赛事', 'gameId': gameId, 'code': -1}
                return True, {'msg': '获取成功', 'data': {
                    'matchDatas': matchInfoMap[gameId], 'enrollInfo': enrollInfo}, 'gameId': gameId, 'code': 0}
            else:
                return True, {'msg': '获取成功', 'data': {'matchDatas': matchInfoMap, 'enrollInfo': enrollInfo}, 'code': 0}
        return flag, cb_data

    @classmethod
    def enroll_do(cls, self, uid, gameId, matchId):
        flag, cb_data = MatchOperate.existMatchGameMatchId(self=self, gameId=gameId, matchId=matchId)
        if flag:
            _, cb_data = MatchOperate.getUserMatchEnrollInfo(self=self, uid=uid)
            enrollInfo = cb_data.get('enrollInfo', {})
            if enrollInfo:
                return False, {'msg': '报名失败, 您当前已存在报名了的赛事, 不可同时报名多场比赛',
                               'data': {'enrollInfo': enrollInfo}, 'code': -1, 'gameId': gameId, 'matchId': matchId}
            matchMgr = self.getMatchMgr(gameId=gameId, matchId=matchId)
            if matchMgr.enroll_status != CanEnrollStatus:
                return False, {'msg': '报名失败, 当前不可报名', 'code': -1, 'gameId': gameId, 'matchId': matchId}
            flag, cb_data = matchMgr.userEnroll_do(uid=uid)
            if not flag:
                return False, {'msg': cb_data.get('msg', '报名失败, 请稍后重试'), 'code': -1, 'gameId': gameId,
                               'matchId': matchId}
            enrollInfo = cb_data.get('enrollInfo', {})
            changeTrade = cb_data.get('changeTrade', {})
            return True, {'msg': '报名成功', 'data': {'enrollInfo': enrollInfo, 'changeTrade': changeTrade}, 'code': 0,
                          'gameId': gameId, 'matchId': matchId}
        return flag, cb_data

    @classmethod
    def enroll_cancle(cls, self, uid, gameId, matchId):
        _, cb_data = MatchOperate.getUserMatchEnrollInfo(self=self, uid=uid)
        enrollInfo = cb_data.get('enrollInfo', {})
        if not enrollInfo:
            return False, {'msg': '当前无已报名的赛事', 'code': -1, 'gameId': gameId, 'matchId': matchId}
        flag, cb_data = MatchOperate.existMatchGameMatchId(self=self, gameId=gameId, matchId=matchId)
        if flag:
            if int(enrollInfo['state']) != MatchOperate.State_Enroll:
                return False, {'msg': '你有正在进行的比赛,不能取消,请尽快加入比赛', 'data': {'enrollInfo': enrollInfo}, 'code': -1,
                               'gameId': gameId, 'matchId': matchId}
            elif int(enrollInfo['gameId']) != gameId or int(enrollInfo['matchId']) != matchId:
                return False, {'msg': '所需取消报名的比赛并未报名,无需取消,存在其他已报名赛事',
                               'data': {'enrollInfo': enrollInfo}, 'code': -1, 'gameId': gameId, 'matchId': matchId}
            else:
                matchMgr = self.getMatchMgr(gameId=gameId, matchId=matchId)
                if not matchMgr:
                    return False, {'msg': '赛事不存在', 'code': -1, 'gameId': gameId, 'matchId': matchId}
                flag, cb_data = matchMgr.userEnroll_cancel(uid=uid)
                if not flag:
                    return False, {'msg': cb_data.get('msg', '取消报名失败, 请稍后重试'), 'code': -1, 'gameId': gameId,
                                   'matchId': matchId}
                changeTrade = cb_data.get('changeTrade', {})
                return True, {'msg': '取消报名成功', 'data': {'changeTrade': changeTrade}, 'code': 0, 'gameId': gameId,
                              'matchId': matchId}
        else:
            redis = getInst()
            Match_UserEnroll_Key = Key_Match_UserEnroll % uid
            pipe = redis.pipeline()
            pipe.delete(Match_UserEnroll_Key)
            pipe.zrem(Key_Match_EnrollUsers_Zset % (gameId, matchId), uid)
            pipe.execute()
            noticeMsg = '您想要取消的赛事编号为[%s-%s]已被删除,现帮您取消报名状态,取消后您可以参加其他赛事,如果当初报名含有报名费,请联系客服补偿,敬请谅解.'
            cls.send_mail(uids_list=uid, title='比赛场取消报名须知',
                          body=noticeMsg % (gameId, matchId),
                          emailType=Email_Type.notice)
            return True, {'msg': '报名已取消,报名费请留意邮件', 'data': {'changeTrade': {}}, 'code': 0, 'gameId': gameId,
                          'matchId': matchId}
        # return flag, cb_data

    @classmethod
    def send_mail(cls, uids_list: Union[list, int, str], title: str, body: str, enclosure_id: int = 0,
                  enclosure_num: int = 0, emailType=Email_Type.none):
        '''
        发送邮件接口
        :param uid: 用户,多个可用逗号分隔
        :param title: 标题
        :param body: 内容
        :param enclosure_id: 附件id
        :param enclosure_num: 附件数量
        :return: None
        '''
        USER_EMAIL_SET = "user:uid:%s:email:set"
        USER_EMAIL_DATE_SET = "user:email:date:%s:set"
        EMAIL_HASH = "email:id:%s:hash"

        redis = getInst()

        curTime = datetime.now()
        date = curTime.strftime("%Y-%m-%d")

        awards = ''
        if enclosure_id and enclosure_num:
            awards = '%s,%s' % (enclosure_id, enclosure_num)

        if isinstance(uids_list, (int, str)):
            uids_list = [uids_list]
        for uid in uids_list:
            email_id = uuid.uuid4().hex
            redis.sadd(USER_EMAIL_DATE_SET % date, email_id)
            redis.sadd(USER_EMAIL_SET % uid, email_id)
            redis.hmset(EMAIL_HASH % email_id, {
                "title": title,
                "body": body,
                "awards": awards,
                "send_time": curTime.strftime('%Y-%m-%d %H:%M:%S'),
                "read": 0,
                "timestamp": int(time.time() * 1000),
                'email_type': '',
                'userId': uid,
                'emailType': emailType,
            })
