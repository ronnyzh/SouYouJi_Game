#coding:utf-8
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    背包
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
from common.utilt import *
from common.log import *
from datetime import datetime
from web_db_define import *
from access_module import *
from common import encrypt_util,convert_util,json_util,web_util
from bag.bag_config import bag_redis
from model.bagModel import *
from model.red_envelope_db_define import *
from model.statisticsModel import *
from db_define.db_define_consts import *

import json
import uuid

@admin_app.get('/bag/create/item')
@checkAccess
def createItem(redis,session):

    lang    = getLang()

    info = {
            'title'                  :       '创建道具',
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'submitUrl'              :       BACK_PRE + "/bag/create/item"
    }

    return template('admin_bag_create_item',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=0)

@admin_app.post('/bag/create/item')
@checkAccess
def createItem(redis,session):
    """创建道具"""
    lang    = getLang()

    item_id = request.forms.get('item_id', '').strip()
    title = request.forms.get('title', '').strip()
    des = request.forms.get('des', '').strip()
    icon = request.forms.get('icon', '').strip()
    price = request.forms.get('price', '').strip()
    times = request.forms.get('times', '').strip()
    days = request.forms.get('days', '').strip()
    unit = request.forms.get('unit', '').strip()
    can_reward = request.forms.get('can_reward', '').strip()

    if not title or not item_id or not des:
        return {'code': 1, 'msg': '请添加道具参数'}

    for iid in bag_redis.smembers(ITEM_ID_SET):
        if item_id == iid:
            return {'code': 1, 'msg': '道具ID重复'}

    bag_redis.hmset(ITEM_ATTRS%item_id,{
        "item_id":item_id,
        "title":title,
        "des":des,
        "is_delete":0,
        "price":price,
        "is_goods":1,
        "days":days,
        "times":times,
        "bag_show":1,
        "unit":unit,
        "can_reward":can_reward,
    })

    bag_redis.sadd(ITEM_ID_SET,item_id)
    return {'code': 0, 'msg': '道具创建成功'}

@admin_app.get('/bag/list')
@checkAccess
def getCurOnline(redis,session):
    """
        道具列表
    """
    lang    =  getLang()
    isList  =  request.GET.get('list','').strip()

    if isList:
        return getItemListInfo()
    else:
        info = {
                'title'                  :           '道具列表',
                'listUrl'                :           BACK_PRE+'/bag/list?list=1',
                'createUrl'              :           BACK_PRE+'/bag/create/item',
                'addTitle'               :           '创建道具',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
        }

        return template('admin_bag_list',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=0)

@admin_app.get('/bag/item/changeI')
@checkAccess
def DeleteItem(redis,session):
    """
        删除或恢复道具
    """

    lang    =  getLang()
    item_id  =  request.GET.get('item_id','').strip()
    ci  =  request.GET.get('ci','').strip()

    changeIsDelete(item_id,ci)

    info = {
        'title'                  :           '道具列表',
        'listUrl'                :           BACK_PRE+'/bag/list?list=1',
        'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_bag_list',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=1)

@admin_app.get('/bag/item/isgoods')
@checkAccess
def DeleteItem(redis,session):
    """
        设定道具是否可在商城购买
    """

    lang    =  getLang()
    item_id  =  request.GET.get('item_id','').strip()
    ig  =  request.GET.get('ig','').strip()

    changeIsGoods(item_id,ig)

    info = {
        'title'                  :           '道具列表',
        'listUrl'                :           BACK_PRE+'/bag/list?list=1',
        'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_bag_list',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=1)

@admin_app.get('/bag/item/can_use')
@checkAccess
def canUseItem(redis,session):
    """
        设定道具是否使用
    """

    lang    =  getLang()
    item_id  =  request.GET.get('item_id','').strip()
    cu  =  request.GET.get('cu','').strip()

    changeCanUse(item_id,cu)

    info = {
        'title'                  :           '道具列表',
        'listUrl'                :           BACK_PRE+'/bag/list?list=1',
        'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_bag_list',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=1)

@admin_app.get('/bag/item/modify')
@checkAccess
def itemModify(redis,session):
    """
        修改道具信息
    """

    lang    =  getLang()
    item_id  =  request.GET.get('item_id','').strip()

    dic =  getModifyItemInfo(item_id)

    info = {
        'title'                  :           '修改道具信息',
        'submitUrl'              :           BACK_PRE + "/bag/item/modify",
        'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_bag_item_modify',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=0,**dic)

@admin_app.post('/bag/item/modify')
@checkAccess
def itemModify(redis,session):

    lang    = getLang()

    item_id = request.forms.get('item_id', '').strip()
    title = request.forms.get('title', '').strip()
    des = request.forms.get('des', '').strip()
    icon = request.forms.get('icon', '').strip()
    price = request.forms.get('price', '').strip()
    times = request.forms.get('times', '').strip()
    days = request.forms.get('days', '').strip()
    unit = request.forms.get('unit', '').strip()
    can_reward = request.forms.get('can_reward', '').strip()

    dic =  getModifyItemInfo(item_id)

    info = {
        'title'                  :       '创建道具',
        'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
        'submitUrl'              :       BACK_PRE + "/bag/item/modify",
    }

    if not title or not item_id or not des:
        return template('admin_bag_item_modify',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=2,**dic)

    bag_redis.hmset(ITEM_ATTRS%item_id,{
        "item_id":item_id,
        "title":title,
        "des":des,
        "price":price,
        "times":times,
        "days":days,
        "unit":unit,
        "can_reward":can_reward,
    })

    return template('admin_bag_item_modify',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=1,**dic)

@admin_app.get('/bag/send/mail')
@checkAccess
def send_mail(redis,session):
    """
        发送邮件页面
    """

    lang    = getLang()

    items = {'1': 'roomCard', '3': 'gamePoint'}
    items = {'1': '钻石', '3': '积分'}
    info = {
            'title'                  :       '发送邮件',
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'submitUrl'              :       BACK_PRE + "/bag/send/mail"
    }

    return template('admin_bag_send_mail',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=0,items=items)

@admin_app.post('/bag/send/mail')
@checkAccess
def send_mail(redis,session):
    """
        发送邮件接口
    """
    lang    = getLang()
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d")

    title = request.forms.get('title', '').strip()
    uid = request.forms.get('uid', '').strip()
    body = request.forms.get('body', '').strip()
    enclosure = request.forms.get('enclosure', '').strip()
    recipientType = request.forms.get('recipientType', '0').strip()

    if int(recipientType):
        uid_list = getAgentAllMemberIds(redis, session.get('id'))
    else:
        if not uid or not re.match('^\d+(,\d+)*$', uid):
            return {'code': 1, 'msg': '请填写收件人ID或收件人格式错误'}
        else:
            uid_list = uid.split(',')

    if not title:
        return {'code': 1, 'msg': '请填写邮件标题'}

    if not body:
        return {'code': 1, 'msg': '请填写邮件内容'}

    awards = ''
    if enclosure:
        enclosure_num = request.forms.get('enclosure_num', '').strip()
        if not enclosure_num:
            return {'code': 1, 'msg': '请填写附件数量'}
        awards = '%s,%s' % (enclosure, enclosure_num)

    pipe = bag_redis.pipeline()
    for uid in uid_list:
        e_num = bag_redis.scard(USER_EMAIL_SET % uid)
        # if int(e_num) >= 200:
        #     return {'code': 1, 'msg': '发送失败！用户[%s]邮件已达到上限200！'}
        email_id = uuid.uuid4().hex
        pipe.sadd(USER_EMAIL_DATE_SET % date, email_id)
        pipe.sadd(USER_EMAIL_SET % uid, email_id)
        pipe.hmset(EMAIL_HASH % email_id, {"title": title, "body": body, "awards": awards,
                                                "send_time": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                                                "read": 0, "timestamp": int(time.time()*1000), 'email_type': '', 'userId': uid})
        if awards:
            # 统计当天后台发送邮件附件总数量
            enclosure_name = Define_Currency.getCurrencyName(enclosure)
            pipe.hincrby('email:send:enclosure:%s:hash' % date, '%s' % enclosure_name, enclosure_num)
    pipe.execute()
    return {'code': 0, 'msg': '发送成功', 'jumpUrl': ''}

@admin_app.get('/bag/mail/list')
@admin_app.get('/bag/mail/list/<remove_type>')
def get_mailList(redis, session, remove_type="cards"):
    """
    邮件列表
    """
    curTime = datetime.now()
    lang = getLang()
    islist = request.GET.get('isList', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    eid = request.GET.get('eid', '').strip()
    userId = request.GET.get('userId', '').strip()
    enclosureType = request.GET.get('enclosureType', '').strip()
    isRead = request.GET.get('isRead', '').strip()
    isGet = request.GET.get('isGet', '').strip()

    if islist:
        res = []
        condition = {'eid': eid, 'userId': userId, 'enclosureType': enclosureType, 'isRead': isRead, 'isGet': isGet}
        get_week_date_list = get_week_date_obj(startDate, endDate)
        res = get_bag_mail_list(redis, session, get_week_date_list, condition)
        return json.dumps(res)
    info = {
        'title': '邮件列表',
        'tableUrl': BACK_PRE + '/bag/mail/list?isList=1',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
    }
    return template('admin_bag_mail_list', info=info, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.post('/bag/mail/delete')
@checkLogin
def do_MailDelete(redis,session):
    """
    删除邮件
    """
    lang = getLang()
    email_id = request.forms.get('eid', '').strip()
    send_time = request.forms.get('send_time', '').strip()
    user = request.forms.get('user', '').strip()

    if not email_id and not send_time and not user:
        return {'code': 1, 'msg': '参数错误'}
    uid = user.split(' / ')[0]
    date = send_time.split(' ')[0]
    eid = email_id
    pipe = bag_redis.pipeline()
    pipe.delete(EMAIL_HASH % eid)
    pipe.srem(USER_EMAIL_DATE_SET % date, eid)
    pipe.srem(USER_EMAIL_SET % uid, eid)
    pipe.execute()
    return {'code': 0, 'msg': '删除邮件成功', 'jumpUrl': ''}

@admin_app.get('/bag/vcoin/day')
@checkAccess
def getVcoinDay(redis,session):
    """
    当天元宝信息
    """
    curTime  = datetime.now()
    lang     = getLang()

    fields = ('isList','id','startDate','endDate','date')
    for field in fields:
        exec("%s = request.GET.get('%s','').strip()"%(field,field))

    if date:
        endDate = date

    if not id:
        id = session['id']

    if isList:
        selfUid = id
        report = get_redbag_info(redis,selfUid,startDate,endDate)
        return json.dumps(report)
    else:
        """ 返回模板信息 """
        info = {
                    'title'                  :       '元宝当天信息',
                    'listUrl'                :       BACK_PRE+'/bag/vcoin/day?isList=1',
                    'searchTxt'              :       '',
                    'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                    'submitUrl'              :       BACK_PRE + "/bag/triggergoodhand/modify"
        }
    
    rules = bag_redis.smembers(TRIGGER_GOOD_HAND_RULE)
    if rules:
        dic = rules.pop()
        dic = eval(dic)
    else:
        dic = { 'min_possess_value':'', 'max_possess_value':'', 'max_round_value':'', 'good_hand_per':'' }

    log_debug('modifyTriggerGoodHand getVcoinDay [%s] '%(dic))
    return template('admin_bag_vcoin_day',info=info,lang=lang,RES_VERSION=RES_VERSION,**dic)


@admin_app.post('/bag/triggergoodhand/modify')
@checkAccess
@web_util.allow_cross_request
def modifyTriggerGoodHand(redis,session):

    lang    = getLang()

    min_possess_value = request.forms.get('min_possess_value', '').strip()
    max_possess_value = request.forms.get('max_possess_value', '').strip()
    max_round_value = request.forms.get('max_round_value', '').strip()
    good_hand_per = request.forms.get('good_hand_per', '').strip()

    info = {
        'title'                  :       '元宝当天信息',
        'listUrl'                :       BACK_PRE+'/bag/vcoin/day?isList=1',
        'searchTxt'              :       '',
        'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
        'submitUrl'              :       BACK_PRE + "/bag/triggergoodhand/modify"
    }

    log_debug('modifyTriggerGoodHand [%s] [%s] [%s] [%s] '%(min_possess_value, max_possess_value, max_round_value, good_hand_per))
    if not min_possess_value or not max_possess_value:
        bag_redis.delete(TRIGGER_GOOD_HAND_RULE)
    else:
        try:
            min_possess_value = int(min_possess_value)
            max_possess_value = int(max_possess_value)
            max_round_value = int(max_round_value)
            good_hand_per = int(good_hand_per)
            if min_possess_value < 0 or max_possess_value < 0 or min_possess_value > max_possess_value or max_round_value < 0 or good_hand_per < 0 or good_hand_per > 100:
                raise Exception()
            dic = { 'min_possess_value':min_possess_value, 'max_possess_value':max_possess_value,'max_round_value':max_round_value, 'good_hand_per':good_hand_per }
            dic = str(dic)
            bag_redis.delete(TRIGGER_GOOD_HAND_RULE)
            bag_redis.sadd(TRIGGER_GOOD_HAND_RULE, dic)
        except Exception, e:
            # log(u'modifyTriggerGoodHand failed[%s]'%(e))
            log_debug('modifyTriggerGoodHand failed min_possess_value[%s] max_possess_value[%s] max_round_value[%s] good_hand_per[%s]  '%(min_possess_value, max_possess_value, max_round_value, good_hand_per))
            # return False
    
    rules = bag_redis.smembers(TRIGGER_GOOD_HAND_RULE)

    log_debug('modifyTriggerGoodHand [%s] '%(rules))
    if rules:
        dic = rules.pop()
        dic = eval(dic)
    else:
        dic = { 'min_possess_value':'', 'max_possess_value':'', 'max_round_value':'', 'good_hand_per':'' }

    return template('admin_bag_vcoin_day',info=info,lang=lang,RES_VERSION=RES_VERSION,**dic)

@admin_app.get('/bag/vcoin/sum')
def getVcoinDay(redis,session):
    """
         元宝总表
    """
    lang    =  getLang()
    isList  =  request.GET.get('list','').strip()

    if isList:
        return get_redbag_sum_info()
    else:
        info = {
                'title'                  :           '元宝总表',
                'listUrl'                :           BACK_PRE+'/bag/vcoin/sum?list=1',
                'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
        }

        return template('admin_bag_vcoin_sum',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=0)

@admin_app.get('/bag/exchange/list')
@checkAccess
def getCurOnline(redis,session):
    """
        商城兑换列表
    """
    lang    =  getLang()
    isList  =  request.GET.get('list','').strip()

    if isList:
        return get_exchange_info()
    else:
        info = {
            'title'                  :           '商城兑换列表',
            'listUrl'                :           BACK_PRE+'/bag/exchange/list?list=1',
            'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
        }

        return template('admin_bag_exchange_list',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=0)

@admin_app.get('/bag/create/exchange')
@checkAccess
def createItem(redis,session):
    '''
        创建兑换套餐
    :param redis:
    :param session:
    :return:
    '''

    lang    = getLang()

    info = {
            'title'                  :       '创建兑换套餐',
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'submitUrl'              :       BACK_PRE + "/bag/create/exchange"
    }

    return template('admin_bag_create_exchange',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=0)

@admin_app.post('/bag/create/exchange')
@checkAccess
def createItem(redis,session):
    '''
        创建兑换套餐
    :param redis:
    :param session:
    :return:
    '''

    lang    = getLang()

    cid = request.forms.get('cid', '').strip()
    name = request.forms.get('name', '').strip()
    cost_type = request.forms.get('cost_type', '').strip()
    cost = request.forms.get('cost', '').strip()
    gain_type = request.forms.get('gain_type', '').strip()
    gain = request.forms.get('gain', '').strip()
    cost_title = request.forms.get('cost_title', '').strip()
    gain_title = request.forms.get('gain_title', '').strip()

    info = {
        'title'                  :       '创建兑换套餐',
        'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
        'submitUrl'              :       BACK_PRE + "/bag/create/exchange"
    }

    if not all([cid,name,cost_type,cost,gain_type,gain]):
        return template('admin_bag_create_exchange',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=2)

    if cid in bag_redis.smembers("currency:change:course:set"):
        return template('admin_bag_create_exchange',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=3)

    bag_redis.hmset("currency:change:course:%s:hesh"%cid,{
        "name":name,
        "cost":cost,
        "cost_type":cost_type,
        "gain":gain,
        "gain_type":gain_type,
        "cost_title":cost_title,
        "gain_title":gain_title
    })

    bag_redis.sadd("currency:change:course:set",cid)
    return template('admin_bag_create_exchange',info=info,lang=lang,RES_VERSION=RES_VERSION,post_res=1)

@admin_app.get('/bag/exchange/del')
@checkAccess
def DeleteItem(redis,session):
    """
        删除兑换套餐
    """

    lang    =  getLang()
    cid =  request.GET.get('cid','').strip()

    bag_redis.srem("currency:change:course:set",cid)
    bag_redis.delete("currency:change:course:%s:hesh"%cid)

    info = {
        'title'                  :           '商城兑换列表',
        'listUrl'                :           BACK_PRE+'/bag/exchange/list?list=1',
        'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_bag_exchange_list',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=0)

@admin_app.get('/bag/exchange/modify')
@checkAccess
def exchangeModify(redis,session):
    """
        修改兑换套餐
    """

    lang    =  getLang()
    cid =  request.GET.get('cid','').strip()
    dic = bag_redis.hgetall("currency:change:course:%s:hesh"%cid)

    info = {
        'title'                  :           '修改兑换套餐',
        'submitUrl'              :           BACK_PRE + "/bag/exchange/modify",
        'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_bag_exchange_modify',info=info,lang=lang,RES_VERSION=RES_VERSION,cid=cid,post_res=0,**dic)

@admin_app.post('/bag/exchange/modify')
@checkAccess
def createItem(redis,session):
    '''
        修改兑换套餐
    '''

    lang    = getLang()

    cid = request.forms.get('cid', '').strip()
    name = request.forms.get('name', '').strip()
    cost_type = request.forms.get('cost_type', '').strip()
    cost = request.forms.get('cost', '').strip()
    gain_type = request.forms.get('gain_type', '').strip()
    gain = request.forms.get('gain', '').strip()
    cost_title = request.forms.get('cost_title', '').strip()
    gain_title = request.forms.get('gain_title', '').strip()
    big_type_id = request.forms.get('big_type_id', '').strip()
    big_type_title = request.forms.get('big_type_title', '').strip()

    info = {
        'title'                  :           '商城兑换列表',
        'listUrl'                :           BACK_PRE+'/bag/exchange/list?list=1',
        'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    bag_redis.hmset("currency:change:course:%s:hesh"%cid,{
        "name":name,
        "cost":cost,
        "cost_type":cost_type,
        "gain":gain,
        "gain_type":gain_type,
        "cost_title":cost_title,
        "gain_title":gain_title,
        "big_type_title":big_type_title,
        "big_type_id":big_type_id,
    })

    return template('admin_bag_exchange_list',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=1)


@admin_app.get('/bag/item/bag_show')
@checkAccess
def canUseItem(redis,session):
    """
        设定道具是否使用
    """

    lang    =  getLang()
    item_id  =  request.GET.get('item_id','').strip()
    bs  =  request.GET.get('bs','').strip()

    changeBagShow(item_id,bs)

    info = {
        'title'                  :           '道具列表',
        'listUrl'                :           BACK_PRE+'/bag/list?list=1',
        'STATIC_LAYUI_PATH'      :           STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :           STATIC_ADMIN_PATH
    }

    return template('admin_bag_list',info=info,lang=lang,RES_VERSION=RES_VERSION,op_res=1)


@admin_app.get('/bag/select/userid')
def get_selectUserId(redis, session):
    """
    搜索框获取用户ID信息
    """
    userid = request.GET.get("name", '').strip()
    page = request.GET.get("page", '').strip()
    if userid:
        user_table = FORMAT_USER_TABLE % userid
        if redis.exists(user_table):
            nickname = redis.hget(user_table, 'nickname')
            return {"data": {"users": [{"id": userid, 'name': '%s : %s' % (userid, nickname)}]}}
        else:
            return {"data": {"users": []}}
    else:
        page = int(page)
        skip = page * 10
        start = skip - 10
        end = skip
        data = dict()
        user_list = []
        account_weixin_list = list(redis.smembers(ACCOUNT4WEIXIN_SET))
        for account in account_weixin_list[start:end]:
            user_table = redis.get("users:account:%s" % account)
            user_id = user_table.split(':')[-1]
            nickname = redis.hget(user_table, 'nickname')
            user_list.append({'id': user_id, 'name': '%s : %s' % (user_id, nickname)})
        data['users'] = user_list
        data['count'] = redis.scard(ACCOUNT4WEIXIN_SET)
        more = page * 10 < data["count"]
        data["more"] = more
        return {'data': data}


@admin_app.get('/bag/select/agentid')
def get_selectUserId(redis, session):
    """
    搜索框获取代理ID信息
    """
    lang = getLang()
    agentid = request.GET.get("name", '').strip()
    page = request.GET.get("page", '').strip()
    if agentid:
        agent_table = AGENT_TABLE % agentid
        if redis.exists(agent_table):
            account, type = redis.hmget(agent_table, ('account', 'type'))
            return {"data": {"users": [{"id": agentid, 'name': '%s : %s : %s' % (agentid, account, lang.TYPE_2_ADMINTYPE[type])}]}}
        else:
            return {"data": {"users": []}}
    else:
        agentid = session.get('id')
        page = int(page)
        skip = page * 10
        start = skip - 10
        end = skip
        data = dict()
        user_list = []
        all_agent_list = getAllChildAgentId(redis, agentid)
        all_agent_list.insert(0, agentid)
        all_agent_list = sorted(all_agent_list)
        for agent in all_agent_list[start:end]:
            agent_table = AGENT_TABLE % agent
            account, type = redis.hmget(agent_table, 'account', 'type')
            user_list.append({'id': agent, 'name': '%s : %s : %s' % (agent, account, lang.TYPE_2_ADMINTYPE[type])})
        data['users'] = user_list
        data['count'] = len(all_agent_list)
        more = page * 10 < data["count"]
        data["more"] = more
        return {'data': data}

@admin_app.get('/bag/mail/enclosure')
def get_mailList(redis, session):
    """
    邮件列表
    """
    curTime = datetime.now()
    lang = getLang()
    isList = request.GET.get('isList', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    userId = request.GET.get('userId', '').strip()
    enclosureType = request.GET.get('enclosureType', '').strip()
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
                    info = dict(zip(('userId', 'agentId', 'roomCard', 'card', 'dateTime', 'enclosure_type', 'eid'), compensate.split('|')))
                    if userId and userId != info.get('userId'):
                        continue
                    account, nickname = redis.hmget(FORMAT_USER_TABLE % info.get('userId'), ('account', 'nickname'))
                    info['account'] = account
                    info['nickname'] = nickname
                    info['time'] = dateStr
                    info['enclosure_type'] = '%s' % (MATCH_AWARDS_NAME_TABLE[info.get('enclosure_type')])
                    if enclosureType and enclosureType != info.get('enclosure_type'):
                        continue
                    info['enclosure_Num'] = info.get('card')
                    info['after_card'] = int(info.get('roomCard')) + int(info.get('card'))
                    info['op'] = [
                        {'url': '/admin/bag/look/mail', 'method': 'GET', 'txt': '查看邮件'},
                    ]
                    res.append(info)
            endDate -= deltaTime
        return {"count": len(res), "data": res}
    info = {
        'title': '邮件附件领取记录',
        'tableUrl': BACK_PRE + '/bag/mail/enclosure?isList=1',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'enclosureEchartUrl': BACK_PRE + '/bag/mail/enclosure/echarts'
    }
    return template('admin_bag_mail_enclosure', info=info, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.get('/bag/look/mail')
def get_lookMail(redis, session):
    """
    邮件列表
    """
    curTime = datetime.now()
    lang = getLang()
    eid = request.GET.get('eid', '').strip()
    userId = request.GET.get('userId', '').strip()
    mailInfo = get_bag_look_mail(redis, session, userId, eid)
    info = {
        'title': '查看邮件',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'backUrl': BACK_PRE + '/bag/mail/list',
    }
    return template('admin_bag_mail_look', info=info, mailInfo=mailInfo, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.get('/bag/mail/enclosure/echarts')
def get_mailListEcharts(redis, session):
    """
    获取邮件领取附件图表数据
    """
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    get_week_date_list = get_week_date_obj(startDate, endDate)
    show_obj = {
        'data': ['钻石', '积分'],
        'roomCard': [],
        'gamePoint': [],
    }

    for week_date in get_week_date_list:
        enclosure_card_table = ENCLOSURE_MAIL_DAY % week_date
        roomCard_count, gamePoint_count = 0, 0
        if redis.exists(enclosure_card_table):
            for compensate in redis.lrange(enclosure_card_table, 0, -1):
                _, _, _, enclosure_num, _, enclosure_type, _ = compensate.split('|')
                if enclosure_type == 'roomCard':
                    roomCard_count += int(enclosure_num)
                if enclosure_type == 'gamePoint':
                    gamePoint_count += int(enclosure_num)
        show_obj['roomCard'].append(roomCard_count)
        show_obj['gamePoint'].append(gamePoint_count)

    show_obj['series'] = [
        {'name': '钻石', 'type': 'line', 'data': show_obj['roomCard'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
        {'name': '积分', 'type': 'line', 'data': show_obj['gamePoint'],
         'itemStyle': {'normal': {'label': {'show': 'true'}}}, 'areaStyle': {'normal': {}}},
    ]

    dataZoom_start = 7.0 / len(get_week_date_list) * 100
    return web_util.do_response(1, msg="", jumpUrl="", data={
        'week': get_week_date_list, 'series': show_obj['series'],
        'legen': show_obj['data'], 'dataZoom_start': dataZoom_start,
    })