#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    活动设置模块
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION,ACTIVICE_TYPE_LIST,ACTIVICE_RESOURCE_TYPE_LIST
from common.utilt import *
from common.log import *
from datetime import datetime
from web_db_define import *
from model.activeModel import *
from access_module import *
import hashlib
import json
import traceback
import copy
import admin_activice_check
#
# 页面输出
#


@admin_app.get('/activice/index')
def getActiviceIndex(redis,session):
    """
    活动设置
    """
    lang = getLang()
    # 输出可选配置类型列表
    setting = {
        "typeList" : ACTIVICE_TYPE_LIST,
        "gameList" : getGamesList(redis)
    }


    # 权限
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/activice/resource_add'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'

    # 是否拥有限定工会的权限
    agentListUrl = BACK_PRE + '/activice/create/agentList'
    isAdmin = True if agentListUrl in redis.smembers(AGENT2ACCESS % (agentId)) else False
    # log_debug("************session id is {0}-{1}-{2}".format(agentId,isAdmin,redis.smembers(AGENT2ACCESS % (agentId))))

    info = {
        "title"                 :   lang.MENU_ACTIVICE_SETTING,
        "submitUrl"             :   BACK_PRE+"/activice/create",
        'STATIC_LAYUI_PATH'     :   STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'     :   STATIC_ADMIN_PATH,
        'back_pre'              :   BACK_PRE,
        'backUrl'               :   BACK_PRE+"/activice/list",
        'showPlus'              :   "false",
        'createAccess'          :   createAg,
        'searchTxt'             :   '奖品id',
        'listUrl'               :   BACK_PRE+"/activice/reward/list?list=1",
        'resourceUrl'           :   BACK_PRE+"/activice/resource?list=1",
        'isAdmin'               :   isAdmin,
        'agentListUrl'          :   BACK_PRE+'/activice/agentlist'
    }


    return template('admin_activice_create',info=info, setting= setting,lang=lang,RES_VERSION=RES_VERSION)


@admin_app.post('/activice/create')
def doActiviceCreate(redis,session):
    """
        新建活动
    """
    log_debug("*************************  request.json {0}".format(request.json))

    title = request.json.get('title','')
    ac_template = request.json.get('type','')
    mission_list = request.json.get('missionList','')
    reward_list = request.json.get('rewardList','')
    startdate = request.json.get('startdate','')
    enddate = request.json.get('enddate', '')

    checkNullFields = [
            {'field':title,'msg':'请输入你的活动标题'},
            {'field': startdate, 'msg': '请输入活动开始时间'},
            {'field': enddate, 'msg': '请输入活动结束时间'},
            {'field':ac_template,'msg':'请输入你的活动类型'},
            {'field': mission_list, 'msg': '请添加你的任务列表'},
            {'field': reward_list, 'msg': '请添加你的奖品列表'},
    ]
    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    try:
        createActivice(redis, session['id'], copy.deepcopy(request.json))
    except Exception, ex:
        log_debug('error:{0}'.format(ex))
        return {'code': 1, 'msg': '添加新活动失败'}
    return {'code': 0, 'msg': '新增活动成功.', 'jumpUrl': BACK_PRE + '/activice/list'}


@admin_app.get('/activice/list')
@checkLogin
def getActiviceList(redis, session):
    """
    活动列表
    """
    lang = getLang()
    isList  = request.GET.get('list','').strip()
    if isList:
        noticList = getActivicesList(redis,session,lang,session['id'])
        return json.dumps(noticList)
    else:
        info = {
                'title'                 :       lang.MENU_ACTIVICE_LIST,
                'tableUrl'              :       BACK_PRE+'/activice/list?list=1',
                'createUrl'             :       BACK_PRE+'/activice/index',
                'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
                'back_pre'              :       BACK_PRE,
                'addTitle'              :       lang.ACTIVICE_CREATE_TXT
        }
        return template('admin_activice_list',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/activice/read')
@checkLogin
def getActiviceList(redis, session):
    """
    查看活动
    """
    lang = getLang()
    acid  = request.GET.get('id','').strip()
    noticList = getActivicesList(redis, session, lang, session['id'])
    for item in noticList['data']:
        if item.get('id') == acid:
            data = item

    log_debug('test********************************{0}'.format(data))

    agentId = session['id']
    confirmUrl = BACK_PRE+'/activice/confirm'

    isConfirm = True if \
        int(session['id']) == systemId \
        and not confirmUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)) \
        and str(data['status']) in [STATUS_NON_CHECKED,STATUS_CHECKING,STATUS_FAIL]\
        else False
    log_debug(
        "----isComfirm: {0},\r\n----base:{1}----and:{2}in{3}".format(
            isConfirm,
            AGENT2ACCESSBAN % (agentId),
            str(data['status']),
            [STATUS_NON_CHECKED,STATUS_CHECKING,STATUS_FAIL]
        )
    )

    # 是否拥有限定工会的权限
    agentListUrl = BACK_PRE + '/activice/create/agentList'
    isAdmin = True if agentListUrl in redis.smembers(AGENT2ACCESS % (agentId)) else False;
    # log_debug("************session id is {0}-{1}-{2}".format(agentId,isAdmin,redis.smembers(AGENT2ACCESS % (agentId))))

    setting = {
        "data"      : data,
        "dataString": json.dumps(data),
        "typeList"  : ACTIVICE_TYPE_LIST,
        "gameList"  : getGamesList(redis),
        "isConfirm" : isConfirm,
        "readOnly"  : True
    }
    info = {
            'title'                 :       lang.ACTIVICE_CONFIRM_TXT if isConfirm else lang.ACTIVICE_READ_TXT,
            'tableUrl'              :       BACK_PRE+'/activice/list?list=1',
            'createUrl'             :       BACK_PRE+'/activice/index',
            'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
            'back_pre'              :       BACK_PRE,
            'backUrl'               :       BACK_PRE + '/activice/list',
            'submitText'            :       '通过',
            'submitUrl'             :       BACK_PRE+'/activice/confirm?result=1&id=%s' % acid,
            'refuseText'            :       '不通过',
            'refuseUrl'             :       BACK_PRE+'/activice/confirm?result=0&id=%s' % acid,
            'searchTxt'             :       '奖品id',
            'showPlus'              :       'false',
            'listUrl'               :       BACK_PRE + "/activice/reward/list?list=1&accessId=%s" % data['agentid'],
            'addTitle'              :       lang.ACTIVICE_CREATE_TXT,
            'isAdmin'               :       isAdmin,
            'agentListUrl'          :       BACK_PRE + '/activice/agentlist'

    }
    return template('admin_activice_create',info=info,setting = setting,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/activice/modify')
@checkLogin
def getActiviceList(redis, session):
    """
    修改活动
    """
    # return redirect(BACK_PRE+'/activice/confirm?result=1&id=%s' % request.GET.get('id', '').strip())
    lang = getLang()
    acid  = request.GET.get('id','').strip()
    noticList = getActivicesList(redis, session, lang, session['id'])
    for item in noticList['data']:
        if item.get('id') == acid:
            data = item

    agentId = session['id']
    confirmUrl = BACK_PRE+'/activice/confirm'

    # 是否拥有限定工会的权限
    agentListUrl = BACK_PRE + '/activice/create/agentList'
    isAdmin = True if agentListUrl in redis.smembers(AGENT2ACCESS % (agentId)) else False;

    setting = {
        "data"      : data,
        "dataString": json.dumps(data),
        "typeList"  : ACTIVICE_TYPE_LIST,
        "gameList"  : getGamesList(redis),
        "isConfirm" : False,
        "readOnly"  : False
    }
    info = {
            'title'                 :       lang.ACTIVICE_MODIFY,
            'tableUrl'              :       BACK_PRE+'/activice/list?list=1',
            'createUrl'             :       BACK_PRE+'/activice/index',
            'STATIC_LAYUI_PATH'     :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'     :       STATIC_ADMIN_PATH,
            'back_pre'              :       BACK_PRE,
            'backUrl'               :       BACK_PRE + '/activice/list',
            'submitText'            :       '修改',
            'submitUrl'             :       BACK_PRE+'/activice/modify?id=%s' % acid,
            'searchTxt'             :       '奖品id',
            'showPlus'              :       'false',
            'listUrl'               :       BACK_PRE + "/activice/reward/list?list=1&accessId=%s" % data['agentid'],
            'addTitle'              :       lang.ACTIVICE_CREATE_TXT,
            'isAdmin'               :       isAdmin,
            'agentListUrl'          :       BACK_PRE + '/activice/agentlist'
    }
    return template('admin_activice_create',info=info,setting = setting,lang=lang,RES_VERSION=RES_VERSION)


@admin_app.post('/activice/modify')
@checkLogin
def getActiviceList(redis, session):
    ''' 修改活动  '''
    fail = {'code': 1, 'msg': '修改活动失败.', 'jumpUrl': BACK_PRE + '/activice/list'}
    success = {'code': 0, 'msg': '修改活动成功.', 'jumpUrl': BACK_PRE + '/activice/list'}
    isEdit = request.GET.get('id','').strip()
    if isEdit:
        try:
            acid = isEdit
            info = request.json.copy()
            log_debug('55555555555555555****************5555555555555555555555 {0}'.format(info))
            editActivice(redis,session['id'],acid,info)

            if int(session['id']) != systemId:
                setActiviceStatus(redis, acid, STATUS_NON_CHECKED)

        except Exception, ex:
            traceback.print_exc()
            return fail
        return success


@admin_app.get('/activice/del')
@checkLogin
def getActiviceList(redis, session):
    ''' 删除活动 '''
    fail = {'code': 1, 'msg': '删除活动失败.', 'jumpUrl': BACK_PRE + '/activice/list'}
    success = {'code': 0, 'msg': '删除活动成功.', 'jumpUrl': BACK_PRE + '/activice/list'}
    tableid = request.GET.get('id', '').strip()
    if not tableid:
        return fail
    try:
        delActivice(redis,session['id'],tableid)
    except Exception,ex:
        traceback.print_exc()
        return fail
    return success

# --------------------------------  奖品相关 -----------------------------------------------------


@admin_app.get('/activice/reward/list')
def ActiviceRewardList(redis, session):
    """
    活动奖品管理页面+ 奖品列表搜索
    """
    lang = getLang()

    isList = request.GET.get('list', '').strip()
    agentId = request.GET.get('accessId', '').strip()
    searchId = request.GET.get('searchId', '').strip()
    if not agentId:
        agentId = session['id']

    if isList:
        res = get_rewardList(redis, session, agentId, searchId, lang)
        return json.dumps(res)

    # 权限
    creatAgUrl = BACK_PRE + '/activice/resource_add'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'


    info = {
        'title'             :       lang.ACTIVICE_REWARD_LIST_INDEX,
        'STATIC_LAYUI_PATH' :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH' :       STATIC_ADMIN_PATH,
        'showPlus'          :       "false",
        'createAccess'      :       createAg,
        'searchTxt'         :       '奖品id',
        'back_pre'          :       BACK_PRE,
        'backUrl'           :       BACK_PRE + '/activice/reward/list',
        'createUrl'         :       BACK_PRE + '/activice/reward/add',
        'listUrl'           :       BACK_PRE + '/activice/reward/list?list=1',
    }
    return template("admin_activice_reward_list",info = info, lang = lang,RES_VERSION=RES_VERSION  )


@admin_app.get('/activice/reward/add')
def do_activiceRewardAdd(redis,session):
    """
    新增奖品
    """
    lang = getLang()
    agentId = request.GET.get('accessId', '').strip()
    if not agentId:
        agentId = session['id']
    # 权限
    creatAgUrl = BACK_PRE + '/activice/reward/add'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'

    setting = {
        'typeList': ACTIVICE_RESOURCE_TYPE_LIST
    }
    info = {
        'title': lang.ACTIVICE_REWARD_LIST_ADD,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'showPlus': "false",
        'createAccess': createAg,
        'searchTxt': '奖品id',
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + '/activice/reward/list',
        'submitUrl': BACK_PRE + '/activice/reward/add',
        'imgListUrl': BACK_PRE + '/activice/resource?list=1',
        'listUrl': BACK_PRE + '/activice/reward/list?list=1&searchType=normal',
    }
    return template("admin_activice_reward_create", info=info,setting = setting, lang=lang, RES_VERSION=RES_VERSION)


def reward_check_before_au():
    """
        奖品添加或修改需要检查输入
    """
    imgid = request.json.get('imgId', '').strip()
    reward_type = request.json.get('type', '').strip()
    reward_count = request.json.get('baseRewardCount','').strip()
    pricetotal = request.json.get('priceTotal', '').strip()
    singledatas = request.json.get('singleData', '')
    check_null_fields = [
        {'field': imgid, 'msg':'请添加奖品图片'},
        {'field': reward_type, 'msg': '请选择奖品属性'},
        {'field': pricetotal, 'msg': '请输入奖品总价值'},
        {'field': reward_count, 'msg': '请输入奖品发放数量'},
    ]
    for check in check_null_fields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}
    # 礼包
    if reward_type == 'pack' and not singledatas:
        return {'code': 1, 'msg': '请配置礼包内奖品'}
    return {'code': 0}


@admin_app.post('/activice/reward/add')
@checkLogin
def do_activiceRewardAdd(redis,session):
    """
    新增奖品
    """
    # log_debug("*************************  request.json {0}".format(request.json))
    lang = getLang()
    fail = {'code': 1, 'msg': lang.ACTIVICE_REWARD_LIST_ADD_FAIL, 'jumpUrl': BACK_PRE + '/activice/reward/add'}
    success = {'code': 0, 'msg': lang.ACTIVICE_REWARD_LIST_ADD_SUCCESS,'jumpUrl': BACK_PRE + '/activice/reward/list'}

    is_create = request.json.get('title', '').strip()
    result = reward_check_before_au()
    if result['code'] != 0:
        return result
    if is_create:
        info = request.json.copy()
        try:
            addReward(redis,session['id'],info)
            return success
        except Exception,ex:
            traceback.print_exc()
    return fail


@admin_app.get('/activice/reward/edit')
def do_activiceRewardEdit(redis,session):
    """
    修改奖品
    """
    curTime = datetime.now()
    lang = getLang()
    id = request.GET.get("id","")
    if not id :
        return redirect(BACK_PRE + '/activice/reward/list')
    agentId = session['id']

    searchId = id
    res = get_rewardList2(redis,agentId,searchId,lang)
    if not res or res.get("code") != 0 :
        return redirect(BACK_PRE + '/activice/reward/list')
    log_debug("-----------获取奖品信息:{0}".format(res))

    setting = {
        'typeList': ACTIVICE_RESOURCE_TYPE_LIST,
        "data" : res.get("data")[0],
        "dataString": json.dumps(res.get("data")[0]),
        "readOnly" : False
    }
    info = {
            'title': lang.ACTIVICE_REWARD_LIST_EDIT,
            'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
            'showPlus': "false",
            'searchTxt': '奖品id',
            'back_pre': BACK_PRE,
            'backUrl': BACK_PRE + '/activice/reward/list',
            'submitUrl': BACK_PRE + '/activice/reward/edit?id=%s' % id,
            'imgListUrl': BACK_PRE + '/activice/resource?list=1',
            'listUrl': BACK_PRE + '/activice/reward/list?list=1&searchType=normal',
        }
    return template('admin_activice_reward_create',info=info,setting = setting, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.post('/activice/reward/edit')
def do_activiceRewardEdit(redis,session):
    """
    修改奖品
    """
    # log_debug("*************************  request.json {0}".format(request.json))
    fail = {'code': 1, 'msg': '修改奖品失败.', 'jumpUrl': BACK_PRE + '/activice/reward/list'}
    success = {'code': 0, 'msg': '修改奖品成功.', 'jumpUrl': BACK_PRE + '/activice/reward/list'}
    isedit = request.GET.get('id', '').strip()
    result = reward_check_before_au()
    if result['code'] != 0:
        return result
    if isedit:
        try:
            # 如果活动列表中使用了奖品，则该奖品不应该被修改和删除
            if isRewardInActiveList(redis, session['id'], isedit):
                return {'code': 1, 'msg': '奖品已经被加到活动中'}
            info = request.json.copy()
            editReward(redis,session['id'],isedit,info)
        except:
            traceback.print_exc()
            return fail
        return success
    return fail


@admin_app.get('/activice/reward/del')
def do_activiceRewardDel(redis,session):
    """
    删除奖品
    """
    fail = {'code': 1, 'msg': '删除奖品失败.', 'jumpUrl': BACK_PRE + '/activice/reward/list'}
    success = {'code': 0, 'msg': '删除奖品成功.', 'jumpUrl': BACK_PRE + '/activice/reward/list'}
    tableid = request.GET.get('id', '').strip()
    if not tableid:
        return fail
    try:
        # 如果活动列表中使用了奖品，则该奖品不应该被修改和删除
        if isRewardInActiveList(redis, session['id'], tableid):
            return fail
        delReward(redis,session['id'],tableid)
    except Exception, ex:
        traceback.print_exc()
        return fail
    return success


#------------------------------------------------  资源相关 ---------------------------------------


@admin_app.get('/activice/resource')
def getResourceList(redis, session):
    """
    资源列表
    """
    lang = getLang()

    isList = request.GET.get('list', '').strip()
    agentId = request.GET.get('id', '').strip()
    searchId = request.GET.get('searchId', '').strip()

    log_debug("资源列表的isList = %s \r\n" % (str(isList)) )

    if not agentId:
        agentId = session['id']

    if isList :
        res = get_resourceList(redis,session,searchId,lang)
        return json.dumps(res)


    # 权限
    creatAgUrl = BACK_PRE + '/activice/resource_add'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN%(agentId)):
        createAg = '0'
    else:
        createAg = '1'

    info = {
        'title'             : lang.MENU_RESOURCE_LIST,
        'STATIC_LAYUI_PATH' : STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH' : STATIC_ADMIN_PATH,
        'showPlus'          :'false',
        'createAccess'      : createAg,
        'searchTxt'         : '资源名称',
        'createUrl'         : BACK_PRE + '/activice/resource_add',
        'listUrl'           : BACK_PRE + '/activice/resource?list=1',
        'back_pre'          : BACK_PRE,
        'backUrl'           : BACK_PRE + '/activice/resource',
    }
    return template("admin_resource_list",info = info, lang = lang,RES_VERSION=RES_VERSION )


@admin_app.get('/activice/resource_add')
def do_ResourceAdd(redis, session):
    """
    新增资源页面
    """
    lang = getLang()
    info = {
        'title': lang.RESOURCE_ADD_TEXT,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'submitUrl': BACK_PRE + '/activice/resource_add',
        'listUrl': BACK_PRE + '/activice/resource?list=1',
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + '/activice/resource',
    }
    return template("resource_create", info=info, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.post('/activice/resource_add')
def do_ResourceAdd(redis, session):
    """
    新增资源接口
    """
    lang = getLang()
    title = request.forms.get('title', '').strip()
    note = request.forms.get('note', '').strip()
    upload = request.files.get('file')
    try:
        if upload.content_type not in RESOURCE_ALLOW_TYPES:
            return redirect(BACK_PRE+'/activice/resource_add')
        messageInfo = {
            'title': title,
            'note': note,
        }
        addResource(redis, session['id'], messageInfo,upload)
    except Exception, ex:
        log_debug('error:{0}'.format(ex))
        return redirect(BACK_PRE+'/activice/resource_add')
    return redirect(BACK_PRE+'/activice/resource')


@admin_app.get('/activice/resource_del')
def do_ResourceDel(redis, session):
    """
    删除资源页面
    """
    tableid = request.GET.get('id', '').strip()
    if not tableid:
        return {'code': 1, 'msg': '删除资源失败.', 'jumpUrl': BACK_PRE + '/activice/resource'}

    # 如果奖品列表中使用了资源，则该资源不应该被修改和删除
    if isResourceInRewardList(redis, session['id'], tableid):
        return {'code': 1, 'msg': '删除资源失败.', 'jumpUrl': BACK_PRE + '/activice/resource'}

    delResource(redis,session['id'],tableid)

    return {'code': 0, 'msg': '删除资源成功.', 'jumpUrl': BACK_PRE + '/activice/resource'}


@admin_app.get('/activice/resource_edit')
@admin_app.post('/activice/resource_edit')
def do_ResourceEdit(redis, session):
    """
    修改资源信息
    """
    lang = getLang()
    imgId = request.GET.get('id','').strip()
    isEdit = request.forms.get('id','').strip()
    if isEdit:
        #修改
        title = request.forms.get('title', '').strip()
        note = request.forms.get('note', '').strip()
        upload = request.files.get('file')
        try:

            # 如果奖品列表中使用了资源，则该资源不应该被修改和删除
            if isResourceInRewardList(redis,session['id'],isEdit):
                return redirect(BACK_PRE + '/activice/resource')

            if upload and upload.content_type not in RESOURCE_ALLOW_TYPES:
                return redirect(BACK_PRE + '/activice/resource_add')
            messageInfo = {
                'title': title,
                'note': note,
                'id': isEdit,
            }
            editResource(redis, session['id'], messageInfo, upload)
        except Exception, ex:
            traceback.print_exc()
        return redirect(BACK_PRE + '/activice/resource')
    searchId = imgId
    res = get_resourceList(redis, session, searchId, lang)
    setting = res["data"][0]
    info={
        'title': lang.RESOURCE_EDIT_TEXT,
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + '/activice/resource',
        'submitUrl': BACK_PRE + '/activice/resource_edit',
        'submitText' : '修改'
    }
    return template("resource_create",info = info, lang = lang,RES_VERSION=RES_VERSION, setting = setting)


#------------------------------------------------  统计相关 ---------------------------------------


@admin_app.get('/activice/statis/record')
def get_statis_record(redis, session):
    """
    普通获奖记录
    """
    lang = getLang()
    isList = request.GET.get('list','').strip()
    acId = request.GET.get('id','').strip()
    searchId = request.GET.get('searchId','').strip()

    if isList :
        # 通过活动id查询对应记录 acId
        data = get_awardees_byacic(redis,acId,searchId,record=False)
        return  {'code':0,'msg':'','data':data}

    # 权限
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/activice/statis/record'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'


    info = {
        "title": lang.ACTIVICE_STATIS_RECORD,
        "submitUrl": BACK_PRE + "/activice/create",
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/activice/statis/record",
        'showPlus': "false",
        'createAccess': createAg,
        'searchTxt': '玩家ID',
        'listUrl': BACK_PRE + "/activice/statis/record?list=1&id=%s" % acId,
    }
    return template("admin_statis_record",info = info, lang = lang,RES_VERSION=RES_VERSION)


@admin_app.get('/activice/statis/special')
def get_statis_special(redis, session):
    """
    实物获奖记录
    """
    lang = getLang()
    isList = request.GET.get('list','').strip()
    acId = request.GET.get('id', '').strip()
    searchId = request.GET.get('searchId', '').strip()

    if isList :
        # data = [{
        #     "date":"2017年9月20日21:18:25",
        #     "id":"1",
        #     "name":"test21",
        #     "rewardTitle":"钻石*3",
        #     "rewardId":"1",
        #     "phone":"130xxxxxxxx"
        # }]
        data = get_awardees_byacic(redis, acId, searchId, record=True)
        return  {'code':0,'msg':'','data':data}

    # 权限
    agentId = session['id']
    creatAgUrl = BACK_PRE + '/activice/statis/special'
    if creatAgUrl in redis.smembers(AGENT2ACCESSBAN % (agentId)):
        createAg = '0'
    else:
        createAg = '1'


    info = {
        "title": lang.ACTIVICE_STATIS_SPECIAL,
        "submitUrl": BACK_PRE + "/activice/create",
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/activice/statis/special",
        'showPlus': "false",
        'createAccess': createAg,
        'searchTxt': '玩家ID',
        'listUrl': BACK_PRE + "/activice/statis/special?list=1&id=%s" % acId,
    }
    return template("admin_statis_special",info = info, lang = lang,RES_VERSION=RES_VERSION)


@admin_app.get('/activice/agentlist')
def get_agent_list(redis, session):
    """ 
        创建活动查询代理列表
    """
    is_list = request.GET.get('list', '').strip()
    if not is_list:
        return
    agentid = session['id']
    parent_table = AGENT_CHILD_TABLE % agentid
    subids = redis.smembers(parent_table)
    sub_ag_lists = []
    for subid in subids:
        agent_table = AGENT_TABLE % subid
        atype, account, aid = redis.hmget(agent_table,('type','account','id'))
        if not account or atype == '4':
            continue
        if not aid:
            continue
        sub_ag_lists.append({'parentId': aid,'agentType': atype,'parentAg': account})
    return json.dumps({'count': len(sub_ag_lists),'data': sub_ag_lists})
