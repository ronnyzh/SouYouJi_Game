#coding:utf-8
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    金币场
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
from common.utilt import *
from common.log import *
from datetime import datetime
from web_db_define import *
from model.protoclModel import *
from model.goldModel import *
from access_module import *
from common import encrypt_util,convert_util,json_util,web_util

import hashlib
import json
from collections import Counter

@admin_app.get('/gold/field')
@checkAccess
def getGoldField(redis,session):

    lang    = getLang()
    # isList  = request.GET.get('list','').strip()
    # search = request.GET.get('search','').strip()

    fields = ('isList', 'startDate', 'endDate', 'pageSize', 'pageNumber', 'searchId', 'sort_name', 'sort_method')
    for field in fields:
        exec ("%s = request.GET.get('%s','').strip()" % (field, field))
    if not pageNumber:
        pageNumber = 1
    else:
        pageNumber = convert_util.to_int(pageNumber)
    if isList:
        return getGoldListInfos(redis, searchId, int(pageSize), int(pageNumber))
    else:
        info = {
                'title'                  :       '金币场用户数据总表',
                'listUrl'                :       BACK_PRE+'/gold/field?isList=1',
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'searchTxt'              :       '输入玩家账号搜索',
                'sort_bar'              : True,  # 开启排序
                'member_page'           : True,  # 开启排序
                'cur_page'              : pageNumber,
                'cur_size'              : pageSize,
                'remove_type'           : '',
        }
        return template('admin_gold_field',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/gold/operate')
@checkAccess
def getGoldOperate(redis,session):
    """
    金币场运营总表
    """
    curTime  = datetime.now()
    lang     = getLang()
    isList = request.GET.get('list','').strip()
    selfUid  = request.GET.get('id','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate  =  request.GET.get('endDate','').strip()
    date     =  request.GET.get('date','').strip()
    niuniu_type = request.GET.get('niuniu_type', MASTER_GAMEID).strip()
    if isList:
        report = getGoldOperateInfos(redis,selfUid,startDate,endDate,niuniu_type)
        return json.dumps(report)
    else:
        online_people_sum,online_room_num,user_current_gold_sum = getOnlineOperateInfos(redis)
        info = {
                    'title'                  :       '金币场运营总表',
                    'listUrl'                :       BACK_PRE+'/gold/operate?list=1&niuniu_type='+niuniu_type,
                    'searchTxt'              :       '',
                    'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                    'online_people_sum'      :       online_people_sum,
                    'online_room_num'        :       online_room_num,
                    'user_current_gold_sum'  :       user_current_gold_sum,
                    'niuniu_type'            :       niuniu_type,

        }

    return template('admin_gold_operate',PAGE_LIST=PAGE_LIST,info=info,lang=lang,RES_VERSION=RES_VERSION)


@admin_app.get('/gold/ai')
@checkAccess
def getGoldAI(redis,session):
    """
        机器人数据表
    """
    curTime  = datetime.now()
    lang     = getLang()
    isList = request.GET.get('list','').strip()
    selfUid  = request.GET.get('id','').strip()
    startDate = request.GET.get('startDate','').strip()
    endDate  =  request.GET.get('endDate','').strip()
    date     =  request.GET.get('date','').strip()
    # B档 或 D档
    grade = request.GET.get('grade','b').strip()

    if isList:
        report = getGoldAIInfos(redis,selfUid,startDate,endDate,grade)
        return json.dumps(report)
    else:
        online_ai_sum, online_ai_room_num, cur_ai_gold_sum = getOnlineAIInfos(redis)
        info = {
                    'title'                  :       '金币场AI数据表',
                    'listUrl'                :       BACK_PRE+'/gold/ai?list=1',
                    'searchTxt'              :       '',
                    'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                    'online_ai_sum'          :       online_ai_sum,
                    'online_ai_room_num'     :       online_ai_room_num,
                    'cur_ai_gold_sum':  cur_ai_gold_sum,
                    'grade'                  :       grade,

        }

    return template('admin_gold_ai',PAGE_LIST=PAGE_LIST,info=info,lang=lang,RES_VERSION=RES_VERSION)


@admin_app.get('/gold/buy_record')
def get_buy_record(redis, session):
    """
        购买金币记录
    """
    lang = getLang()
    isList = request.GET.get('list', '').strip()
    account = request.GET.get('account', '').strip()
    if isList:
        if not account:
            res = []
        else:
            res = getBuyGoldRecord(redis, account)
        return {'code': 0, 'data': res}

    info = {
        "title":  '购买金币流水',
        "tableUrl": BACK_PRE + "/gold/buy_record?list=%s&account=%s" % (1, account),
        'searchTxt': 'uid',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/gold/filed" ,
    }
    return template('admin_gold_buy_record', info=info, lang=lang, RES_VERSION=RES_VERSION)

@admin_app.get('/gold/journal')
def get_journal(redis, session):
    """
        金币游戏记录
    """
    lang = getLang()
    isList = request.GET.get('list', '').strip()
    account = request.GET.get('account', '').strip()
    if isList:
        if not account:
            res = []
        else:
            res = getJournal(redis, account)
        return {'code': 0, 'data': res}

    info = {
        "title":  '金币战绩流水',
        "tableUrl": BACK_PRE + "/gold/journal?list=%s&account=%s" % (1, account),
        'searchTxt': 'uid',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/gold/filed" ,
    }
    return template('admin_gold_journal', info=info, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.get('/gold/buy_record_info')
def get_buy_record_info(redis, session):
    """
        购买金币人数
    """
    lang = getLang()
    isList = request.GET.get('list', '').strip()
    date = request.GET.get('date', '').strip()
    if isList:
        if not date:
            res = []
        else:
            res = getBuyGoldAccounts(redis, date)
        return {'code': 0, 'data': res}

    info = {
        "title":  '购买金币玩家',
        "tableUrl": BACK_PRE + "/gold/buy_record_info?list=%s&date=%s" % (1, date),
        'searchTxt': 'uid',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + "/gold/operate" ,
    }
    return template('admin_gold_buy_record_info', info=info, lang=lang, RES_VERSION=RES_VERSION)


@admin_app.get('/gold/wechat/record')
def get_wechat_records(redis,session):
    """
    获取微信售钻记录接口
    action通知是获取捕鱼还是棋牌
    """
    lang = getLang()
    fields = ('isList','startDate','endDate','memberId','orederNo')
    for field in fields:
        exec('%s = request.GET.get("%s","").strip()'%(field,field))

    if isList:
        condition = {
                'startDate'         :       startDate,
                'endDate'           :       endDate,
                'memberId'          :       memberId,
                'orderNo'           :       orederNo
        }
        records = get_wechat_gold_records(redis, condition)
        return json.dumps(records,cls=json_util.CJsonEncoder)
    else:
        params = 'isList=1&startDate=%s&endDate=%s'%(startDate,endDate)
        info = {
                    'title'         :        "商城购买金币记录",
                    'tableUrl'      :        BACK_PRE+'/gold/wechat/record?{}'.format(params),
                    'searchUrl'     :        BACK_PRE+'/gold/wechat/record',
                    'STATIC_LAYUI_PATH':       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH':       STATIC_ADMIN_PATH,
                    'startDate'     :        startDate,
                    'endDate'       :        endDate
        }
        return template('admin_gold_wechat_record',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/gold/get_yuanbao_gold_value')
def get_yuanbao_gold_value(redis,session):
    user_current_gold_sum = get_all_users_gold_coin(redis)
    user_current_yuanbao_sum = get_yuanbao_quantity(redis)
    from model.goldModel import get_tool_price,transfer_into_RMB
    tool_price = get_tool_price()
    user_current_gold_sum = transfer_into_RMB(tool_price,'gold',user_current_gold_sum)
    user_current_yuanbao_sum = transfer_into_RMB(tool_price,'yuanbao',user_current_yuanbao_sum)
    user_current_gold_sum = translate_big_number(user_current_gold_sum)
    user_current_yuanbao_sum = translate_big_number(user_current_yuanbao_sum)
    res = [{'gold':user_current_gold_sum,'yuanbao':user_current_yuanbao_sum}]
    return json.dumps({'data':res})

@admin_app.get('/gold/get_user_gold_rank_whole_server')
def get_user_gold_rank_whole_server(redis,session):
    '''
    用于处理获取全服金币排行的请求
    '''  
    from bag.bag_config import bag_redis
    rank_list_of_gold = get_user_gold_rank_in_whole_server(redis)
    res = []
    tool_price = get_tool_price()
    for obj in rank_list_of_gold:
        uid = obj[0]
        gold = transfer_into_RMB(tool_price,'gold',obj[1])
        yuanbao = bag_redis.hget(PLAYER_ITEM_HASH%uid,'3')
        yuanbao = transfer_into_RMB(tool_price,'yuanbao',int(yuanbao))
        if yuanbao == None:
            yuanbao = 0
        user_info = {'user_id':uid,'user_gold':gold,'user_yuanbao':yuanbao}
        res.append(user_info)
    return json.dumps({'data':res})
        

@admin_app.get('/gold/get_user_yuanbao_rank_whole_server')
def get_user_yuanbao_rank_whole_server(redis,session):
    '''
    用于处理获取全服元宝排行的请求
    '''     
    rank_list_of_yuanbao = get_user_yuanbao_rank_in_whole_server(redis)
    res = []
    tool_price = get_tool_price()
    for obj in rank_list_of_yuanbao:     
        uid = obj[0]
        yuanbao = transfer_into_RMB(tool_price,'yuanbao',obj[1])
        gold = redis.hget('users:%s'%uid, 'gold')
        gold = transfer_into_RMB(tool_price,'gold',int(gold))
        user_info = {'user_id':uid,'user_gold':gold,'user_yuanbao':yuanbao}
        res.append(user_info)  
    return json.dumps({'data':res})                      
     

@admin_app.get('/gold/operate_data')
@checkAccess
def get_operate_data(redis,session):
        lang = getLang()
        condition = {}
        isList = request.GET.get('list', '').strip()
        startDate = request.GET.get('startDate', '').strip()
        endDate = request.GET.get('endDate', '').strip()
        if isList:
                condition = {
                        'startDate'         :       startDate,
                        'endDate'         :       endDate
                }
                data_report = get_gold_operate_data(redis,condition)
                return json.dumps(data_report)
        else:
                user_current_gold_sum = '点击刷新获取'
                user_current_yuanbao_sum = '点击刷新获取'
                info = {
                        'title'         :        "运营数据表",
                        'listUrl'                :       BACK_PRE+'/gold/operate_data?list=1',
                        'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                        'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                        'user_current_gold_sum'  :       user_current_gold_sum,
                        'user_current_yuanbao_sum' : user_current_yuanbao_sum
                }
                return template('admin_gold_operate_data',lang=lang,info=info,RES_VERSION=RES_VERSION)

@admin_app.get('/gold/active_player_data')
@checkAccess
def active_player_data(redis,session):
    lang = getLang()
    condition = {}
    isList = request.GET.get('list', '').strip()
    startDate = request.GET.get('startDate', '').strip()
    endDate = request.GET.get('endDate', '').strip()
    if isList:
            condition = {
                    'startDate'         :       startDate,
                    'endDate'         :       endDate
            }
            data_report = get_active_player_data(redis,condition)
            return json.dumps(data_report)
    else:
            info = {
                    'listUrl'                :       BACK_PRE+'/gold/active_player_data?list=1',
                    'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            }
            return template('admin_gold_active_player',lang=lang,info=info,RES_VERSION=RES_VERSION)
    

@admin_app.get('/gold/update_special_value')
def update_special_value(redis,session):
    lang = getLang()
    data_date = request.GET.get('data_date', '').strip()
    value =  request.GET.get('value', '').strip()
    table_type =  request.GET.get('table_type', '').strip()
    update_special_fee_in_db(value,data_date,table_type)
    user_current_gold_sum = '点击刷新获取'
    user_current_yuanbao_sum = '点击刷新获取'

    if '0' == table_type: 
        info = {
                'title'         :        "运营数据表",
                'listUrl'                :       BACK_PRE+'/gold/operate_data?list=1',
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'user_current_gold_sum'  :       user_current_gold_sum,
                'user_current_yuanbao_sum' : user_current_yuanbao_sum
                }    
        return template('admin_gold_operate_data',lang=lang,info=info,RES_VERSION=RES_VERSION)            

    elif '1' == table_type:
            info = {
                    'listUrl'                :       BACK_PRE+'/gold/active_player_data?list=1',
                    'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            }
            return template('admin_gold_active_player',lang=lang,info=info,RES_VERSION=RES_VERSION)        


@admin_app.get('/gold/ai_config')
@checkAccess
def ai_config(redis,session):
    lang = getLang()    
    game_id = request.GET.get('game_id', '').strip()
    

    info = {
        'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
        'url_pre'                    :       '/admin/gold/ai_config'
    }
    if game_id:
        original_arguments = get_ai_config_value(redis,game_id)
        return template('admin_gold_level_d_robot_setting_input',lang=lang,info=info,RES_VERSION=RES_VERSION,game_id=game_id,\
        original_arguments=original_arguments)
    else:
        return template('admin_gold_level_d_robot_setting',lang=lang,info=info,RES_VERSION=RES_VERSION)

@admin_app.post('/gold/ai_config')
@checkAccess
def ai_config(redis,session):
    game_id = request.forms.get('game_id', '')
    field_pre = "ai_config"
    value_list = []
    for i in range(0,6):
        member = [i]
        for j in range(0,3):
            field_name = 'ai_config_%s_%s' % (i,j)
            field_value = request.forms.get(field_name, '').strip()
            member.append(float(field_value))
        value_list.append(member)

    save_playid_gold(redis,game_id,value_list)
    return "<h1>保存成功<h1>"

@admin_app.post('/gold/robot_good_hand')
@admin_app.get('/gold/robot_good_hand')
@checkAccess
def robot_good_hand(redis, session):
    lang = getLang()
    print 'robot_good_hand',request.forms.getall(None)
    # op = request.forms.get('op', '')
    op = request.query.get('op','')
    # isList = request.forms.get('isList', '')
    isList = request.query.get('isList', '')
    game_id = request.forms.get('game_id', '559')
    robot_level = request.forms.get('robot_level', 'C')
    tile_type = request.forms.get('tile_type', '')
    tile_type_per = request.forms.get('tile_type_per', '')
    log_debug('robot_good_hand params game_id[%s] robot_level[%s] op[%s] tile_type[%s] tile_type_per[%s] isList[%s] forms[%s] '%(game_id, robot_level, op, tile_type, tile_type_per, isList, request.forms.getall(None)))
    info = {
        'title'                  :        "C档AI转换及好牌概率配置",
        'gameId'                 :        game_id,
        'robotLevel'             :        robot_level,
        'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
        'listUrl'                :       '/admin/gold/robot_good_hand?isList=1',
        'submitUrl'              :       '/admin/gold/robot_switch',
        'addUrl'                 :       '/admin/gold/robot_good_hand',
        'modifyUrl'              :       '/admin/gold/robot_good_hand?op=mod',
        'deleteUrl'              :       '/admin/gold/robot_good_hand?op=del',
    }
    if op:
        if op == 'add':
            tile_type = request.forms.get('tile_type', '')
            tile_type_per = request.forms.get('tile_type_per', '')
            set_robot_good_hand_rule(redis, game_id, robot_level, tile_type, tile_type_per)
        elif op == 'mod':
            old_tile_type = request.query.get('old_tile_type', '')
            new_tile_type = request.query.get('new_tile_type', '')
            old_tile_type_per = request.query.get('old_tile_type_per', '')
            new_tile_type_per = request.query.get('new_tile_type_per', '')
            set_robot_good_hand_rule(redis, game_id, robot_level, old_tile_type, new_tile_type_per, new_tile_type, new_tile_type_per)
        elif op == 'del':
            tile_type = request.query.get('tile_type', '')
            tile_type_per = request.query.get('tile_type_per', '')
            redis.hdel(ROBOT_GOOD_HAND_RULE % (game_id, robot_level), tile_type)
        # report = get_robot_good_hand_rule(redis, game_id, robot_level)
        # return json.dumps(report)
    elif isList:
        report = get_robot_good_hand_rule(redis, game_id, robot_level)
        return json.dumps(report)
    
    info.update(get_robot_switch(redis, game_id, robot_level))
    dic = get_robot_good_hand_rule(redis, game_id, robot_level)
    # log_debug('robot_good_hand AAA info[%s] dic[%s]' % ( info, dic) )
    return template('admin_robot_good_hand_rule',info=info,lang=lang,RES_VERSION=RES_VERSION,**dic)


@admin_app.post('/gold/robot_switch')
@checkAccess
def robot_switch(redis, session):
    lang = getLang()
    game_id = request.forms.get('game_id', '559')
    robot_level = request.forms.get('robot_level', 'C')
    switch_per = request.forms.get('switch_per', '')
    set_robot_switch(redis, game_id, robot_level, switch_per)
    
    info = {
        'title'                  :        "C档AI转换及好牌概率配置",
        'gameId'                 :        game_id,
        'robotLevel'             :        robot_level,
        'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
        'listUrl'                :       BACK_PRE + '/admin/gold/robot_good_hand',
        'submitUrl'              :       '/admin/gold/robot_switch',
        'addUrl'                 :       '/admin/gold/robot_good_hand?op=add',
        'modifyUrl'              :       '/admin/gold/robot_good_hand?op=mod',
        'deleteUrl'              :       '/admin/gold/robot_good_hand?op=del',
    }

    info.update(get_robot_switch(redis, game_id, robot_level))
    dic = get_robot_good_hand_rule(redis, game_id, robot_level)
    # log_debug('robot_good_hand BBB info[%s] dic[%s]' % ( info, dic) )
    # return template('admin_robot_good_hand_rule',info=info,lang=lang,RES_VERSION=RES_VERSION,**dic)
    return redirect('/admin/gold/robot_good_hand')


@admin_app.get('/gold/accumulated_value_setting')
@checkAccess
def accumulated_value_setting(redis,session):
    lang = getLang()
    info = {
        'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
    }
    original_info = get_gold_ai_accumulated_value(redis)
    return template('admin_gold_accumulated_value_setting',lang=lang,info=info,RES_VERSION=RES_VERSION,original_info=original_info)

@admin_app.post('/gold/accumulated_value_setting')
def accumulated_value_setting(redis,session):
    ai_ratio_list = ['level_b_ai_radio','level_d_ai_radio','player_radio','initial_accumulated_value']
    ai_ratio_redis_key = {'level_b_ai_radio':'Ai_B_Pct','level_d_ai_radio':'Ai_D_Pct','player_radio':'Player_Pct','initial_accumulated_value':'Default_Pct'}
    ai_ratio_map = {}
    for field_name in ai_ratio_list:
        ai_ratio_map[ai_ratio_redis_key[field_name]] = request.forms.get(field_name, '').strip()
        if ai_ratio_map[ai_ratio_redis_key[field_name]] == '':
            return "<h1>参数错误，保存失败</h1>"
    save_addValue_pct(redis,0,ai_ratio_map)

    range_value_dic = {}
    range_row_set = set()
    for _key in request.forms.keys():
        try:
            _split = _key.split('_')
            if _split[0] == 'accumulated':
                range_row_set.add(_split[1])
        except:
            pass

    range_row_list = []
    for _row in range_row_set:
        input1_value = request.forms.get('accumulated_%s_0' % _row, '').strip()
        input2_value = request.forms.get('accumulated_%s_1' % _row, '').strip()
        input3_value = request.forms.get('accumulated_%s_2' % _row, '').strip()
        sub_list = [input1_value,input2_value,input3_value]
        range_row_list.append(sub_list)
    
    save_RangeValue(redis,range_row_list)            
    return "<h1>保存成功</h1>"

@admin_app.post('/gold/active_players_info')
def active_players_info(redis,session):
    '''
    处理活跃玩家报表信息
    '''    
    pass

def save_playid_gold(redis, gameid, values):
    '''
    保存游戏的每个场次的金币
    :param redis: redis主库
    :param gameid: 游戏id
    :param values: [[1,100,200,100],[2,200,300,100],[3,300,400,100],[4,400,500,100],[5,500,600,100]]
    :param values: [[场次id,最小值,最大值,变化值],[场次id,最小值,最大值,变化值]]
    :return:
    '''
    key1 = 'RobotD:%s:gold:hesh'
    tmpdict = {}
    for _value in values:
        playid = _value[0]
        min_value = _value[1]
        max_value = _value[2]
        variation = _value[3]
        _value = '|'.join(map(lambda x: str(x), [min_value, max_value, variation]))
        tmpdict[playid] = _value
    if tmpdict:
        redis.hmset(key1 % (gameid),tmpdict)

def get_robot_switch(redis, gameid, robot_level):
    '''
    获取转换成机器人的概率
    '''
    switch_per = redis.hget(ROBOT_SWITCH % gameid, robot_level)
    if switch_per is None or switch_per == 'None':
        switch_per = ''
    return {'switch_per': switch_per}

def set_robot_switch(redis, gameid, robot_level, switch_per):
    '''
    获取转换成机器人的概率
    '''
    try:
        if not gameid or not robot_level:
            raise Exception('gameid、 robot_level不能为空')
        switch_per = int(switch_per)
        if switch_per < 0 or switch_per > 100:
            raise Exception('转换概率数值范围:[0-100]')
        redis.hset(ROBOT_SWITCH % gameid, robot_level, switch_per)
    except Exception, e:
        log_debug('set_robot_switch failed gameid[%s] robot_level[%s] switch_per[%s] error[%s]'%(gameid, robot_level, switch_per, e))


def get_robot_good_hand_rule(redis, gameid, robot_level):
    '''
    获取机器人获取的好牌及概率配置
    '''
    robot_good_hand_rule = redis.hgetall(ROBOT_GOOD_HAND_RULE % (gameid, robot_level))
    print 'robot_good_hand_rule', robot_good_hand_rule
    if robot_good_hand_rule is None or robot_good_hand_rule == 'None':
        robot_good_hand_rule = {}
    res = []
    for k, v in robot_good_hand_rule.items():
        info = {}
        info['tile_type'] = k
        info['tile_type_per'] = v
        res.append(info)
    return {"count":len(res),"data":res}

def set_robot_good_hand_rule(redis, gameid, robot_level, tile_type, tile_type_per, new_tile_type = None, new_tile_type_per = None):
    '''
    获取机器人获取的好牌及概率配置
    '''
    try:
        if not gameid or not robot_level:
            raise Exception('gameid、 robot_level不能为空')
        
        tile_type = checkTileType(tile_type)
        new_tile_type = checkTileType(new_tile_type)
        if not tile_type or ( not new_tile_type and new_tile_type_per):
            raise Exception('tile_type不能为空，或者修改时new_tile_type不能为空')
        
        tile_type_per = int(tile_type_per)
        if tile_type_per < 0 or tile_type_per > 100:
            raise Exception('好牌概率数值范围:[0-100]')
        if new_tile_type_per is not None:
            new_tile_type_per = int(new_tile_type_per)
            if new_tile_type_per < 0 or new_tile_type_per > 100:
                raise Exception('好牌概率数值范围:[0-100]')
            else:
                if new_tile_type != tile_type and redis.hexists(ROBOT_GOOD_HAND_RULE % (gameid, robot_level),new_tile_type):
                    raise Exception('new_tile_type[%s]已经存在，防止覆盖，可以前往修改，或删除'%new_tile_type)
                
                redis.hdel(ROBOT_GOOD_HAND_RULE % (gameid, robot_level), tile_type)
                tile_type = new_tile_type
                tile_type_per = new_tile_type_per
        else:
            if redis.hexists(ROBOT_GOOD_HAND_RULE % (gameid, robot_level),tile_type):
                raise Exception('tile_type[%s]已经存在'%tile_type)
        redis.hset(ROBOT_GOOD_HAND_RULE % (gameid, robot_level), tile_type, tile_type_per)
    except Exception, e:
        log_debug('set_robot_good_hand_rule failed gameid[%s] robot_level[%s] tile_type[%s] tile_type_per[%s] new_tile_type[%s] new_tile_type_per[%s] error[%s]'%(gameid, robot_level, tile_type, tile_type_per, new_tile_type, new_tile_type_per, e))

def checkTileType(tile_type):
    if not tile_type:
        return tile_type
    target_tile_type_set = set(['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'])
    tile_type_set = set(tile_type)
    for invalid_tile in tile_type_set - target_tile_type_set:
        tile_type = tile_type.replace(invalid_tile,'')
    
    tile_type_dict = Counter(tile_type)
    for tile, tileCnt in tile_type_dict.items():
        if tileCnt > 4:
            return None
    # if tile_type_set - target_tile_type_set:
    #     return False
    # return True
    tile_type = list(tile_type)
    tile_type.sort()
    tile_type = ''.join(tile_type)
    return tile_type

def save_addValue_pct(redis, gameid, values):
    '''
    保存游戏累计值比例
    :param redis:redis主库
    :param gameid:游戏id
    :param values: {'Ai_B_Pct':0.02,'Ai_D_Pct':0.02,'Player_Pct':0.03,'Default_Pct':0.04}
    :return:
    '''
    import traceback
    key2 = 'RobotD:AddValue:hesh'
    for _key in values.keys():
        try:
            values[_key] = float(values[_key])
        except Exception as error:
            traceback.print_exc()
            return
    redis.hmset(key2, values)

def save_RangeValue(redis, values):
    '''
    保存累计值对应的概率
    :param redis: redis主库
    :param gameid: 游戏id
    :param values: [[100,200,0.1],[500,300,0.2],[300,400,0.3]]
    :return:
    '''
    values = sorted(values,key=lambda x:x[0],reverse=False)
    key3 = 'RobotD:RangeValue:list'
    redis.delete(key3)
    for _value in values:
        start = _value[0]
        end = _value[1]
        pct = _value[2]
        _value = '|'.join(map(lambda x: str(x), [start, end, pct]))
        redis.lpush(key3, _value)

def translate_big_number(num):
    # 把大数字改成以万和亿为单位
    new_num = None
    num = float(num)
    if num > pow(10,8):
        new_num = round(num / pow(10,8), 2)
        new_num = str(new_num) + '亿'
    elif num > pow(10,4):
        new_num = round(num / pow(10,4), 2)
        new_num = str(new_num) + '万'
    return new_num or num

def get_all_users_gold_coin(redis):
    # 统计所有玩家当前的金币数
    user_set = redis.smembers(ACCOUNT4WEIXIN_SET)
    user_current_gold_sum = 0

    from bag.bag_config import bag_redis
    insurance_dic = bag_redis.hgetall(SAVE_BOX_HASH)
    for _key in insurance_dic.keys():
        if 'None' == _key:
            continue
        uid_in = int(_key)
        gold_in = int(insurance_dic[_key])
        # 排除uid是 0到2000的账户
        if int(uid_in) >=0 and int(uid_in) <= 2000:
            continue
        user_current_gold_sum += gold_in	

    for account in user_set:
        user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
        if not user_table:
            continue
        # 排除uid是 0到2000的账户
        uid =  user_table.split(':')[1]
        if int(uid) >=0 and int(uid) <= 2000:
            continue

        gold = redis.hget(user_table, 'gold')
        gold = int(gold) if gold else 0
        user_current_gold_sum += gold
    return user_current_gold_sum    

def get_yuanbao_quantity(redis):
    # 统计所有玩家当前元宝数
    from bag.bag_config import bag_redis
    user_current_yuanbao_sum = 0
    user_set = redis.smembers(ACCOUNT4WEIXIN_SET)
    
    for user in user_set:
        account2user_table = FORMAT_ACCOUNT2USER_TABLE%(user)
        userTable = redis.get(account2user_table)
        if not userTable:
            continue
        uid = userTable.split(':')[1]
        # 排除uid是 0到2000 的账户
        if int(uid) >=0 and int(uid) <= 2000:
            continue

        user_yuanbao = bag_redis.hget(PLAYER_ITEM_HASH%uid,'3')
        if user_yuanbao:
            user_current_yuanbao_sum = user_current_yuanbao_sum + int(user_yuanbao)
            
    return user_current_yuanbao_sum

def get_user_gold_rank_in_whole_server(redis):
    # 得到全服玩家金币的排行
    user_set = redis.smembers(ACCOUNT4WEIXIN_SET)
    from bag.bag_config import bag_redis
    insurance_dic = bag_redis.hgetall(SAVE_BOX_HASH)
    uid_gold_list = []
    for account in user_set:
        user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
        if not user_table:
            continue
        # 排除uid是 0到2000的账户
        uid =  user_table.split(':')[1]
        if int(uid) >=0 and int(uid) <= 2000:
            continue

        gold = redis.hget(user_table, 'gold')
        gold = int(gold) if gold else 0
        # 加上宝箱
        if insurance_dic.has_key(uid):
            gold += int(insurance_dic[uid])
        uid_gold_list.append((uid,gold))
    # 排序
    list_after_rank =  sorted(uid_gold_list, key=lambda s: s[1],reverse=True)
    return list_after_rank[0:10]

def get_user_yuanbao_rank_in_whole_server(redis):
    """
        得到全服玩家元宝排行
    """
    from bag.bag_config import bag_redis
    user_set = redis.smembers(ACCOUNT4WEIXIN_SET)
    
    uid_yuanbao_list = []
    for user in user_set:
        account2user_table = FORMAT_ACCOUNT2USER_TABLE%(user)
        userTable = redis.get(account2user_table)
        if not userTable:
            continue
        uid = userTable.split(':')[1]
        # 排除uid是 0到2000 的账户
        if int(uid) >=0 and int(uid) <= 2000:
            continue

        user_yuanbao = bag_redis.hget(PLAYER_ITEM_HASH%uid,'3')
        if user_yuanbao:
            user_yuanbao = int(user_yuanbao)
            uid_yuanbao_list.append((uid,user_yuanbao))
    # 排序
    list_after_rank =  sorted(uid_yuanbao_list, key=lambda s: s[1],reverse=True)
    return list_after_rank[0:10]