#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    系统会员模块
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,PLAYER_BASE_SCORE,DEFAULT_BASE_SCORE,RES_VERSION
from common.utilt import *
from common.log import *
from datetime import datetime
from web_db_define import *
from bag.bag_config import bag_redis
from model.agentModel import *
from model.protoclModel import *
from model.userModel import *
from model.orderModel import *
from model.hallModel import tryExitGroup
from common import encrypt_util,convert_util,json_util,web_util
import hashlib
import json

@admin_app.get('/member/list')
@checkLogin
def get_member_list(redis,session):
    """
    获取会员列表接口
    """
    lang    =  getLang()
    curTime =  datetime.now()
    fields = ('isList','startDate','endDate','pageSize','pageNumber','searchId','sort_name','sort_method')
    for field in fields:
        exec("%s = request.GET.get('%s','').strip()"%(field,field))

    # print(isList, startDate, endDate, pageSize, pageNumber, searchId, sort_name, sort_method)
    account = request.forms.get('userName','').strip()
    account = session.get('account')
    agentId = getAgentId(redis, account)
    agentTable = AGENT_TABLE%(agentId)
    aType = redis.hget(agentTable,('type'))
    selfUid  = session['id']
    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)

    if isList:
        # 取消代理管理
        selfUid = '1'
        res = getMemberList(redis,session,selfUid,searchId,lang,pageSize,pageNumber,sort_name,sort_method)
        return json.dumps(res)
    else:
        info = {
                'title'                  :           lang.MEMBER_LIST_TITLE_TXT,
                'listUrl'                :           BACK_PRE+'/member/list?isList=1&pageNumber={}&pageSize={}'.format(pageNumber,pageSize),
                'searchTxt'              :           lang.MEMBER_INPUT_TXT,
                'sort_bar'               :           True,#开启排序
                'member_page'            :           True,#开启排序
                'cur_page'               :           pageNumber,
                'cur_size'               :           pageSize,
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'remove_type'            :           'cards',
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'a_type'                 :            aType
        }

        return template('admin_member_list',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/member/kick')
def do_kickDirectMember(redis,session):
    """
    踢出直属会员
    """
    lang    =  getLang()
    curTime =  datetime.now()
    selfUid  = session['id']
    memberId = request.GET.get('id','').strip()

    userTable = FORMAT_USER_TABLE%(memberId)
    userParent = redis.hget(userTable,'parentAg')
    userParentTable = FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(userParent)
    if not userParent:
        return {'code':1,'msg':'会员编号[%s]的公会不存在.'%(memberId)}
    #print userTable
    pipe = redis.pipeline()
    try:
        pipe.srem(userParentTable, memberId) #上线代理需要获得
        pipe.hset(userTable, 'parentAg', '')
    except Exception,e:
        log_debug('[%s][member][kick][error] agentId[%s] member[%s] kick error,reason[%s]'%(curTime,selfUid,memberId,e))

    pipe.execute()
    #记录操作日志
    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                        'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['uncheckMember']%(memberId)}
    writeAgentOpLog(redis,selfUid,logInfo)

    return {'code':0,'msg':'移除会员[%s]成功'%(memberId),'jumpUrl':BACK_PRE+'/member/list'}

@admin_app.get('/member/changeCard')
@admin_app.get('/member/changeCard/<remove_type>')
def get_changeCard(redis,session,remove_type="cards"):
    """
    增减钻石
    """
    curTime = datetime.now()
    lang    = getLang()
    memberId =  request.GET.get('id','').strip()
    pageNumber = request.GET.get('cur_page','').strip()
    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)

    if not memberId:
        return {'code':'1','msg':'非法操作!'}

    page_title =  '增减会员(%s)钻石'%(memberId)
    parentAg   =   redis.hget(FORMAT_USER_TABLE%(memberId),'parentAg')
    room_card  =   redis.get(USER4AGENT_CARD%(parentAg, memberId))
    back_url   =   BACK_PRE+'/member/list?pageNumber={}'.format(pageNumber)

    parentAg =  redis.hget(FORMAT_USER_TABLE%(memberId),'parentAg')
    memberTable = FORMAT_USER_TABLE%(memberId)
    name,headImgUrl = redis.hmget(memberTable,('nickname','headImgUrl'))

    memberInfo = {
            'title'         :       page_title,
            'backUrl'       :       back_url,
            'agentId'       :       parentAg,
            'memberId'      :       memberId,
            'submitUrl'     :       BACK_PRE+'/member/changeCard/{}/{}'.format(pageNumber,remove_type),
            'roomcard'      :       room_card if room_card else 0 ,
            'name'          :       name,
            'headImgUrl'    :       headImgUrl,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH
    }

    return template('admin_member_changeCard',page=remove_type,info=memberInfo,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/member/changeCard')
@admin_app.post('/member/changeCard/<page:int>/<remove_type>')
@checkLogin
def do_changeCard(redis,session,page=1,remove_type="cards"):
    """
    增减钻石
    page:当前是操作第几页
    """
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d")
    dateTime = curTime.strftime("%Y-%m-%d %H:%M:%S")
    lang    = getLang()
    fields = ('roomcard','agentId','changeCard','memberId', 'changeType', 'note')
    for field in fields:
        exec("%s = request.forms.get('%s','').strip()"%(field,field))

    if not changeType:
        return {'code':1, 'msg': '请选择增减类型'}

    if not changeCard:
        return {'code':1,'msg':'请填写增减钻石数'}

    if isinstance(changeCard, float):
        return {'code':1,'msg':lang.MEMBER_DIOMAN_INPUT_NUM_TXT}

    changeCard   = convert_util.to_int(changeCard)
    roomcard = convert_util.to_int(roomcard)
    jump_url = "/admin/member/list?&pageNumber={}".format(page)
    if changeType == 'add':
        if changeCard <= 0:
            return {'code': 1, 'msg': lang.MEMBER_DIOMAN_LT_TXT}
        try:
            success_msg = lang.MEMBER_COIN_ADD_SUCCESS
            redis.lpush(COMPENSATE_CARD_DAY % date,'%s|%s|%s|%s|%s|%s' % (memberId, agentId, roomcard, changeCard, dateTime, note))
            redis.incrby(USER4AGENT_CARD % (agentId, memberId), changeCard)

            logInfo = {'datetime': curTime.strftime('%Y-%m-%d %H:%M:%S'), 'ip': request.remote_addr, 'desc': lang.AGENT_OP_LOG_TYPE['addRoomCard'] % (memberId, changeCard)}
            writeAgentOpLog(redis, agentId, logInfo)
        except Exception as err:
            log_util.debug('[try do_addCard] add Exception reason[%s]' % (err))
            return {'code': 1, 'msg': '增加失败'}
    else:
        if changeCard > roomcard:
            return {'code':1,'msg':lang.MEMBER_DIOMAN_GT_TXT}
        try:
            success_msg = lang.MEMBER_DIOMAN_REMOVE_SUCCESS
            redis.lpush(COMPENSATE_CARD_DAY % date, '%s|%s|%s|%s|%s|%s' % (memberId, agentId, roomcard, -changeCard, dateTime, note))
            redis.incrby(USER4AGENT_CARD%(agentId, memberId),-changeCard)
            logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'), 'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['removeRoomCard'] % (memberId,changeCard)}
            writeAgentOpLog(redis,agentId,logInfo)
        except Exception as err:
            log_util.debug('[try do_removeCard] remove Exception reason[%s]'%(err))
            return {'code':1,'msg':'移除失败'}

    return {'code':0,'msg':success_msg % (memberId,changeCard),'jumpUrl':jump_url}

@admin_app.get('/member/changeGamepoint')
@admin_app.get('/member/changeGamepoint/<remove_type>')
def get_changeGamepoint(redis,session,remove_type="cards"):
    """
    增减积分
    """
    curTime = datetime.now()
    lang    = getLang()
    memberId =  request.GET.get('id','').strip()
    pageNumber = request.GET.get('cur_page','').strip()
    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)

    if not memberId:
        return {'code':'1','msg':'非法操作!'}

    page_title =  '增减会员(%s)积分'%(memberId)
    gamePoint, parentAg   =   redis.hmget(FORMAT_USER_TABLE % (memberId), ('gamePoint', 'parentAg'))
    back_url   =   BACK_PRE+'/member/list?pageNumber={}'.format(pageNumber)

    parentAg =  redis.hget(FORMAT_USER_TABLE%(memberId),'parentAg')
    memberTable = FORMAT_USER_TABLE%(memberId)
    name,headImgUrl = redis.hmget(memberTable,('nickname','headImgUrl'))

    memberInfo = {
            'title'         :       page_title,
            'backUrl'       :       back_url,
            'agentId'       :       parentAg,
            'memberId'      :       memberId,
            'submitUrl'     :       BACK_PRE+'/member/changeGamepoint/{}/{}'.format(pageNumber,remove_type),
            'gamePoint'      :        gamePoint if gamePoint else 0 ,
            'name'          :       name,
            'headImgUrl'    :       headImgUrl,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH
    }

    return template('admin_member_changeGamepoint',page=remove_type,info=memberInfo,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/member/changeGamepoint')
@admin_app.post('/member/changeGamepoint/<page:int>/<remove_type>')
@checkLogin
def do_changeGamepoint(redis,session,page=1,remove_type="cards"):
    """
    增减积分
    page:当前是操作第几页
    """
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d")
    dateTime = curTime.strftime("%Y-%m-%d %H:%M:%S")
    lang    = getLang()
    fields = ('gamePoint','agentId','changePoint','memberId', 'changeType', 'note')
    for field in fields:
        exec("%s = request.forms.get('%s','').strip()"%(field,field))

    if not changeType:
        return {'code':1, 'msg': '请选择增减类型'}

    if not changePoint:
        return {'code':1,'msg':'请填写增减积分数'}

    if isinstance(changePoint, float):
        return {'code':1,'msg':lang.MEMBER_DIOMAN_INPUT_NUM_TXT}

    changePoint   = convert_util.to_int(changePoint)
    gamePoint = convert_util.to_int(gamePoint)
    jump_url = "/admin/member/list?&pageNumber={}".format(page)
    if changeType == 'add':
        if changePoint <= 0:
            return {'code': 1, 'msg': '积分数不能少于0'}
        try:
            success_msg = '增加会员[%s] %s 积分成功'
            redis.lpush(COMPENSATE_POINT_DAY % date,'%s|%s|%s|%s|%s|%s' % (memberId, agentId, gamePoint, changePoint, dateTime, note))
            redis.hincrby(FORMAT_USER_TABLE % (memberId), 'gamePoint', changePoint)

            logInfo = {'datetime': curTime.strftime('%Y-%m-%d %H:%M:%S'), 'ip': request.remote_addr, 'desc': '向玩家[%s]补充了积分[%s]个' % (memberId, changePoint)}
            writeAgentOpLog(redis, agentId, logInfo)
        except Exception as err:
            print(err)
            log_util.debug('[try do_addGamepoint] add Exception reason[%s]' % (err))
            return {'code': 1, 'msg': '增加失败'}
    else:
        if changePoint > gamePoint:
            return {'code':1,'msg':lang.MEMBER_DIOMAN_GT_TXT}
        try:
            success_msg = '移除会员[%s] %s 积分成功'
            redis.lpush(COMPENSATE_POINT_DAY % date, '%s|%s|%s|%s|%s|%s' % (memberId, agentId, gamePoint, -changePoint, dateTime, note))
            redis.hincrby(FORMAT_USER_TABLE % (memberId), 'gamePoint', -changePoint)
            logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'), 'ip':request.remote_addr,'desc': '从玩家[%s]移除了积分[%s]个' % (memberId, changePoint)}
            writeAgentOpLog(redis,agentId,logInfo)
        except Exception as err:
            log_util.debug('[try do_removeCard] remove Exception reason[%s]'%(err))
            return {'code':1,'msg':'移除失败'}

    return {'code':0,'msg':success_msg % (memberId,changePoint),'jumpUrl':jump_url}

@admin_app.get('/member/removeCard')
@admin_app.get('/member/removeCard/<remove_type>')
def get_removeCard(redis,session,remove_type="cards"):
    """
    移除会员的钻石
    """
    curTime = datetime.now()
    lang    = getLang()
    memberId =  request.GET.get('id','').strip()
    pageNumber = request.GET.get('cur_page','').strip()

    if not memberId:
        return {'code':'1','msg':'非法操作!'}

    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)

    if remove_type == 'cards':
        """ 移除钻石操作 """

        page_title =  '移除会员(%s)钻石'%(memberId)
        parentAg   =   redis.hget(FORMAT_USER_TABLE%(memberId),'parentAg')
        room_card  =   redis.get(USER4AGENT_CARD%(parentAg, memberId))
        back_url   =   BACK_PRE+'/member/list?pageNumber={}'.format(pageNumber)
        nickname, agentId, headImgUrl = redis.hmget(FORMAT_USER_TABLE % memberId, ('nickname', 'parentAg', 'headImgUrl'))
    else:
        """ 移除金币操作 """
        page_title =  '移除会员[%s]金币'%(memberId)
        room_card  =   redis.hget(FORMAT_USER_TABLE%(memberId),'coin')
        room_card  =   convert_util.to_int(room_card)
        back_url   =   BACK_PRE+'/fish/member/list?pageNumber={}'.format(pageNumber)
        nickname, agentId, headImgUrl = redis.hmget(userTable % memberId, ('nickname', 'parentAg', 'headImgUrl'))
    memberInfo = {
            'title'         :       page_title,
            'backUrl'       :       back_url,
            'agentId'       :       parentAg if remove_type=='cards' else '',
            'memberId'      :       memberId,
            'submitUrl'     :       BACK_PRE+'/member/removeCard/{}/{}'.format(pageNumber,remove_type),
            'roomcard'      :       room_card if room_card else 0,
            'memberId'      :       memberId,
            'nickname'      :       nickname,
            'agentId'       :       agentId,
            'headImgUrl'    :       headImgUrl,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH
    }

    return template('admin_member_removeCard',page=remove_type,info=memberInfo,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/member/removeCard')
@admin_app.post('/member/removeCard/<page:int>/<remove_type>')
@checkLogin
def do_removeCard(redis,session,page=1,remove_type="cards"):
    """
    移除会员的钻石接口
    page:当前是操作第几页
    """
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d")
    dateTime = curTime.strftime("%Y-%m-%d %H:%M:%S")
    lang    = getLang()
    fields = ('roomcard','agentId','remove','memberId', 'note')
    for field in fields:
        exec("%s = request.forms.get('%s','').strip()"%(field,field))

    if not remove:
        return {'code':1,'msg':lang.MEMBER_DIOMAN_INPUT_TXT}

    if isinstance(remove,float):
        return {'code':1,'msg':lang.MEMBER_DIOMAN_INPUT_NUM_TXT}

    remove   = convert_util.to_int(remove)
    roomcard = convert_util.to_int(roomcard)
    if remove > roomcard:
        return {'code':1,'msg':lang.MEMBER_DIOMAN_GT_TXT}
    try:
        if remove_type == 'cards':
            jump_url = "/admin/member/list?&pageNumber={}".format(page)
            success_msg = lang.MEMBER_DIOMAN_REMOVE_SUCCESS
            redis.lpush(COMPENSATE_CARD_DAY % date, '%s|%s|%s|%s|%s' % (memberId, agentId, roomcard, -remove, dateTime, note))
            redis.incrby(USER4AGENT_CARD%(agentId, memberId),-remove)
        else:
            jump_url = "/admin/fish/member/list?&pageNumber={}".format(page)
            success_msg = lang.MEMBER_COIN_REMOVE_SUCCESS
            redis.lpush(COMPENSATE_CARD_DAY % date, '%s|%s|%s|%s|%s' % (memberId, agentId, roomcard, -remove, dateTime, note))
            redis.hincrby(FORMAT_USER_TABLE%(memberId),'coin',-remove)

        logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                            'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['removeRoomCard']%(memberId,remove)}
        writeAgentOpLog(redis,agentId,logInfo)
    except Exception,e:
        log_util.debug('[try do_removeCard] remove Exception reason[%s]'%(e))
        return {'code':1,'msg':'移除失败'}

    return {'code':0,'msg':success_msg%(memberId,remove),'jumpUrl':jump_url}

@admin_app.get('/member/addCard')
@admin_app.get('/member/addCard/<remove_type>')
def get_addCard(redis,session,remove_type="cards"):
    """
    增加会员钻石接口
    """
    curTime = datetime.now()
    lang    = getLang()
    memberId =  request.GET.get('id','').strip()
    pageNumber = request.GET.get('cur_page','').strip()
    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)

    if not memberId:
        return {'code':'1','msg':'非法操作!'}

    if remove_type == 'cards':
        """ 增加钻石操作 """

        page_title =  '增加会员(%s)钻石'%(memberId)
        parentAg   =   redis.hget(FORMAT_USER_TABLE%(memberId),'parentAg')
        room_card  =   redis.get(USER4AGENT_CARD%(parentAg, memberId))
        back_url   =   BACK_PRE+'/member/list?pageNumber={}'.format(pageNumber)
    else:

        """ 存金币操作 """
        page_title =  '增加会员[%s]金币'%(memberId)
        room_card  =   redis.hget(FORMAT_USER_TABLE%(memberId),'coin')
        room_card  =   convert_util.to_int(room_card)
        back_url   =   BACK_PRE+'/fish/member/list?pageNumber={}'.format(pageNumber)

    parentAg =  redis.hget(FORMAT_USER_TABLE%(memberId),'parentAg')
    memberTable = FORMAT_USER_TABLE%(memberId)
    name,headImgUrl = redis.hmget(memberTable,('nickname','headImgUrl'))

    memberInfo = {
            'title'         :       page_title,
            'backUrl'       :       back_url,
            'agentId'       :       parentAg,
            'memberId'      :       memberId,
            'submitUrl'     :       BACK_PRE+'/member/addCard/{}/{}'.format(pageNumber,remove_type),
            'roomcard'      :       room_card,
            'name'          :       name,
            'headImgUrl'    :       headImgUrl,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH
    }

    return template('admin_member_addCard',page=remove_type,info=memberInfo,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/member/addCard')
@admin_app.post('/member/addCard/<page:int>/<remove_type>')
def do_addCard(redis,session,page=1,remove_type="cards"):
    """
    增加会员钻石接口
    """
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d")
    dateTime = curTime.strftime("%Y-%m-%d %H:%M:%S")
    lang    = getLang()
    fields = ('roomcard','agentId','add','memberId', 'note')
    for field in fields:
        exec("%s = request.forms.get('%s','').strip()"%(field,field))
    selfUid = session['id']

    if not add:
        return {'code':1,'msg':lang.MEMBER_DIOMAN_INPUT_TXT}

    if isinstance(add,float):
        return {'code':1,'msg':lang.MEMBER_DIOMAN_INPUT_NUM_TXT}

    add      = convert_util.to_int(add)
    roomcard = convert_util.to_int(roomcard)
    if add <= 0 :
        return {'code':1,'msg':lang.MEMBER_DIOMAN_LT_TXT}
    try :
        if remove_type == 'cards':
            jump_url    = "/admin/member/list?&pageNumber={}".format(page)
            #提示成功
            success_msg = lang.MEMBER_DIOMAN_ADD_SUCCESS
            redis.lpush(COMPENSATE_CARD_DAY % date, '%s|%s|%s|%s|%s|%s' % (memberId, agentId, roomcard, add, dateTime, note))
            redis.incrby(USER4AGENT_CARD%(agentId, memberId),add)
        else:
            jump_url = "/admin/fish/member/list?&pageNumber={}".format(page)
            success_msg = lang.MEMBER_COIN_ADD_SUCCESS
            redis.lpush(COMPENSATE_CARD_DAY % date, '%s|%s|%s|%s|%s|%s' % (memberId, agentId, roomcard, add, dateTime, note))
            redis.hincrby(FORMAT_USER_TABLE%(memberId),'coin',add)

        logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                            'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['addRoomCard']%(memberId,add)}
        writeAgentOpLog(redis,agentId,logInfo)
    except Exception,e:
        return {'code':1,'msg':lang.MEMBER_DIOMAN_INPUT_NUM_TXT}


    return {'code':0,'msg':success_msg%(memberId,add),'jumpUrl':jump_url}

@admin_app.get('/member/modify')
@admin_app.get('/member/modify/<modify_type>')
def get_modifyMember(redis,session,modify_type="cards"):
    """
    修改代理下属玩家信息
    """
    curTime = datetime.now()
    lang    = getLang()
    memberId =   request.GET.get('id','').strip()
    pageNumber = request.GET.get('cur_page','').strip()
    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)

    if not memberId:
        return {'code':'1','msg':'非法操作!'}

    memberTable = FORMAT_USER_TABLE%(memberId)
    maxScore,baseScore,headImgUrl,nickname, agentId = redis.hmget(memberTable,('maxScore','baseScore', 'headImgUrl', 'nickname', 'parentAg'))

    if modify_type == 'cards':
        page_title  =    "用户[%s]-信息修改" % (memberId)
        back_url    =    BACK_PRE+'/member/list?pageNumber={}'.format(pageNumber)
    else:
        page_title  =    "捕鱼会员[%s]-信息修改" % (memberId)
        back_url = BACK_PRE+'/fish/member/list?pageNumber={}'.format(pageNumber)
    memberInfo = {
            'title'         :       page_title,
            'backUrl'       :       back_url,
            'memberId'      :       memberId,
            'submitUrl'     :       BACK_PRE+'/member/modify/{}'.format(modify_type),
            'maxScore'      :       maxScore if maxScore else 1,
            'baseScore'     :       baseScore if baseScore else DEFAULT_BASE_SCORE,
            'headImgUrl'    :       headImgUrl,
            'nickname'      :       nickname,
            'agentId'       :       agentId,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH
    }

    return template('admin_member_modify',baseScore=PLAYER_BASE_SCORE,info=memberInfo,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/member/modify')
@admin_app.post('/member/modify/<modify_type>')
@checkLogin
def do_modifyMember(redis,session,modify_type='cards'):
    """
    修改会员信息接口
    """
    curTime = datetime.now()
    lang     = getLang()
    selfUid  = session['id']

    fields = (
                'memberId',
                'maxScore',
                'score1',
                'score2',
                'score3',
                'score4',
                'score5',
                'score6',
                'score7',
                'score8',
                'score9',
                'score10',
                'score11',
                'score12',
                'score13',
                'score14',
                'score15',
                'score16',
                'score17',
                'score18',
                'score19',
                'score20',
                'cur_page'
    )

    for field in fields:
        exec("%s = request.forms.get('%s','').strip()"%(field,field))

    if not cur_page:
        cur_page = 1
    else:
        cur_page = convert_util.to_int(cur_page)

    if not memberId:
        return {'code':1,'msg':'非法修改会员!'}

    base_score_list = []
    score_list = [score1,score2,score3,score4,score5,score6,score7,score8,score9,\
                        score10,score11,score12,score13,score14,score15,score16,score17,score18,score19,score20]

    for score in score_list:
        if score:
            base_score_list.append(score)

    pipe = redis.pipeline()
    memebrTable  =  FORMAT_USER_TABLE%(memberId)
    try:
        pipe.hmset(memebrTable,{'maxScore':max(score_list)})
        pipe.hmset(memebrTable,{'baseScore':base_score_list})
    except Exception,e:
        log_util.debug('[try ModifyMember][error] memberId[%s] modify info error. reason[%s]'%(memberId,e))
        return {'code':1,'msg':'修改会员[%s]信息失败'%(memberId)}

    #记录操作日志
    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                        'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['modifyMember']%(memberId)}
    writeAgentOpLog(redis,selfUid,logInfo)

    if modify_type =='cards':
        """ 修改捕鱼玩家 """
        jump_url = '/admin/member/list?&pageNumber={}'.format(cur_page)
    else:
        jump_url = '/admin/fish/member/list?&pageNumber={}'.format(cur_page)

    pipe.execute()
    return {'code':0,'msg':'修改会员(%s)成功'%(memberId),'jumpUrl':jump_url}

@admin_app.get('/member/change/agent')
@admin_app.get('/member/change/agent/<change_type>')
def get_ChangeMemberAgent(redis, session, change_type='cards'):
    """
    修改代理下玩家的公会
    """
    curTime = datetime.now()
    lang = getLang()
    memberId = request.GET.get('id', '').strip()
    pageNumber = request.GET.get('cur_page', '').strip()
    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)

    if not memberId:
        return {'code': '1', 'msg': '非法操作!'}

    memberTable = FORMAT_USER_TABLE % (memberId)
    headImgUrl, nickname, agentId = redis.hmget(memberTable, ('headImgUrl', 'nickname', 'parentAg'))

    page_title = "用户[%s]-转移公会" % (memberId)
    back_url = BACK_PRE + '/member/list?pageNumber={}'.format(pageNumber)

    memberInfo = {
        'title': page_title,
        'backUrl': back_url,
        'memberId': memberId,
        'submitUrl': BACK_PRE + '/member/change/agent/{}/{}'.format(pageNumber, change_type),
        'headImgUrl': headImgUrl,
        'nickname': nickname,
        'agentId': agentId,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH
    }
    return template('admin_member_change_agent', page=pageNumber, info=memberInfo, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.post('/member/change/agent')
@admin_app.post('/member/change/agent/<page:int>/<change_type>')
@checkLogin
def do_ChangeMemberAgent(redis, session, page=1, change_type='cards'):
    """
    修改代理下玩家的公会
    """
    curTime = datetime.now()
    lang     = getLang()
    selfUid  = session['id']

    memberId = request.forms.get('memberId', '').strip()
    groupId = request.forms.get('changeId', '').strip()

    if not page:
        cur_page = 1
    else:
        cur_page = convert_util.to_int(page)

    if not memberId:
        return {'code':1,'msg':'非法修改会员!'}

    if not groupId:
        return {'code':1, 'msg': '转移公会不能为空'}

    agent_Table = AGENT_TABLE % groupId
    if not redis.exists(agent_Table):
        return {'code':1, 'msg': '该公会不存在'}
    else:
        agent_type, agValid = redis.hmget(agent_Table, ('type', 'valid'))
        if agValid in ['0']:
            return {'code':1, 'msg': '该公会已被冻结'}
        if agent_type in ['0', '1']:
            return {'code': 1, 'msg': '该公会不能直接加入'}

    pipe = redis.pipeline()
    userTable = FORMAT_USER_TABLE % (memberId)
    account = redis.hmget(userTable, ('account'))
    try:
        # 自动退出当前公会
        groupId4old = redis.hget(userTable, 'parentAg')
        adminTable4Old = AGENT_TABLE % (groupId4old)
        if redis.exists(adminTable4Old) and redis.exists(userTable):
            tryExitGroup(redis, userTable, account, memberId, groupId4old)

        # 如果存在,绑定
        redis.hset(FORMAT_USER_TABLE % (memberId), 'parentAg', groupId)
        redis.sadd(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE % (groupId), memberId)
        ag, lastGroup = redis.hmget(userTable, ('parentAg', 'lastGroup'))
        if lastGroup:
            lastParentAg = getTopAgentId(redis,lastGroup)  # 540302  034033
            nowParentAg  = getTopAgentId(redis,ag)  # 875020  227402
            if lastParentAg == nowParentAg:
                defaultCard = redis.get(USER4AGENT_CARD % (lastGroup, memberId))
            else:
                provinceAgId = getTopAgentId(redis, ag)  # 875020  227402
                defaultCard = redis.get(USER4AGENT_CARD % (provinceAgId, memberId))
                if not defaultCard:
                    if lastGroup:
                        defaultCard = redis.get(USER4AGENT_CARD % (ag, memberId))
                        if not defaultCard:
                            defaultCard = 0
                    else:
                        defaultCard = redis.hget(AGENT_TABLE % (provinceAgId), 'defaultRoomCard')
                        if not defaultCard:
                            defaultCard = 0
        else:
            provinceAgId = getTopAgentId(redis, ag)
            defaultCard = redis.get(USER4AGENT_CARD % (provinceAgId, memberId))
            if not defaultCard:
                if lastGroup:
                    defaultCard = redis.get(USER4AGENT_CARD % (ag, memberId))
                    if not defaultCard:
                        defaultCard = 0
                else:
                    defaultCard = redis.hget(AGENT_TABLE % (provinceAgId), 'defaultRoomCard')
                    if not defaultCard:
                        defaultCard = 0

        if not defaultCard:
            defaultCard = 0

        redis.set(USER4AGENT_CARD %(ag, memberId),int(defaultCard))
        redis.hset(userTable,'baseScore','[1]')
    except Exception as err:
        print(err)
        # log_util.debug('[try ChangeMemberAgent][error] memberId[%s] change info error. reason[%s]' % ( memberId,err))
        return {'code':1,'msg':'转移会员公会[%s]失败'%(memberId)}

    #记录操作日志
    # logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'), 'ip':request.remote_addr,'desc': lang.AGENT_OP_LOG_TYPE['rejectMember']%(memberId)}
    # writeAgentOpLog(redis,selfUid,logInfo)

    jump_url = '/admin/member/list?&pageNumber={}'.format(cur_page)
    pipe.execute()
    return {'code':0,'msg':'转移会员公会(%s)成功'%(memberId), 'jumpUrl':jump_url}

@admin_app.get('/member/search')
@admin_app.get('/member/search/<action>')
@checkAccess
def getMemberSearch(redis,session,action="hall"):
    """
    会员查询充卡
    """
    action = action.upper()
    curTime = datetime.now()
    lang    = getLang()
    memberId = request.GET.get('memberId','').strip()

    info = {
                'title'             :               lang.MENU_MEMBER_SEARCH_TXT if action=='HALL' else lang.MENU_MEMBER_SEARCH_COIN_TXT,
                'memberId'          :               memberId,
                'searchUrl'         :               BACK_PRE+'/member/recharge',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_member_search',info=info,message=None,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/member/recharge')
@admin_app.get('/member/recharge/<action>')
@checkLogin
def getMemberRecharge(redis,session,action="hall"):
    """
    会员充卡
    """
    curTime = datetime.now()
    lang    = getLang()
    action = action.upper()
    dateStr = curTime.strftime('%Y-%m-%d')

    selfAccount,selfUid = session['account'],session['id']
    fields = ('memberId',)
    for field in fields:
        exec('%s = request.GET.get("%s","").strip()'%(field,field))

    memberTable = FORMAT_USER_TABLE%(memberId)
    if action == 'HALL':
        memberChildIds = redis.smembers(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%(selfUid))
        if not redis.exists(memberTable) or (memberId not in memberChildIds):
            info = {
                    'title'             :                lang.MENU_MEMBER_SEARCH_TXT,
                    'memberId'          :                memberId,
                    'searchUrl'         :                BACK_PRE+'/member/recharge/{}'.format(action),
                    'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
            }
            log_debug('[%s][roomCard][member recharge] memberId[%s] is not exists.'%(curTime,memberId))
            return template('admin_member_search',info=info,message='会员[%s]不存在'%(memberId),lang=lang,RES_VERSION=RES_VERSION)

        account,name,openID,headImgUrl = redis.hmget(memberTable,('account','nickname','openid','headImgUrl'))
        if not redis.exists(USER4AGENT_CARD%(selfUid,memberId)):
            redis.set(USER4AGENT_CARD%(selfUid,memberId),0)

        roomcard     = redis.get(USER4AGENT_CARD%(selfUid,memberId))
        title = '钻石充值 [当前会员:%s]'%(account)
        back_url = '/admin/member/list'
        submit_utl = '/admin/member/recharge'
        recharge_type = ROOMCARD2TYPE['member.cards']
    else:
        account,name,openID,headImgUrl = redis.hmget(memberTable,('account','nickname','openid','headImgUrl'))
        if not redis.sismember(ACCOUNT4WEIXIN_SET4FISH,account):
            info = {
                    'title'             :                lang.MENU_MEMBER_SEARCH_COIN_TXT,
                    'memberId'          :                memberId,
                    'searchUrl'         :                BACK_PRE+'/member/recharge/{}'.format(action),
                    'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
            }
            return template('admin_member_search',action=action,info=info,message='会员[%s]不存在'%(memberId),lang=lang,RES_VERSION=RES_VERSION)

        roomcard = redis.hget(memberTable,'coin')
        title = '金币充值[当前会员:%s]'%(account)
        back_url = '/admin/fish/member/list'
        submit_utl = '/admin/member/recharge/coin'
        recharge_type = ROOMCARD2TYPE['member.coin']

    token_value  = str(memberId)+str(time.time())
    #生成页面提交token
    submit_token = encrypt_util.to_md5(token_value)
    session['recharge_token'] = submit_token

    info = {
                'title'             :           title,
                'submitUrl'         :           submit_utl,
                'backUrl'           :            back_url,
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'memberId'          :           memberId,
                'account'           :           account,
                'name'              :           name,
                'roomCard'          :           roomcard,
                'headImgUrl'        :           headImgUrl,
                'submit_token'      :           submit_token,
                'rechargeTypes'     :           recharge_type,
                'openId'            :           openID
    }

    return template('admin_member_recharge',action=action,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/member/recharge')
@checkLogin
def do_memberRecharge(redis,session):
    """
    会员充卡逻辑
    """
    curTime  =  datetime.now()
    lang     =  getLang()
    dateStr  =  curTime.strftime('%Y-%m-%d')
    memberId = request.forms.get('memberId', '').strip()
    cardNums = request.forms.get('cardNums', '').strip()
    passwd = request.forms.get('passwd', '').strip()
    token = request.forms.get('token', '').strip()
    selfAccount, selfUid = session['account'], session['id']

    if not memberId or not cardNums or not passwd:
        return {'code': 1, 'msg': '参数不能为空'}

    userTable  = FORMAT_USER_TABLE%(memberId)
    if not redis.exists(userTable):
        return {'field': cardNums, 'msg': '会员不存在'}

    memberChildIds = redis.smembers(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE % (selfUid))
    if not redis.exists(userTable) or (memberId not in memberChildIds):
        return {'code': 1, 'msg': '会员不存在'}

    roomCard2AgentTable = USER4AGENT_CARD%(selfUid,memberId)
    agentTable = AGENT_TABLE%(selfUid)
    roomcard,name,selfPasswd,type,parent_id = redis.hmget(agentTable,('roomcard','name','passwd','type','parentAg'))

    if selfPasswd != encrypt_util.to_sha256(passwd):
        return {'code':1,'msg':'您的密码不正确'}

    pipe  =  redis.pipeline()
    if int(type) not in [0,1]:
        if int(roomcard) < int(cardNums):
            return {'code':4,'msg':lang.CARD_NOT_ENGOUGHT_TXT,'jumpUrl':BACK_PRE+'/order/buy'}
        pipe.hincrby(agentTable,'roomcard',-int(cardNums))

    pipe.incrby(roomCard2AgentTable,cardNums)
    orderNo = getOrderNo(selfUid)
    orderInfo = {
            'orderNo'                :       orderNo,
            'cardNums'               :       cardNums,
            'applyAccount'           :       memberId+"(玩家)",
            'status'                 :       1,
            'apply_date'             :       curTime.strftime('%Y-%m-%d %H:%M:%S'),
            'finish_date'            :       curTime.strftime('%Y-%m-%d %H:%M:%S'),
            'type'                   :       0,
            'note'                   :       '',
            'saleAccount'            :       selfAccount
    }

    cardNums = convert_util.to_int(cardNums)
    if createOrder(redis,orderInfo):
        #创建订单
        pipe.lpush(AGENT_SALE_ORDER_LIST%(selfUid,dateStr),orderNo)
        pipe.lpush(AGENT_SALESUCCESS_ORDER_LIST%(selfUid,dateStr),orderNo)

        if redis.exists(AGENT_SALE_CARD_DATE%(selfUid,dateStr)):
            pipe.hincrby(AGENT_SALE_CARD_DATE%(selfUid,dateStr),'cardNums',cardNums)
            pipe.hincrby(AGENT_SALE_CARD_DATE%(selfUid,dateStr),'totalNums',cardNums)
        else:
            try:
                his_total_nums = redis.get(AGENT_SALE_TOTAL%(selfUid))
                if not his_total_nums:
                    his_total_nums = 0
            except:
                his_total_nums = 0
            pipe.hmset(AGENT_SALE_CARD_DATE%(selfUid,dateStr),{'cardNums':cardNums,'date':dateStr,'totalNums':int(his_total_nums)+cardNums})

        pipe.execute()
        return {'code':0,'msg':'成功向[%s]充值了钻石[%s]张'%(memberId,cardNums),'jumpUrl':BACK_PRE+'/member/search/hall'}

    return {'code':1,'msg':'充值失败'}

@admin_app.post('/member/recharge/coin')
@checkLogin
def do_memberRechargeCoin(redis,session):
    """
    代理给会员充值金币接口
    """
    selfUid = session['id']

    fields = ('memberId','cardNums','passwd','token')
    for field in fields:
        exec('%s = request.forms.get("%s",'').strip()'%(field,field))

    if session.get('recharge_token') == None:
        log_debug('session[%s]'%(session['recharge_token']))
        return {'code':1,'msg':'非法提交订单'}

    if token != session['recharge_token']:
        log_debug('[try do_memberRecharge] token is not match. submit_token[%s] session_token[%s]'%(token,session['recharge_token']))
        return {'code':0,'msg':'不能重复确认订单.','jumpUrl':BACK_PRE+'/member/search'}

    user_table = FORMAT_USER_TABLE%(memberId)
    agent_table = AGENT_TABLE%(selfUid)
    selfPasswd = redis.hget(agent_table,'passwd')

    info  =  {
                'title'             :       '会员金币充值',
                'backUrl'           :       BACK_PRE+'/fish/member/list'
    }

    checkNullFields = [
        {'field':cardNums,'msg':'充值金币数不能为空'},
        {'field':passwd,'msg':'请输入你的密码'}
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    if selfPasswd != encrypt_util.to_sha256(passwd):
        return {'code':1,'msg':'您的密码不正确'}

    pipe = redis.pipeline()
    try:
        cardNums = convert_util.to_int(cardNums)
        pipe.hincrby(user_table,'coin',cardNums)
    except Exception,e:
        log_util.debug('[try do_memberRechargeCoin] ERROR. memberId[%s] reason[%s]'%(memberId,e))
        return {'code':1,'msg':'充值失败'}

    pipe.execute()
    return {'code':0,'msg':'成功向[%s]充值了金币[%s]个'%(memberId,cardNums),'jumpUrl':BACK_PRE+'/member/search/fish'}

@admin_app.get('/member/joinList')
def getMemberApplyList(redis,session):
    """
    获取下线代理申请列表
    """
    curTime = datetime.now()
    lang    = getLang()
    selfAccount,selfUid  =  session['account'],session['id']

    isList = request.GET.get('list','').strip()

    if isList:
        applyLists = getmemberApplyList(redis,selfUid)
        return json.dumps(applyLists)
    else:
        info = {
                    'title'                  :          '玩家申请列表',
                    'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                    'listUrl'                :           BACK_PRE+'/member/joinList?list=1'
        }

        return template('admin_member_apply_list',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/member/join/comfirm')
def do_memberJoinComfirm(redis,session):
    """
    审核会员加入公会
    """
    curTime = datetime.now()
    lang    = getLang()
    selfAccount,selfUid   =   session['account'],session['id']

    memberId  =  request.forms.get('id','').strip()
    if not memberId:
        return {'code':1,'msg':'会员编号[%s]错误'%(memberId)}

    try:
        memberJoinComfirm(redis,selfUid,memberId)
    except Exception,e:
        print '[%s][join Comfirm][error] reason[%s]'%(curTime,e)
        return {'code':1,'msg':'审核会员异常'}

    #记录操作日志
    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                        'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['checkMember']%(memberId)}
    writeAgentOpLog(redis,selfUid,logInfo)
    return {'code':0,'msg':'会员[%s]审核通过.'%(memberId),'jumpUrl':BACK_PRE+'/member/modify?id=%s'%(memberId)}

@admin_app.post('/member/join/reject')
def do_memberJoinReject(redis,session):
    """
    拒绝会员加入公会
    """
    curTime = datetime.now()
    lang = getLang()
    selfAccount,selfUid  =  session['account'],session['id']

    memberId   =   request.forms.get('id','').strip()
    if not memberId:
        return {'code':1,'msg':'会员编号[%s]错误'%(memberId)}

    pipe = redis.pipeline()
    try:
        log_debug('[%s][reject Member][info] agentId[%s] reject memberId[%s]'%(curTime,selfUid,memberId))
        pipe.lrem(JOIN_GROUP_LIST%(selfUid),memberId)
    except Exception,e:
        log_debug('[%s][reject member][error] memberId[%s] reject error. reason[%s]'%(curTime,memberId,e))
        return {'code':1,'msg':'会员[%s]拒绝失败'%(memberId)}

    pipe.execute()
    #记录操作日志
    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                        'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['rejectMember']%(memberId)}
    writeAgentOpLog(redis,selfUid,logInfo)
    return {'code':0,'msg':'会员[%s]已拒绝加入公会'%(memberId),'jumpUrl':BACK_PRE+'/member/joinList'}

@admin_app.get('/member/kicks')
@checkLogin
def do_memberKick(redis,session):
    """
    踢出会员
    """
    account = request.GET.get('account','').strip()

    account2user_table = FORMAT_ACCOUNT2USER_TABLE%(account)
    memberTable = redis.get(account2user_table)
    if not redis.exists(memberTable):
        return {'code':1,'msg':'会员[%s]不存在'%(account)}

    #发送提出玩家协议给服务端
    sendProtocol2AllGameService(redis,HEAD_SERVICE_PROTOCOL_KICK_MEMBER%(account))

    return {'code':0,'msg':'会员(%s)已被踢出游戏!'%(account),'jumpUrl':BACK_PRE+'/agent/member/curOnline'}

@admin_app.get('/member/gm/list')
def getGmsList(redis,session):
    """
    获取gm列表
    """
    lang    =  getLang()
    curTime =  datetime.now()
    #接收的值
    fileds = ('show_list','pageSize','pageNumber','searchId')
    for filed in fileds:#动态定义
        exec("%s = request.GET.get('%s','').strip()"%(filed,filed))

    if show_list:
        res = getGmList(redis,session,searchId,int(pageSize),int(pageNumber))
        return json.dumps(res)
    else:
        info = {
                'title'                  :           'GM玩家列表',
                'listUrl'                :           BACK_PRE+'/member/gm/list?show_list=1',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'searchTxt'              :               '输入玩家编号',
                'cur_page'               :           pageNumber,
                'cur_size'               :           pageSize,
                'removeUrl'              :           BACK_PRE + '/member/gm/kick',
                'addGMUrl'               :           BACK_PRE + '/member/gm/add'
        }

        return template('admin_member_gm_list',PAGE_LIST=PAGE_LIST,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/member/gm/kick')
def do_kickGmMember(redis,session):
    """
    移除会员GM权限接口
    """
    lang    =  getLang()
    curTime =  datetime.now()
    selfUid  = session['id']
    gm_ids = request.GET.get('id','').strip()

    if not gm_ids:
        log_debug('[try do_kickGmMember] gm_ids[%s] is not illegs.'%(gm_ids))
        return {'code':1,'msg':'GM_IDS参数错误.'}

    gm_ids = gm_ids.split(",")
    gm_table = 'GMAccount:set'

    pipe = redis.pipeline()

    for gm_id in gm_ids:
        if not redis.sismember(gm_table,gm_id):
            continue
        pipe.srem(gm_table, gm_id) #上线代理需要获得

    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                        'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['kickGm']%(gm_ids)}
    writeAgentOpLog(redis,selfUid,logInfo)
    pipe.execute()
    return {'code':0,'msg':'移除玩家[%s]GM权限成功'%(gm_ids),'jumpUrl':BACK_PRE+'/member/gm/list'}

@admin_app.get('/member/gm/add')
@checkLogin
def get_addGmMember(redis,session):
    curTime = datetime.now()
    lang    = getLang()
    info = {
                'title'             :               '添加GM权限',
                'addUrl'            :               BACK_PRE+'/member/gm/add',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_member_gm_add',info=info,message=None,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/member/gm/showHis')
@checkLogin
def get_addGmMember(redis,session):
    curTime = datetime.now()
    lang    = getLang()
    userId  = request.GET.get('userId','').strip()
    isList  = request.GET.get('list','').strip()

    if not userId:
        return

    if isList:
        gm_his = get_gm_op_list(redis,userId)
        return json.dumps(gm_his)
    else:
        info = {
                    'title'             :               '玩家[%s]GM历史'%(userId),
                    'addUrl'            :               BACK_PRE+'/member/gm/list',
                    'dataUrl'           :               BACK_PRE+'/member/gm/showHis?list=1&userId=%s'%(userId),
                    'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
        }

        return template('admin_member_gm_his',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/member/gm/add')
@checkLogin
def do_addGmMember(redis,session):
    curTime = datetime.now()
    lang    = getLang()
    memberId = request.forms.get('memberId','').strip()
    memberTable = FORMAT_USER_TABLE%(memberId)
    selfUid = session['id']

    if not redis.exists(memberTable):
        return {'code':1,'msg':'会员[%s]不存在'%(memberId)}

    account = redis.hget(memberTable,'account')

    gmTable = 'GMAccount:set'

    if redis.sismember(gmTable,account):
        return {'code':1,'msg':'会员[%s]已经拥有gm权限'%(memberId)}
    try:
        redis.sadd(gmTable,account) #上线代理需要获得
    except Exception,e:
        log_debug('[%s][member][gm][add][error] gmAccount[%s]  add error,reason[%s]'%(curTime,account,e))
        return {'code':1,'msg':'添加会员[%s] gm权限失败'%(account)}

    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                        'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['addGm']%(account)}
    writeAgentOpLog(redis,selfUid,logInfo)
    return {'code':0,'msg':'给会员[%s]设置gm权限成功'%(memberId),'jumpUrl':BACK_PRE+'/member/gm/list'}

@admin_app.get('/member/freeze')
@admin_app.get('/member/freeze/<action>')
@checkLogin
def do_freezeMember(redis,session,action='hall'):
    """
    冻结玩家操作接口
    """
    action = action.upper()
    curTime = datetime.now()
    lang    = getLang()
    memberId = request.GET.get('id','').strip()
    pageNumber = request.GET.get('cur_page','').strip()
    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)

    freezeDesc = {
            '1'     :     '冻结成功',
            '0'     :     '解冻成功'
    }

    if not memberId:
        return {'code':1,'msg':'memberId请求错误'}


    memberTable = FORMAT_USER_TABLE%(memberId)
    if not redis.exists(memberTable):
        return {'code':1,'msg':'会员[%s]不存在'%(memberId)}

    valid = redis.hget(memberTable,'valid')
    pipe = redis.pipeline()
    if valid == '1':
        pipe.hset(memberTable,'valid','0')
    else:
        pipe.hset(memberTable,'valid','1')

    pipe.execute()

    if action in ['HALL','hall']:
        jump_url = BACK_PRE+'/member/list?pageNumber={}'.format(pageNumber)
    else:
        jump_url = BACK_PRE+'/fish/member/list?pageNumber={}'.format(pageNumber)

    return {'code':0,'msg':'会员[%s] %s'%(memberId,freezeDesc[valid]),'jumpUrl':jump_url}

@admin_app.get('/member/dayUseCard')
def get_member_day_useCard(redis,session):
    """
    玩家每日消耗钻石数统计
    """
    curTime = datetime.now()
    lang = getLang()
    isList = request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate = request.GET.get('endDate','').strip()
    memberId = request.GET.get('searchId','').strip()
    if isList:
        res = getMemberUseCardsByDay(redis,startDate,endDate,memberId)
        return json.dumps(res)
    else:
        info = {
                'title'     :       '玩家每日消耗钻石数',
                'listUrl'                :           BACK_PRE+'/member/dayUseCard?list=1&searchId=0',
                'room_listUrl'           :           BACK_PRE + '/member/dayUseCard/room?list=1&searchId=0',
                'searchTxt'              :           '会员编号',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
                'atype'     :   session.get('type'),
                'searchUrl'             :           BACK_PRE + "/bag/select/userid"
        }

        return template('admin_member_dayuser',PAGE_LIST=PAGE_LIST,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/member/dayUseCard/room')
def get_member_day_useCard_room(redis,session):
    """
    玩家每日消耗钻石房间详情
    """
    curTime = datetime.now()
    lang = getLang()
    isList = request.GET.get('list','').strip()
    roomId = request.GET.get('roomId','').strip()
    date = request.GET.get('date','').strip()
    parentAg = request.GET.get('parentAg','').strip()
    account = request.GET.get('account', '').strip()
    if isList:
        res = []
        player_room_table = PLAYER_PLAY_ROOM % account
        if redis.exists(player_room_table):
            for roomTable in redis.lrange(player_room_table, 0, -1):
                _, his_roomId, _, his_date, _, _ = roomTable.split(':')
                his_date = time.strftime("%Y-%m-%d",time.localtime(int(his_date)/1000))
                if his_date == date and roomId == his_roomId == roomId:
                    info = {}
                    gameid, startTime, ag, descs, player, score, roomSettings, ownner, endTime = redis.hmget(roomTable,('gameid','startTime',
                                                                                                              'ag','descs','player','score',
                                                                                                              'roomSettings','ownner','endTime'))
                    startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(startTime)/1000))
                    endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(endTime) / 1000))
                    gamename = redis.hget(GAME_TABLE % (gameid), 'name')
                    player_conf = {i.split(',')[0]:i.split(',')[-1]  for i in player.split(':')}
                    info['gameid'] = gameid
                    info['gamename'] = gamename
                    info['ownner'] = player_conf.get(ownner)
                    info['startTime'] = startTime
                    info['endTime'] = endTime
                    info['player'] = player_conf
                    info['score'] = score.split(':')
                    info['roomSettings'] = roomSettings.split('|')
                    info['descs'] = descs.split('|')
                    info['ag'] = ag
                    res.append(info)
        data = {'data': res, 'count': len(res)}
        return json.dumps(data)

@admin_app.post('/member/open_auth')
def do_openAuth(redis,session):
    """
    开启玩家的代开房间权限
    """
    curTime = datetime.now()
    lang    = getLang()
    selfAccount,selfUid = session['account'],session['id']
    memberId = request.forms.get('id','').strip()

    login_info_dict = {
            '0'             :       'openMemberAuth',
            '1'             :       'unOpenMemberAuth'
    }

    memberTable = FORMAT_USER_TABLE%(memberId)
    if not redis.exists(memberTable):
        log_debug('[try do_openAuth][error] member[%s] is not exists!'%(memberId))
        return {'code':1,'msg':lang.MEMBER_NOT_EXISTES_TXT%(memberId)}

    open_auth = redis.hget(memberTable,'open_auth')
    if not open_auth:
        open_auth = '0'

    if open_auth == '0':
        redis.hset(memberTable,'open_auth',1)
        #doAgentChange(redis,agentId,'open_auth',1)
    else:
        redis.hset(memberTable,'open_auth',0)

    #记录操作日志
    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                    'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE[login_info_dict[open_auth]]%(memberId)}
    writeAgentOpLog(redis,selfUid,logInfo)
    return {'code':0,'msg':lang.GROUP_CHECK_SETTING_SUCCESS,'jumpUrl':BACK_PRE+'/member/list'}


@admin_app.get('/member/compensate')
def get_compensate(redis,session):
    """
    获取补偿记录
    """
    lang    =  getLang()
    curTime =  datetime.now()

    fields = ('isList', 'startDate', 'endDate')
    for filed in fields:
        exec("%s = request.GET.get('%s','').strip()" % (filed, filed))

    if isList:
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
            compensate_card_table = COMPENSATE_CARD_DAY % dateStr
            if redis.exists(compensate_card_table):
                for compensate in redis.lrange(COMPENSATE_CARD_DAY % dateStr, 0, -1):
                    info = dict(zip(('userId', 'agentId', 'roomcard', 'card', 'dateTime', 'note'), compensate.split('|')))
                    account, nickname = redis.hmget(FORMAT_USER_TABLE % info.get('userId'), ('account', 'nickname'))
                    info['account'] = account
                    info['nickname'] = nickname
                    info['time'] = dateStr
                    info['after_card'] = int(info.get('roomcard')) + int(info.get('card'))
                    res.append(info)
            endDate -= deltaTime
        return {"count": len(res), "data": res}
    else:
        info = {
                'title'                  :           '会员钻石/积分增减记录',
                'listUrl'                :           BACK_PRE+'/member/compensate?isList=1',
                'maillistUrl'            :           BACK_PRE + '/member/compensate/point?isList=1',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH,
        }

        return template('admin_member_compensate_list', info=info, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.get('/member/compensate/point')
def get_compensatePoint(redis,session):
    """
    获取积分增减记录
    """
    lang    =  getLang()
    curTime =  datetime.now()

    fields = ('isList', 'startDate', 'endDate')
    for filed in fields:
        exec("%s = request.GET.get('%s','').strip()" % (filed, filed))

    if isList:
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
            compensate_card_table = COMPENSATE_POINT_DAY % dateStr
            if redis.exists(compensate_card_table):
                for compensate in redis.lrange(compensate_card_table, 0, -1):
                    info = dict(zip(('userId', 'agentId', 'roomcard', 'card', 'dateTime', 'note'), compensate.split('|')))
                    account, nickname = redis.hmget(FORMAT_USER_TABLE % info.get('userId'), ('account', 'nickname'))
                    info['account'] = account
                    info['nickname'] = nickname
                    info['time'] = dateStr
                    info['after_card'] = int(info.get('roomcard')) + int(info.get('card'))
                    res.append(info)
            endDate -= deltaTime
        return {"count": len(res), "data": res}

@admin_app.get('/member/compensate/mail')
def get_compensateMail(redis,session):
    """
    获取邮件补偿记录
    """
    lang    =  getLang()
    curTime =  datetime.now()

    fields = ('isList', 'startDate', 'endDate')
    for filed in fields:
        exec("%s = request.GET.get('%s','').strip()" % (filed, filed))

    if isList:
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
            compensate_card_table = ENCLOSURE_MAIL_DAY % dateStr
            if redis.exists(compensate_card_table):
                for compensate in redis.lrange(compensate_card_table, 0, -1):
                    info = dict(zip(('userId', 'agentId', 'roomcard', 'card', 'dateTime', 'enclosure_type'), compensate.split('|')))
                    account, nickname = redis.hmget(FORMAT_USER_TABLE % info.get('userId'), ('account', 'nickname'))
                    info['account'] = account
                    info['nickname'] = nickname
                    info['time'] = dateStr
                    info['enclosure_type'] = MATCH_AWARDS_NAME_TABLE[info.get('enclosure_type')]
                    info['after_card'] = int(info.get('roomcard')) + int(info.get('card'))
                    res.append(info)
            endDate -= deltaTime
        return {"count": len(res), "data": res}


@admin_app.get('/member/mail/list')
@admin_app.get('/member/mail/list/<remove_type>')
def get_mailList(redis, session, remove_type="cards"):
    """
    用户邮件列表
    """
    curTime = datetime.now()
    lang = getLang()
    userId = request.GET.get('id', '').strip()
    islist = request.GET.get('isList', '').strip()
    notTime = int(time.time()*1000)
    if islist:
        res = []
        mail_list = bag_redis.smembers(USER_EMAIL_SET % userId)
        nickname, account = redis.hmget(FORMAT_USER_TABLE % userId, ('nickname', 'account'))
        for mail in mail_list:
            mail_info = bag_redis.hgetall(EMAIL_HASH % mail)
            if not mail_info:
                bag_redis.srem(USER_EMAIL_SET % userId, mail)
                continue
            read_time, valid_time = mail_info.get('read_time'), mail_info.get('valid_time')
            if valid_time and read_time:
                if int(notTime) - int(read_time) > int(valid_time) * 86400 * 1000:
                    bag_redis.srem(USER_EMAIL_SET % userId, mail)
                    continue
            awards = mail_info.get('awards', '')
            awardStr = ''
            enclosureNum = ''
            if awards:
                bagId, bagNum = awards.split(',')
                bagName = MATCH_AWARDS_TYPE_TABLE[bagId]
                bagName = MATCH_AWARDS_NAME_TABLE[bagName]
                awardStr = '%s' % bagName
                enclosureNum = '%s' % bagNum
            mail_info['awardStr'] = awardStr
            mail_info['enclosureNum'] = enclosureNum
            mail_info['user'] = '%s / %s / %s' % (userId, nickname, account)
            mail_info['eid'] = mail
            if mail_info.get('valid_time'):
                timeStamp = int(read_time) + int(valid_time) * 86400 * 1000
                timeStamp = int(str(timeStamp)[:10])
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                mail_info['valid_time'] = otherStyleTime
            if mail_info.get('read_time'):
                readTimeStamp = time.localtime(int(str(read_time)[:10]))
                read_time = time.strftime("%Y-%m-%d %H:%M:%S", readTimeStamp)
                mail_info['read_time'] = read_time
            if mail_info.get('is_get'):
                award_time = mail_info.get('award_time')
                awardTimeStamp = time.localtime(int(str(award_time)[:10]))
                award_time = time.strftime("%Y-%m-%d %H:%M:%S", awardTimeStamp)
                mail_info['is_get'] = award_time
            else:
                if awardStr:
                    mail_info['is_get'] = '尚未领取'
                else:
                    mail_info['is_get'] = '空'
            res.append(mail_info)
        return json.dumps(res)
    info = {
        'title': '邮件列表',
        'tableUrl': BACK_PRE + '/member/mail/list?isList=1&id=%s' % (userId),
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
    }
    return template('admin_member_mail_list', info=info, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.get('/member/gamePoint')
def get_gamePointList(redis, session):
    """
    查询会员椰云积分
    """
    curTime = datetime.now()
    lang = getLang()
    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    memberId = request.GET.get('searchId', '').strip()
    exchangeType = request.GET.get('exchangeType', '').strip()
    shopMail = request.GET.get('shopMail', '').strip()
    if isList:
        week_date_list = get_week_date_obj(startDate, endDate)
        res = []
        if not memberId:
            for day in week_date_list:
                if shopMail and shopMail == 'cocogc':
                    res.extend(get_shopmail_pointIncome(redis, session, week_date_list, day=day, status=exchangeType))
                if shopMail and shopMail == 'cygse':
                    res.extend(get_shopmail_pointIncome(redis, session, week_date_list, day=day, shopmail='cygse', status=exchangeType))
                if not shopMail:
                    res.extend(get_shopmail_pointIncome(redis, session, week_date_list, day=day, status=exchangeType))
                    res.extend(get_shopmail_pointIncome(redis, session, week_date_list, day=day, shopmail='cygse', status=exchangeType))
            res = sorted(res, key=lambda s: s.get('endTime', '0'), reverse=True)
            data = {'data': res, 'total': len(res)}
            return json.dumps(data)
        else:
            if not redis.exists(FORMAT_USER_TABLE % memberId):
                return json.dumps({'data': res, 'total': len(res)})
            nickname, headImgUrl = redis.hmget(FORMAT_USER_TABLE % memberId, ('nickname', 'headImgUrl'))
            if shopMail and shopMail == 'cocogc':
                res.extend(get_shopmail_pointIncome(redis, session, week_date_list, account=memberId))
            elif shopMail and shopMail == 'cygse':
                res.extend(get_shopmail_pointIncome(redis, session, week_date_list, shopmail='cygse', account=memberId))
            else:
                res.extend(get_shopmail_pointIncome(redis, session, week_date_list, account=memberId))
                res.extend(get_shopmail_pointIncome(redis, session, week_date_list, shopmail='cygse', account=memberId))
            res = sorted(res, key=lambda s: s.get('endTime', '0'), reverse=True)
            data = {'data': res, 'total': len(res), 'name': nickname, 'img': headImgUrl}
            return json.dumps(data)
    else:
        info = {
            'title': lang.MENU_MEMBER_SEARCH_GAMEPOINT_TXT,
            'listUrl': BACK_PRE + '/member/gamePoint?list=1&searchId=0',
            'searchTxt': '会员编号',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'atype': session.get('type'),
            'searchUrl': BACK_PRE + "/bag/select/userid"
        }

        return template('admin_member_gamepoint', info=info, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.get('/member/share')
def get_shareGameList(redis, session):
    """
    查询会员分享获取的积分流水
    """
    curTime = datetime.now()
    lang = getLang()
    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    memberId = request.GET.get('searchId', '').strip()
    if isList:
        res = []
        startDateScore = time.mktime(time.strptime('%s 00:00:00' % startDate, '%Y-%m-%d %H:%M:%S'))
        endDateScore = time.mktime(time.strptime('%s 23:59:59' % endDate, '%Y-%m-%d %H:%M:%S'))
        startDateScore = int(startDateScore) * 1000
        endDateScore = int(endDateScore) * 1000
        if not memberId:
            week_date_lists = get_week_date_obj(startDate, endDate)
            for date in week_date_lists:
                startDateScore = time.mktime(time.strptime('%s 00:00:00' % date, '%Y-%m-%d %H:%M:%S'))
                endDateScore = time.mktime(time.strptime('%s 23:59:59' % date, '%Y-%m-%d %H:%M:%S'))
                startDateScore = int(startDateScore) * 1000
                endDateScore = int(endDateScore) * 1000
                for share_userId in redis.smembers(SHARE_GAME_DATE_ZSET % date):
                    userTable = FORMAT_USER_TABLE % share_userId
                    account, nickname, headImgUrl = redis.hmget(userTable, ('account', 'nickname', 'headImgUrl'))
                    for useStr in redis.zrangebyscore(SHARE_GAME_USER_ZSET % share_userId, startDateScore, endDateScore):
                        info = {}
                        share_roomcard, roomcard, share_agent, timestamp = useStr.split('|')
                        timeStamp = float(str(timestamp)[:10])
                        timeArray = time.localtime(timeStamp)
                        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        info['date'] = otherStyleTime
                        info['userId'] = share_userId
                        info['nickname'] = nickname
                        info['account'] = account
                        info['parentAg'] = share_agent
                        info['share_roomcard'] = share_roomcard
                        info['roomcard'] = roomcard
                        res.append(info)
            res = sorted(res, key=itemgetter('date'), reverse=True)
            return {'data': res, 'count': len(res)}
        else:
            userTable = FORMAT_USER_TABLE % memberId
            if not redis.exists(userTable):
                return {'data': res, 'count': len(res)}
            account, nickname, headImgUrl = redis.hmget(userTable, ('account','nickname', 'headImgUrl'))
            for useStr in redis.zrangebyscore(SHARE_GAME_USER_ZSET % memberId, startDateScore, endDateScore):
                info = {}
                share_roomcard, roomcard, share_agent, timestamp = useStr.split('|')
                timeStamp = float(str(timestamp)[:10])
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                info['date'] = otherStyleTime
                info['userId'] = memberId
                info['nickname'] = nickname
                info['account'] = account
                info['parentAg'] = share_agent
                info['share_roomcard'] = share_roomcard
                info['roomcard'] = roomcard
                res.append(info)
            res = sorted(res, key=itemgetter('date'), reverse=True)
            return {'data': res, 'count': len(res), 'name': nickname, 'headImgUrl': headImgUrl}
    else:
        info = {
            'title': lang.MENU_AGENT_MEMBER_SHARE_TXT,
            'listUrl': BACK_PRE + '/member/share?list=1&searchId=0',
            'searchTxt': '会员编号',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'atype': session.get('type'),
            'searchUrl': BACK_PRE + "/bag/select/userid"
        }

        return template('admin_member_sharegame', info=info, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.get('/member/defaultCard')
def get_defaultCardList(redis, session):
    """
    查询会员领取默认钻石流水
    """
    curTime = datetime.now()
    lang = getLang()
    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    memberId = request.GET.get('searchId', '').strip()
    if isList:
        res = []
        week_date_lists = get_week_date_obj(startDate, endDate)
        for dayTime in week_date_lists:
            defaultCard_set = AGENT_DEFAULTCARD_SET % dayTime
            if redis.exists(defaultCard_set):
                for userInfo in redis.smembers(defaultCard_set):
                    userId, parentAg, provinceAgId, defaultCard, receiveTime = userInfo.split(':')
                    if memberId and memberId != userId:
                        continue
                    nickname, account, headImgUrl = redis.hmget(FORMAT_USER_TABLE % userId, ('nickname', 'account', 'headImgUrl'))
                    info = {}
                    info['userId'] = userId
                    info['nickname'] = nickname
                    info['account'] = account
                    info['parentAg'] = parentAg
                    info['provinceAgId'] = provinceAgId
                    info['defaultCard'] = defaultCard
                    info['receiveTime'] = receiveTime
                    res.append(info)
        if memberId:
            nickname, account, headImgUrl = redis.hmget(FORMAT_USER_TABLE % memberId, ('nickname', 'account', 'headImgUrl'))
        else:
            nickname, headImgUrl = '', ''
        return {'data': res, 'count': len(res), 'name': nickname, 'headImgUrl': headImgUrl}
    else:
        info = {
            'title': lang.MENU_AGENT_MEMBER_DEFAULTCARD_TXT,
            'listUrl': BACK_PRE + '/member/defaultCard?list=1&searchId=0',
            'searchTxt': '会员编号',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'atype': session.get('type'),
            'searchUrl': BACK_PRE + "/bag/select/userid"
        }

        return template('admin_member_defaultCard', info=info, lang=lang, RES_VERSION=RES_VERSION)