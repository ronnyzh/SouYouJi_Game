#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    活动模型
"""
from web_db_define import *
from admin  import access_module
from config.config import *
from common.log import *
import random
from datetime import datetime
import os
import json



# --------------------------------  奖品相关 -----------------------------------------------------

def addReward(redis,agentid,messageInfo):
    ''' 添加奖品 '''
    table = REWARD_LIST_TABLE % agentid
    tableId = redis.incr(REWARD_COUNT_TABLE)
    messageInfo['id'] = tableId
    pipe = redis.pipeline()
    pipe.hmset(REWARD_TABLE % tableId, messageInfo)
    pipe.lpush(table, tableId)
    return pipe.execute()


def get_rewardList(redis,session,agentId,searchId,lang, searchType = ''):
    """
    获取奖品列表
    """
    tableIds = redis.lrange(REWARD_LIST_TABLE % (agentId), 0, -1)
    infos = []
    for _id in tableIds:
        table = REWARD_TABLE % _id
        if not table:
            continue
        info = redis.hgetall(table)
        infos.append(info)

    res = []
    for listObj in infos:
        # 根据imgId查询图片
        if listObj.get('imgId'):
            img_searchId = listObj['imgId']
            imgRes = get_resourceList2(redis,agentId,img_searchId, lang)
            listObj['imgUrl'] = imgRes['data'][0]['url']

        # 如果有searchId 则进行过滤
        rewardId = listObj['id']

        if bool( searchId and not rewardId in searchId.split(',') ) :
            continue

        # 根据rewardId 查奖品
        if bool(listObj.get('rewardId') and listObj['rewardId']):
            rewardSearchId =  listObj['rewardId']
            rewardData = get_rewardList(redis,session,agentId,rewardSearchId,lang)
            listObj['rewardData'] = rewardData['data']

        listObj['op'] = []
        for access in access_module.ACCESS_GAME_REWARD_LIST:
            if access.url in eval(session['access']):
                listObj['op'].append({'url':access.url,'method':access.method,'txt':access.getTxt(lang)})
        res.append(listObj)

    # 过滤searchType
    if searchType:
        data = []
        for i, value in enumerate(res):
            if (value['type'] == searchType):
                data.append(value)
        res = data

    return {
        "code": 0,
        "msg": lang.ACTIVICE_REWARD_LIST_SUCCESS,
        'count': len(res),
        'data': res
    }

def get_rewardList2(redis,agentId,searchId,lang, searchType = ''):
    """
    获取奖品列表
    """
    tableIds = redis.lrange(REWARD_LIST_TABLE % (agentId), 0, -1)
    infos = []
    for _id in tableIds:
        table = REWARD_TABLE % _id
        if not table:
            continue
        info = redis.hgetall(table)
        infos.append(info)

    res = []
    for listObj in infos:
        # 根据imgId查询图片
        if listObj.get('imgId'):
            img_searchId = listObj['imgId']
            imgRes = get_resourceList2(redis,agentId, img_searchId, lang)
            listObj['imgUrl'] = imgRes['data'][0]['url']

        # 如果有searchId 则进行过滤
        rewardId = listObj['id']

        if bool( searchId and not rewardId in searchId.split(',') ) :
            continue

        # 根据rewardId 查奖品
        if bool(listObj.get('rewardId') and listObj['rewardId']):
            rewardSearchId =  listObj['rewardId']
            rewardData = get_rewardList2(redis,agentId,rewardSearchId,lang)
            listObj['rewardData'] = rewardData['data']
        res.append(listObj)

    # 过滤searchType
    if searchType:
        data = []
        for i, value in enumerate(res):
            if (value['type'] == searchType):
                data.append(value)
        res = data

    return {
        "code": 0,
        "msg": lang.ACTIVICE_REWARD_LIST_SUCCESS,
        'count': len(res),
        'data': res
    }


def delReward(redis,agentId,tableid):
    log_debug('删除奖品id {0}'.format(tableid))
    pipe = redis.pipeline()
    pipe.delete(REWARD_TABLE % tableid)
    pipe.lrem(REWARD_LIST_TABLE % agentId, tableid,0)
    return pipe.execute()


def editReward(redis,agentId,tableid,messageInfo):

    if tableid not in redis.lrange(REWARD_LIST_TABLE % agentId, 0, -1):
        raise Exception("no such table id!")
    log_debug('修改奖品id {0}'.format(tableid))
    pipe = redis.pipeline()
    pipe.hmset(REWARD_TABLE % tableid, messageInfo)
    return pipe.execute()


def getRewardInfo(redis,key_id):
    ''' 获取奖品信息 '''
    key = REWARD_TABLE % key_id
    if redis.exists(key):
        data = redis.hgetall(key)
        if data.get('type') == 'pack':
            data['singleData'] = eval(data['singleData'])
        return data


# --------------------------------  活动相关 -----------------------------------------------------


def getActiviceListInfos(redis,session,agentId,searchId,lang):
    """
    获取活动列表
    """
    curTime = datetime.now()
    selfUid = session['id']
    list = [
        {"id": "001", "title": "活动1", "desc": "活动描述", "note": "note"},
        {"id": "002", "title": "红包", "desc": "奖品描述", "note": "note"}
    ]
    logInof = {'datetime': curTime, 'data': str(list)}
    writeAgentOpLog(redis, selfUid, logInof)
    return {
        'count': len(list),
        'data': list
    }

def getActiviceInfosByAcId(redis,session,acId,searchId,lang):
    """
    通过acId获取活动详细信息
    """
    curTime = datetime.now()
    list = {
        'acId'      :       '1',
        'title'     :       '测试活动',
        'template'  :       'turnlate',
    }
    return list


def createActivice(redis, agentid, messageInfo):
    """
    创建一条新活动
    """
    table = ACTIVICE_LIST_TABLE % agentid
    activeid = redis.incr(ACTIVICE_COUNT_TABLE)
    readurl = HALL_PRE + '/activice/route?type=%s&id=%s&agentId=%s' % (messageInfo['type'], activeid, agentid)
    messageInfo['read'] = '0'
    messageInfo['id'] = activeid
    messageInfo['link'] = readurl
    messageInfo['agentid'] = agentid

    if int(agentid) == systemId:
        messageInfo['status'] = STATUS_PASS
    else:
        messageInfo['status'] = STATUS_NON_CHECKED
    pipe = redis.pipeline()
    try:
        for rewardinfo in messageInfo['rewardList']:
            rewardid = rewardinfo['rewardId']
            rewardput = rewardinfo.get('rewardPut','')
            if rewardput:
                pipe.set(ACTIVICE_REWARD_NUM % (activeid, rewardid), rewardput)
        pipe.hmset(ACTIVICE_TABLE % activeid, messageInfo)
        pipe.lpush(table, activeid)
    except Exception, e:
        log_debug('[createActivice][error] reason[%s]' % e)
        raise Exception("createActivice except")
    return pipe.execute()


def getActivicesList(redis,session,lang,agentId):
    """
    获取活动列表
    """
    activeList = []
    activeIds = redis.lrange(ACTIVICE_LIST_TABLE % (agentId), 0, -1)
    for activeId in activeIds:
        table = ACTIVICE_TABLE%(activeId)
        if not table:
            continue
        noticeInfo = redis.hgetall(table)
        noticeInfo['op'] = []
        for access in access_module.ACCESS_GAME_ACTIVICE_LIST:
            if access.url in eval(session['access']):
                if noticeInfo['status'] == STATUS_CLOSE and access.url == access_module.ACCESS_GAME_ACTIVICE_MODIFY.url:
                    continue
                if noticeInfo['status'] == STATUS_STARTING and access.url == access_module.ACCESS_GAME_ACTIVICE_DEL.url:
                    continue
                if noticeInfo['status'] == STATUS_STARTING and access.url == access_module.ACCESS_GAME_ACTIVICE_MODIFY.url:
                    continue
                noticeInfo['op'].append({'url':access.url,'method':access.method,'txt':access.getTxt(lang)})
        if noticeInfo['status'] == STATUS_NON_CHECKED:
            access = access_module.ACCESS_GAME_ACTIVICE_CHECK
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
        elif noticeInfo['status'] == STATUS_PASS:
            access = access_module.ACCESS_GAME_ACTIVICE_READY
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
        elif noticeInfo['status'] == STATUS_READY:
            access = access_module.ACCESS_GAME_ACTIVICE_CLOSE
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
        elif noticeInfo['status'] == STATUS_FAIL:
            access = access_module.ACCESS_GAME_ACTIVICE_CHECK
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
        elif noticeInfo['status'] == STATUS_STARTING:
            access = access_module.ACCESS_GAME_ACTIVICE_CLOSE
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
            access = access_module.ACCESS_GAME_ACTIVICE_RECORD
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
            access = access_module.ACCESS_GAME_ACTIVICE_SPECAIL
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
        elif noticeInfo['status'] == STATUS_CLOSE:
            access = access_module.ACCESS_GAME_ACTIVICE_RECORD
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
            access = access_module.ACCESS_GAME_ACTIVICE_SPECAIL
            noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
        activeList.append(noticeInfo)

    subids = []
    if int(agentId) == systemId:
        subids = getsubAgents(redis,agentId)
    for subid in subids:
        activeIds = redis.lrange(ACTIVICE_LIST_TABLE % (subid), 0, -1)
        for activeId in activeIds:
            table = ACTIVICE_TABLE%(activeId)
            if not table:
                continue
            noticeInfo = redis.hgetall(table)
            if noticeInfo['status'] not in [STATUS_CHECKING, STATUS_READY, STATUS_STARTING]:
                continue

            noticeInfo['op'] = []
            access = access_module.ACCESS_GAME_ACTIVICE_READ
            if access.url in eval(session['access']):
                noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})

            if noticeInfo['status'] in [STATUS_READY,STATUS_STARTING]:
                access = access_module.ACCESS_GAME_ACTIVICE_CLOSE
                noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})

            if noticeInfo['status'] in [STATUS_STARTING, STATUS_CLOSE]:
                access = access_module.ACCESS_GAME_ACTIVICE_RECORD
                noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
                access = access_module.ACCESS_GAME_ACTIVICE_SPECAIL
                noticeInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})

            activeList.append(noticeInfo)




    return {'data':activeList,'count':len(activeList)}



def delActivice(redis,agentid,tableid):
    ''' 删除活动 '''
    log_debug('删除活动id {0}'.format(tableid))
    pipe = redis.pipeline()
    pipe.delete(ACTIVICE_TABLE % (tableid))
    pipe.lrem(ACTIVICE_LIST_TABLE % (agentid),tableid,0)
    return pipe.execute()


def editActivice(redis,agentId,tableid,messageInfo):

    if tableid not in redis.lrange(ACTIVICE_LIST_TABLE % agentId, 0, -1):
        raise Exception("no such table id!")
    log_debug('修改活动id {0}'.format(tableid))
    pipe = redis.pipeline()
    pipe.hmset(ACTIVICE_TABLE % tableid, messageInfo)
    return pipe.execute()


#------------------------------------------------  资源相关 ---------------------------------------

def get_resourceList(redis,session,searchId,lang):
    """
    获取资源列表（图片）
    """

    tableIds = redis.lrange(RESOURCE_LIST_TABLE % session['id'], 0, -1)
    list = []
    for _id in tableIds:
        table = RESOURCE_TABLE%(_id)
        if not table:
            continue
        info = redis.hgetall(table)
        info['op'] = []
        for access in access_module.ACCESS_GAME_RESOURCE_LIST:
            if access.url in eval(session['access']):
                info['op'].append({'url':access.url,'method':access.method,'txt':access.getTxt(lang)})
        list.append(info)
        log_debug('wwwww**********************{0}'.format(info))

    data = list
    if searchId :
        for i, value in enumerate(list):
            if(value['id'] == searchId):
                data = [value]

    return {
        "code"  : 0,
        "msg"   : lang.RESOURCE_LIST_SUCCESS,
        'count' : len(list),
        "data"  : data
    }

def get_resourceList2(redis,agentid,searchId,lang):
    """
    获取资源列表（图片）
    """

    tableIds = redis.lrange(RESOURCE_LIST_TABLE % agentid, 0, -1)
    list = []
    for _id in tableIds:
        table = RESOURCE_TABLE%(_id)
        if not table:
            continue
        info = redis.hgetall(table)
        list.append(info)

    data = list
    if searchId :
        for i, value in enumerate(list):
            if(value['id'] == searchId):
                data = [value]

    return {
        "code"  : 0,
        "msg"   : lang.RESOURCE_LIST_SUCCESS,
        'count' : len(list),
        "data"  : data
    }




def delResource(redis, agentid,tableid):
    ''' 删除资源 '''
    info = redis.hgetall(RESOURCE_TABLE % (tableid))
    absname = STATIC_FILE_DIR + info['url']
    pipe = redis.pipeline()
    try:
        pipe.delete(RESOURCE_TABLE % (tableid))
        pipe.lrem(RESOURCE_LIST_TABLE % agentid,tableid,0)
    except Exception, e:
        log_debug('[delResource][error] reason[%s]' % (e))
        return None
    log_debug('[delResource][info]************************{0} '.format(tableid))
    if os.path.exists(absname):
        os.remove(absname)
    return pipe.execute()

def addResource(redis, agentId, messageInfo,upload):
    ''' 添加资源 '''
    table = RESOURCE_LIST_TABLE % agentId
    tableId = redis.incr(RESOURCE_COUNT_TABLE)
    name, ext = os.path.splitext(upload.filename)
    upload.filename = ''.join((str(tableId), ext))
    log_debug("新增资源接口1：{0} {1} ".format(upload.content_type, upload.filename))
    basename = os.path.join(STATIC_ACTIVICE_DOWNLOAD_PATH,upload.filename)

    upload.save(STATIC_FILE_DIR + basename, overwrite=True)
    messageInfo['id'] = tableId
    messageInfo['filename'] = upload.filename
    messageInfo['url'] = basename
    pipe = redis.pipeline()
    try:
        pipe.hmset(RESOURCE_TABLE % (tableId), messageInfo)
        pipe.lpush(table, tableId)
    except Exception, e:
        log_debug('[addResource][error] reason[%s]' % (e))
        return None
    log_debug('[addResource][info] messageInfo[%s]' % (messageInfo))
    return pipe.execute()

def isResourceInRewardList(redis,agentid,id):
    """
        检查资源
    """
    reward_keys = redis.lrange(REWARD_LIST_TABLE % agentid, 0, -1)
    for key in reward_keys:
        table = REWARD_TABLE % key
        info = redis.hgetall(table)
        if info.get('imgId','') == id:
            return True
    return False

def isRewardInActiveList(redis,agentid,id):
    """
        检查奖品
    """
    active_keys = redis.lrange(ACTIVICE_LIST_TABLE % agentid, 0, -1)
    for key in active_keys:
        acinfo = getActiciveInfo(redis,key)
        reward_list = acinfo.get('rewardList')
        for reward_info in reward_list:
            if reward_info.get('rewardId','') == id:
                return True
    return False


def editResource(redis, agentId, messageInfo,upload):
    """
        修改资源  
    """
    tableId = messageInfo['id']
    if upload:
        name, ext = os.path.splitext(upload.filename)
        upload.filename = ''.join((str(tableId), ext))
        basename = os.path.join(STATIC_ACTIVICE_DOWNLOAD_PATH,upload.filename)
        upload.save(STATIC_FILE_DIR + basename, overwrite=True)
        messageInfo['filename'] = upload.filename
        messageInfo['url'] = basename
    else:
        info = redis.hgetall(RESOURCE_TABLE % (tableId))
        messageInfo['filename'] = info['filename']
        messageInfo['url'] = info['url']

    pipe = redis.pipeline()
    try:
        pipe.hmset(RESOURCE_TABLE % (tableId), messageInfo)
    except Exception, e:
        log_debug('[editResource][error] reason[%s]' % (e))
        return None
    log_debug('[editResource][info] messageInfo[%s]' % (messageInfo))
    return pipe.execute()


#  ----------------------------------------------   小模块      -----------------------------------------------

def getGamesList(redis):
    """
    获取游戏列表
    """
    gameIds = redis.lrange(GAME_LIST,0,-1)
    gameList = []
    print gameIds
    for gameId in gameIds:
        gameInfo = redis.hgetall(GAME_TABLE%(gameId))
        gameList.append({'id':gameInfo['id'],'name':gameInfo['name']})
    log_debug('game list ************** {0}'.format(gameList))
    return gameList

def getGamesName(redis,gameid):
    """
    获取游戏列表
    """
    gameInfo = redis.hgetall(GAME_TABLE%(gameid))
    log_debug('game info {0}'.format(gameInfo))
    return gameInfo.get('name','任意游戏')

'''
def getRewardInfos(redis):
    """
    获取游戏列表
    """

    tableIds = redis.lrange(REWARD_LIST_TABLE, 0, -1)
    infos = []
    for _id in tableIds:
        table = REWARD_TABLE%(_id)
        if not table:
            continue
        info = redis.hgetall(table)
        infos.append(info)
    return infos
'''


def getsubAgents(redis,agentId):
    ''' 获取下级代理 '''
    parentTable = AGENT_CHILD_TABLE%(agentId)
    subIds = redis.smembers(parentTable)
    return list(subIds)

def getActiviceStatus(redis,tableid):
    ''' 获取活动状态 '''
    status = None
    table = ACTIVICE_TABLE % (tableid)
    if redis.exists(table):
        status = redis.hget(table,'status')
        return status

def getActiciveAgentid(redis,tableid):
    ''' 获取活动所属工会 '''
    table = ACTIVICE_TABLE % (tableid)
    if redis.exists(table):
        return redis.hget(table,'agentid')

def setActiviceStatus(redis,tableid,status):
    ''' 设置活动状态 '''
    table = ACTIVICE_TABLE % (tableid)
    if redis.exists(table):
        redis.hmset(table, {'status': status})

def getActiciveInfo(redis, tableid):
    table = ACTIVICE_TABLE % tableid
    if redis.exists(table):
        info = redis.hgetall(table)
        info["missionList"] = eval(info["missionList"])
        info["rewardList"] = eval(info["rewardList"])
        if info.get('allowAgent',[]):
            info["allowAgent"] = eval(info["allowAgent"])
        if info.get('specialPlan',[]):
            info["specialPlan"] = eval(info["specialPlan"])
        return info

# 在线活动操作

def get_online_activices(redis,agentId):
    """
    获取正在进行活动列表
    """
    lists = []
    activeids = redis.lrange(ONLINE_ACTIVICE_LIST % agentId, 0, -1)
    for activeId in activeids:
        table = ACTIVICE_TABLE % activeId
        if not redis.exists(table):
            continue
        info = redis.hgetall(table)
        info["missionList"] = eval(info["missionList"])
        info["rewardList"] = eval(info["rewardList"])
        if info.get('allowAgent',[]):
            info["allowAgent"] = eval(info["allowAgent"])
        if info.get('specialPlan',[]):
            info["specialPlan"] = eval(info["specialPlan"])
        lists.append(info)
    return lists

def add_online_activice(redis,agentid,acid):
    '''
        加入在线活动
    '''
    setActiviceStatus(redis, acid, STATUS_STARTING)
    redis.lpush(ONLINE_ACTIVICE_LIST % (agentid), acid)

def rm_online_activice(redis,agentid,acid):
    '''
        删除在线活动
    '''
    setActiviceStatus(redis, acid, STATUS_CLOSE)
    redis.lrem(ONLINE_ACTIVICE_LIST % agentid, acid, 0)

def check_activice_isonline(redis, acid):
    """检查活动是否正在执行"""
    status = redis.hget( ACTIVICE_TABLE % acid, "status" )
    if status == STATUS_STARTING:
        return True
    else:
        return False
    # STATUS_STARTING



def get_lottery_num(redis,acid,account):
    key = LOTTERY_NUM_TABLE % (acid,account)
    if redis.exists(key):
        return int(redis.get(key))
    return 0

def desc_lottery_num(redis,acid,account):
    ''' 用户抽奖次数减1 '''
    key = LOTTERY_NUM_TABLE % (acid, account)
    return redis.decr(key)

def get_lottery_server_count(redis):
    key = LOTTERY_COUNT_TOTAL
    if redis.exists(key):
        return redis.get(key)
    return 0



def get_lottery_activice_count(redis,acid):
    ''' 该活动总抽奖次数  '''
    key = LOTTERY_COUNT_AC_TOTAL % acid
    if redis.exists(key):
        return redis.get(key)
    return 0

def set_lottery_activice_count(redis,acid):
    ''' 活动总抽奖次数自增  '''
    key = LOTTERY_COUNT_AC_TOTAL % acid
    return redis.incr(key,1)


def get_awardees(redis,groupid,acid):
    ''' 获取抽奖人名单 '''
    lists = []
    keys = redis.lrange(ACTIVICE_REWAREES_LIST % (acid,groupid), 0, 15)
    for key in keys:
        info = redis.get(ACTIVICE_REWAREES_TABLE % (acid, key))
        info = json.loads(info)
        # 移除未中奖记录
        if info.get('type','') == 'empty':
            continue
        lists.append(info)
    return lists

def get_awardees_byacic(redis,acid,searchid,record=False):
    ''' 活动 获奖记录 '''
    lists = []
    keys = redis.keys(ACTIVICE_REWAREES_LIST % (acid,'*'))
    log_debug('555555555555555555555555keys {0}'.format(keys))
    if searchid:
        for key in keys:
            raw_keys = redis.lrange(key, 0, -1)
            for raw_key in raw_keys:
                info = redis.get(ACTIVICE_REWAREES_TABLE % (acid, raw_key))
                if not info:
                    continue
                info = json.loads(info)
                if searchid == info.get('id',''):
                    if record and not info.get('record',''):
                        continue
                    lists.append(info)
    else:
        for key in keys:
            raw_keys = redis.lrange(key, 0, -1)
            for raw_key in raw_keys:
                info = redis.get(ACTIVICE_REWAREES_TABLE % (acid, raw_key))
                if not info:
                    continue
                info = json.loads(info)
                if record and not info.get('record', ''):
                    continue
                lists.append(info)
    return lists

def set_awardees(redis,groupid,acid,info):
    ''' 存入抽奖人 '''
    reid = redis.incr(ACTIVICE_REWAREES_COUNT)
    key = ACTIVICE_REWAREES_LIST % (acid,groupid)
    pipe = redis.pipeline()
    pipe.set(ACTIVICE_REWAREES_TABLE % (acid,reid),json.dumps(info))
    pipe.lpush(key, reid)
    pipe.execute()
    return reid

def modify_awardees(redis,id,acid,message):
    '''  '''
    key = ACTIVICE_REWAREES_TABLE % (acid,id)
    info = redis.get(key)
    log_debug("---------------modify_awardees   {0}".format(info));
    info = json.loads(info)
    info['phone'] = message['phone']
    info['realName'] = message['name']
    redis.set(key,json.dumps(info))

def set_noreward_awardees(redis, account, acid ,reid, info):
    """ 加入实物未领取列表"""
    key = ACTIVICE_NOREWARD_KEY % (account,acid, reid)
    redis.set(key, json.dumps(info))

def check_noreward_awardees(redis, account):
    """ 是否在实物未领取列表"""
    tablekey = ACTIVICE_NOREWARD_KEY % (account, '*', '*')
    keys = redis.keys(tablekey)
    ret = []
    for key in keys:
        data = redis.get(key)
        data = json.loads(data)
        ret.append(data)
    return ret

def remove_noreward_awardees(redis,account, acid, reid):
    """ 从实物未领取列表中删除"""
    key = ACTIVICE_NOREWARD_KEY % (account, acid, reid)
    redis.delete(key)


def get_user_schedule(redis, acid, account):
    ''' 获取用户进度 '''
    key = ACTIVICE_USER_INFO % (acid, account)
    if redis.exists(key):
        return json.loads(redis.get(key))

def init_user_schedule(redis,info):

    user_schedule = info[:]
    for mission in user_schedule:
        mission["gameName"] = getGamesName(redis, mission['gameId'])
        mission['gameFinishNum'] = 0
        mission["isFinish"] = 0  # 1：已完成  0：未完成
    return user_schedule


def init_all_user_schedule(redis):
    keys = redis.keys(ACTIVICE_LIST_TABLE % ('*'))
    pipe = redis.pipeline()
    for key in keys:
        for acid in redis.lrange(key, 0, -1):
            _keys = redis.keys(ACTIVICE_USER_INFO % (acid, '*'))
            for _key in _keys:
                pipe.delete(_key)
    return pipe.execute()


def get_active_reward_num(redis,acid,reid):
    """
        获取活动奖品库存
    """
    key = ACTIVICE_REWARD_NUM % (acid, reid)
    if not redis.exists(key):
        return 9999999
    return int(redis.get(key))

def decr_active_reward_num(redis,acid,reid):
    """
        获取活动奖品库存
    """
    key = ACTIVICE_REWARD_NUM % (acid, reid)
    if not redis.exists(key):
        return
    if int(redis.get(key) == 0):
        return
    return redis.decr(key)





