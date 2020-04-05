#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    游戏模块
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

@admin_app.get('/game/list')
@checkAccess
def get_game_list_api(redis):
    """
        游戏列表视图
    """
    lang = getLang()

    isList = request.GET.get('list','').strip()

    info = {
            'title'         :     lang.GAME_LIST_TXT,
            'addTitle'      :     lang.GAME_CREATE_TXT,
            'setTitle'      :     lang.GAME_SET_DEFAULT_TXT,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'setUrls'       :     BACK_PRE+'/game/setting/defaultGames',
            'serversUrl'    :     BACK_PRE+'/game/server/list?list=1',
            'tableUrl'      :     BACK_PRE+'/game/list?list=1'
    }
    #accesses = eval(session['access'])
    if isList:
        res = get_game_list(redis)
        return json.dumps(res)
    else:
        #info['createAccess'] = True if BACK_PRE+'/game/create' in accesses else False
        info['createUrl']   = BACK_PRE+'/game/create'
        return template('admin_game_list',PAGE_LIST=PAGE_LIST,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/game/set_game_gold')
def set_game_gold_api(redis):

    number = request.forms.get("number", "").strip()
    win_number = request.forms.get("win_number", "").strip()
    chets_level = request.forms.get("chets_level", "").strip()
    chets_win_level = request.forms.get("chets_win_level", "").strip()
    game_id = request.forms.get("game_id", "").strip()
    level = request.forms.get("level", "").strip()

    chets_tables = CHETS_TASK_GAME % {"gameId": game_id, "level":level}
    chets_win_tables = CHETS_TASK_WIN_GAME % {"gameId": game_id, "level": level}

    pipe = redis.pipeline()
    pipe.hmset(chets_tables, {
        "number": number,
        "level" : chets_level
    })
    pipe.hmset(chets_win_tables, {
        "number": win_number,
        "level" : chets_win_level
    })
    pipe.execute()
    return {"code": 0, "msg": "成功"}

@admin_app.post("/game/chets/close")
def chets_closed(redis):
    """

    :param redis:
    :return:
    """
    game_id = request.forms.get("game_id", "").strip()
    level = request.forms.get("level", "").strip()
    status = request.forms.get("status", '').strip()
    chets_tables = CHETS_TASK_GAME % {"gameId": game_id, "level":level}
    chets_win_tables = CHETS_TASK_WIN_GAME % {"gameId": game_id, "level": level}

    redis.hmset(chets_tables, {"status": status})
    redis.hmset(chets_win_tables, {"status": status})
    return {"code": 0, "msg": "成功", "status": int(status)}

@admin_app.post("/game/setting/chets")
def setting_chets(redis):


    game_id = request.forms.get("game_id", "").strip()
    level = request.forms.get("level", "").strip()
    chets_values = request.forms.get("chets_values", "").strip()
    chets_win_values = request.forms.get("chets_win_values", "").strip()
    chets_type = request.forms.get("chets_type", "").strip()
    chets_win_type = request.forms.get("chets_win_type", "").strip()

    chets_tables = CHETS_TASK_GAME % {"gameId": game_id, "level": level}
    chets_win_tables = CHETS_TASK_WIN_GAME % {"gameId": game_id, "level": level}

    chets_values = json.loads(chets_values)
    chets_win_values = json.loads(chets_win_values)

    print game_id, level, chets_values, chets_win_values, chets_type, chets_win_type

    pipe = redis.pipeline()

    chets_result = {"type": chets_type, "result": json.dumps(chets_values)}
    chets_win_result = {"type": chets_win_type, "result": json.dumps(chets_win_values)}

    pipe.hmset(chets_tables, chets_result)
    pipe.hmset(chets_win_tables, chets_win_result)
    pipe.execute()

    return {"code": 0, "msg": "成功"}

@admin_app.get("/game/setting/chets")
def setting_chets(redis):
    """
    :param redis:
    :return:
    """
    gameId = request.params.get("gameId", '').strip()
    lang = getLang()
    info = {
        'gameId': gameId,
        'title': lang.GAME_LIST_TXT,
        'addTitle': lang.GAME_CREATE_TXT,
        'setTitle': lang.GAME_SET_DEFAULT_TXT,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'setUrls': BACK_PRE + '/game/setting/defaultGames',
        'serversUrl': BACK_PRE + '/game/server/list?list=1',
        'tableUrl': BACK_PRE + '/game/gold_list?list=1'
    }
    result = []
    queryKeys = {
        "0": '新手场',
        "1": '普通场',
        "2": '中级场',
        "3": '高级场',
        '4': "土豪场",
        '5': '至尊场'
    }

    queryTypeKeys = {
        0: "铜",
        1: "银",
        2: "金"
    }

    ResultTypeKeys = {
        0: "金币",
        1: "元宝",
        2: "道具"
    }
    defaultResult = [
        {"key": 0, "value": 0, "txt": "金币"},
        {"key": 0, "value": 0, "txt": "金币"},
        {"key": 0, "value": 0, "txt": "金币"},
    ]
    for level in range(0, 6):
        chets_tables = CHETS_TASK_GAME % {"gameId": gameId, "level":level}
        chets_win_tables = CHETS_TASK_WIN_GAME % {"gameId": gameId, "level": level}
        chets = redis.hgetall(chets_tables)

        chets_win = redis.hgetall(chets_win_tables)
        chets_result = chets.get("result")
        chets_result = json.loads(chets_result) if chets_result else defaultResult
        chets_type = chets.get("type")
        chets_type = int(chets_type) if chets_type else 0


        chets_win_result = chets_win.get("result")
        chets_win_result = json.loads(chets_win_result) if chets_win_result else defaultResult
        chets_win_type = chets_win.get("type")
        chets_win_type = int(chets_win_type) if chets_win_type else 0

        for k, v in enumerate(chets_win_result):
            v["txt"] = ResultTypeKeys[int(v["key"])]
            chets_win_result[k] = v

        for k, v in enumerate(chets_result):
            v["txt"] = ResultTypeKeys[int(v["key"])]
            chets_result[k] = v

        result.append(
            {
                "level": level,
                "chets_result": chets_result,
                "chets_win_result": chets_win_result,
                "txt": queryKeys[str(level)],
                "chets_win_type": {"key": chets_win_type, "value": queryTypeKeys[chets_win_type]},
                "chets_type": {"key": chets_type, "value": queryTypeKeys[chets_type]},
            }
        )

    return template('admin_game_gold_chets_setting.tpl', lang=lang, info=info, RES_VERSION=RES_VERSION, result=result)

@admin_app.get('/game/gold_list')
def get_game_gold_list_api(redis):
    """
        游戏列表视图
    """
    lang = getLang()

    isList = request.GET.get('list','').strip()

    info = {
            'title'         :     lang.GAME_LIST_TXT,
            'addTitle'      :     lang.GAME_CREATE_TXT,
            'setTitle'      :     lang.GAME_SET_DEFAULT_TXT,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'setUrls'       :     BACK_PRE+'/game/setting/defaultGames',
            'serversUrl'    :     BACK_PRE+'/game/server/list?list=1',
            'tableUrl'      :     BACK_PRE+'/game/gold_list?list=1'
    }
    #accesses = eval(session['access'])
    if isList:
        res = get_gold_game_list(redis)
        return json.dumps(res)
    else:
        #info['createAccess'] = True if BACK_PRE+'/game/create' in accesses else False
        info['createUrl']   = ''
        return template('admin_game_gold_chets.tpl',PAGE_LIST=PAGE_LIST,info=info,lang=lang,RES_VERSION=RES_VERSION)



@admin_app.get('/game/create')
@checkLogin
def get_game_create(redis,session):
    """
    创建游戏视图
    """
    lang = getLang()

    info = {
            'title'             :       lang.GAME_CREATE_TXT,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'back_pre'          :       BACK_PRE,
            'backUrl'          :       BACK_PRE+'/game/list',
            'submitUrl'         :       BACK_PRE+'/game/create',
            'uploadUrl'         :       BACK_PRE+'/game/iconUpload',
            'partyPlayerMax'    :       PARTY_PLAYER_COUNT,
            'module_id'         :       '',
            'name'              :       '',
            'icon_path'         :       '',
            'web_tag'           :       '',
            'apk_tag'           :       '',
            'ipa_tag'           :       '',
            'pc_tag'            :       '',
            'apksize'           :       '',
            'apkmd5'            :       '',
            'downloadUrl'       :       '',
            'version'           :       '',
            'minVersion'        :       '',
            'iosVersion'        :       '',
            'pack_name'         :       '',
            'game_rule'         :       '',
            'maxRoomCount'      :       ''
    }

    return template('admin_game_create',message='',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/game/create')
def do_gameCreate(redis,session):
    """ 创建游戏控制器 """
    curTime = datetime.now()
    lang    = getLang()

    for gameField in GAME_FIELDS:
        exec(gameField)

    checkNullFields = [
        {'field':name,'msg':lang.GAME_NAME_NOT_EMPTY_TXT},
        {'field':version,'msg':lang.GAME_VER_NOT_EMPTY_TXT}
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    if partyPlayerCount:
        try:
            if not (int(partyPlayerCount) > 1 and int(partyPlayerCount) <= PARTY_PLAYER_COUNT) :
                return {'code':1,'msg':'娱乐模式人数设置必须大于1人小于%s人'%(PARTY_PLAYER_COUNT)}
        except:
            return {'code':1,'msg':'娱乐模式人数设置必须为整数'}
    else :
        partyPlayerCount = PARTY_PLAYER_COUNT

    #print
    print '[%s][gameCreate][info] name[%s] version[%s] minVersion[%s] iosVersion[%s] apk_size[%s] module_id[%s]'\
                    %(curTime,name,version,minVersion,iosVersion,apk_size,module_id)

    gameInfo = {
            'id'            :       gameId,
            'name'          :       name,
            'version'       :       version,
            'web_tag'       :       web_tag,
            'ipa_tag'       :       ipa_tag,
            'apk_tag'       :       apk_tag,
            'minVersion'    :       minVersion,
            'iosVersion'    :       iosVersion,
            'pack_name'      :      pack_name,
            'other_info'    :       other_info,
            'game_sort'     :       game_sort,
            'downloadUrl'   :       downloadUrl,
            'apk_size'      :       apk_size,
            'apk_md5'       :       apk_md5,
            'game_rule'     :       game_rule,
            'module_id'     :       module_id,
            'maxRoomCount'  :       maxRoomCount,
            'dependSetting' :       dependSettingStr,
            'dependAndSetting' :       dependAndSettingStr,
            'party_player_count' :  partyPlayerCount
    }

    game_id =  do_create_game(redis,gameId,gameInfo)
    pipe = redis.pipeline()
    if game_id:
        #增加钻石规则
        try:
            if redis.exists(USE_ROOM_CARDS_RULE%(game_id)):
                redis.delete(USE_ROOM_CARDS_RULE%(game_id))

            cardRules = cardSettingStr.split(',')
            for cardRule in cardRules:
                pipe.lpush(USE_ROOM_CARDS_RULE%(game_id),cardRule)
        except:
            return {'code':1,'msg':'钻石配置格式不正确'}

        if radio1 and title1 and content1:
            pipe.rpush(GAME2RULE%(game_id),1)
            pipe.hmset(GAME2RULE_DATA%(game_id,1),{'title':title1,'type':radio1,'rule':content1,'row':number1,'depend':depend1})
        if radio2 and title2 and content2:
            pipe.rpush(GAME2RULE%(game_id),2)
            pipe.hmset(GAME2RULE_DATA%(game_id,2),{'title':title2,'type':radio2,'rule':content2,'row':number2,'depend':depend2})
        if radio3 and title3 and content3:
            pipe.rpush(GAME2RULE%(game_id),3)
            pipe.hmset(GAME2RULE_DATA%(game_id,3),{'title':title3,'type':radio3,'rule':content3,'row':number3,'depend':depend3})
        if radio4 and title4 and content4:
            pipe.rpush(GAME2RULE%(game_id),4)
            pipe.hmset(GAME2RULE_DATA%(game_id,4),{'title':title4,'type':radio4,'rule':content4,'row':number4,'depend':depend4})
        if radio5 and title5 and content5:
            pipe.rpush(GAME2RULE%(game_id),5)
            pipe.hmset(GAME2RULE_DATA%(game_id,5),{'title':title5,'type':radio5,'rule':content5,'row':number5,'depend':depend5})

        if radio6 and title6 and content6:
            pipe.rpush(GAME2RULE%(game_id),6)
            pipe.hmset(GAME2RULE_DATA%(game_id,6),{'title':title6,'type':radio6,'rule':content6,'row':number6,'depend':depend6})

        if radio7 and title7 and content7:
            pipe.rpush(GAME2RULE%(game_id),7)
            pipe.hmset(GAME2RULE_DATA%(game_id,7),{'title':title7,'type':radio7,'rule':content7,'row':number7,'depend':depend7})

        if radio8 and title8 and content8:
            pipe.rpush(GAME2RULE%(game_id),8)
            pipe.hmset(GAME2RULE_DATA%(game_id,8),{'title':title8,'type':radio8,'rule':content8,'row':number8,'depend':depend8})
    else:
        return {'code':1,'msg':lang.GAME_ID_REPEAT_TXT%(game_id)}

    pipe.execute()
    #记录操作日志
    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                    'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['createGame']%(name)}
    #记录日志
    writeAgentOpLog(redis,session['id'],logInfo)
    return {'code':0,'msg':lang.GAME_CREATE_SUCCESS_TXT%(name),'jumpUrl':BACK_PRE+'/game/list'}


@admin_app.get('/game/modify')
@admin_app.get('/game/modify/<game_id>')
def getGameModify(redis,session,game_id=None):
    """
    游戏信息修改视图
    """
    curTime = datetime.now()
    lang    = getLang()
    gameId  = request.GET.get('gameId','').strip()

    gameInfo  =  getGameInfo(redis,gameId)
    gameSetting = getGameSetting(redis,gameId)

    cardSetting = getGameCardSetting(redis,gameId)
    ruleDepends = getGameRuleDepends(redis,gameId,gameSetting)
    try:
        partyPlayerCount = gameInfo['party_player_count'] if gameInfo['party_player_count'] else PARTY_PLAYER_COUNT
    except :
        partyPlayerCount = PARTY_PLAYER_COUNT
    info = {
                'title'     :       lang.GAME_MODIFY_TXT%(gameInfo['name']),
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'back_pre'          :       BACK_PRE,
                'cardSetting'       :       cardSetting,
                'backUrl'           :       BACK_PRE+'/game/list',
                'submitUrl'         :       BACK_PRE+'/game/modify',
                'uploadUrl'         :       BACK_PRE+'/game/iconUpload',
                'partyPlayerCount'  :       partyPlayerCount,
                'dependSettingStr'  :       gameInfo['dependSetting'] if 'dependSetting' in gameInfo.keys() else '',
                'dependAndSettingStr'  :       gameInfo['dependAndSetting'] if 'dependAndSetting' in gameInfo.keys() else '',
                'maxRoomCount'      :       gameInfo['maxRoomCount'] if 'maxRoomCount' in gameInfo.keys() else '',
                'partyPlayerMax'    :       PARTY_PLAYER_COUNT
    }

    return template('admin_game_modify',info=info,gameInfo=gameInfo,lang=lang,gameId=gameId,gameSetting=gameSetting,RES_VERSION=RES_VERSION)

@admin_app.post('/game/modify')
def do_gameModify(redis,session):
    """
        游戏信息修改控制器
    """

    curTime = datetime.now()
    lang    = getLang()

    for gameField in GAME_FIELDS:
        exec(gameField)

    checkNullFields = [
        {'field':name,'msg':lang.GAME_NAME_NOT_EMPTY_TXT},
        {'field':version,'msg':lang.GAME_VER_NOT_EMPTY_TXT}
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    #print
    print '[%s][gameModify][info] name[%s] version[%s] minVersion[%s] iosVersion[%s] apk_size[%s] module_id[%s]'\
                    %(curTime,name,version,minVersion,iosVersion,apk_size,module_id)
    if partyPlayerCount:
        try:
            if not (int(partyPlayerCount) > 1 and int(partyPlayerCount) <= PARTY_PLAYER_COUNT) :
                return {'code':1,'msg':'娱乐模式人数设置必须大于1人小于%s人'%(PARTY_PLAYER_COUNT)}
        except:
            return {'code':1,'msg':'娱乐模式人数设置必须为整数'}
    else :
        partyPlayerCount = PARTY_PLAYER_COUNT

    gameInfo = {

            'name'          :       name,
            'version'       :       version,
            'web_tag'       :       web_tag,
            'ipa_tag'       :       ipa_tag,
            'apk_tag'       :       apk_tag,
            'minVersion'    :       minVersion,
            'iosVersion'    :       iosVersion,
            'pack_name'      :      pack_name,
            'other_info'    :       other_info,
            'game_sort'     :       game_sort,
            'downloadUrl'   :       downloadUrl,
            'apk_size'      :       apk_size,
            'apk_md5'       :       apk_md5,
            'game_rule'     :       game_rule,
            'module_id'        :       module_id,
            'party_player_count' :  partyPlayerCount,
            'dependSetting'    :       dependSettingStr,
            'dependAndSetting' :       dependAndSettingStr,
            'maxRoomCount'  :       maxRoomCount
    }

    pipe = redis.pipeline()
    if gameModify(redis,gameId,gameInfo):
        #修改游戏
        try:
            if redis.exists(USE_ROOM_CARDS_RULE%(gameId)):
                redis.delete(USE_ROOM_CARDS_RULE%(gameId))

            cardRules = cardSettingStr.split(',')
            for cardRule in cardRules:
                pipe.rpush(USE_ROOM_CARDS_RULE%(gameId),cardRule)
        except:
            return {'code':1,'msg':'钻石配置格式不正确'}

        if radio1 and title1 and content1 and int(radio1) != -1:
            pipe.lrem(GAME2RULE%(gameId),1)
            pipe.rpush(GAME2RULE%(gameId),1)
            pipe.hmset(GAME2RULE_DATA%(gameId,1),{'title':title1,'type':radio1,'rule':content1,'row':number1,'depend':depend1})
        else:
            pipe.lrem(GAME2RULE%(gameId),1)

        if radio2 and title2 and content2 and int(radio2) != -1:
            pipe.lrem(GAME2RULE%(gameId),2)
            pipe.rpush(GAME2RULE%(gameId),2)
            pipe.hmset(GAME2RULE_DATA%(gameId,2),{'title':title2,'type':radio2,'rule':content2,'row':number2,'depend':depend2})
        else:
            pipe.lrem(GAME2RULE%(gameId),2)

        if radio3 and title3 and content3 and int(radio3) != -1:
            pipe.lrem(GAME2RULE%(gameId),3)
            pipe.rpush(GAME2RULE%(gameId),3)
            pipe.hmset(GAME2RULE_DATA%(gameId,3),{'title':title3,'type':radio3,'rule':content3,'row':number3,'depend':depend3})
        else:
            pipe.lrem(GAME2RULE%(gameId),3)

        if radio4 and title4 and content4 and int(radio4) != -1:
            pipe.lrem(GAME2RULE%(gameId),4)
            pipe.rpush(GAME2RULE%(gameId),4)
            pipe.hmset(GAME2RULE_DATA%(gameId,4),{'title':title4,'type':radio4,'rule':content4,'row':number4,'depend':depend4})
        else:
            pipe.lrem(GAME2RULE%(gameId),4)

        if radio5 and title5 and content5 and int(radio5) != -1:
            pipe.lrem(GAME2RULE%(gameId),5)
            pipe.rpush(GAME2RULE%(gameId),5)
            pipe.hmset(GAME2RULE_DATA%(gameId,5),{'title':title5,'type':radio5,'rule':content5,'row':number5,'depend':depend5})
        else:
            pipe.lrem(GAME2RULE%(gameId),5)

        if radio6 and title6 and content6 and int(radio6) != -1:
            pipe.lrem(GAME2RULE%(gameId),6)
            pipe.rpush(GAME2RULE%(gameId),6)
            pipe.hmset(GAME2RULE_DATA%(gameId,6),{'title':title6,'type':radio6,'rule':content6,'row':number6,'depend':depend6})
        else:
            pipe.lrem(GAME2RULE%(gameId),6)

        if radio7 and title7 and content7 and int(radio7) != -1:
            pipe.lrem(GAME2RULE%(gameId),7)
            pipe.rpush(GAME2RULE%(gameId),7)
            pipe.hmset(GAME2RULE_DATA%(gameId,7),{'title':title7,'type':radio7,'rule':content7,'row':number7,'depend':depend7})
        else:
            pipe.lrem(GAME2RULE%(gameId),7)

        if radio8 and title8 and content8 and int(radio8) != -1:
            pipe.lrem(GAME2RULE%(gameId),8)
            pipe.rpush(GAME2RULE%(gameId),8)
            pipe.hmset(GAME2RULE_DATA%(gameId,8),{'title':title8,'type':radio8,'rule':content8,'row':number8,'depend':depend8})
        else:
            pipe.lrem(GAME2RULE%(gameId),8)

        pipe.execute()
        logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                        'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['modifyGame']%(name)}
        #记录日志
        writeAgentOpLog(redis,session['id'],logInfo)
        return {'code':0,'msg':lang.GAME_MODIFY_SUCCESS_TXT%(name),'jumpUrl':BACK_PRE+'/game/list'}

    return {'code':1,'msg':lang.GAME_MODIFY_ERROR_TXT%(name)}

@admin_app.post('/game/delete')
def do_gameDelete(redis,session):
    """
    游戏删除
    """
    curTime = datetime.now()
    lang = getLang()
    gameId  = request.forms.get('id','').strip()

    if not gameId:
        return {'code':1,'msg':'gameId不正确.'}
    try:
        gameDelete(redis,gameId)
        logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                        'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['deleteGame']%(gameId)}
        #记录日志
        writeAgentOpLog(redis,session['id'],logInfo)
    except Exception,e:
        return {'code':1,'msg':'game[%s]删除失败 reason[%s]'%(gameId,e)}

    return {'code':0,'msg':'删除游戏[%s]成功'%(gameId),'jumpUrl':BACK_PRE+'/game/list'}

@admin_app.get('/game/broadcast')
def getGameBroadCast(redis,session):
    """
    创建广播
    """
    lang = getLang()
    fields = ('broad_belone',)
    for field in fields:
        exec("%s=request.GET.get('%s','').strip()"%(field,field))

    agent_table = AGENT_TABLE%(session['id'])
    agent_type = redis.hget(agent_table,'type')

    info = {
        'title'                 :       lang.GAME_BROCAST_TXT,
        'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
        'subUrl'                :       BACK_PRE+"/game/broadcast",
        'back_pre'              :       BACK_PRE,
        'agent_type'            :       agent_type,
        'broad_belone'          :       broad_belone,
        'defaultGameId'         :       '',
        'backUrl'               :        BACK_PRE + "/game/broadList?broad_belone=HALL",
    }

    return template('admin_game_broadcast', info=info, lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/game/broadcast')
def do_GameBroadCast(redis,session):
    """
    创建广播_逻辑
    """
    fields = ('broad_type','start_date','end_date','content','per_sec','broad_belone')

    for field in fields:
        exec("%s = request.forms.get('%s','').strip()"%(field,field))
    print(broad_type, start_date, end_date, content, per_sec, broad_belone)
    lang = getLang()
    curTime = datetime.now()
    selfUid = session['id']

    if not content:
        return {'code':1,'msg':lang.GAME_BROCAST_CON_TXT}
    try:
        per_sec = int(per_sec)
        if per_sec < 0:
            raise ValueError
        if per_sec > 60:
            return {'code':1,'msg':'广播的最大间隔为60秒..'}
    except ValueError:
        return {'code':1,'msg':lang.GAME_BROCAST_SEC_ERR_TXT}

    broad_id = redis.incr(HALL_BRO_COUNT)
    if broad_type in ['0','2']:#如果是维护广播,则结束时间置空
        end_date = ""
    broad_title = BROAD_TYPE_2_TITLE[broad_type]
    broadcastInfo = {
        'broad_id'          :   broad_id,
        'parent_ag'         :   selfUid,
        'content'           :   broad_title+content, #携带标题s
        'per_sec'           :   per_sec,
        'start_date'        :   start_date,
        'end_date'          :   end_date,
        'status'            :   0,
        'broad_type'        :   broad_type,
        'create_date'       :   curTime.strftime("%Y-%m-%d %H:%M:%S")
    }

    log_util.debug('[try do_GameBroadCast] selfUid[%s] broadcastInfo[%s]'%(selfUid,broadcastInfo))
    try:
        push_broacast(redis,broadcastInfo,broad_type,selfUid,broad_belone)
    except Exception,e:
         log_debug('[do_GameBroadCast][Error] bid[%s] send error. reason[%s]'%(broad_id,e))
         return {'code':1,'msg':lang.GAME_BROCAST_SEND_ERROR}

    return {'code':0,'msg':lang.GAME_BROCAST_SEND_SUCCESS,'jumpUrl':BACK_PRE+'/game/broadList?broad_belone=%s'%(broad_belone)}

@admin_app.get('/game/broadList')
def getBroadsList(redis,session):
    """
    广播发送列表
    """
    lang = getLang()
    fields = ('isList','startDate','endDate','broad_belone')
    for field in fields:
        exec("%s = request.GET.get('%s','').strip()"%(field,field))

    selfUid = session['id']

    if isList:
        # 取消以代理管理
        selfUid = '1'
        noticList = get_borad_list(redis,selfUid,lang,broad_belone)
        return json.dumps(noticList)
    else:
        info = {
                'title'                 :       lang.GAME_BROAD_LIST_TXT,
                'tableUrl'              :       BACK_PRE+'/game/broadList?isList=1&broad_belone=%s'%(broad_belone),
                'createUrl'             :       BACK_PRE+'/game/broadcast?broad_belone=%s'%(broad_belone),
                'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
                'back_pre'              :       BACK_PRE,
                'batchDelUrl'           :       BACK_PRE+"/game/broadcast/batch_del",
                'broad_belone'          :       broad_belone,
                'addTitle'              :       lang.GAME_BROAD_CREATE_TXT
        }
        return template('admin_broad_list',PAGE_LIST=PAGE_LIST,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/game/broadcast/batch_del')
def do_delBroadsList(redis,session):
    """
    广播删除
    """
    lang = getLang()
    fields = ('broadIds','broad_belone')
    for field in fields:
        exec('%s = request.forms.get("%s","").strip()'%(field,field))

    if not broadIds:
        return {'code':1,'msg':'参数错误'}

    broadIds = broadIds.split(",")
    log_util.debug('[try do_delBroadsList] broadIds[%s] broad_belone[%s]'%(broadIds,broad_belone))

    for broadId in broadIds:
        try:
            do_deleteBroads(redis,broadId,broad_belone)
        except Exception,e:
            log_util.debug('[try do_delBroadsList] error broadId[%s] reason[%s]'%(broadId,e))
            return {'code':1,'msg':'清楚广播失败.'}

    return {'code':0,'msg':'清除广播成功!','jumpUrl':BACK_PRE+'/game/broadList?broad_belone=%s'%(broad_belone)}

@admin_app.get('/game/SingleGameBroadcast')
def getSingleGameBroadcast(redis,session):
    """
        创建单个游戏广播
    """
    lang = getLang()
    gameId = request.GET.get('gameId','').strip()
    gameName = getGameField(redis,gameId,'name')
    info = {
        'title'                 :       '游戏[%s]广播'%(gameName),
        'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
        'subUrl'                :       BACK_PRE+"/game/SingleGameBroadcast",
        'back_pre'              :       BACK_PRE,
        'defaultGameId'         :       gameId,
    }

    return template('admin_game_single_broad', info=info, lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/game/SingleGameBroadcast')
def do_SingleGameBroadcast(redis,session):
    """
        创建单个游戏广播_逻辑
    """
    lang = getLang()
    curTime = datetime.now()
    selfUid = session['id']
    content = request.forms.get('content','').strip()
    repeatTimes = request.forms.get('repeatTimes','').strip()
    repeatInterval = request.forms.get('repeatInterval','').strip()
    gameId = request.forms.get('gameId', '').strip()
    if not gameId:
        abort(403)
    if not content:
        return {'code':1,'msg':lang.GAME_BROCAST_CON_TXT}

    try:
        repeatTimes = int(repeatTimes)
        if repeatTimes < 0:
            raise ValueError
    except ValueError:
        return {'code':1,'msg':lang.GAME_BROCAST_REPEAT_ERR_TXT}

    try:
        repeatInterval = int(repeatInterval)
        if repeatInterval < 0:
            raise ValueError
    except ValueError:
        return {'code':1,'msg':lang.GAME_BROCAST_SEC_ERR_TXT}
    #检查游戏服务器是否开启
    isServiceRunning = isGameServiceRunning(redis, gameId)
    if not isServiceRunning:
        return {'code':1,'msg':'请先开启游戏服务器'}

    bid = '00'
    if isServiceRunning:
        sendProtocol2GameService(redis, gameId, HEAD_SERVICE_PROTOCOL_AGENT_BROADCAST%(selfUid, content, repeatTimes, repeatInterval,bid))

    return {'code':0,'msg':lang.GAME_BROCAST_SEND_SUCCESS,'jumpUrl':BACK_PRE+'/game/list'}

@admin_app.get('/game/server/list')
def getServerList(redis,session):
    """
    获取server列表
    """
    curTime = datetime.now()

    gameId = request.GET.get('id','').strip()
    if not gameId:
        return

    gameServers = getGameServersById(redis,gameId)
    return json.dumps(gameServers)

@admin_app.post('/game/server/close')
def do_serverClose(redis,session):
    """
        尝试关闭游戏服
    """
    curTime = datetime.now()
    opAccount = session['account']
    gameId    = request.forms.get('gameId','').strip()
    if not gameId:
        return {'code':1,'msg':'游戏ID错误'}

    #print
    log_debug('[%s][server close][info] opreator[%s] action[Close Server]'%(curTime,opAccount))

    try:
        tryCloseServer(redis,gameId)
        if not waitServer(redis,gameId, False):
                raise 'close time out'
        #产品环境都是linux,需要确保该进程已关闭
        # if os.name != 'nt':
        #     subprocess.Popen("ps aux | grep -E 'python -m run_server.+\-n %s' | awk '{print $2}' | xargs kill"%('mahjong'), shell=True)

    except Exception,e:
        log_debug('[%s][server close][error] close error.  reason[%s]'%(curTime,e))
        return {'code':1,'msg':'游戏服务器关闭失败.'}

    #return
    return {'code':0,'msg':'游戏服务器关闭成功','jumpUrl':BACK_PRE+'/game/list'}

@admin_app.get('/game/introSetting')
def get_editDesc(redis,session):
    """
    编辑游戏规则
    生成游戏静态页面
    """
    curTime = datetime.now()
    lang = getLang()
    gameId = request.GET.get('gameId','').strip()

    if not gameId:
        return {'code':1,'msg':'gameId错误.'}

    gameDescTable = GAME2DESC%(gameId)
    gameDesc =  redis.get(gameDescTable)
    gameTable = GAME_TABLE%(gameId)
    gameName = redis.hget(gameTable,'name')

    info = {
          'title'                 :       lang.GAME_EDIT_DESC%(gameName),
          'gameId'                :       gameId,
          'gameDesc'              :       gameDesc if gameDesc else '',
          'backUrl'               :       BACK_PRE+'/game/list',
          'submitUrl'             :       BACK_PRE+'/game/introSetting',
          'back_pre'              :       BACK_PRE,
          'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
          'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
    }

    return template('admin_game_editDesc',info=info,lang=lang,GAME_SETTING_INFO=GAME_SETTING_INFO,RES_VERSION=RES_VERSION)

@admin_app.post('/game/introSetting')
def do_editDesc(redis,session):
    """
    编辑 游戏的文字描述逻辑
    """
    gameId = request.forms.get('gameId','').strip()
    gameDesca = request.forms.get('content','').strip()
    curTime = datetime.now()
    lang=getLang()

    if not gameId:
        return {'code':1,'msg':lang.GAME_ID_ERROR_TXT}

    if not gameDesca:
        return {'code':1,'msg':lang.GAME_INTRO_NOT_EMPTY}

    gameTable = GAME_TABLE%(gameId)
    gameName = redis.hget(gameTable,'name')
    gameDescTable = GAME2DESC%(gameId)
    pipe = redis.pipeline()
    log_debug('[GAME][url:/game/introSetting] gameId[%s] gameDesc[%s]'%(gameId,gameDesca))
    try:
        gameDesc =  pipe.set(gameDescTable,gameDesca)
    except Exception,e:
        log_debug('[%s][GAME][intr][error] editDesc error.  reason[%s]'%(curTime,e))
        return {'code':1,'msg':lang.GAME_INTRO_CREATE_ERROR%(gameName)}

    #生成静态文件模板
    tempAddr = createGameIntroTemp(gameId,gameDesca)
    if not tempAddr:
        log_debug('[%s][GAME][intr][error] gameId[%s] rule create template faile!'%(curTime,gameId))

    pipe.hset(gameTable,'template_url',tempAddr)
    pipe.execute()
    #记录操作日志
    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                    'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['createGameRule']%(gameName)}
    #记录日志
    writeAgentOpLog(redis,session['id'],logInfo)
    return {'code':0,'msg':lang.GAME_INTRO_CREATE_SUCCESS%(gameName),'jumpUrl':BACK_PRE+'/game/list'}

@admin_app.post('/game/setting/defaultGames')
def do_setDefaultGame(redis,session):
    """
    设置默认的游戏设置
    """
    curTime = datetime.now()
    gameIds = request.forms.get('id','').strip()

    log_debug('[try setDefaultGames] gameIds[%s]'%(gameIds))
    if not gameIds:
        return {'code':-1,'msg':'gameIds参数错误.'}

    gameIds = gameIds.split(',')
    defaultIds = redis.smembers(GAME_DEFAULT_BIND)
    pipe = redis.pipeline()
    op_dict = {
        True    :     pipe.srem,
        False   :     pipe.sadd
    }
    try:
        for gameId in gameIds:
            #将默认游戏放入到集合中
            op_dict[gameId in defaultIds](GAME_DEFAULT_BIND,gameId)
    except Exception,e:
        log_debug('[try setDefaultGames] gameIds[%s] bind error. reason[%s]'%(gameIds,e))
        return {'code':-1,'msg':'绑定游戏错误.'}

    pipe.execute()
    return {'code':0,'msg':'设置成功','jumpUrl':BACK_PRE+"/game/list"}
