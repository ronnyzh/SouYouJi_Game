#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    邮件公告模块
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,PARTY_PLAYER_COUNT
from common.utilt import *
from common.log import *
from datetime import datetime
from model.gameModel import *
from model.agentModel import *
from model.mailModel import *
from model.protoclModel import *
from model.userModel import getAgentAllMemberIds
from common import log_util,convert_util,json_util
import json
import hashlib
import md5

@admin_app.get('/notic/list')
@admin_app.get('/notic/list/<action>')
@checkLogin
def get_notic_list(redis,session,action='HALL'):
    lang = getLang()
    action = action.upper()
    fields = ('startDate','endDate','isList')
    sessionId = session['id']
    for field in fields:
        exec('%s = request.GET.get("%s","").strip()'%(field,field))

    log_util.debug('[get_notic_list] get params startDate[%s] endDate[%s] isList[%s] action[%s]'\
                        %(startDate,endDate,isList,action))
    if isList:
        # 取消代理管理
        sessionId = '1'
        noticList = getNoticsList(redis,session,lang,sessionId,action)
        return json.dumps(noticList,cls=json_util.CJsonEncoder)
    else:
        customerInfo = redis.hgetall('notic:customer:service:hash')
        info = {
                'title'                 :       lang.MENU_NOTIC_LIST_TXT,
                'tableUrl'              :       BACK_PRE+'/notic/list/{}?isList=1'.format(action),
                'createUrl'             :       BACK_PRE+'/notice/create/{}'.format(action),
                'gameInfoUrl'          :        BACK_PRE+'/notice/gameinfo',
                'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
                'back_pre'              :       BACK_PRE,
                'agentId'               :       session['id'],
                'addTitle'              :       lang.GAME_NOTIFY_CREATE_TXT,
                'batchDelUrl'           :       BACK_PRE + '/notice/notice_del',

        }
        return template('admin_notice_list',info=info,lang=lang,RES_VERSION=RES_VERSION, customerInfo=customerInfo)

@admin_app.get('/notice/create')
@admin_app.get('/notice/create/<action>')
def do_createNotice(redis,session,action="HALL"):
    """
        创建新公告
    """
    lang = getLang()
    selfUid = session['id']
    action = action.upper()

    # adminTable = AGENT_TABLE%(selfUid)
    # # adminType  = redis.hget(adminTable,'type')
    info = {
        "title"                 :   '发布公告',
        "submitUrl"             :   BACK_PRE+"/notice/create",
        'STATIC_LAYUI_PATH'     :   STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'     :   STATIC_ADMIN_PATH,
        'back_pre'              :   BACK_PRE,
        'action'                :   action,
        'backUrl'               :   BACK_PRE+"/notic/list/{}".format(action)
    }

    return template('admin_game_notice_create',selfUid=selfUid,MAIL_SETTING_INFO=MAIL_SETTING_INFO,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/notice/create')
@checkLogin
def do_createNotice(redis,session):
    lang = getLang()
    fields = {
            ('title','公告信息标题',''),
            ('validDate','有效日期',''),
            ('messageType','信息类型',''),
            ('content','信息内容',''),
            ('action','后台系统','')
    }

    for field in fields:
        exec('%s = web_util.get_form("%s","%s","%s")'%(field[0],field[0],field[1],field[2]))

    log_util.debug('[try do_createNotice] title[%s] validDate[%s] messageType[%s] content[%s] action[%s]'\
                            %(title,validDate,messageType,content,action))
    try:
        messageInfo = {
                'title'         :       title,
                'validDate'     :       validDate,
                'messageType'   :       messageType,
                'content'       :       content
        }
        createNotice(redis,session['id'],messageInfo,action)
    except Exception,e:
        log_util.debug('[try do_createNotice] ERROR reason[%s]'%(e))
        return {'code':1,'msg':'添加新公告失败'}

    #记录操作日志
    return {'code':0,'msg':lang.GAME_NOTIFY_SEND_SUCCESS_TXT,'jumpUrl':BACK_PRE+'/notic/list/{}'.format(action)}

@admin_app.get('/notice/del')
def getGameNoticeDel(redis,session):
    """
    删除公告消息
    """
    noticId = request.GET.get('id','').strip()
    if not noticId:
        return {'code':1,'msg':'noticId[%s]不存在'%(noticId)}

    noticListTable = FORMAT_GAMEHALL_NOTIC_LIST_TABLE
    noticTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticId)
    if not redis.exists(noticTable):
        return {'code':1,'msg':'noticId[%s]的公告已被删除.'}

    info = {
            'title'         :       lang.GAME_NOTIFY_DEL_TXT,
    }

    pipe = redis.pipeline()
    try:
        pipe.lrem(noticListTable,noticId)
        pipe.delete(noticTable)
    except:
        return {'code':1,'msg':lang.GAME_NOTIFY_DEL_ERR_TXT}

    pipe.execute()
    return {'code':0,'msg':lang.GAME_NOTIFY_DEL_SUCCESS_TXT,'jumpUrl':BACK_PRE+'/notic/list'}

@admin_app.post('/notice/notice_del')
def do_delNoticeList(redis,session):
    """
    系统公告删除
    """
    lang = getLang()
    noticIds = request.forms.get("noticIds","").strip()

    if not noticIds:
        return {'code':1,'msg':'参数错误'}

    noticIds = noticIds.split(",")
    log_util.debug('[try do_delnoticLists] noticIds[%s]'%(noticIds))

    pipe = redis.pipeline()
    for noticId in noticIds:
        try:
            noticListTable = FORMAT_GAMEHALL_NOTIC_LIST_TABLE
            noticTable = FORMAT_GAMEHALL_NOTIC_TABLE % (noticId)
            groupId, status = redis.hmget(noticTable, ('groupId', 'status'))
            if status == '1':
                return {'code': 1, 'msg': '请先对公告进行取消推送再进行删除.'}
            pipe.lrem(noticListTable, noticId)
            pipe.delete(noticTable)
            pipe.lrem(FORMAT_MGR_SEND_MESSAGE_LIST % groupId, noticId)
        except Exception as err:
            log_util.debug('[try do_delnoticLists] error noticId[%s] reason[%s]' % (noticId,e))
            return {'code':1,'msg':'清除公告失败.'}
    pipe.execute()
    return {'code':0,'msg':'清除公告成功!','jumpUrl':BACK_PRE+'/notic/list'}

@admin_app.get('/notice/modify')
@admin_app.get('/notice/modify/<action>')
def get_notice_modify(redis,session,action="HALL"):
    lang=getLang()
    action = action.upper()
    fields = {
            ('noticeId','公告信息ID','')
    }
    for field in fields:
        exec('%s = web_util.get_query("%s","%s","%s")'%(field[0],field[0],field[1],field[2]))

    noticTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticeId)
    if not redis.exists(noticTable):
        log_util.debug('[try get_notice_modify] noticeId[%s] is not exists.'%(noticeId))
        return {'code':'1','msg':'公告消息不存在.'}

    noticInfo = redis.hgetall(noticTable)
    info = {
          'title'                 :      lang.GAME_NOTIFY_MODIFY_TXT,
          'noticeId'              :       noticeId,
          'backUrl'               :       BACK_PRE+'/notic/list/{}'.format(action),
          'submitUrl'             :       BACK_PRE+'/notice/modify/{}'.format(action),
          'back_pre'              :       BACK_PRE,
          'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
          'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
    }

    return template('admin_game_notice_modify',info=info,MSGTYPE2DESC=MSGTYPE2DESC,noticInfo=noticInfo,MAIL_SETTING_INFO=MAIL_SETTING_INFO,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/notice/modify')
@admin_app.post('/notice/modify/<action>')
def do_noticModify(redis,session,action="HALL"):
    lang = getLang()
    action = action.upper()
    fields = {
            ('noticeId','公告信息ID',''),
            ('title','公告信息标题',''),
            ('validDate','有效日期',''),
            ('messageType','信息类型',''),
            ('content','信息内容','')
    }
    for field in fields:
        exec('%s = web_util.get_form("%s","%s","%s")'%(field[0],field[0],field[1],field[2]))

    noticTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticeId)
    pipe  =  redis.pipeline()
    messageInfo = {
            'title'         :       title,
            'validDate'     :       validDate,
            'messageType'   :       DESC2MSGTYPE[messageType.encode('utf-8')],
            'content'       :       content
    }
    log_util.debug('[try do_noticModify] noticeId[%s] messageInfo[%s] action[%s]'%(noticeId,messageInfo,action))
    pipe.hmset(noticTable,messageInfo)

    pipe.execute()
    return {'code':0,'msg':lang.GAME_NOTIFY_MODIFY_SUC_TXT,'jumpUrl':BACK_PRE+'/notic/list/{}'.format(action)}

@admin_app.get('/notice/push')
@admin_app.get('/notice/push/<action>')
def pushNotices(redis,session,action='hall'):
    """
    将消息放进玩家的信息列表
    """
    type2Msg = {'0':'推送','1':'取消推送'}
    action = action.upper()
    timeStr = convert_util.to_dateStr(datetime.now())
    agentId  = session['id']
    noticId = request.GET.get('id','').strip()

    pipe = redis.pipeline()
    #超级管理员发的公告需要塞到所有玩家的信息盒子
    noticeTable = FORMAT_GAMEHALL_NOTIC_TABLE%(noticId)
    senderId = redis.hget(noticeTable,'groupId')
    if not senderId:
        # senderId = 1
        return {"code": 1, "msg": "此公告已失效，请重新创建一个新的公告, 或者联系客服处理。错误代码FX0123。"}

    memberIds = getAgentAllMemberIds(redis,senderId)

    if action == 'HALL':
        user_msg_table_list = FORMAT_USER_MESSAGE_LIST
    else:
        user_msg_table_list = FORMAT_USER_MSG_FISH_LIST

    #推送所有公告
    status = convert_util.to_int(redis.hget(noticeTable,'status'))
    log_util.debug('[try pushNotices] agentId[%s] memberIds[%s] status[%s] action[%s]'%(agentId,memberIds,status,action))
    try:
        if status == 0:
            for memberId in memberIds:
                pipe.hset(FORMAT_GAMEHALL_NOTIC_TABLE%(noticId),'time',timeStr)
                pipe.lpush(user_msg_table_list%(memberId),noticId)
            pipe.hset(noticeTable,'status','1')
        else:
            for memberId in memberIds:
                pipe.lrem(user_msg_table_list%(memberId),noticId)
                pipe.srem(FORMAT_MSG_READ_SET%(noticId),memberId)
            pipe.hset(noticeTable,'status','0')
    except Exception,e:
        log_util.debug('[try pushNotices] ERROR agentId[%s] reason[%s]'%(agentId,e))
        return {'code':1,'msg':type2Msg[str(status)]+'失败.'}

    pipe.execute()
    return {'code':0,'msg':type2Msg[str(status)]+'成功.','jumpUrl':BACK_PRE+'/notic/list/{}'.format(action)}

@admin_app.get('/notice/read')
def getNoticeReadPage(redis,session):
    """
    读取信息
    """
    curTime = datetime.now()
    lang    = getLang()
    msgType = request.GET.get('type','').strip()
    msgId   = request.GET.get('id','').strip()
    agentId = request.GET.get('agentId','').strip()
    memberId = request.GET.get('memberId','').strip()
    action   = request.GET.get('action','').strip()

    #log
    #log_util.debug('[try getNoticeReadPage] msgId[%s] msgType[%s] agentId[%s] action[%s]'%(curTime,msgId,msgType,agentId,action))

    noticeItem = FORMAT_GAMEHALL_NOTIC_TABLE%(msgId)
    if not redis.exists(noticeItem):
        return template('notice_not_exists')

    noticeReads = FORMAT_MSG_READ_SET%(msgId)
    readList = redis.smembers(noticeReads)

    #设置消息为已读
    if memberId not in readList:
        redis.sadd(noticeReads,memberId)

    title,content = redis.hmget(noticeItem,('title','content'))

    if msgType == MAIL_TYPE:
        #setReward2User(msgId,userId)
        deleteMsg(redis,msgId,memberId)

    # log_util.debug('[try getNoticeReadPage] RETURN msgId[%s] title[%s] content[%s] action[%s]'%(curTime,msgId,title,content,action))
    return template('notice_content_page',content=content,title=title)

@admin_app.post('/notice/gameinfo')
def do_noticeGameInfo(redis,session):
    """
    添加系统公告，QQ号/群等信息
    """
    lang = getLang()
    curTime = datetime.now()
    timeStr = curTime.strftime("%Y-%m-%d %H:%M")
    server_WeChat = request.forms.get("server_WeChat", "")
    server_QQ = request.forms.get("server_QQ", "")
    server_Email = request.forms.get("server_Email", "")
    server_phone = request.forms.get("server_phone", "")

    pipe = redis.pipeline()
    try:
        pipe.hmset('notic:customer:service:hash', {
            'wechat': server_WeChat,
            'qq': server_QQ,
            'email': server_Email,
            'phone': server_phone
        })
    except:
        return {'code': 1, 'msg': '设置错误', 'jumpUrl': ''}
    pipe.execute()
    return {'code': 1 , 'msg': '设置成功', 'jumpUrl': ''}

@admin_app.get('/notic/ad')
@checkLogin
def getNoticAdList(redis,session):
    """
    游戏广告
    """
    lang = getLang()
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d %H:%M:%S")

    isList = request.GET.get('isList', '').strip()

    if isList:
        ad_list = redis.smembers(NOTIC_AD_ID_SET)
        res = []
        if ad_list:
            for ad_id in ad_list:
                ad_info = redis.hgetall(NOTIC_AD_TABLE % ad_id)
                ad_info['op'] = [
                    {'url': '/admin/notic/ad/modify', 'method': 'POST', 'txt': '编辑'},
                    {'url': '/admin/notic/ad/delete', 'method': 'POST', 'txt': '删除'}
                ]
                res.append(ad_info)
        return json.dumps(res)
    else:
        info = {
            'title': lang.MENU_NOTIC_AD_TXT,
            'addTitle': '添加广告',
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'tableUrl': BACK_PRE + '/notic/ad?isList=1',
            'createUrl': BACK_PRE + '/notic/ad/create'
        }

    return template('admin_notice_ad_list',message='',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/notic/ad/create')
@checkLogin
def getNoticAdCreate(redis,session):
    """
    创建游戏广告
    """
    lang = getLang()
    timeStamp = str(time.time())

    md5 = hashlib.md5()
    if not isinstance(timeStamp, bytes):
        timeStamp = str(timeStamp).encode('utf-8')
    page_token = md5.update(timeStamp)

    info = {
            'title'             :       '添加广告',
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'back_pre'          :       BACK_PRE,
            'backUrl'           :       BACK_PRE+'/notic/ad',
            'submitUrl'         :       BACK_PRE+'/notic/ad/create',
            'upload_url'        :       BACK_PRE+'/notic/ad/upload',
            'token'             :       page_token

    }
    return template('admin_notice_ad_create',message='',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/notic/ad/create')
def do_reward_create(redis,session):
    """
    创建捕鱼兑换奖品视图
    """
    lang = getLang()
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d %H:%M:%S")

    title = request.forms.get('title', '').strip()
    order = request.forms.get('order', '').strip()
    note = request.forms.get('note', '').strip()
    img_path = request.forms.get('img_path', '').strip()

    if not title :
        return {'code': 1, 'msg': '请填写广告名称'}

    if not img_path:
        return {'code': 1, 'msg': '请上传图片'}

    if not order:
        order = 999

    ad_id = redis.incr(NOTIC_AD_ID_COUNT)
    ad_info = {
        'ad_id': ad_id,
        'title': title,
        'order': order,
        'img_path': img_path[14:],
        'note': note,
        'create_time': date
    }

    try:
        pipe = redis.pipeline()
        pipe.sadd(NOTIC_AD_ID_SET, ad_id)
        pipe.hmset(NOTIC_AD_TABLE % ad_id, ad_info)
        pipe.execute()
    except Exception,e:
        return {'code':1,'msg': '创建广告失败'}

    return {'code':0,'msg':'创建广告[ %s ]成功！' % (title),'jumpUrl': BACK_PRE + '/notic/ad'}

@admin_app.get('/notic/ad/modify')
@checkLogin
def getNoticAdCreate(redis,session):
    """
    创建游戏广告
    """
    lang = getLang()
    timeStamp = str(time.time())
    ad_id = request.GET.get('adId', '').strip()

    md5 = hashlib.md5()
    if not isinstance(timeStamp, bytes):
        timeStamp = str(timeStamp).encode('utf-8')
    page_token = md5.update(timeStamp)

    ad_info = redis.hgetall(NOTIC_AD_TABLE % ad_id)
    info = {
            'title'             :       '编辑[ %s ]广告' % ad_id,
            'STATIC_LAYUI_PATH' :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH' :       STATIC_ADMIN_PATH,
            'back_pre'          :       BACK_PRE,
            'backUrl'           :       BACK_PRE+'/notic/ad',
            'submitUrl'         :       BACK_PRE+'/notic/ad/modify',
            'upload_url'        :       BACK_PRE+'/notic/ad/upload',
            'token'             :       page_token,

    }
    return template('admin_notice_ad_modify',message='',info=info,ad_info=ad_info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/notic/ad/modify')
def do_reward_modify(redis,session):
    """
    创建捕鱼兑换奖品视图
    """
    lang = getLang()
    curTime = datetime.now()

    ad_id = request.forms.get('adId', '').strip()
    title = request.forms.get('title', '').strip()
    order = request.forms.get('order', '').strip()
    note = request.forms.get('note', '').strip()
    img_path = request.forms.get('img_path', '').strip()

    if not title :
        return {'code': 1, 'msg': '请填写广告名称'}

    if not order:
        order = 999

    ad_info = {
        'ad_id': ad_id,
        'title': title,
        'order': order,
        'note': note,
    }

    if img_path:
        ad_info['img_path'] = img_path[14:]

    try:
        pipe = redis.pipeline()
        pipe.hmset(NOTIC_AD_TABLE % ad_id, ad_info)
        pipe.execute()
    except Exception,e:
        return {'code':1,'msg': '编辑广告失败'}

    return {'code':0,'msg':'编辑广告[ %s ]成功！' % (title),'jumpUrl': BACK_PRE + '/notic/ad'}

@admin_app.post('/notic/ad/upload')
def do_file_upload(redis,session):
    '''
    奖品图片上传接口
    @params:
    '''
    files = request.files.get('files')
    try:
        file_name,file_ext = files.filename.split('.')
    except:
        return json.dumps({'error':'文件名称不符合规范 ，请不要包含特殊字符!'})
    #文件新名称
    new_file_name = file_name + md5.new(str(file_name)+str(time.time())).hexdigest()+"."+file_ext
    #文件上传路劲
    file_save_path = NOTIC_AD_UPLOAD_PATH+"/"+new_file_name

    if not os.path.exists(NOTIC_AD_UPLOAD_PATH):
        os.mkdir(NOTIC_AD_UPLOAD_PATH, 0755)
    files.save(file_save_path)
    return json.dumps({'path':file_save_path})


@admin_app.post('/notic/ad/delete')
def do_NoticeAdDelete(redis,session):
    '''
    删除广告
    @params:
    '''
    ad_id = request.forms.get('id', '').strip()
    if not ad_id:
        return {'code': 1, 'msg': '参数错误'}

    ad_table = NOTIC_AD_TABLE % ad_id
    if not redis.exists(ad_table):
        return {'code': 1, 'msg': '该广告不存在'}

    pipe = redis.pipeline()
    pipe.srem(NOTIC_AD_ID_SET, ad_id)
    pipe.delete(NOTIC_AD_TABLE)
    pipe.execute()

    return {'code': 0, 'msg': '删除广告成功', 'jumpUrl': ''}