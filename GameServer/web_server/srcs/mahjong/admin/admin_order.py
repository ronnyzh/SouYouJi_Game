#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
   订单模块
"""


from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
from common.utilt import *
from common import encrypt_util,log_util,web_util,json_util
from web_db_define import *
from datetime import datetime,timedelta
from model.orderModel import *
from model.agentModel import *
import json
import hashlib

@admin_app.get('/order/buy')
def getBuyPage(redis,session):
    """
    购买钻石
    """
    curTime = datetime.now()
    lang    = getLang()

    selfAccount,selfId = session['account'],session['id']

    agentTable = AGENT_TABLE%(selfId)
    parent_id = redis.hget(agentTable,'parent_id')

    parentAg,type = redis.hmget(AGENT_TABLE%(parent_id),('account','type'))
    if not parentAg:
        parentAg = lang.TYPE_2_ADMINTYPE[1]

    info = {
                'title'               :       lang.CARD_BUY_ONLINE_TXT%(parentAg),
                'parentAccount'       :        parentAg,
                'backUrl'             :       '/admin/order/buy',
                'submitUrl'           :       '/admin/order/buy',
                'rechargeTypes'       :       ROOMCARD2TYPE['agent'],
                'STATIC_LAYUI_PATH'   :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'   :       STATIC_ADMIN_PATH
    }

    return template('admin_order_buy',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/order/buy')
@checkAccess
def do_BuyPage(redis,session):
    """
        购买钻石操作
    """
    lang = getLang()
    curTime = datetime.now()

    selfAccount,selfId = session['account'],session['id']
    parentAg  =  request.forms.get('parentAg','').strip()
    cardNums  =  request.forms.get('cardNums','').strip()
    present_card = request.forms.get('parent_card','').strip()
    passwd    =  request.forms.get('passwd','').strip()
    note      =  request.forms.get('note','').strip()

    #[print]
    print '[%s][orderBuy][info] selfAccount[%s] parentAg[%s] cardNums[%s] present_card[%s] passwd[%s] note[%s]'\
                %(curTime,selfAccount,parentAg,cardNums,present_card,passwd,note)

    try:
        if int(cardNums) <=0:
            return {'code':1,'msg':'充值的钻石数必须大于0.'}
    except:
        return {'code':1,'msg':'非法的钻石数.'}

    checkNullFields = [
            {'field':parentAg,'msg':lang.CARD_SALER_NOT_EXISTS},
            {'field':cardNums,'msg':lang.CARD_RECHARGE_NUMS_REQUEST},
            {'field':passwd,'msg':lang.CARD_RECHARGE_PASSWD_REQ}
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    adminTable = AGENT_TABLE%(selfId)
    selfPasswd,selfRoomCard,type,parent_id = redis.hmget(adminTable,('passwd','roomcard','type','parent_id'))

    #验证代理密码
    if selfPasswd != hashlib.sha256(passwd).hexdigest():
        return {'code':1,'msg':lang.CARD_HANDLE_TIPS_TXT}

    #生成充值订单号
    orderNo = getOrderNo(selfId)

    orderInfo = {
            'orderNo'                :       orderNo,
            'cardNums'               :       cardNums,
            'card_present'           :       present_card,
            'applyAccount'           :       selfAccount,
            'status'                 :       0,
            'apply_date'             :       curTime.strftime('%Y-%m-%d %H:%M:%S'),
            'finish_date'            :       '',
            'type'                   :       0,
            'note'                   :       note,
            'saleAccount'            :       parentAg
    }

    if createOrder(redis,orderInfo):
        dateStr = curTime.strftime('%Y-%m-%d')
        pipe = redis.pipeline()
        #将订单写入购卡订单
        pipe.lpush(AGENT_BUY_ORDER_LIST%(selfId,dateStr),orderNo)
        pipe.lpush(AGENT_BUYPENDING_ORDER_LIST%(selfId,dateStr),orderNo)
        #将订单写入售卡订单
        pipe.lpush(AGENT_SALE_ORDER_LIST%(parent_id,dateStr),orderNo)
        pipe.lpush(AGENT_SALEPENDING_ORDER_LIST%(parent_id,dateStr),orderNo)

        pipe.execute()
        return {'code':0,'msg':lang.CARD_APPLY_SUCCESS_TXT%(orderNo),'jumpUrl':BACK_PRE+'/order/buy/record'}

    return {'code':1,'msg':lang.CARD_APPLY_ERROR_TXT%(orderNo)}


@admin_app.get('/order/buy/record')
@checkAccess
def getBuyRecordPage(redis,session):
    """
        获取购买钻石记录
    """
    curTime = datetime.now()
    lang    = getLang()

    selfAccount,selfId = session['account'],session['id']
    isList = request.GET.get('list','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate   = request.GET.get('endDate','').strip()

    if not startDate or not endDate:
        #默认显示一周时间
        startDate,endDate = getDaya4Week()

    if isList:
        orders = getBuyOrdersById(redis,selfId,startDate,endDate)
        return json.dumps(orders)
    else:
        info = {
                    'title'               :       lang.CARD_BUY_RECORD_TXT,
                    'startDate'           :       startDate,
                    'endDate'             :       endDate,
                    'searchUrl'           :       BACK_PRE+'/order/buy/record?list=1',
                    'tableUrl'            :       BACK_PRE+'/order/buy/record?list=1',
                    'STATIC_LAYUI_PATH'   :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'   :       STATIC_ADMIN_PATH
        }

        return template('admin_order_buy_record',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/order/sale/record')
@checkAccess
def getSaleRecordPage(redis,session):
    """
        获取售卖钻石记录
    """
    curTime = datetime.now()
    lang    = getLang()

    selfAccount,selfId = session['account'],session['id']

    startDate = request.GET.get('startDate','').strip()
    endDate   = request.GET.get('endDate','').strip()

    if not startDate or not endDate:
        #默认显示一周时间
        startDate,endDate = getDaya4Week()

    isList = request.GET.get('list','').strip()

    if isList:
        orders = getSaleOrdersById(redis,selfId,startDate,endDate)
        return json.dumps(orders)
    else:
        info = {
                    'title'               :       lang.CARD_SALE_RECORD_TXT,
                    'startDate'           :       startDate,
                    'endDate'             :       endDate,
                    'searchUrl'           :       BACK_PRE+'/order/sale/record?list=1',
                    'tableUrl'            :       BACK_PRE+'/order/sale/record?list=1',
                    'STATIC_LAYUI_PATH'   :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'   :       STATIC_ADMIN_PATH
        }

        return template('admin_order_sale_record',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/order/comfirm')
@checkLogin
def do_orderComfirm(redis,session):
    """
    代理订单确认
    """
    lang = getLang()
    curTime = datetime.now()
    dateStr = curTime.strftime('%Y-%m-%d')

    selfAccount,selfUid = session['account'],session['id']
    fields = ('orderNo','token')
    for field in fields:
        exec('%s = request.forms.get("%s","").strip()'%(field,field))

    try:
        log_debug('[try do_orderComfirm] orderNo[%s] token[%s] session_token[%s]'%(orderNo,token,session['comfirm_token']))
    except:
        return {'code':-300,'msg':'接口参数请求错误'}

    if session.get('comfirm_token') == None:
        return {'code':1,'msg':'不合法的操作!'}

    if token != session['comfirm_token']:
        return {'code':0,'msg':'请勿重复确认订单','jumpUrl':BACK_PRE+'/order/sale/record'}

    orderTable = ORDER_TABLE%(orderNo)
    if not orderTable:
        return {'code':1,'msg':lang.CARD_ORDER_NOT_EXISTS%(orderNo)}

    applyAccount,cardNums,present_card,status = \
                redis.hmget(orderTable,('applyAccount','cardNums','card_present','status'))

    buyerId = getAgentId(redis,applyAccount)

    buyerTable = AGENT_TABLE%(buyerId)
    salerTable = AGENT_TABLE%(selfUid)

    saleType,salerRoomCard = redis.hmget(AGENT_TABLE%(selfUid),('type','roomcard'))
    if not salerRoomCard:
        salerRoomCard = 0

    orderUpdateInfo = {
                'status'            :       1,
                'finish_date'       :       curTime.strftime('%Y-%m-%d %H:%M:%S')
    }

    #置空
    session['comfirm_token'] = None
    pipe = redis.pipeline()
    try:
        if int(saleType) not in [SYSTEM_ADMIN]:
            #如果不是系统管理员或总公司需要减去对应钻石
            if int(salerRoomCard) < int(cardNums):
                return {'code':4,'msg':lang.CARD_NOT_ENGOUGHT_TXT,'jumpUrl':BACK_PRE+'/order/buy'}
            pipe.hincrby(salerTable,'roomcard',-int(cardNums))

        pipe.hincrby(buyerTable,'roomcard',int(cardNums))
        #将订单从pendding移除
        pipe.lrem(AGENT_BUYPENDING_ORDER_LIST%(buyerId,dateStr),orderNo)
        pipe.lpush(AGENT_BUYSUCCESS_ORDER_LIST%(buyerId,dateStr),orderNo)
        #将订单写入售卡订单
        pipe.lrem(AGENT_SALEPENDING_ORDER_LIST%(selfUid,dateStr),orderNo)
        pipe.lpush(AGENT_SALESUCCESS_ORDER_LIST%(selfUid,dateStr),orderNo)
        #更改订单状态
        pipe.hmset(orderTable,orderUpdateInfo)

        #统计代理购卡
        if redis.exists(AGENT_BUY_CARD_DATE%(buyerId,dateStr)):
            pipe.hincrby(AGENT_BUY_CARD_DATE%(buyerId,dateStr),'cardNums',int(cardNums))
            pipe.hincrby(AGENT_BUY_CARD_DATE%(buyerId,dateStr),'totalNums',int(cardNums))
        else:
            try:
                his_total_nums = redis.get(AGENT_BUY_TOTAL%(buyerId))
                if not his_total_nums:
                    his_total_nums = 0
            except:
                his_total_nums = 0
            pipe.hmset(AGENT_BUY_CARD_DATE%(buyerId,dateStr),{'cardNums':int(cardNums),'date':dateStr,'totalNums':int(his_total_nums)+int(cardNums)})

        #统计代理售卡
        if redis.exists(AGENT_SALE_CARD_DATE%(selfUid,dateStr)):
            pipe.hincrby(AGENT_SALE_CARD_DATE%(selfUid,dateStr),'cardNums',int(cardNums))
            pipe.hincrby(AGENT_SALE_CARD_DATE%(selfUid,dateStr),'totalNums',int(cardNums))
        else:
            try:
                his_total_nums = redis.get(AGENT_SALE_TOTAL%(selfUid))
                if not his_total_nums:
                    his_total_nums = 0
            except:
                his_total_nums = 0
            pipe.hmset(AGENT_SALE_CARD_DATE%(selfUid,dateStr),{'cardNums':int(cardNums),'date':dateStr,'totalNums':int(his_total_nums)+int(cardNums)})
    except Exception,e:
        log_debug('[try order error] reason[%s]'%(e))
        return {'code':1,'msg':'订单确认失败.'}

    pipe.execute()
    return {'code':0,'msg':lang.CARD_COMFIRM_SUCCESS_TXT%(orderNo),'jumpUrl':BACK_PRE+'/order/sale/record'}

@admin_app.get('/order/info')
def getOrderInfo(redis,session):
    """
    订单信息查询
    """
    curTime = datetime.now()
    lang    = getLang()
    fields = ('orderNo','backUrl','isAjax')
    for field in fields:
        exec('%s = request.GET.get("%s","").strip()'%(field,field))

    try:
        log_debug('[try getOrderInfo] orderNo[%s] backUrl[%s] isAjax[%s] is_xhr[%s]'%(orderNo,backUrl,isAjax,request.is_xhr))
    except:
        return {'code':-300,'msg':'接口参数错误'}

    orderTable = ORDER_TABLE%(orderNo)
    if not redis.exists(orderTable):
        print '[%s][order info] orderNo[%s] is not exists.'%(curTime,orderNo)
        return None

    cardNums,applyAccount,status,apply_date,finish_date,note,saleAccount = \
                        redis.hmget(orderTable,('cardNums','applyAccount','status','apply_date','finish_date','note','saleAccount'))

    submit_token = encrypt_util.to_sha256(orderNo)
    session['comfirm_token'] = submit_token
    orderInfo = {
            'title'                 :           lang.CARD_DETAIL_TXT%(orderNo),
            'orderNo'               :           orderNo,
            'cardNums'              :           cardNums,
            'applyAccount'          :           saleAccount,
            'status'                :           lang.COMFIRM_ALREADY_TXT if status=='1'  else lang.COMFIRM_NOT_TXT,
            'applyDate'             :           apply_date,
            'finishDate'            :           finish_date,
            'note'                  :           note,
            'token'                 :           submit_token,
            'rechargeAccount'       :           applyAccount
    }

    if request.is_xhr:
        return orderInfo

    return template('agent_orderInfo',info=orderInfo,RES_VERSION=RES_VERSION)

@admin_app.post('/order/cancel')
def do_orderCancel(redis,session):
    """
    取消订单
    """
    lang = getLang()
    curTime = datetime.now()
    dateStr = curTime.strftime('%Y-%m-%d')

    selfAccount,selfUid,selfType = session['account'],session['id'],session['type']

    orderNo = request.forms.get('orderNo','').strip()
    #print
    print '[%s][order cancel][info] orderNo[%s]'%(curTime,orderNo)

    orderTable = ORDER_TABLE%(orderNo)
    if not orderTable:
        print '[%s][order cancel][error] orderNo[%s] is not exists.'
        return {'code':1,'msg':lang.CARD_ORDER_NOT_EXISTS%(orderNo)}

    saleAccount,cardNums,present_card,status = \
                redis.hmget(orderTable,('saleAccount','cardNums','card_present','status'))

    salerId = getAgentId(redis,saleAccount)

    buyerTable = AGENT_TABLE%(selfUid)
    salerTable = AGENT_TABLE%(salerId)

    pipe = redis.pipeline()

    try:
        #将订单从pendding移除
        pipe.lrem(AGENT_BUYPENDING_ORDER_LIST%(selfUid,dateStr),orderNo)
        pipe.lrem(AGENT_BUY_ORDER_LIST%(selfUid,dateStr),orderNo)
        #将订单写入售卡订单
        pipe.lrem(AGENT_SALE_ORDER_LIST%(salerId,dateStr),orderNo)
        pipe.lrem(AGENT_SALEPENDING_ORDER_LIST%(salerId,dateStr),orderNo)
        pipe.lrem(ORDER_LIST,orderNo)
        pipe.delete(orderTable)
        pipe.execute()
    except Exception,e:
        print '[%s][order cancel][error] orderNo[%s] reason[%s]'%(curTime,orderNo,e)
        return {'code':1,'msg':lang.CARD_CANCEL_ERROR_TXT}

    return {'code':0,'msg':lang.CARD_CANCEL_SUCCESS_TXT%(orderNo),'jumpUrl':BACK_PRE+'/order/buy/record'}


@admin_app.post('/order/sale/cancel')
def do_orderCancel(redis,session):
    """
    取消订单
    """
    lang = getLang()
    curTime = datetime.now()
    dateStr = curTime.strftime('%Y-%m-%d')

    selfAccount,selfUid,selfType = session['account'],session['id'],session['type']

    orderNo = request.forms.get('orderNo','').strip()
    #print
    print '[%s][order cancel][info] orderNo[%s]'%(curTime,orderNo)

    orderTable = ORDER_TABLE%(orderNo)
    if not orderTable:
        print '[%s][order cancel][error] orderNo[%s] is not exists.'
        return {'code':1,'msg':lang.CARD_ORDER_NOT_EXISTS%(orderNo)}

    applyAccount,cardNums,present_card,status = \
                redis.hmget(orderTable,('applyAccount','cardNums','card_present','status'))

    buyerId = getAgentId(redis,applyAccount)

    buyerTable = AGENT_TABLE%(buyerId)
    salerTable = AGENT_TABLE%(selfUid)

    pipe = redis.pipeline()

    try:
        #将订单从pendding移除
        pipe.lrem(AGENT_BUYPENDING_ORDER_LIST%(buyerId,dateStr),orderNo)
        pipe.lrem(AGENT_BUY_ORDER_LIST%(buyerId,dateStr),orderNo)
        #将订单写入售卡订单
        pipe.lrem(AGENT_SALE_ORDER_LIST%(selfUid,dateStr),orderNo)
        pipe.lrem(AGENT_SALEPENDING_ORDER_LIST%(selfUid,dateStr),orderNo)
        pipe.lrem(ORDER_LIST,orderNo)
        pipe.delete(orderTable)
        pipe.execute()
    except Exception,e:
        print '[%s][order cancel][error] orderNo[%s] reason[%s]'%(curTime,orderNo,e)
        return {'code':1,'msg':lang.CARD_CANCEL_ERROR_TXT}

    return {'code':0,'msg':lang.CARD_CANCEL_SUCCESS_TXT%(orderNo),'jumpUrl':BACK_PRE+'/order/sale/record'}

@admin_app.get('/order/wechat/record')
@admin_app.get('/order/wechat/record/<action>')
def get_wechat_records(redis,session,action="HALL"):
    """
    获取微信售钻记录接口
    action通知是获取捕鱼还是棋牌
    """
    lang = getLang()
    action = action.upper()
    fields = ('isList','startDate','endDate','memberId','orderNo', 'orderType', 'payType')
    for field in fields:
        exec('%s = request.GET.get("%s","").strip()'%(field,field))

    log_util.debug('[try get_wechat_records] get params isList[%s] startDate[%s] endDate[%s] memberId[%s] orderNo[%s] action[%s]'\
                        %(isList,startDate,endDate,memberId,orderNo,action))
    if isList:
        condition = {
                'startDate'         :       startDate,
                'endDate'           :       endDate,
                'memberId'          :       memberId,
                'orderNo'           :       orderNo,
                'order_type'         :       orderType,
                'pay_type'           :       payType,
        }
        records = get_wechat_order_records(redis,session['id'],condition,action)
        return json.dumps(records,cls=json_util.CJsonEncoder)
    else:
        params = 'isList=1&startDate=%s&endDate=%s' % (startDate, endDate)
        info = {
                    'title'         :        lang.WECHAT_RECORD_TITLE if action =="HALL" else lang.WECHAT_FISH_RECORD_TITLE,
                    'tableUrl'      :        BACK_PRE+'/order/wechat/record/{}?{}'.format(action,params),
                    'searchUrl'     :        BACK_PRE+'/order/wechat/record/{}'.format(action),
                    'STATIC_LAYUI_PATH'   :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'   :       STATIC_ADMIN_PATH,
                    'startDate'     :        startDate,
                    'action'        :       action,
                    'endDate'       :        endDate,
                    'wechatRecordUrl':       BACK_PRE + '/order/wechat/record/echarts'
        }

        return template('admin_wechat_record',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/order/wechat/record/echarts')
def getGraphsOrderCount(redis, session):
    """
    订单图表
    """
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    # 获取当前一周日期并格式化为字符串
    week_date_lists = get_week_date_obj(startDate, endDate)
    show_obj = {
        'data': [u'商城总订单', u'成功订单', u'挂起订单', u'成功订单交易总金额', u'挂起订单交易总金额'],
        'wechat_count': [],
        'succee_count': [],
        'pending_count': [],
        'success_list': [],
        'pending_list': [],
    }
    for week_date in week_date_lists:
        selfUid = '1'  # session['id']
        wechat = redis.llen(DAY_ORDER % week_date)
        succee, pengding, succeeNum, pendingNum = 0, 0, 0, 0
        if wechat:
            for each in redis.lrange(DAY_ORDER % week_date, 0, -1):
                orderTable = redis.hgetall(ORDER_TABLE % (each))
                if orderTable.get('type') == 'successful':
                    succee += 1
                    succeeNum += round(float(orderTable.get('money')) * 0.01, 2)
                elif orderTable.get('type') == 'pending':
                    pengding += 1
                    pendingNum += round(float(orderTable.get('money')) * 0.01, 2)

        try:
            show_obj['wechat_count'].append(round(convert_util.to_float(wechat), 2))
            show_obj['succee_count'].append(round(convert_util.to_float(succee), 2))
            show_obj['pending_count'].append(round(convert_util.to_float(pengding), 2))
            show_obj['success_list'].append(round(convert_util.to_float(succeeNum), 2))
            show_obj['pending_list'].append(round(convert_util.to_float(pendingNum), 2))
        except Exception as err:
            show_obj['wechat_count'].append(round(convert_util.to_float('0'), 2))
            show_obj['succee_count'].append(round(convert_util.to_float('0'), 2))
            show_obj['pending_count'].append(round(convert_util.to_float('0'), 2))
            show_obj['success_list'].append(round(convert_util.to_float('0'), 2))
            show_obj['pending_list'].append(round(convert_util.to_float('0'), 2))

    show_obj['series'] = [
        {'name': u'商城总订单', 'type': 'line', 'data': show_obj['wechat_count'],'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}},
        {'name': u'成功订单', 'type': 'line', 'data': show_obj['succee_count'],'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}},
        {'name': u'挂起订单', 'type': 'line', 'data': show_obj['pending_count'],'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}},
        {'name': u'成功订单交易总金额', 'type': 'line', 'data': show_obj['success_list'],'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}},
        {'name': u'挂起订单交易总金额', 'type': 'line', 'data': show_obj['pending_list'],'itemStyle' : { 'normal': {'label' : {'show': 'true'}}},'areaStyle': {'normal': {}}},
    ]

    dataZoom_start = 7.0 / len(week_date_lists) * 100
    return web_util.do_response(1, msg="", jumpUrl="", data={
        'week': week_date_lists, 'series': show_obj['series'],
        'legen': show_obj['data'], 'dataZoom_start': dataZoom_start,
    })

