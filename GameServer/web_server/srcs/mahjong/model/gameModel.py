#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    游戏及游戏模块模型
"""

from web_db_define import *
from gold_db_define import *
from datetime import datetime,timedelta
from admin  import access_module
from common.log import *
from common import log_util,convert_util
from config.config import *
from bottle import template
from operator import itemgetter
import copy
import json
"""
GAMEMODEL_FILED
游戏模型字段
"""
GAME_FIELDS = [

    "gameId   =  request.forms.get('id','').strip()",
    "name     =  request.forms.get('name','').strip()",
    "version  =  request.forms.get('version','').strip()",
    "web_tag  =  request.forms.get('web_tag','').strip()",
    "ipa_tag  =  request.forms.get('ipa_tag','').strip()",
    "apk_tag  =  request.forms.get('apk_tag','').strip()",
    "minVersion  =  request.forms.get('minVersion','').strip()",
    "iosVersion  =  request.forms.get('iosVersion','').strip()",
    "pack_name  =  request.forms.get('pack_name','').strip()",
    "downloadUrl  =  request.forms.get('downloadUrl','').strip()",
    "IPAURL  =  request.forms.get('IPAURL','').strip()",
    "apk_size  =  request.forms.get('apk_size','').strip()",
    "apk_md5  =  request.forms.get('apk_md5','').strip()",
    "game_rule  =  request.forms.get('game_rule','').strip()",
    "module_id  =  request.forms.get('module_id','').strip()",
    "partyPlayerCount  = request.forms.get('partyPlayerCount','').strip()",
    "maxRoomCount  = request.forms.get('maxRoomCount','').strip()",
    "other_info  = request.forms.get('other_info','').strip()",
    "game_sort  = request.forms.get('game_sort','').strip()",

    #可选项
    "radio1 = request.forms.get('radio1','').strip()",
    "title1 = request.forms.get('title1','').strip()",
    "content1 = request.forms.get('content1','').strip()",
    "number1  = request.forms.get('number1','').strip()",
    "depend1  = request.forms.get('depend1','').strip()",

    "radio2 = request.forms.get('radio2','').strip()",
    "title2 = request.forms.get('title2','').strip()",
    "content2 = request.forms.get('content2','').strip()",
    "number2  = request.forms.get('number2','').strip()",
    "depend2  = request.forms.get('depend2','').strip()",

    "radio3 = request.forms.get('radio3','').strip()",
    "title3 = request.forms.get('title3','').strip()",
    "content3 = request.forms.get('content3','').strip()",
    "number3  = request.forms.get('number3','').strip()",
    "depend3  = request.forms.get('depend3','').strip()",

    "radio4 = request.forms.get('radio4','').strip()",
    "title4 = request.forms.get('title4','').strip()",
    "content4 = request.forms.get('content4','').strip()",
    "number4 = request.forms.get('number4','').strip()",
    "depend4 = request.forms.get('depend4','').strip()",

    "radio5 = request.forms.get('radio5','').strip()",
    "title5 = request.forms.get('title5','').strip()",
    "content5 = request.forms.get('content5','').strip()",
    "number5 = request.forms.get('number5','').strip()",
    "depend5 = request.forms.get('depend5','').strip()",

    "radio6 = request.forms.get('radio6','').strip()",
    "title6 = request.forms.get('title6','').strip()",
    "content6 = request.forms.get('content6','').strip()",
    "number6 = request.forms.get('number6','').strip()",
    "depend6 = request.forms.get('depend6','').strip()",

    "radio7 = request.forms.get('radio7','').strip()",
    "title7 = request.forms.get('title7','').strip()",
    "content7 = request.forms.get('content7','').strip()",
    "number7 = request.forms.get('number7','').strip()",
    "depend7 = request.forms.get('depend7','').strip()",

    "radio8 = request.forms.get('radio8','').strip()",
    "title8 = request.forms.get('title8','').strip()",
    "content8 = request.forms.get('content8','').strip()",
    "number8 = request.forms.get('number8','').strip()",
    "depend8 = request.forms.get('depend8','').strip()",

    "cardSettingStr = request.forms.get('cardSetting','').strip()",
    "dependSettingStr = request.forms.get('dependSettingStr','').strip()",
    "dependAndSettingStr = request.forms.get('dependAndSettingStr','').strip()",
]


HALL_BRO_OP = [
        {'url':BACK_PRE+'/game/broadcast/batch_del','txt':'清除','method':"POST"}
]
"""
游戏模块模型的一些基本配置
"""
GAME_SETTING_INFO = {

        'ruleTextWidth'         :   '100%',                         #规则编辑框宽度
        'ruleTextHeight'        :   '650px',                        #规则编辑框高度
        'gameIntroPath'         :   './mahjong/static/intro/game_%s.html',  #静态规则模板路径
        'gameIntroBgPath'       :   './bg.png',                     #静态规则模板的背景图片
}

"""
游戏规则模板
"""
GAME_INTRO_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>{{title}}</title>
        <style type="text/css">
            *{margin:0;padding:0;}
            #wrap{
                        width:100%;
                        height:auto;
                        background:url({{bgUrl}});
                        background-size:100% 100%;
            }
            .wrap-content{
                    padding:8px;
            }
        </style>
    </head>
    <body>
        <div id='wrap'>
             <div class="wrap-content">
                 {{!content}}
             </div>
        </div>
    </body>
</html>
"""

"""
游戏列表可操作集合
"""
GAME_OP_LIST = [
                    {'url':BACK_PRE+'/game/introSetting','txt':'游戏规则设置','method':'GET'},
                    {'url':BACK_PRE+'/game/SingleGameBroadcast','txt':'设置广播','method':'GET'},\
                    {'url':BACK_PRE+'/game/modify','txt':'修改','method':'POST'},\
                    {'url':BACK_PRE+'/game/delete','txt':'删除','method':'POST'}
]

TASK_OP_LIST = [
                    {'url':BACK_PRE+'/task/delete','txt':'删除','method':'POST'}
]


GAME_LIST_FIELD = ('id','name','version','pack_name')

def getGameInfo(redis,gameId):
    """ 获取某个游戏的所有字段 """
    return redis.hgetall(GAME_TABLE%(gameId))

def getGameField(redis,gameId,field):
    """
    获取游戏单个字段
    """
    return redis.hget(GAME_TABLE%(gameId),field)

def get_game_list(redis,limit=None):
    """
    获取游戏列表
    """
    game_ids = redis.lrange(GAME_LIST,0,-1)
    defaultIds = redis.smembers(GAME_DEFAULT_BIND)
    game_list = []
    for game_id in game_ids:
        id,name,version,pack_name = redis.hmget(GAME_TABLE%(game_id),GAME_LIST_FIELD)
        tempOp = []
        tempOp = copy.copy(GAME_OP_LIST)
        tempOp.append({'url':BACK_PRE+'/game/setting/defaultGames','txt':'全部关闭' if game_id in defaultIds else '全部开启','method':'POST'})
        game_info = {
                'id'        :   id,
                'name'      :   name,
                'version'   :   version,
                'pack_name' :   pack_name,
                'op'        :   tempOp,
                'default'   :   '1' if game_id in defaultIds else '0'
        }
        game_list.append(game_info)

    return {'data':game_list,'count':len(game_list)}

def get_gold_game_list(redis,limit=None):
    """
    获取游戏列表
    """
    #game_ids = redis.lrange(GAME_LIST,0,-1)
    #defaultIds = redis.smembers(GAME_DEFAULT_BIND)
    game_list = []
    goldList = [
                "555",
                "556",
                "666",
                "444",
                "557",
                "445",
                "446",
                "447",
                "448",
                "449",
                "559",
                ]
    for game_id in goldList:
        id,name,version,pack_name = redis.hmget(GAME_TABLE%(game_id),GAME_LIST_FIELD)
        chets_list = []
        chets_win_list = []
        for level in range(0, 6):
            chets = redis.hgetall(CHETS_TASK_GAME % {"gameId": game_id, "level":level})
            chets_win = redis.hgetall(CHETS_TASK_WIN_GAME % {"gameId": game_id, "level":level})
            chets_number = chets.get("number")
            chets_number = int(chets_number) if chets_number else -1
            chets_result = chets.get("result")
            chets_status = chets.get("status")
            chets_status = int(chets_status) if chets_status else 0

            #chets_result = json.loads(chets_result) if chets_result else {}
            #chets_result = json.dumps(chets_result)
            chets_level  =  chets.get("level")
            chets_level  =  int(chets_level) if chets_level else 0
            chets_win_number = chets_win.get("number")
            chets_win_number = int(chets_win_number) if chets_win_number else -1
            chets_win_level = chets_win.get("level")
            chets_win_level = int(chets_win_level) if chets_win_level else 0
            chets_win_status = chets_win.get("status")
            chets_win_status = int(chets_win_status) if chets_win_status else 0


            chets_list.append({"chets_number": chets_number,
                               "chets_level": chets_level,
                               "chets_win_number": chets_win_number,
                               "chets_win_level": chets_win_level,
                               "gold_level": level,
                               "chets_status": chets_status,
                               "chets_win_status": chets_win_status
                               })


        tempOp = []
        tempOp.append({'url': BACK_PRE + '/game/setting/chets', 'txt': "奖励设置", 'method': 'get'})
        game_info = {
                'id'        :   id,
                'name'      :   name,
                'version'   :   version,
                'pack_name' :   pack_name,
                'op'        :   tempOp,
                "chets_result": chets_list,
                "chets_win_result": chets_win_list,
                'default'   :   '1' if game_id in PARTY_GOLD_GAME_LIST_SORT else '0'
        }
        game_list.append(game_info)

    return {'data':game_list,'count':len(game_list)}

def get_task_list(redis,limit=None):
    """
    获取任务列表
    """

    task_ids = redis.smembers(TASK_LIST)

    task_list = []
    for _id in task_ids:
        id,description,result,title,status = redis.hmget(TASK_CONTENT %(_id), "id", "description", "results", "title", "status")
        result = json.loads(result)
        status = int(status) if status else 0
        tempOp = []
        tempOp = copy.copy(TASK_OP_LIST)
        op_txt = "开启" if status == 0 else "关闭"
        status = "关闭" if status == 0 else "开启"
        tempOp.append({'url':BACK_PRE+'/task/modify','txt':op_txt,'method':'POST'})
        task_info = {
                'id'        :   id,
                'description'      :   description,
                'result'    :   result,
                'title'     :   title,
                'status'    :   status,
                'op'        :   tempOp,
        }
        task_list.append(task_info)
    task_list = sorted(task_list, key=lambda x: int(x["id"]))
    return {'data':task_list,'count':len(task_list)}


def do_create_game(redis,game_id,gameInfo):
    """
    创建新游戏
    @param:
        redis      redis链接实例
        gameInfo   游戏信息
    """

    if game_id in GAMEID_SET:
        return None

    game_table = GAME_TABLE%(game_id)
    pipe = redis.pipeline()
    try:
        pipe.hmset(game_table,gameInfo)
        pipe.sadd(GAMEID_SET,game_id)
        pipe.lpush(GAME_LIST,game_id)
    except Exception,e:
        log_util.error('[try do_create_game] reason[%s]'%(e))
        return None
    pipe.execute()
    return game_id

def gameModify(redis,gameId,gameInfo):
    """ 游戏模块修改 """
    return redis.hmset(GAME_TABLE%(gameId),gameInfo)

def gameDelete(redis,gameId):
    """
    游戏删除
    """
    gameTable  = GAME_TABLE%(gameId)
    pipe = redis.pipeline()

    try:
        pipe.delete(gameTable)
        pipe.delete(GAME2DESC%(gameId))
        pipe.delete(GAME2RULE%(gameId))
        pipe.delete(USE_ROOM_CARDS_RULE%(gameId))
        pipe.delete(GAME2RULE_DATA%(gameId,'*'))
        pipe.delete(GAME2RULE_DATA_DEPEND%(gameId,'*'))
        pipe.lrem(GAME_LIST,gameId)
        pipe.srem(GAMEID_SET,gameId)
    except Exception,e:
        print '[gameDelete][info] gameId[%s] delete error. reason[%s]'%(gameId,e)
        return None

    return pipe.execute()

def getGameInfoById(redis,gameId):
    """
    获取游戏信息
    """
    gameTable = GAME_TABLE%(gameId)

    return redis.hmget(gameTable)

def getGameSetting(redis,gameId):
    """
    获取游戏配置
    """
    gameRuleList = GAME2RULE%(gameId)

    ruleIds = redis.lrange(gameRuleList,0,-1)

    ruleList = []
    for ruleId in ruleIds:
        print '[getGameSetting][info] gameId[%s] ruleId[%s]'%(gameId,ruleId)
        ruleInfo = redis.hgetall(GAME2RULE_DATA%(gameId,ruleId))
        ruleInfo['id'] = ruleId
        if 'row' not in ruleInfo.keys():
            ruleInfo['row'] = ''
        if 'depend' not in ruleInfo.keys():
            ruleInfo['depend'] = ''
        ruleList.append(ruleInfo)

    return ruleList

def getGameRuleDepends(redis,gameId,gameSetting):
    """
    获取游戏配置依赖
    """
    gameDependList = []
    for setting in gameSetting:
        gameDependInfo = redis.hgetall(GAME2RULE_DATA_DEPEND%(gameId,setting['id']))
        print 'gameDependInfo',gameDependInfo

    return

def getNoticsList(redis,session,lang,startDate,endDate):
    """
    获取公告列表
    params:
    """
    try:
        startDate = datetime.strptime(startDate,'%Y-%m-%d')
        endDate   = datetime.strptime(endDate,'%Y-%m-%d')
    except:
        weekDelTime = timedelta(7)
        weekBefore = datetime.now()-weekDelTime
        startDate = weekBefore
        endDate   = datetime.now()

    totalList = []
    noticeListTable = FORMAT_GAMEHALL_NOTIC_LIST_TABLE
    noticeIds = redis.lrange(noticeListTable, 0, -1)
    for noticeId in noticeIds:
        noticeTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticeId)
        noticeInfo = redis.hgetall(noticeTable)
        noticeInfo['id'] = noticeId
        noticeInfo['op'] = []
        # sessiob['access']
        for access in access_module.ACCESS_GAME_NOTICE_LIST:
            if access.url in eval(session['access']):
                if access.url == '/admin/game/notice/push':
                    noticeInfo['op'].append({'url':access.url,'txt':'推送' \
                                if noticeInfo['status'] == '0' else '取消推送','method':access.method})
                else:
                    noticeInfo['op'].append({'url':access.url,'method':access.method,'txt':access.getTxt(lang)})
        totalList.append(noticeInfo)

    return {'data':totalList}

def get_borad_list(redis,selfUid,lang,broad_belone):
    """
    获取广播列表的数据
    :params redis  数据库连接实例
    :params selfUid 当前的操作人ID
    :lang  语言实例
    :params broad_belone   获取系统广播 ['HALL','FISH']
    :return 广播列表 [{},{}]
    """
    if broad_belone == 'HALL':
        if int(selfUid) == 1:
            broad_list = HALL_BRO_LIST
        else:
            broad_list = HALL_BRO_AG_LIST%(selfUid)
    elif broad_belone == 'FISH':
        broad_list = FISH_BRO_LIST
    else:
        broad_list = []

    broad_ids = redis.lrange(broad_list, 0, -1)
    totalList = []
    for broad_id in broad_ids:
        broadTable =  HALL_BRO_TABLE%(broad_id)
        broadInfo  = redis.hgetall(broadTable)
        broadInfo['op'] = HALL_BRO_OP
        totalList.append(broadInfo)

    return {'data':totalList, 'count': len(totalList)}


def getGameCardSetting(redis,gameId):
    """
    获取游戏钻石配置
    """
    cardRule = []
    cardRules = redis.lrange(USE_ROOM_CARDS_RULE%(gameId),0,-1)

    for rule in cardRules:
        cardRule.append(rule)

    if cardRule:
        return ",".join(cardRule)

    return ''

def getGameServersById(redis,gameId):
    """
    通过gameId获取游戏服务器
    """
    servers = redis.lrange(FORMAT_GAME_SERVICE_SET%(gameId), 0, -1)
    serverList = []
    for server in servers:
        _,_,_,desc,ip,port = server.split(":")
        serverInfo = {
                'id'          :   gameId,
                'serverUrl'   :   ip+":"+port,
                'desc'        :   desc,
                'op'          :   [
                                        {'txt':'关闭服务器','url':BACK_PRE+'/game/server/close','method':'POST'}
                                  ]
        }
        serverList.append(serverInfo)

    return serverList

def createGameIntroTemp(gameId,gameDesc):
    """
    生成静态模板
    """

    html = template(GAME_INTRO_TEMPLATE,title="规则介绍",content=gameDesc,bgUrl=GAME_SETTING_INFO['gameIntroBgPath'])

    log_debug('[FUNC][createGameIntroTemp][info] gameId[%s] gameDesc[%s] html[%s]'%(gameId,gameDesc,html))

    try:
        with open(GAME_SETTING_INFO['gameIntroPath']%(gameId),'wb') as f:
            f.write(html.encode('utf-8'))
    except Exception,e:
        log_debug('[FUNC][createGameIntroTemp][error] gameId[%s] gameDesc[%s] error. reason[%s]'%(gameId,gameDesc,e))
        return None

    return "/intro/game_%s.html"%(gameId)

def push_broacast(redis,broadcastInfo,broad_type,selfUid,broad_belone):
    """
    将新创建的广播推送
    params : redis,broadcastInfo,broad_type,selfUid
    """
    log_debug('[try push_broacast]')
    broad_id = broadcastInfo['broad_id']
    pipe = redis.pipeline()

    pipe.hmset(HALL_BRO_TABLE%(broad_id),broadcastInfo)
    #放入相应的列表
    log_util.debug('[try push_broadcast] broad_belone[%s] broad_id[%s] selfUid[%s]'%(broad_belone,broad_id,selfUid))
    if broad_belone == 'HALL':
        pipe.lpush(HALL_BRO_LIST,broad_id)
        if int(selfUid) != 1:
            redis.lpush(HALL_BRO_AG_LIST%(selfUid),broad_id)
            redis.lpush(HALL_BRO_CONTAIN_AG_LIST%(broad_type,selfUid),broad_id)
        #放入类型表
        pipe.lpush(HALL_BRO_CONTAIN_ALL_LIST%(broad_type),broad_id)
    elif broad_belone == "FISH":
        pipe.lpush(FISH_BRO_LIST,broad_id)
        pipe.lpush(FISH_BRO_CONTAIN_ALL_LIST%(broad_type),broad_id)
    else:
        return

    pipe.execute()

def do_deleteBroads(redis,broad_id,broad_belone):
    """
    广播清除方法
    :params broad_id 广播id
    :params broad_belone 广播所属
    : return pipeline obj 告诉是否删除成功
    """
    log_debug('[try do_deleteBroads]')
    out_set = redis.smembers(HALL_BRO_OUT_SET)
    play_set = redis.smembers(HALL_BRO_PLAY_SET)
    pipe = redis.pipeline()
    send_ag,send_type = redis.hmget(HALL_BRO_TABLE%(broad_id),('parent_ag','broad_type'))
    if broad_belone == 'HALL':
        pipe.lrem(HALL_BRO_LIST,broad_id)
        pipe.lrem(HALL_BRO_AG_LIST%(send_ag),broad_id)
        pipe.lrem(HALL_BRO_CONTAIN_AG_LIST%(send_ag,send_type),broad_id)
        pipe.lrem(HALL_BRO_CONTAIN_ALL_LIST%(send_type),broad_id)
    elif broad_belone == 'FISH':
        pipe.lrem(FISH_BRO_LIST,broad_id)
        pipe.lrem(FISH_BRO_CONTAIN_ALL_LIST%(send_type),broad_id)
    else:
        pass

    if broad_id in out_set:
        redis.srem(HALL_BRO_OUT_SET,broad_id)

    if broad_id in play_set:
        redis.srem(HALL_BRO_PLAY_SET,broad_id)

    pipe.delete(HALL_BRO_TABLE%(broad_id))
    pipe.execute()

def get_game_info(redis,group_id,isRefresh=False):
    """ 获取游戏信息 """
    group_id_games = AGENT_OWN_GAME%(group_id)
    try:
        game_id_sets = redis.smembers(group_id_games)
    except:
        game_id_sets = redis.lrange(group_id_games, 0, -1)

    defaultGameSet = redis.smembers(GAME_DEFAULT_BIND)
    #增加绑定游戏
    if not defaultGameSet:
        defaultGameSet = []
    game_id_sets,defaultGameSet = list(game_id_sets),list(defaultGameSet)
    game_id_sets.extend(defaultGameSet)
    game_id_sets = set(game_id_sets)

    game_list = {}
    for game_id in game_id_sets:
        game_table = GAME_TABLE%(game_id)
        if not redis.exists(game_table):
            continue
        name, webTag, version,packName,game_sort = redis.hmget(game_table, ('name', 'web_tag', 'version','pack_name','game_sort'))
        game_list[game_id] = {
            'id'                :           game_id,
            'name'              :           name,
            'web_tag'           :           webTag,
            'version'           :           version,
            'downloadUrl'       :           packName,
            'sort'              :           convert_util.to_int(game_sort)
        }
    game_list = sorted(game_list.iteritems(),key=lambda d:d[1]['sort'])
    if isRefresh:
        game_list = {int(game[0]):game[1] for game in game_list}
    return game_list
