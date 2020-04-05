#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    代理模型
"""
from web_db_define import *
from admin  import access_module
from datetime import datetime,timedelta
from config.config import *
from common.log import *
from common.utilt import get_week_date_obj
import random
from datetime import datetime
from operator import itemgetter
from common import convert_util,log_util

# 菜单权限
TYPE2ACCESS={
    '0'   :    access_module.ACCESS_SADMIN_MODULES,
    '1'   :    access_module.ACCESS_COMPANY_MODULES,
    '2'   :    access_module.ACCESS_AG_ONE_CLASS_MODULES,
    '3'   :    access_module.ACCESS_AG_TWO_CLASS_MODULES

}
# 列表权限
TYPE2ACCESSLIST={
    '0'   :    access_module.ACCESS_SADMIN_LIST,
    '1'   :    access_module.ACCESS_COMPANY_LIST,
    '2'   :    access_module.ACCESS_AG_ONE_CLASS_LIST,
    '3'   :    access_module.ACCESS_AG_TWO_CLASS_LIST

}
#代开描述
OPENAUTH_2_TXT = {
        0         :       '所有玩家代开',
        1         :       '仅权限玩家代开'
}

#钻石套餐
ROOMCARD2TYPE = {
    'agent'        :   [
        {'txt':'220个钻石','roomCard':'220'},
        {'txt':'550个钻石','roomCard':'550'},
        {'txt':'1100个钻石','roomCard':'1100'},
        {'txt':'2200个钻石','roomCard':'2200'},
        {'txt':'5500个钻石','roomCard':'5500'},
        {'txt':'11000个钻石','roomCard':'11000'}
    ],

    'member.cards'        :            [

        {'type':'0','txt':'1个','roomCard':'1'},
        {'type':'1','txt':'2个','roomCard':'2'},
        {'type':'2','txt':'3个','roomCard':'3'},
        {'type':'3','txt':'4个','roomCard':'4'},
        {'type':'4','txt':'5个','roomCard':'5'},
        {'type':'5','txt':'6个','roomCard':'6'},
        {'type':'6','txt':'7个','roomCard':'7'},
        {'type':'7','txt':'8个','roomCard':'8'},
        {'type':'8','txt':'9个','roomCard':'9'},
        {'type':'9','txt':'10个','roomCard':'10'},
        {'type':'10','txt':'20个','roomCard':'20'},
        {'type':'11','txt':'30个','roomCard':'30'},
        {'type':'12','txt':'40个','roomCard':'40'},
        {'type':'13','txt':'50个','roomCard':'50'},
        {'type':'14','txt':'60个','roomCard':'60'},
        {'type':'15','txt':'70个','roomCard':'70'},
        {'type':'16','txt':'80个','roomCard':'80'},
        {'type':'17','txt':'90个','roomCard':'90'},
        {'type':'18','txt':'100个','roomCard':'100'},
        {'type':'19','txt':'500个','roomCard':'500'},
        {'type':'20','txt':'1000个','roomCard':'1000'},

    ],

    'member.coin'        :            [

        {'type':'0','txt':'1000金币','roomCard':'1000'},
        {'type':'1','txt':'5000金币','roomCard':'5000'},
        {'type':'2','txt':'10000金币','roomCard':'10000'},
        {'type':'3','txt':'50000金币','roomCard':'5000'},


    ]
}

"""
代理模型的数据类型
添加一个模型field
注意:
    模板的提交名称属性必须与此处新增的一致，否则服务器将解析不到提交数据
"""
AGENT_FIELDS = (
                    'parentAg',
                    'account',
                    'passwd',
                    'shareRate',
                    'unitPrice',
                    'comfirPasswd',
                    'myRate',
                    'defaultRoomCard',
                    'recharge',
                    'agentId'
)

"""
代理列表需要展示的参数
"""
AGENT_LIST_DIS = (
            'type',                 #类型
            'valid',                #状态
            'regDate',              #注册日期
            'account',              #账户
            'roomcard',             #钻石数
            'id',                   #公会iD
            'isTrail',              #试玩标志
            'isCreate',             #是否有创建权限
            'recharge',             #代理线上充值
            'auto_check',           #是否自动审核
            'create_auth',          #是否允许创建3级公会
            'open_auth',            #仅权限者带开房
            'managers',             #使用邀请码成为的管理
            'invite_code',           #邀请码
)

#仅超管和一级代理需要显示的操作
ONLY_SUPERNTOP_SHOW = [
                    '/admin/agent/create_auth'
]
#只有2三级需要显示
ONLY_2_3_SHOW = [
                '/admin/agent/open_auth'
]

def getAgentIdNo(redis):
    """
    生成会员Id号(6位且不重复)
    """
    agentId = ''
    for i in range(6):
        # a = random.randint(0,9)
        a = random.randrange(9)
        agentId += str(a)
    if not redis.sadd(AGENT_ID_TABLE,agentId):
        getAgentIdNo(redis,session)
    return agentId

def getTopAgentId(redis,agentId):
    """
    获取总公司ID
    """
    agType = redis.hget(AGENT_TABLE%(agentId),'type')
    if agType in ['0','1']:
        return agentId

    while 1:
        agentId = redis.hget(AGENT_TABLE%(agentId),'parent_id')
        agType = redis.hget(AGENT_TABLE%(agentId),'type')
        try:
            if int(agType) == 1:
                return agentId
        except:
            return agentId

def getAgentOwnGames(redis,agentId):
    """
        获取代理自己被勾选(拥有)的所有游戏
    """
    try:
        gameList = redis.lrange(AGENT_OWN_GAME%(agentId),0,-1)
    except:
        gameList = redis.smembers(AGENT_OWN_GAME%(agentId))
    exterGame = redis.smembers(GAME_DEFAULT_BIND)
    if not exterGame:
        exterGame = []
    gameList,exterGame = list(gameList),list(exterGame)
    gameList.extend(exterGame)
    return set(gameList)


def getCreatAgentGames(redis,agentId):
    """
        创建代理时获取代理下的所有游戏
    """
    exterGames = redis.smembers(GAME_DEFAULT_BIND)
    if agentId == '1':
        gameList = redis.lrange(GAME_LIST,0,-1)
    else :
        try:
            gameList = redis.smembers(AGENT_OWN_GAME%(agentId))
            gameList = list(gameList)
            gameList.extend(list(exterGames))
        except:
            gameList = redis.lrange(AGENT_OWN_GAME%(agentId),0,-1)
            gameList.extend(exterGames)
    #增加游戏
    gameList = list(set(gameList))
    gamesInfo =[]
    for game in gameList:
        gameInfo = {}
        name = redis.hget(GAME_TABLE%(game),'name')
        other_info = redis.hget(GAME_TABLE % game,'other_info')
        if not other_info:
            other_info = ""
        if not name:
            name = ""
        extlist = other_info.split(',')
        extstr = extlist[1] if len(extlist) > 1 else ""
        gameInfo['name'] = name + ' ' + extstr
        gameInfo['id'] = game
        gamesInfo.append(gameInfo)
    return gamesInfo


def getAgentGames(redis,parentId,agentId):
    """
        获取代理下的所有游戏
    """
    exterGames = redis.smembers(GAME_DEFAULT_BIND)
    if parentId == '1':
        parentGameList = redis.lrange(GAME_LIST,0,-1)

    else :
        try:
            parentGameList = redis.smembers(AGENT_OWN_GAME%(parentId))
            parentGameList = list(parentGameList)
            parentGameList.extend(list(exterGames))
        except:
            parentGameList = redis.lrange(AGENT_OWN_GAME%(parentId),0,-1)
    try:
        agentGameList = redis.smembers(AGENT_OWN_GAME%(agentId))
        agentGameList = list(agentGameList)
        agentGameList.extend(list(exterGames))
    except:
        agentGameList = redis.lrange(AGENT_OWN_GAME%(agentId),0,-1)

    gameList = list(set(parentGameList).union(set(agentGameList)))
    gamesInfo =[]
    for game in gameList:
        gameInfo = {}
        name = redis.hget(GAME_TABLE%(game),'name')
        other_info = redis.hget(GAME_TABLE % game,'other_info')
        if not other_info:
            other_info = ""
        if not name:
            name = ""
        extlist = other_info.split(',')
        extstr = extlist[1] if len(extlist) > 1 else ""
        gameInfo['name'] = name + ' ' + extstr
        gameInfo['id'] = game
        gamesInfo.append(gameInfo)
    return gamesInfo


def modifyAgentGames(request,redis,agentId):
    """
        通代理Id 给修改代理的游戏
    """
    agentOwnGamesTabel = AGENT_OWN_GAME%(agentId)
    agentTable = AGENT_TABLE%(agentId)
    aType,parentId = redis.hmget(agentTable,('type','parent_id'))
    if aType == '1':
        parentGameList = redis.lrange(GAME_LIST,0,-1)
    else :
        try:
            parentGameList = redis.smembers(AGENT_OWN_GAME%(parentId))
        except:
            parentGameList = redis.lrange(AGENT_OWN_GAME%(parentId),0,-1)
    try:
        agentGameList = redis.smembers(AGENT_OWN_GAME%(agentId))
    except:
        agentGameList = redis.lrange(AGENT_OWN_GAME%(agentId),0,-1)

    gameList = list(set(parentGameList).union(set(agentGameList)))

    for game in gameList:
        if request.forms.get('game%s'%(game)):
            try:
                redis.sadd(agentOwnGamesTabel,game)
            except:
                redis.delete(agentOwnGamesTabel)
                redis.sadd(agentOwnGamesTabel,game)
        else:
            redis.srem(agentOwnGamesTabel,game)

def setAgentGames(request,redis,parentId,agentId):
    """
    通过父代理Id 给代理存储代理的游戏
    """
    agentOwnGamesTabel = AGENT_OWN_GAME%(agentId)
    if parentId == '1':
        gameList = redis.lrange(GAME_LIST,0,-1)
    else :
        try:
            gameList = redis.smembers(AGENT_OWN_GAME%(parentId))
        except:
            gameList = redis.lrange(AGENT_OWN_GAME%(parentId),0,-1)


    default_ids = redis.smembers(GAME_DEFAULT_BIND)
    pipe = redis.pipeline()
    for game in gameList:
        if request.forms.get('game%s'%(game)):
            pipe.sadd(agentOwnGamesTabel,game)

    for game in default_ids:
        #加入默认游戏
        pipe.sadd(agentOwnGamesTabel,game)

    pipe.execute()

def getListBanAccess(redis,agentId):
    """
        获得代理被禁用的权限列表
    """
    banTabel = AGENT2ACCESSBAN%(agentId)
    banList = redis.smembers(banTabel)
    return banList


def banAgentAccess(redis,request,agentType,agentId):
    """
        禁用代理的权限
    """
    agentType = str(agentType)
    banTabel = AGENT2ACCESSBAN%(agentId)
    accesslists = getAgentNewListAccessUrl(agentType)
    for accesslist in accesslists:
        if not request.forms.get('url%s'%(accesslist)):
            redis.sadd(banTabel,accesslist)

def banAgentAccessModify(redis,request,agentType,agentId):
    """
        修改禁用代理的权限
    """
    agentType = str(agentType)
    banTabel = AGENT2ACCESSBAN%(agentId)
    accesslists = getAgentNewListAccessUrl(agentType)
    for accesslist in accesslists:
        if not request.forms.get('url%s'%(accesslist)):
            redis.sadd(banTabel,accesslist)
        else :
           redis.srem(banTabel,accesslist)


def setAgentAccess(redis,agentType,agentId):
    """
        通过代理Id 和代理类型给代理存储权限
    """
    agentType = str(agentType)
    accessTable = AGENT2ACCESS%(agentId)

    for accessObj in TYPE2ACCESS[agentType]:
        redis.sadd(accessTable, accessObj.url)

    for access in TYPE2ACCESSLIST[agentType]:
        if access.url not in [menu.url for menu in TYPE2ACCESS[agentType]] and access.url not in [menu.url for menu in access_module.MENU_MODULES] :
            redis.sadd(accessTable, access.url)

def getNewAccess(redis,agentId) :
    """
        代理登录后台生成最新的权限
    """
    agentTable = AGENT_TABLE%(agentId)
    aType = redis.hget(agentTable,('type'))
    # print redis.sadd('str',)
    accessTable = AGENT2ACCESS%(agentId)
    # 获得菜单权限
    Access = TYPE2ACCESS[aType]
    # 获得列表权限
    ListAccess = TYPE2ACCESSLIST[aType]
    lists=[]
    for listac in ListAccess:
        if listac.url not in [menu.url for menu in TYPE2ACCESS[aType]] and listac.url not in [menu.url for menu in access_module.MENU_MODULES]:
            lists.append(listac)
    lists = tuple(lists)
    Access = Access + lists

    s1 = redis.smembers(accessTable)
    accessUrlsList = []
    for access in Access:
        redis.sadd(accessTable, access.url)
        accessUrlsList.append(access.url)
    #
    s2 = redis.smembers(accessTable)
    deleteUrls = []
    for s in s2:
        if s not in accessUrlsList:
            deleteUrls.append(s)
    if deleteUrls:
        redis.srem(accessTable,*deleteUrls)
    # 被勾选掉的权限
    accessBan = redis.smembers(AGENT2ACCESSBAN%(agentId))
    if accessBan:
        redis.srem(accessTable,*accessBan)

def getAgentNewListAccessUrl(aType):
    aType = str(aType)
    menuAccess = access_module.MENU_MODULES
    menulist = [acc.url for acc in menuAccess]
    newList = []
    sd = 1
    for access in TYPE2ACCESSLIST[aType]:
        if access.url in menulist :
            if access.url in [menu.url for menu in TYPE2ACCESS[aType]]:
                sd=1
            else:
                sd=0
        elif sd == 1:
            newList.append(access.url)
    return newList

def getAgentNewListAccess(aType):
    aType = str(aType)
    menuAccess = access_module.MENU_MODULES
    menulist = [acc.url for acc in menuAccess]
    newList = []
    sd = 1
    for access in TYPE2ACCESSLIST[aType]:
        if access.url in menulist :
            if access.url in [menu.url for menu in TYPE2ACCESS[aType]]:
                newList.append(access)
                sd=1
            else:
                sd=0
        elif sd == 1:
            newList.append(access)
    return newList

def getListAccess(aType,lang):
    """
        创建代理它拥有的列表权限
    """
    lists=[]
    sublists=[]
    aType = str(aType)
    for access in getAgentNewListAccess(aType):
        if access.url in [menu.url for menu in TYPE2ACCESS[aType]]:
            sub={}
            sublists =[]
            sub['belong'] = access.getTxt(lang)
            sub['sub'] = sublists
            lists.append(sub)
        else:
            sublists.append(access)
    return lists

def getAgentId(redis,account):
    agentIdTable = AGENT_ACCOUNT_TO_ID%(account)
    return redis.get(agentIdTable)

def get_agent_list_infos(redis,sub_agent_ids,agent_own_accesses,lang):
    sub_ag_lists = []
    curTime = datetime.now()
    for subId in sub_agent_ids:

        agentTable = AGENT_TABLE%(subId)
        aType,valid,reg_date,account,roomCard,aId,isTrail,isCreate,recharge,auto_check,create_auth,open_auth,managers,invite_code= \
                        redis.hmget(agentTable,AGENT_LIST_DIS)
        if not managers:
            m_list = []
        else:
            m_list = managers.split(',')
        m_num = len(m_list)
        if not account or aType == '4':
            continue

        agInfo = {
                'valid'      :       valid,
                'parentId'   :       aId,
                'regDate'    :       reg_date,
                'members'    :       getAgentMembers(redis,subId),
                'allMembers' :       getAgentAllMembers(redis,subId),
                'agentType'  :       lang.TYPE_2_ADMINTYPE[aType],
                'parentAg'   :       account,
                'recharge'   :       recharge if recharge else '0',
                'roomCard'   :       getAgentRoomByDay(redis,subId,curTime.strftime('%Y-%m-%d')),
                'leaf_roomcard' :    convert_util.to_int(roomCard),
                'isTrail'    :       isTrail if isTrail else '0',
                'auto_check' :       auto_check if auto_check else '1',
                'create_auth':       create_auth if create_auth else '0', #默认不开启
                'open_auth'  :       open_auth if open_auth else '0', #默认不开启
                'invite_code':       invite_code,
                'managers'   :       managers,
                'm_num'      :       m_num,
        }

        #获取操作权限
        agInfo['op'] = []
        for access in access_module.ACCESS_AGENT_LIST:
            if access.url in agent_own_accesses:

                if (aType != '1' and (aType in ['3'] or  create_auth != '1') and access.url == '/admin/agent/create'):
                    #最多只能创建三级代理
                    continue

                if (aType in ['2','3']) and access.url in ONLY_SUPERNTOP_SHOW: #只有管理员显示开启和关闭
                    continue

                if (aType in ['1']) and access.url in ONLY_2_3_SHOW:#只有二三级显示
                    continue

                if access.url[-5:] == 'trail':
                    agInfo['op'].append({'url':access.url,'txt':'设置试玩' \
                                        if agInfo['isTrail'] == '0' else '解除试玩','method':access.method})
                elif access.url[-8:] == 'recharge':
                    agInfo['op'].append({'url':access.url,'txt':'开放商城' \
                                        if agInfo['recharge'] == '0' else '关闭商城','method':access.method})
                elif access.url[-10:]== 'auto_check':
                    agInfo['op'].append({'url':access.url,'txt':'开启自动审核' \
                                        if agInfo['auto_check'] == '0' else '关闭自动审核','method':access.method})
                elif access.url[-11:]== 'create_auth':
                    agInfo['op'].append({'url':access.url,'txt':'开启市级(2)' \
                                        if agInfo['create_auth'] == '0' else '关闭市级(2)','method':access.method})
                elif access.url[-9:]== 'open_auth':
                    agInfo['op'].append({'url':access.url,'txt':'所有玩家代开房)' \
                                        if agInfo['open_auth'] == '1' else '仅权限玩家代开房','method':access.method})
                elif access.url[-6:] == 'freeze':
                    agInfo['op'].append({'url':access.url,'txt':'冻结' \
                                if agInfo['valid'] == '1' else '解冻','method':access.method})
                else:
                    agInfo['op'].append({'url':access.url,'method':access.method,'txt':access.getTxt(lang)})
                '''
                elif access.url[-6:] == 'invite' and aType != '1':
                    pass
                elif access.url[-3:] == 'set' and aType != '1':
                    pass
                '''
        sub_ag_lists.append(agInfo)
    return sub_ag_lists

def getAgListInfos(redis,session,agentId,condition,lang):
    """
    获取代理列表
    """
    parentTable = AGENT_CHILD_TABLE%(agentId)
    subIds = redis.smembers(parentTable)
    is_super_admin = int(agentId) in [systemId]

    sub_agent_ids = []
    is_search_time,is_search_id = False,False
    if condition['start_date'] and not condition['searchId']:
        is_search_time = True
        date_lists = get_week_date_obj(condition['start_date'],condition['end_date'])
        for date in date_lists:
            sub_agent_ids.extend(list(redis.smembers(AGENT_CREATE_DATE%(date))))


    if condition['searchId']: #搜索ID
        is_search_id = True
        if redis.exists(AGENT_ACCOUNT_TO_ID % condition['searchId']):
            sub_agent_ids = [redis.get(AGENT_ACCOUNT_TO_ID % condition['searchId'])]
        else:
            sub_agent_ids = [condition['searchId']]

    sub_ag_lists = []
    sub_agent_own_ids = []
    if sub_agent_ids:
        for sub_agent_id in sub_agent_ids:
            if sub_agent_id in subIds:
                sub_agent_own_ids.append(sub_agent_id)

        if is_search_id and is_super_admin: # 管理员不需要检查ID是否存在
            if redis.exists(AGENT_ACCOUNT_TO_ID % condition['searchId']):
                sub_agent_own_ids = [redis.get(AGENT_ACCOUNT_TO_ID % condition['searchId'])]
            else:
                sub_agent_own_ids = [condition['searchId']]
    else:
        if is_search_time:
            sub_agent_own_ids = []
        else:
            sub_agent_own_ids = subIds

    agent_own_accesses = eval(session['access'])
    sub_ag_lists = get_agent_list_infos(redis,sub_agent_own_ids,agent_own_accesses,lang)

    return {'count' :len(sub_ag_lists),'data':sub_ag_lists}

def agentOpLog(redis, account, atype,ip):
    """
    写登录日志
    @params:
        redis     redis实例
        account   操作代理ID
        toAccount      操作日期
        atype      状态,1成功 2密码错误
    """
    curTime = datetime.now()
    dateStr = curTime.strftime("%Y-%m-%d")
    timeStr = curTime.strftime("%Y-%m-%d %H:%M:%S")

    adminLogDatesetTable = FORMAT_AGENT_OP_LOG_DATESET_TABLE%(dateStr)
    #创建新的操作日志
    id = redis.incr(FORMAT_AGENT_OP_LOG_COUNT_TABLE)
    adminLogTable = FORMAT_AGENT_OP_LOG_TABLE%(id)
    pipe = redis.pipeline()
    pipe.hmset(adminLogTable, {
        'account'           :   account,
        'type'              :   atype,
        'datetime'          :   timeStr,
        'ip'                :   ip
    })
    pipe.expire(adminLogTable, LOG_TABLE_TTL)
    pipe.lpush(adminLogDatesetTable, id)
    pipe.execute()


def writeAgentOpLog(redis,agentId,logInfo):
    """
    写操作日志
    @params:
        redis     redis实例
        agentId   操作代理ID
        date      操作日期
        desc      操作记录描述
    """
    curTime = datetime.now()

    dateStr = curTime.strftime('%Y-%m-%d')

    logId = redis.incr(AGENT_OP_COUNT)
    logTable = AGENT_OP_LOG_TABLE%(logId)
    agentLogTable = AGENT_OP_LOG_DATESET_TABLE%(agentId,dateStr)
    pipe = redis.pipeline()
    pipe.hmset(logTable,logInfo)
    pipe.lpush(agentLogTable,logId)
    pipe.execute()

def getAgentOpLog(redis,agentId,startDate,endDate):
    """
    获取代理操作日志
    @params:
        redis    链接实例
        agentId  代理ID
        startDate   开始日期
        endDate     结束日期
    """
    deltaTime = timedelta(1)

    startDate = datetime.strptime(startDate,'%Y-%m-%d')
    endDate  = datetime.strptime(endDate,'%Y-%m-%d')

    opList = []
    while endDate >= startDate:

        agentLogTable = AGENT_OP_LOG_DATESET_TABLE%(agentId,endDate.strftime('%Y-%m-%d'))
        if not redis.exists(agentLogTable):
            endDate-=deltaTime
            continue

        logIds = redis.lrange(agentLogTable,0,-1)
        for logId in logIds:
            logInfo = redis.hgetall(AGENT_OP_LOG_TABLE%(logId))

            opList.append(logInfo)

        endDate = endDate-deltaTime

    return opList

def agentFreeze(redis,agentId):
    """
    冻结代理所有下属代理
    @params:
        redis    链接实例
        agentId  代理ID
    """
    pipe = redis.pipeline()
    adminTable = AGENT_TABLE%(agentId)
    pipe.hset(adminTable,'valid','0')
    childList = redis.smembers(AGENT_CHILD_TABLE%(agentId))
    if childList:
        for child in childList:
            pipe.hset(AGENT_TABLE%(child),'valid','0')
            childSonList = redis.smembers(AGENT_CHILD_TABLE%(child))
            if childSonList:
                for childson in childSonList:
                    pipe.hset(AGENT_TABLE%(childson),'valid','0')

    pipe.execute()

def doAgentChange(redis,agentId,field,change):
    """
    设置代理所有下属代理
    @params:
        redis    链接实例
        agentId  代理ID
    """

    log_debug('-'*66)
    log_debug('-'*66)
    log_debug(agentId)
    log_debug(field)
    log_debug(change)
    log_debug('-'*66)
    log_debug('-'*66)
    pipe = redis.pipeline()
    adminTable = AGENT_TABLE%(agentId)
    pipe.hset(adminTable,field,change)
    childList = redis.smembers(AGENT_CHILD_TABLE%(agentId))

    if childList:
        for child in childList:
            pipe.hset(AGENT_TABLE%(child),field,change)
            childSonList = redis.smembers(AGENT_CHILD_TABLE%(child))
            if childSonList:
                for childson in childSonList:
                    pipe.hset(AGENT_TABLE%(childson),field,'0')

    pipe.execute()

def getAllChildAgentId(redis,agentId):
    """
    返回所有下级代理ID
    """
    agentIdList = []
    pipe = redis.pipeline()
    downLines = redis.smembers(AGENT_CHILD_TABLE%(agentId))

    if downLines:
        for downline in downLines:
            agentIdList.append(downline)
            subDownlines = redis.smembers(AGENT_CHILD_TABLE%(downline))
            if subDownlines:
                for subDownline in subDownlines:
                    agentIdList.append(subDownline)

    log_util.debug('[try getAllChildAgentId] agentId[%s] allChildIds[%s]'%(agentId,agentIdList))
    return agentIdList

def getAgRoomListInfos(redis,session,agentId,lang):
    """
        获取代理直属玩家房间列表
    """

    subAgLists = []

    # 获取俱乐部房间列表
    for club_number in redis.smembers("club:list:set"):
        club_user = redis.hget("club:attribute:%s:hash" % club_number, "club_user")
        userTable = redis.get(FORMAT_ACCOUNT2USER_TABLE % club_user)
        parentAg = redis.hget(userTable, "parentAg")
        roomTable = AG2SERVER % ("%s-%s" % (parentAg, club_number))
        subIds = redis.smembers(roomTable)
        if not subIds:
            continue
        for subId in subIds:
            roomInfo = {}
            roomTable = ROOM2SERVER % (subId)
            ag, game_id, room_type, game_name, dealer, player_count, club_number_room = \
                redis.hmget(roomTable, ('ag', 'gameid', 'type', 'gameName', 'dealer', 'playerCount', "club_number"))
            if club_number != club_number_room:
                continue
            roomInfo['id'] = subId
            roomInfo['ag'] = ag
            roomInfo['game_id'] = game_id
            roomInfo['room_type'] = room_type
            roomInfo['game_name'] = game_name
            roomInfo['player_count'] = player_count
            roomInfo['dealer'] = dealer
            roomInfo["club_number"] = club_number
            # roomInfo['gameid'] = redis.hget(GAME_TABLE%(roomInfo['gameid']),'name')
            # 获取操作权限
            roomInfo['op'] = []
            # sessiob['access']
            for access in access_module.ACCESS_AGENT_ROOM_LIST:
                if access.url in eval(session['access']):
                    roomInfo['op'].append({'url': access.url, 'method': access.method, 'txt': access.getTxt(lang)})
            subAgLists.append(roomInfo)

    # 获取代开房间列表
    agentId2Childs = getAllChildAgentId(redis, agentId)
    agentId2Childs.extend(["%s-" % i for i in agentId2Childs])
    for aId in agentId2Childs:
        roomTable = AG2SERVER%(aId)
        subIds = redis.smembers(roomTable)
        if not subIds:
            continue
        for subId in subIds:
            roomInfo = {}
            roomTable = ROOM2SERVER%(subId)
            ag,game_id,room_type,game_name,dealer,player_count =\
                            redis.hmget(roomTable,('ag','gameid','type','gameName','dealer','playerCount'))
            roomInfo['id'] = subId
            roomInfo['ag'] = ag
            roomInfo['game_id'] = game_id
            roomInfo['room_type'] = room_type
            roomInfo['game_name'] = game_name
            roomInfo['player_count'] = player_count
            roomInfo['dealer'] = dealer
            #roomInfo['gameid'] = redis.hget(GAME_TABLE%(roomInfo['gameid']),'name')

            #获取操作权限
            roomInfo['op'] = []
            # sessiob['access']
            for access in access_module.ACCESS_AGENT_ROOM_LIST:
                if access.url in eval(session['access']):
                    roomInfo['op'].append({'url':access.url,'method':access.method,'txt':access.getTxt(lang)})
            subAgLists.append(roomInfo)

    return {
        'data'  :   subAgLists,
        'count' :   len(subAgLists)
    }

def getAgentMembers(redis,agentId):
    """
    获取该公会下的活跃会员总数
    """
    agentIdChilds = getAllChildAgentId(redis,agentId)
    curTime = datetime.now()

    downLineCount = redis.get(DAY_AG_LOGIN_COUNT%(agentId,curTime.strftime('%Y-%m-%d')))
    if not downLineCount:
        downLineCount = 0

    for subId in agentIdChilds:
        count = redis.get(DAY_AG_LOGIN_COUNT%(subId,curTime.strftime('%Y-%m-%d')))
        if not count:
            count = 0
        downLineCount = int(downLineCount)+int(count)
        log_debug('[try getAgentAllMembers] agentId[%s] downLineCount[%s]'%(subId,downLineCount))

    return downLineCount

    curTime = datetime.now()
    count = redis.get(DAY_AG_LOGIN_COUNT%(agentId,curTime.strftime('%Y-%m-%d')))
    if not count:
        return 0

    return int(count)


def getAgentAllMembers(redis,agentId):
    """
    获取该公会下的活跃会员总数
    """
    agentIdChilds = getAllChildAgentId(redis,agentId)
    curTime = datetime.now()

    downLineCount = redis.scard(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(agentId))
    for subId in agentIdChilds:
        downLineCount+=int(redis.scard(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(subId)))
    #downLineCount+=redis.scard(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(agentId))

    return downLineCount


def getAgentMemberTotal(redis,agentId):
    """
    获取所有会员总数
    """
    agentIdChilds = getAllChildAgentId(redis,agentId)
    total = redis.scard(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(agentId))
    if not total:
        total=0
    for subId in agentIdChilds:
        subTotal = redis.scard(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(subId))
        if not subTotal:
            subTotal=0
        total+=int(subTotal)

    return total


def getAgentMemberLogin(redis,agentId,dateStr):
    """
    获取所有会员总数
    """
    agentIdChilds = getAllChildAgentId(redis,agentId)
    total = redis.get(DAY_AG_LOGIN_COUNT%(agentId,dateStr))
    if not total:
        total=0

    total = int(total)
    for subId in agentIdChilds:
        subTotal = redis.get(DAY_AG_LOGIN_COUNT%(subId,dateStr))
        if not subTotal:
            subTotal = 0
        total+=int(subTotal)

    return total

def getAgentRoomByDay(redis,agentId,dateStr):
    """
    获取所有会员总数
    """
    agentIdChilds = getAllChildAgentId(redis,agentId)
    total = redis.get(DAY_AG_PLAY_ROOM_CARD%(agentId,dateStr))
    if not total:
        total = 0
    total = int(total)
    for subId in agentIdChilds:
        subTotal = redis.get(DAY_AG_PLAY_ROOM_CARD%(subId,dateStr))
        if not subTotal:
            subTotal=0
        total+=int(subTotal)

    return total

def getDateAgTotal(redis,agentId,agentIds,endDate,startDate):
    """
    获取某段时间内的总数
    """
    endDate = datetime.strptime(endDate,'%Y-%m-%d')
    deltaTime = timedelta(1)
    count = 0
    while endDate>=startDate:
        date = endDate.strftime('%Y-%m-%d')
        for aid in agentIds:
            nums = redis.get(DAY_AG_LOGIN_COUNT%(aid,date))
            if not nums:
                nums = 0
            count+=int(nums)
        endDate-=deltaTime
    #log_debug('[getDateTotal] startDate[%s],endDate[%s] agentIds[%s] count[%s]'%(startDate,endDate,agentIds,count))
    return count

def get_agent_by_date(redis,agentId,agent_ids,date):
    count = 0
    for agent_id in agent_ids:
        nums = redis.get(DAY_AG_LOGIN_COUNT%(agent_id,date))
        count+=convert_util.to_int(nums)

    return count

def get_agent_active(redis,agentId,startDate,endDate):
    """
    获取直属下级代理活跃数
    """
    self_child_table = AGENT_CHILD_TABLE%(agentId)
    self_child_ids = redis.smembers(self_child_table)

    try:
        startDate = datetime.strptime(startDate,'%Y-%m-%d')
        endDate   = datetime.strptime(endDate,'%Y-%m-%d')
    except:
        weekDelTime = timedelta(7)
        weekBefore = datetime.now()-weekDelTime
        startDate = weekBefore
        endDate   = datetime.now()

    deltaTime = timedelta(1)
    res = []
    now_date = datetime.now()
    while endDate >= startDate:
        if endDate > now_date:
            endDate -= deltaTime
            continue
        for child_id in self_child_ids:
            agentInfo = {}
            agentInfo['id'] = child_id
            agentInfo['date'] = endDate.strftime('%Y-%m-%d')
            count = convert_util.to_int(redis.get(DAY_AG_LOGIN_COUNT%(child_id,agentInfo['date'])))

            parentTable = AGENT_CHILD_TABLE%(child_id)
            agent_ids = redis.smembers(parentTable)
            count = get_agent_by_date(redis,child_id,agent_ids,agentInfo['date'])
            agentInfo['account'] = redis.hget(AGENT_TABLE % child_id, 'account')
            agentInfo['active'] = count
            agentInfo['roomcard'] = getAgentRoomByDay(redis,child_id,agentInfo['date']),
            agentInfo['members'] = getAgentAllMembers(redis,child_id),
            res.append(agentInfo)
        endDate -= deltaTime
    res = sorted(res, key=itemgetter('date','active','id'),reverse=True)
    return {'data':res,'count':len(res)}

def get_agent_role_data(redis, session, agentId, lang):
    """
    获取下线代理角色列表
    """
    allChildAgentList = getAllChildAgentId(redis, agentId)
    res = []
    for agent in allChildAgentList:
        adminTable = AGENT_TABLE % (agent)
        account, aType = redis.hmget(adminTable, ('account', 'type'))
        agentRole = lang.TYPE_2_ADMINTYPE[aType]
        res.append({
            'agentId': agent,
            'account': account,
            'agentRole': agentRole,
            'op': [
                {'url': BACK_PRE + "/agent/role/list/see", 'method': 'GET', 'txt': '查看'}
            ]
        })
    return {'count': len(res), 'data': res}

def get_agent_role_see(redis, session, account, lang):
    """
    获取代理角色权限
    """
    agentId = redis.get(AGENT_ACCOUNT_TO_ID % account)
    # accessTable = AGENT2ACCESS % (agentId)
    accessTable = AGENT2ACCESSBAN % agentId
    agentTable = AGENT_TABLE % (agentId)
    aType = redis.hget(agentTable, 'type')
    mainModules, res, i, j = [], [], -1, 1
    account_info = {'0': access_module.ACCESS_SADMIN_MODULES,
            '1': access_module.ACCESS_COMPANY_MODULES,
            '2': access_module.ACCESS_AG_ONE_CLASS_MODULES,
            '3': access_module.ACCESS_AG_TWO_CLASS_MODULES,
            }
    menus = account_info.get(aType, [])
    for accessObj in menus:
        isOpen = True
        test = {}
        test['1'] = accessObj.url
        if accessObj.check:
            i += 1
            j = -1
            mainModule = {}
            mainModule['url'] = accessObj.url
            mainModule['txt'] = accessObj.getTxt(lang)
            mainModule['subModules'] = []
            mainModules.append(mainModule)
            if redis.sismember(accessTable, accessObj.url):
                isOpen = False
            res.append({'url': accessObj.url, 'isOpen': isOpen, 'txt': mainModule['txt'], 'op': []})
        elif len(accessObj.tree) != 2:
            j += 1
            subModule = {}
            subModule['url'] = accessObj.url
            subModule['txt'] = '%s - %s' % (mainModules[i]['txt'], accessObj.getTxt(lang))
            subModule['subsubModules'] = []
            mainModules[i]['subModules'].append(subModule)
            if redis.sismember(accessTable, accessObj.url):
                isOpen = False
            res.append({'url': accessObj.url, 'isOpen': isOpen, 'txt': subModule['txt'], 'op': [

                ]})
        elif len(accessObj.tree) == 2:
            if j == -1:
                subModule = {}
                subModule['url'] = accessObj.url
                subModule['txt'] = '%s - %s' % (mainModules[i]['txt'], accessObj.getTxt(lang))
                subModule['subsubModules'] = []
                mainModules[i]['subModules'].append(subModule)

                if redis.sismember(accessTable, accessObj.url):
                    isOpen = False
                res.append({'url': accessObj.url, 'isOpen': isOpen, 'txt': subModule['txt'], 'op': [
                    {'url': BACK_PRE + "/agent/role/modify", 'method': 'GET', 'txt': '关闭' if isOpen else '开启'}
                ]})
            else:
                subsubModule = {}
                subsubModule['url'] = accessObj.url
                subsubModule['txt'] = '%s - %s' % (mainModules[i]['subModules'][j]['txt'], accessObj.getTxt(lang))
                mainModules[i]['subModules'][j]['subsubModules'].append(subsubModule)
                if redis.sismember(accessTable, accessObj.url):
                    isOpen = False
                res.append({'url': accessObj.url, 'isOpen': isOpen, 'txt': subsubModule['txt'], 'op': [
                    {'url': BACK_PRE + "/agent/role/modify", 'method': 'GET', 'txt': '关闭' if isOpen else '开启'}
                ]})
    return {'count': len(res), 'data': res, 'account': account, 'role': lang.TYPE_2_ADMINTYPE[aType]}