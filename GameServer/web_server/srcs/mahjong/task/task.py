#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    捕鱼大厅接口
"""

from bottle import request, Bottle, redirect, response,default_app
from web_db_define import *
import mahjong_pb2
import poker_pb2
import replay4proto_pb2

from talk_data import sendTalkData
from wechat.wechatData import *
from common.install_plugin import install_redis_plugin,install_session_plugin
from common.log import *
from common.utilt import allow_cross,getInfoBySid

from datetime import datetime, date, timedelta
from model.goodsModel import *
from model.userModel import do_user_modify_addr,do_user_del_addr,get_user_exchange_list
from model.hallModel import *
from model.protoclModel import sendProtocol2GameService
from model.mailModel import *
from model.agentModel import *
from model.fishModel import get_room_list
from common import web_util,log_util,convert_util
import time
import urllib2
import json
import random
import md5
import re
import pdb
from urlparse import urlparse
from datetime import datetime

ACCEPT_NUM_BASE = 198326
ACCEPT_TT = [md5.new(str(ACCEPT_NUM_BASE+i)).hexdigest() for i in xrange(10)]
SESSION_TTL = 60*60
CHECK_SUCCESS = 1
#生成捕鱼APP
task_app = Bottle()
#获取配置
conf = default_app().config
#安装插件
install_redis_plugin(task_app)
install_session_plugin(task_app)
FORMAT_PARAMS_POST_STR = "%s = request.forms.get('%s','').strip()"
FORMAT_PARAMS_GET_STR  = "%s = request.GET.get('%s','').strip()"

USER_TITLES = "titlesList:user:%s:set"

class TaskResult(object):

    def __init__(self, redis, account):

        self.redis = redis
        self.account = account

    def check_date(self, start_date, end_date):


        now = datetime.now().date()
        if start_date:
            start_date = datetime.strptime(start_date,"%Y-%m-%d").date()

        if end_date:
            end_date = datetime.strptime(end_date,"%Y-%m-%d").date()

        if start_date and end_date:
            if start_date <= now and now <= end_date:
                return True
            return False

        elif start_date:
            if start_date <= now:
                return True
            return False

        elif end_date:
            if end_date >= now:
                return True
            return False

        else:
            return True

    def gold(self, type, value, week, start_date=None, end_date=None):

        if not self.check_date(start_date, end_date):
            return False

        type = int(type)
        value = int(value)
        # 获取玩家的金币信息
        account2user_table = FORMAT_ACCOUNT2USER_TABLE % (realAccount)
        userTable = redis.get(account2user_table)
        gold = redis.hget(userTable, 'gold')
        gold = int(gold) if gold else 0

        # 指定天金币数量最多
        if type == 1:
            pass
        # 当前金币数量
        elif type == 2:
            if gold >= value:
                return True

        return False


    def win(self, type, value, week, start_date=None, end_date=None):

        if not self.check_date(start_date, end_date):
            return False

        type = int(type)


        # 普通胜场
        if type == 1:
            pass
        # 连续胜场
        elif type == 2:
            pass

    def lost(self, type, value, week, start_date=None, end_date=None):

        if not self.check_date(start_date, end_date):
            return False
        type = int(type)

        # 普通敗场
        if type == 1:
            pass

        # 连续敗场
        elif type == 2:
            pass

        # 特殊失败
        elif type == 3:
            pass


    def sports(self, type, value, week, start_date=None, end_date=None, rank=None):

        if not self.check_date(start_date, end_date):
            return False

        type = int(type)

        # 获得竞技场名次奖励
        if type == 1:
            pass


    def other(self, type, value, week, start_date=None, end_date=None):


        if not self.check_date(start_date, end_date):
            return False

        type = int(type)

        # 俱乐部创建者成员数量
        if type == 1:
            pass

        # 分享次数
        elif type == 2:
            pass

        # 抽奖内容
        elif type == 3:
            pass

        # 游戏时常
        elif type == 4:
            pass

        # 连续登录
        elif type == 5:
            pass

        # 钻石消费
        elif type == 6:
            pass


@task_app.get("/list")
@allow_cross
def task_list(redis, session):

    sid = request.params.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    gameDict = {
        1: [],
        2: [],
        3: []
    }
    task_ids = redis.smembers(TASK_LIST)
    task_list = []
    for _id in task_ids:
        id,description,result,title,status, where, gameType = redis.hmget(TASK_CONTENT %(_id), "id", "description", "results", "title", "status", "where", "gameType")
        result = json.loads(result)
        status = int(status) if status else 0
        tempOp = []
        task_info = {
                'id'        :   id,
                'description'      :   description,
                'result'    :   result,
                'title'     :   title,
                "gameType"  :   gameType
        }
        gameType = int(gameType)
        # task_list.append(task_info)
        taskSuccess = redis.smembers("user:task:%s:success:set" % account)
        state = 0
        receive = 0
        if int(id) in taskSuccess:
            state = 1
        else:
            receive = 0
            where = json.loads(where).items()
            taskClass = TaskResult(redis, account)
            name = where[0][0]
            args = where[0][1]
            func = getattr(taskClass, name)
            if func:
                result = func(**args)
                if result:
                    receive = 1

        task_info["state"] = state
        task_info["receive"] = receive
        gameDict[gameType].append(task_info)
    for _iter in gameDict:
        gameDict[_iter] = sorted(gameDict[_iter], key=lambda x: int(x["id"]))

    return {"code": 0, 'list': gameDict}

@task_app.post("/receive")
@allow_cross
def task_receive(redis, session):
    """ 领取奖励

    :param redis:
    :param session:
    :return:
    """
    sid = request.forms.get('sid', '').strip()
    task_id = request.forms.get('task_id', '').strip()
    id, description, result, title, status, where, gameType = redis.hmget(TASK_CONTENT % (task_id), "id", "description",
                                                                          "results", "title", "status", "where",
                                                                          "gameType")
    if not result:
        return {"code": 1, "msg": "没有这个任务"}
    result = json.loads(result)
    status = int(status) if status else 0
    if status == 0:
        return {"code": 1, "msg": "任务不可用"}

    taskSuccess = redis.smembers("user:task:%s:success:set" % account)
    if int(id) in taskSuccess:
        return {"code": 1, "msg": "你已经领取过该任务"}
    else:
        receive = 0
        where = json.loads(where).items()
        taskClass = TaskResult(redis, account)
        name = where[0][0]
        args = where[0][1]
        func = getattr(taskClass, name)
        if func:
            result = func(**args)
            if result:
                receive = 1