#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    任务模块
"""

from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,PARTY_PLAYER_COUNT
from common.utilt import *
from common import log_util
from common.log import *
from datetime import datetime
from model.gameModel import *
from model.agentModel import *
from model.protoclModel import *
import json



@admin_app.get('/task/list')
def get_task_list_api(redis):
    """
        游戏列表视图
    """
    lang = getLang()

    isList = request.GET.get('list','').strip()

    info = {
            'title'         :     "任务列表",
            'addTitle'      :     "创建任务",
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'setUrls'       :     BACK_PRE+'/task/modify',
            'tableUrl'      :     BACK_PRE+'/task/list?list=1'
    }
    if isList:
        res = get_task_list(redis)
        return json.dumps(res)
    else:
        info['createUrl']   = BACK_PRE+'/task/create'
        return template('admin_task_list',PAGE_LIST=PAGE_LIST,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/task/create')
def createTask(redis):
    lang = getLang()
    info = {
        'title': "创建新任务",
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + '/task/list',
        'submitUrl': BACK_PRE + '/task/create',
        'partyPlayerMax': PARTY_PLAYER_COUNT,
        'module_id': '',
        'name': '',
        'icon_path': '',
        'web_tag': '',
        'apk_tag': '',
        'ipa_tag': '',
        'pc_tag': '',
        'apksize': '',
        'apkmd5': '',
        'downloadUrl': '',
        'version': '',
        'minVersion': '',
        'iosVersion': '',
        'pack_name': '',
        'game_rule': '',
        'maxRoomCount': ''
    }
    return template('admin_task_create',message='',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/task/create')
def createTaskAdd(redis):

    """

        description:
        taskType:1
        whereHead:gold
        whereValue:
        whereSort:
        whereWeekType:
        whereStartDate:
        whereEndDate:
        masonry:
        gold:
    """
    fields = (
            'description',
            'taskType',
            'whereHead',
            "whereType",
            'whereValue',
            'whereSort',
            'whereWeekType',
            'whereStartDate',
            "whereEndDate",
            'masonry',
            'gold',
            'title'
              )
    for field in fields:
        exec("%s=request.forms.get('%s','').strip()"%(field,field))

    taskList = redis.smembers(TASK_LIST)
    if not taskList:
        _id = 1
    else:
        max_id = max([int(i) for i in taskList])
        _id = max_id + 1
    redis.sadd(TASK_LIST, _id)
    task = {
        "id": _id,
        "description": description,
        "gameType": taskType,
        "where": json.dumps({whereHead : {"type": whereType, "value": whereValue, "week": whereWeekType, "rank": whereSort, "start_date":whereStartDate, "end_date": whereEndDate}}),
        "results": json.dumps([{"type": 1, "value": gold}, {"type": 2, "value": masonry} ]),
        "status": 1,
        "title": title
    }
    redis.hmset(TASK_CONTENT % _id,task)
    return {"code": 0, "msg": "成功", 'jumpUrl':BACK_PRE+'/task/list'}

@admin_app.post('/task/modify')
def taskModify(redis):

    _id = request.forms.get('id','').strip()
    if redis.exists(TASK_CONTENT % _id):
        status = redis.hget(TASK_CONTENT % _id, "status")
        status = int(status) if status else 0
        if status == 0:
            status = 1
        else:
            status = 0
        redis.hset(TASK_CONTENT % _id, "status", status)
    return {"code": 0, "msg": "成功",  'jumpUrl':BACK_PRE+'/task/list'}

@admin_app.post('/task/delete')
def createTask(redis):

    _id = request.forms.get('id', '').strip()
    if redis.exists(TASK_CONTENT % _id):
        redis.delete(TASK_CONTENT % _id)
        redis.srem(TASK_LIST, _id)
    return {"code": 0, "msg": "成功", 'jumpUrl': BACK_PRE + '/task/list'}