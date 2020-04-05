# -*- coding:utf-8 -*-
# !/usr/bin/python

"""
     金币场数据模型

"""
import time
import json
import random
from common.log import log_debug
from gold_db_define import *
from web_db_define import *
import uuid
import copy
import redis
import traceback
from datetime import datetime, timedelta, date
from common.utilt import ServerPagination
from common import encrypt_util,convert_util
from red_envelope_db_define import *
from common.record_player_info import record_player_balance_change

def get_uuid():
    return uuid.uuid4().hex

def getPrivateRedisInst(redisdb, gameid):
    """
        获取redis连接实例
    """
    try:
        if not redisdb.exists(GAME2REDIS % gameid):
            return None
        info = redisdb.hgetall(GAME2REDIS % gameid)
        ip = info['ip']
        passwd = info['passwd']
        port = int(info['port'])
        dbnum = int(info['num'])
        redisdb = redis.ConnectionPool(host=ip, port=port, db=dbnum, password=passwd)
        return redis.Redis(connection_pool=redisdb)
    except:
        traceback.print_exc()
        return None


def calculateTotalWelfareFee(redis,fee,fee_type,currency):
    # 计算所有福利支出，包括签到、分享、破产、新手礼包、累计奖励、元宝低保、宝箱任务
    fee_type_str_map = {0:'sign',1:'share',2:'bankrupt',3:'new_player_present',4:'7_day_reward',5:'15_day_reward',6:'one_month',7:'vcoin_baselive',8:'baoxiang_task'}
    # 货币类型 0：金币，1：元宝 ，2，背包
    currency_type_str_map = {0:'gold',1:'vcoin',2:'bag'}
    date_str = time.strftime("%Y-%m-%d")
    r_key = WELFARE_DAILY_FEE % (date_str,currency_type_str_map[currency],fee_type_str_map[fee_type])
    redis_db = get_db(8)
    redis_db.incrby(r_key,fee)


def get_user_info(redis, account):
    info = {}
    """ 获取玩家信息"""
    user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
    if not user_table:
        return info
    info = redis.hgetall(user_table)
    info['uid'] = user_table.split(':')[1]
    return info


def sendProtocolResult2Web(redis, _uuid, proto):
    """
        发送处理结果
    """
    redis.set(RESULT_GOLD_SERVICE_PROTOCOL % _uuid, json.dumps(proto))
    redis.expire(RESULT_GOLD_SERVICE_PROTOCOL % _uuid, 5)


def getProtocolResultFromGold(redis, _uuid, timeout=5):
    """ 
        gold server 结果消息返回
    """
    while timeout > 0:
        key = RESULT_GOLD_SERVICE_PROTOCOL % _uuid
        if redis.exists(key):
            return json.loads(redis.get(key))
        time.sleep(0.1)
        timeout = timeout - 0.1


def get_GoldGameList(redis):
    """
    获取金币场场次
    """
    res = []

    NowTime = datetime.now()
    hour = NowTime.strftime("%H")

    for gameid in redis.smembers(GOLD_GAMEID_SET):
        list = PARTY_GOLD_GAME_LIST.get(gameid, PARTY_GOLD_GAME_LIST.get('default'))
        data = copy.deepcopy(list)

        for item in data:
            online = 0
            if gameid == '555':
                item['gameName'] = '经典牛牛'
            elif gameid == '666':
                item['gameName'] = '欢乐牛牛'
            elif gameid == '556':
                item['gameName'] = '明牌牛牛'
            elif gameid == '444':
                item['gameName'] = '搜集游棋牌麻将'
            elif gameid == '559':
                item['gameName'] = '跑得快'
            elif gameid == '557':
                item['gameName'] = '欢乐拼点'
                item['hasOwner'] = '1' # 支持好友开房
            elif gameid == '449':
                item['gameName'] = '二人麻将'
                if item['id'] == 5:
                    item['honor_matching'] = {
                        'gameid':'701',
                        'name':'荣誉场',
                        'msg':'二人麻将随机匹配',
                        'type':'0',
                    }
                    item['honor_team'] = {
                        'gameid':'701',
                        'name':'荣誉场',
                        'msg':'二人麻将好友组房',
                        'type':'1',
                    }
            elif gameid == '560':
                item['gameName'] = '斗地主'
            elif gameid == '452':
                item['gameName'] = '鸡大胡麻将'
            elif gameid == '562':
                item['gameName'] = '十三水'
            elif gameid == '570':
                item['gameName'] = '框架测试'

            if PARTY_GOLD_GAME_ONLINE_NUM_LIST.has_key(gameid) and \
                    PARTY_GOLD_GAME_ONLINE_NUM_LIST[gameid].has_key(hour) and \
                    PARTY_GOLD_GAME_ONLINE_NUM_LIST[gameid][hour].has_key(str(item['id'])):
                if redis.exists(GOLD_ONLINE_NUM_CACHE_KEY % (gameid, item['id'])):
                    online = redis.get(GOLD_ONLINE_NUM_CACHE_VALUE % (gameid, item['id']))
                    online = int(online) if online else 0
                else:
                    first = PARTY_GOLD_GAME_ONLINE_NUM_LIST[gameid][hour][str(item['id'])][0]
                    last = PARTY_GOLD_GAME_ONLINE_NUM_LIST[gameid][hour][str(item['id'])][1]
                    _online = redis.get(GOLD_ONLINE_NUM_CACHE_VALUE % (gameid, item['id']))
                    if _online:
                        # 最大变化值不能大于15
                        _online = int(_online)
                        if first <= _online and last >= _online:
                            first = _online - 15 if _online > first + 15 else first
                            last = _online + 15 if last > _online + 15 else last
                    print 'test *****************  {0} {1}'.format(first, last)
                    online = random.choice(range(first, last))
                    redis.set(GOLD_ONLINE_NUM_CACHE_KEY % (gameid, item['id']), "")
                    redis.set(GOLD_ONLINE_NUM_CACHE_VALUE % (gameid, item['id']), online)
                    redis.expire(GOLD_ONLINE_NUM_CACHE_KEY % (gameid, item['id']), random.choice(range(60, 300)))

            online += int(redis.scard(GOLD_ONLINE_PLAYID_ACCOUNT_SET % (gameid, item['id'])))
            item['online'] = online
        res.append({'gameid': gameid, 'config': data})
    return res





LIST_CACHE_MAXNUM = 10000
LIST_CACHE_TTL = 5*60


def get_user_field(redis, prredis, account):
    user_info = get_user_info(redis, account)
    if not user_info:
        return
    agentid = user_info['parentAg']
    reg_date = user_info['reg_date']
    last_login_date = user_info['last_login_date']
    uid = user_info['uid']
    gold = user_info.get('gold', '')
    roomcard = redis.get(USER4AGENT_CARD % (agentid, uid))
    gold_user_table = GOLD_USER_TABLE % account
    gold_dic = prredis.hgetall(gold_user_table)
    if not gold_dic:
        gold_dic['nickname'] = user_info['nickname']
        gold_dic['uid'] = uid
        gold_dic['agent'] = agentid
        gold_dic['account'] = account
    gold_dic['cur_diamond_num'] = roomcard
    gold_dic['first_log_date'] = reg_date
    gold_dic['last_log_date'] = last_login_date
    # gold_dic['buy_diamond_stream'] = 'buy_record?account=%s' % account
    gold_dic['buy_gold_stream'] = 'buy_record?account=%s' % account
    gold_dic['gold_record_stream'] = 'journal?account=%s' % account
    money = prredis.get(GOLD_BUY_RECORD_ACCOUNT_MOENY_SUM % account)
    if money:
        money = float(money) / 100
    gold_dic['buy_gold_num'] = money
    if not gold_dic.get('agent', ''):
        gold_dic['agent'] = agentid
    # 财富排行
    rank = prredis.zrevrank(GOLD_MONEY_RANK_WITH_AGENT_ZSET % gold_dic['agent'],
                            account)
    if rank != None:
        gold_dic['agent_wealth_rank'] = int(rank) + 1
    else:
        gold_dic['agent_wealth_rank'] = u'无'
    # 胜局排行
    rank = prredis.zrevrank(GOLD_WIN_RANK_WITH_AGENT_ZSET % gold_dic['agent'],
                            account)
    if rank != None:
        gold_dic['agent_win_rank'] = int(rank) + 1
    else:
        gold_dic['agent_win_rank'] = u'无'
    # 胜率
    win = prredis.llen(GOLD_RECORD_ACCOUNT_WIN_LIST % account)
    total = prredis.llen(GOLD_RECORD_ACCOUNT_TOTAL_LIST % account)
    if total:
        gold_dic['gold_win_rate'] = '%.2f' % (win / float(total) * 100 if total else 0)
    gold_dic['cur_gold_num'] = gold
    return gold_dic


def getGoldListInfos(redis, search, page_size, page_num):
    """
        获取金币场用户数据
    """
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)

    '''
    # 如果缓存存在则直接去缓存中取数据
    if not search and redis.exists('gold:data:cache'):
        data = redis.get('gold:data:cache')
        data_list = json.loads(data)
        count = len(data_list)
        return {'total': count, 'result': data_list}
    '''

    # 微信集合
    weixin_sets = prredis.smembers(GOLD_ACCOUNT_SET_TOTAL)
    weixin_sets = weixin_sets | redis.smembers(ACCOUNT4WEIXIN_SET)
    data_list =[]
    if search:
        if search not in weixin_sets:
            return {'total': 0, 'result': []}
        gold_dic = get_user_field(redis, prredis, search)
        if gold_dic:
            data_list.append(gold_dic)
        return {'total': len(gold_dic), 'result': data_list}

    total_count = len(weixin_sets)
    weixin_sets = ServerPagination(weixin_sets, page_size, page_num)
    # 遍历微信集合，从对应表中取出数据字典放入data列表中
    for account in weixin_sets:
        gold_dic = get_user_field(redis, prredis, account)
        if gold_dic:
            data_list.append(gold_dic)

    '''
    # 如果大于10000条数据做一个金币用户表data缓存
    if count >= LIST_CACHE_MAXNUM:
        data_cache = json.dumps(data_list)
        redis.set('gold:data:cache', data_cache)
        # 缓存5分钟
        redis.expire('gold:data:cache', LIST_CACHE_TTL) 
    '''
    return {'total': total_count, 'result': data_list}


# 金币场运营表
def getGoldOperateInfos(redis,selfUid,startDate,endDate,niuniu_type):
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
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
        gameid = niuniu_type
        if prredis.exists(GOLD_OPERATE % (gameid, dateStr)):
            info = prredis.hgetall(GOLD_OPERATE % (gameid, dateStr))
            info['online_user_max'] = redis.hget(GOLD_ONLINE_MAX_ACCOUNT_TABLE % (gameid, dateStr), 'count')
            info['date'] = dateStr
            info['buy_gold_total'] = redis.get(DAILY_GOLD2_SUM % dateStr)
            info['buy_money'] = redis.get(DAILY_GOLD2_MONEY_SUM % dateStr)
            info['buy_money'] = float(info['buy_money']) / 100 if info['buy_money'] else 0
            info['buy_gold_count'] = redis.scard(DAILY_USER_GOLD2_SET % dateStr)
            info['buy_gold_people_num'] = 'buy_record_info?date=%s' % dateStr
            room_num = 0
            if datetime.now().strftime("%Y-%m-%d") == dateStr:
                info['online_user'] = redis.scard(GOLD_ONLINE_ACCOUNT_SET % gameid)
                for roomid in redis.smembers(GOLD_ONLINE_ROOM_SET % gameid):
                    room_table = ROOM2SERVER % roomid
                    pl_count = redis.hget(room_table, 'playerCount')
                    if not pl_count or pl_count <= '0':
                        continue
                    room_num += 1
                info['room_count'] = room_num
            res.append(info)
        endDate -= deltaTime
    return {"count": 1, "data": res}



# 金币场运营表在线人数及在线房间数
def getOnlineOperateInfos(redis):
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
    # 总当前在线人数
    online_people_sum = redis.scard(GOLD_ONLINE_ACCOUNT_SET_TOTAL)
    # 当前在线房间数
    online_room_num = 0
    for roomid in redis.smembers(GOLD_ONLINE_ROOM_SET_TOTAL):
        room_table = ROOM2SERVER % roomid
        pl_count = redis.hget(room_table, 'playerCount')
        if not pl_count or pl_count == '0':
            continue
        online_room_num += 1
    # online_room_num = redis.scard(GOLD_ONLINE_ROOM_SET_TOTAL)
    # 当前玩家金币总数
    user_current_gold_sum = 0
    for account in prredis.smembers(GOLD_ACCOUNT_SET_TOTAL):
        user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
        if not user_table:
            continue
        gold = redis.hget(user_table, 'gold')
        gold = int(gold) if gold else 0
        user_current_gold_sum += gold
    return online_people_sum, online_room_num, user_current_gold_sum

# 金币场在线AI总数及在线AI房间数
def getOnlineAIInfos(redis):
    online_ai_sum = 0
    cur_ai_gold_sum = 0
    online_ai_room_num_set = set()
    for key in redis.smembers('users:robot:accounts:set'):
        online, account, gold= redis.hmget(key, 'isOnline', 'account', 'gold')
        gold = int(gold) if gold else 0
        cur_ai_gold_sum += gold
        if online == '1':
            online_ai_sum += 1
            if redis.exists(GOLD_ROOM_ACCOUNT_KEY % account):
                online_ai_room_num_set.add(redis.get(GOLD_ROOM_ACCOUNT_KEY % account))
    return online_ai_sum, len(online_ai_room_num_set), cur_ai_gold_sum

# 金币场AI数据总表
def getGoldAIInfos(redis,selfUid,startDate,endDate,grade):
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
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
        info = {}
        join_ai_sum = prredis.scard(GOLD_AI_ACCOUNT_SET_BYDAY % dateStr)
        if join_ai_sum:
            ai_room_sum = prredis.scard(GOLD_AI_ROOM_SET_BYDAY % dateStr)
            ai_gold_sum = prredis.llen(GOLD_AI_RECORD_LIST_BYDAY % dateStr)
            info['date'] = dateStr
            info['join_ai_sum'] = join_ai_sum
            info['ai_room_sum'] = ai_room_sum
            info['ai_gold_sum'] = ai_gold_sum
            info['cur_ai_gold_num'] = redis.get('robot:gold:sum:%s' % dateStr)
            res.append(info)
        endDate -= deltaTime

    return {"count": len(res), "data": res}


def saveBuyGoldRecord(redis, account, data):
    """ 
        保存金币流水
    """
    try:
        if not redis.sismember(GOLD_ACCOUNT_SET_TOTAL, account):
            redis.sadd(GOLD_ACCOUNT_SET_TOTAL, account)
        prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
        num = prredis.incr(GOLD_BUY_RECORD_COUNT_TABLE)
        record_key = GOLD_BUY_RECORD_TABLE % num
        pipe = prredis.pipeline()
        data['account'] = account
        pipe.hmset(record_key, data)
        pipe.expire(record_key, GOLD_ROOM_MAX_TIME)
        pipe.lpush(GOLD_BUY_RECORD_ACCOUNT_LIST % account, record_key)
        pipe.lpush(GOLD_BUY_RECORD_LIST_TOTAL, record_key)
        pipe.incr(GOLD_BUY_RECORD_ACCOUNT_GOLD_SUM % account, data['gold'])
        pipe.incr(GOLD_BUY_RECORD_ACCOUNT_MOENY_SUM % account, data['money'])
        pipe.execute()
        user_info = get_user_info(redis, account)
        if not user_info:
            return
        agentid = user_info['parentAg']
        gold = user_info['gold']
        prredis.zadd(GOLD_MONEY_RANK_WITH_AGENT_ZSET % agentid, account, gold)
    except Exception, ex:
        traceback.print_exc()


def player_add_gold(redis, account, gold, card=None,yuanbao=None):
    user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
    if not user_table:
        return
    redis.hincrby(user_table, 'gold', gold)
    user_info = get_user_info(redis, account)
    if not user_info:
        return
    agentid = user_info['parentAg']
    if card:
        redis.incrby(USER4AGENT_CARD % (agentid, user_info['uid']), card)
    if yuanbao:
        acc = redis.get('users:account:%s' % account)
        if acc:
            uid = acc.split(':')[1]
            from bag.bag_func import give_player_item
            give_player_item(3, uid, yuanbao)
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
    if not prredis:
        return
    gold = user_info['gold']
    prredis.zadd(GOLD_MONEY_RANK_WITH_AGENT_ZSET % agentid, account, gold)
    return True


def player_set_gold(redis, account, gold):
    user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
    if not user_table:
        return
    redis.hset(user_table, 'gold', gold)

    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
    user_info = get_user_info(redis, account)
    if not user_info:
        return
    agentid = user_info['parentAg']
    gold = user_info['gold']
    prredis.zadd(GOLD_MONEY_RANK_WITH_AGENT_ZSET % agentid, account, gold)

    return True

def get_signGold4Date( date):
    """
        检查该日期所能获得的金币数
    """
    dateStr = datetime.strptime(date, "%Y-%m-%d")
    def_gold = WELFARE_CONFIG['defaultGold']
    dateNumStr = str(convert_util.to_int(dateStr.strftime("%d")))
    special_gold = WELFARE_CONFIG_SPECIAL_DATE2GOLD.get(dateNumStr, "")
    return special_gold or def_gold

def do_PlayerWelfareSign(redis, account):
    """
        签到接口
    """
    today = datetime.now().strftime("%Y-%m-%d")
    key = WELFARE_USER_SIGN % (account, today)
    if redis.exists(key):
        return

    gold = get_signGold4Date(today)
    isPaySuccess = player_add_gold(redis, account, gold)
    if not isPaySuccess:
        return
    redis.set(key, 1)
    return gold

def do_PlayerWelfareShare(redis, account):
    """
        分享接口
    """

    gold = 2000
    key = GOLD_WELFARE_SHARE % (account)
    today = datetime.now().strftime("%Y-%m-%d")
    if redis.get(key) == today:
        return {'code': 1, 'msg': "今天已经分享过"}
    redis.set(key, today)
    player_add_gold(redis, account, gold)
    return {'code': 0, 'msg': u"恭喜您，获得分享奖励%s金币" % gold,'gold':gold}

def doPatchSign(redis, account, groupId, id, user_table):
    '''
        补签接口
        补签需要消耗3000金币    
        （原来是消耗2钻石，如果需要改回钻石，可以使用doPatchSign_old 方法。）   
    '''
    # gold_fee补签的费用
    gold_fee = PATCH_SIGN_FEE
    user_info = get_user_info(redis, account)
    uid = user_info['uid']
    agentid = user_info['parentAg']    
    user_gold = redis.hget(user_table, 'gold')
    user_gold = int(user_gold) if user_gold else 0

    month = datetime.now().strftime('%m')

    # 获取第一个未签到的天数
    date = ""
    testDate = first_day_of_month()
    for i in xrange( int( datetime.now().strftime("%d") ) ):

        testDateString = testDate.strftime("%Y-%m-%d")

        if not redis.exists(WELFARE_USER_SIGN % (account, testDateString)) \
                and not redis.sismember(WELFARE_USER_PATCH_SIGN % (account, month), testDateString):
            date = testDateString
            break
        testDate += timedelta(1)

    if not date :
        return {'code': 1, 'msg': "没有需要补签的日期"}

    if gold_fee > user_gold :
        return {'code': 1, 'msg': "金币不足，无法补签"}

    key = WELFARE_USER_PATCH_SIGN % (account, month)

    if redis.sismember(key, date):
        return {'code': 1, 'msg': "已补签过"}

    times = redis.scard(key)
    # 每月补签次数是否达到上限
    if times and int(times) > PATCH_SIGN_MAX:
        return {'code': 1, 'msg': "当月补签已达上限"}

    # 获取签到奖励的金币,以及扣除金币费用
    gold = get_signGold4Date(date)
    gold_diff = gold - gold_fee
    isPaySuccess = player_add_gold(redis, account, gold_diff)
    if not isPaySuccess:
        return {'code': 1, 'msg': "补签失败，请稍后重试"}      

    # 成功补签
    redis.sadd(key, date)
    # remove = convert_util.to_int(PATCH_SIGN_FEE)
    # redis.incrby(USER4AGENT_CARD % (groupId, id), -remove)
    patchSignTimes = redis.scard(key)
    user_table = 'users:%s' % id
    from bag.bag_config import bag_redis
    
    record_player_balance_change(bag_redis,user_table,2,-gold_fee,user_gold-gold_fee,34)
    record_player_balance_change(bag_redis,user_table,2,gold,user_gold-gold_fee+gold,35)
    tips = "{0} 补签成功, 获得{1}金币, 剩余补签次数{2}".format(date, gold, PATCH_SIGN_MAX - int(patchSignTimes))
    return {'code': 0, 'msg': tips, 'signDate': date, 'patchsign_times':patchSignTimes, 'patchsign_max': PATCH_SIGN_MAX}          

def doPatchSign_old(redis, account, groupId, id):
    """
        补签接口
        补签需要消耗2张钻石
    """
    user_info = get_user_info(redis, account)
    uid = user_info['uid']
    agentid = user_info['parentAg']
    roomcard = redis.get(USER4AGENT_CARD % (agentid, uid))
    roomcard = int(roomcard) if roomcard else 0

    month = datetime.now().strftime('%m')

    # 获取第一个未签到的天数
    date = ""
    testDate = first_day_of_month()
    for i in xrange( int( datetime.now().strftime("%d") ) ):

        testDateString = testDate.strftime("%Y-%m-%d")

        if not redis.exists(WELFARE_USER_SIGN % (account, testDateString)) \
                and not redis.sismember(WELFARE_USER_PATCH_SIGN % (account, month), testDateString):
            date = testDateString
            break
        testDate += timedelta(1)

    if not date :
        return {'code': 1, 'msg': "没有需要补签的日期"}

    if roomcard < PATCH_SIGN_FEE:
        return {'code': 1, 'msg': "钻石不足"}


    key = WELFARE_USER_PATCH_SIGN % (account, month)

    if redis.sismember(key, date):
        return {'code': 1, 'msg': "已补签过"}

    times = redis.scard(key)
    # 每月补签次数是否达到上限
    if times and int(times) > PATCH_SIGN_MAX:
        return {'code': 1, 'msg': "当月补签已达上限"}

    # 获取签到奖励的金币
    gold = get_signGold4Date(date)
    isPaySuccess = player_add_gold(redis, account, gold)
    if not isPaySuccess:
        return {'code': 1, 'msg': "补签失败，请稍后重试"}

    # 成功补签
    redis.sadd(key, date)
    remove = convert_util.to_int(PATCH_SIGN_FEE)
    redis.incrby(USER4AGENT_CARD % (groupId, id), -remove)
    patchSignTimes = redis.scard(key)
    tips = "{0} 补签成功, 获得{1}金币, 剩余补签次数{2}".format(date, gold, PATCH_SIGN_MAX - int(patchSignTimes))
    return {'code': 0, 'msg': tips, 'signDate': date, 'patchsign_times':patchSignTimes, 'patchsign_max': PATCH_SIGN_MAX}


def doWelfareById(redis, uid, account, id):
    """ 
        福利
    """
    today = datetime.now().strftime("%Y-%m-%d")
    state = MESSION_STATUS_OVER
    if id == '2':
        playerCoin = redis.hget(FORMAT_USER_TABLE % uid, 'gold')
        playerCoin = int(playerCoin) if playerCoin else 0
        from bag.bag_config import bag_redis
        box_gold = bag_redis.hget(SAVE_BOX_HASH,uid)
        box_gold = int(box_gold) if box_gold else 0
        playerCoin =  playerCoin + box_gold
        if int(playerCoin) >= SIGN_LINE:
            return {'code': 1, 'msg': u'未达到低保线无法领取'}
        key = WELFARE_USER_INSURANCE % (account, today)
        if redis.llen(key) >= SIGN_MAX:
            return {'code': 1, 'msg': u'已经领取了 {0} 次'.format(SIGN_MAX)}
        redis.lpush(key, SIGN_COINNUM)
        player_add_gold(redis, account, SIGN_COINNUM)
        if redis.llen(key) >= SIGN_MAX:
            state = MESSION_STATUS_OVER
        else:
            state = MESSION_STATUS_NO
        return {'code': 0, 'msg': u'恭喜您，获得补助%s金币' % SIGN_COINNUM, 'id': id, 'state': state,'gold':int(SIGN_COINNUM)}
    elif id == '1':
        # 新手礼包
        coin = 20000
        card = 0
        if redis.hget(GOLD_REWARD_NEW_PRESENT_HASH, account) == MESSION_STATUS_OVER:
            return {'code': 1, 'msg': u'您已领取，无法再次领取'}
        redis.hset(GOLD_REWARD_NEW_PRESENT_HASH, account, MESSION_STATUS_OVER)
        player_add_gold(redis, account, coin, card)
        return {'code': 0, 'msg': u'恭喜您，获得新手礼包%s金币' % coin, 'id': id, 'state': state,'gold':int(coin)}
    elif id == '0':
        # 每日首冲奖励
        if not redis.sismember(DAILY_USER_GOLD2_SET % today, account):
            return {'code': 1, 'msg': u'您今日还未完成首冲'}
        elif redis.hget(GOLD_REWARD_DAY_BUY_GOLD_HASH % today, account) == MESSION_STATUS_OVER:
            return {'code': 1, 'msg': u'您已领取，无法再次领取'}
        redis.hget(GOLD_REWARD_DAY_BUY_GOLD_HASH % today, account, MESSION_STATUS_OVER)
    elif id == '5':
        # 无限领金币
        # 取消这个功能，2018-05-11
        return
        coin = 20000
        player_add_gold(redis, account, coin, 0)
        state = MESSION_STATUS_OK
        return {'code': 0, 'msg': u'恭喜您，获得%s金币' % coin, 'id': id, 'state': state}

    elif id == '6':
        # 每日登陆获取两张门票
        # 取消这个功能，2018-06-13
        return
        from bag.bag_config import bag_redis
        reward_ticket = 2
        user_table = 'users:%s' % uid
        player_item =  'player:item:uid:%s:hash' % uid
        if redis.get(WELFARE_USER_TICKET%(account,today)) == MESSION_STATUS_OVER:
            return {'code': 1, 'msg': u'您已领取，无法再次领取'}
        original_ticket_num = bag_redis.hget(player_item,'15')
        original_ticket_num = int(original_ticket_num) if original_ticket_num else 0
        final_ticket_num = original_ticket_num + reward_ticket
        bag_redis.hset(player_item,'15',final_ticket_num)
        redis.set(WELFARE_USER_TICKET%(account,today),MESSION_STATUS_OVER)
        return {'code': 0, 'msg': u'恭喜您，获得门票%s张' % reward_ticket, 'id': id, 'state': MESSION_STATUS_OVER,'ticket':reward_ticket}       

    return {'code': 0, 'msg': u'领取成功', 'id': id, 'state': state}


def get_personal_info(redis, account):
    """
    :param redis: 
    :param account: 
    :return: 
        headImgUrl 头像
        nickname
        parentAg 工会号
        win_rate 总胜率
        gold_count 总对局
        clubs 俱乐部
        previous_rank
        last_rank
        this_rank
        
    """
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
    user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
    if not user_table:
        return {}
    params = ('headImgUrl', 'nickname', 'parentAg')
    headImgUrl, nickname, parentAg = redis.hmget(user_table, params)

    # 胜率
    win = prredis.llen(GOLD_RECORD_ACCOUNT_WIN_LIST % account)
    total = prredis.llen(GOLD_RECORD_ACCOUNT_TOTAL_LIST % account)
    clubs = list(redis.smembers("club:account:%s:set"))

    get_gold_week_win_rank(prredis, parentAg)
    get_gold_last_week_win_rank(prredis, parentAg)
    get_gold_previous_week_win_rank(prredis, parentAg)
    previous_rank = prredis.zrevrank('gold:win:rank:%s:prweek:zset' % parentAg, account)
    last_rank = prredis.zrevrank('gold:win:rank:%s:lastweek:zset' % parentAg, account)
    this_rank = prredis.zrevrank('gold:win:rank:%s:thisweek:zset' % parentAg, account)

    info = {
        'headImgUrl': headImgUrl,
        'nickname': nickname,
        'parentAg': parentAg,
        'uid': user_table.split(':')[1],
        'win_rate': '%.2f%s' % (win / float(total) * 100 if total else 0, '%'),
        'gold_count': total,
        'clubs': clubs,
        'previous_rank': int(previous_rank)+1 if previous_rank != None else 0,
        'last_rank': int(last_rank)+1 if last_rank != None else 0,
        'this_rank': int(this_rank)+1 if this_rank != None else 0,
    }
    return {'code': 0, 'data': info}


def doSignRewardById(redis, uid, account, id):
    """ 
        连续签到奖励
    """
    first = first_day_of_month()
    last = date.today()
    today = datetime.now().strftime("%Y-%m-%d")
    month = first.strftime("%m")
    signTotal = 0

    while first <= last:
        if redis.exists(WELFARE_USER_SIGN % (account, first)):
            signTotal = signTotal + 1
        elif redis.sismember(WELFARE_USER_PATCH_SIGN % (account, first.strftime("%m")), first.strftime('%Y-%m-%d')):
            signTotal = signTotal + 1
        first += timedelta(1)

    key = None

    min_count = 30
    if id == '0':
        min_count = 7
        key = GOLD_WELFARE_SIGN_7DAYS % month
    elif id == '1':
        min_count = 7
        key = GOLD_WELFARE_SIGN_15DAYS % month
    elif id == '2':
        min_count = int(last_day_of_month())
        key = GOLD_WELFARE_SIGN_MONTH % month

    if not key:
        return {'code': 1, 'msg': u'请求错误'}

    if signTotal < min_count:
        return {'code': 1, 'msg': u'未达到要求'}

    if redis.hexists(key, account):
        return {'code': 1, 'msg': u'您已领取，无法再次领取'}

    redis.hset(key, account, MESSION_STATUS_OVER)

    gold = 0
    roomcard = 0
    yuanbao = 0
    for item in WELFARE_CONFIG['rewardlist']:
        if item['id'] != int(id):
            continue
        for reward in item['itemList']:
            if reward['reward']['id'] == 0:
                gold += reward['baseRewardCount']
            elif reward['reward']['id'] == 1:
                roomcard += reward['baseRewardCount']
            elif reward['reward']['id'] == 2:
                yuanbao += reward['baseRewardCount']
    player_add_gold(redis, account, gold, roomcard,yuanbao)
    if gold and roomcard:
        msg = u'恭喜您，获得%s金币,%s钻石' % (gold, roomcard)
    elif gold:
        msg = u'恭喜您，获得%s金币' % gold
    elif roomcard:
        msg = u'恭喜您，获得%s钻石' % roomcard
    elif yuanbao:
        msg = u'恭喜您，获得%s元宝' % yuanbao
 
    else:
        msg = u'领取成功'
    return {'code': 0, 'msg': msg,'gold':gold}


def getJournal(redis, account):
    """

    """
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
    res = []
    for table in prredis.lrange(GOLD_RECORD_ACCOUNT_TOTAL_LIST % account, 0, -1):
        info = prredis.hgetall(table)
        if not info.get('start_time', ''):
            continue
        info['rid'] = table.split(':')[4]
        info['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(info['start_time']) / 1000))
        info['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(info['end_time']) / 1000))
        res.append(info)
    return res

def getBuyGoldRecord(redis, account):
    """
        
    """
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
    res = []
    for table in prredis.lrange(GOLD_BUY_RECORD_ACCOUNT_LIST % account, 0, -1):
        info = prredis.hgetall(table)
        info['money'] = float(info['money'])/100
        res.append(info)
    return res


def getBuyGoldAccounts(redis, date):
    """

    """
    res = []
    for account in redis.smembers(DAILY_USER_GOLD2_SET % date):
        info = {}
        info['date'] = date
        info['gold'] = redis.get(DAILY_ACCOUNT_GOLD2_SUM % (account, date))
        money = redis.get(DAILY_ACCOUNT_GOLD2_MONEY_SUM % (account, date))
        info['money'] = float(money) / 100
        info['account'] = account
        res.append(info)
    return res

GOLD_RANK_CACHE = 'gold:rank:cache:%s'


def first_day_of_week():
    """ 
        获取本周第一天
    """
    return date.today() - timedelta(days=date.today().weekday())


def get_gold_week_win_rank(redis, groupid):
    first = first_day_of_week()
    last = first + timedelta(6)
    keys = []
    while first <= last:
        keys.append(GOLD_WIN_RANK_WITH_AGENT_ZSET_BYDAY % (groupid, first.strftime("%Y-%m-%d")))
        first += timedelta(1)
    redis.zunionstore('gold:win:rank:%s:thisweek:zset' % groupid, keys, aggregate='MAX')
    return redis.zrevrange('gold:win:rank:%s:thisweek:zset' % groupid, 0, 10 - 1, True)


def get_gold_last_week_win_rank(redis, groupid):
    """ 
        上周胜局
    """
    first = first_day_of_week() - timedelta(7)
    last = first + timedelta(6)
    keys = []
    while first <= last:
        keys.append(GOLD_WIN_RANK_WITH_AGENT_ZSET_BYDAY % (groupid, first.strftime("%Y-%m-%d")))
        first += timedelta(1)
    redis.zunionstore('gold:win:rank:%s:lastweek:zset' % groupid, keys, aggregate='MAX')
    return redis.zrevrange('gold:win:rank:%s:lastweek:zset' % groupid, 0, 10 - 1, True)


def get_gold_previous_week_win_rank(redis, groupid):
    """ 
        上上周胜局
    """
    first = first_day_of_week() - timedelta(14)
    last = first + timedelta(6)
    keys = []
    while first <= last:
        keys.append(GOLD_WIN_RANK_WITH_AGENT_ZSET_BYDAY % (groupid, first.strftime("%Y-%m-%d")))
        first += timedelta(1)
    redis.zunionstore('gold:win:rank:%s:prweek:zset' % groupid, keys, aggregate='MAX')
    return redis.zrevrange('gold:win:rank:%s:prweek:zset' % groupid, 0, 10 - 1, True)


def get_gold_rank(redis, groupid, account):
    """
        获取排行榜        
    """
    sortby = 'week'

    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
    if not prredis:
        return {}
    today = datetime.now().strftime("%Y-%m-%d")

    # if redis.exists(GOLD_RANK_CACHE % account):
    #     return json.loads(redis.get(GOLD_RANK_CACHE % account))

    res = {}
    res['gold_rank'] = []
    res['win_rank'] = []
    my_user_info = get_user_info(redis, account)

    # 财富排行榜
    rank = 0
    for _account, value in redis.zrevrange(GOLD_MONEY_RANK_WITH_AGENT_ZSET % groupid, 0, 10 - 1, True):
        rank += 1
        value = int(value)
        user_info = get_user_info(redis, _account)
        if not user_info:
            continue
        res['gold_rank'].append({'rank': rank, 'nickname': user_info['nickname'], 'value': value,
                                 'account': _account, 'headImgUrl': user_info['headImgUrl']})

    myrank = prredis.zrevrank(GOLD_MONEY_RANK_WITH_AGENT_ZSET % groupid, account)
    myvalue = prredis.zscore(GOLD_MONEY_RANK_WITH_AGENT_ZSET % groupid, account)
    if my_user_info and myrank != None:
        res['gold_rank'].append({'rank': int(myrank)+1, 'nickname': my_user_info['nickname'], 'value': myvalue,
                                'account': account, 'headImgUrl': my_user_info['headImgUrl'], 'self': '1'})
    else:
        res['gold_rank'].append({'nickname': my_user_info['nickname'],
                                'account': account, 'headImgUrl': my_user_info['headImgUrl'], 'self': '1'})
    # 胜局排行榜
    rank = 0
    for _account, value in get_gold_week_win_rank(prredis, groupid):
        rank += 1
        value = int(value)
        user_info = get_user_info(redis, _account)
        if not user_info:
            continue
        res['win_rank'].append({'rank': rank, 'nickname': user_info['nickname'], 'value': value,
                                'desc': '本周胜局', 'account': _account, 'headImgUrl': user_info['headImgUrl']})
    myrank = prredis.zrevrank('gold:win:rank:%s:thisweek:zset' % groupid, account)
    myvalue = prredis.zscore('gold:win:rank:%s:thisweek:zset' % groupid, account)
    if my_user_info and myrank != None:
        res['win_rank'].append({'rank': int(myrank)+1, 'nickname': my_user_info['nickname'], 'value': myvalue,
                                'desc': '本周胜局', 'account': account, 'headImgUrl': my_user_info['headImgUrl'],
                                'self': '1'})
    else:
        res['win_rank'].append({'nickname': my_user_info['nickname'],
                                'account': account, 'headImgUrl': my_user_info['headImgUrl'], 'self': '1'})
    redis.set(GOLD_RANK_CACHE % account, json.dumps(res))
    redis.expire(GOLD_RANK_CACHE % account, 300)
    return res


def first_day_of_month():
    """ 
        获取本月第一天
    """
    day = date.today().strftime('%d')
    day = int(day)
    return date.today() - timedelta(days=day-1)
def last_day_of_month():
    """
        获取本月最后天
    """
    day = date.today()
    month = day.month + 1
    year = day.year if month <= 12 else day.year + 1
    month = month if month <= 12 else 1
    day = day.replace(year , month, 1)
    day = day - timedelta(1)
    return day.day


def get_welfare_info(redis, account):
    today = datetime.now().strftime("%Y-%m-%d")
    first = first_day_of_month()
    month = first.strftime("%m")
    # last = date.today() - timedelta(days=1)
    last = date.today()
    res = copy.deepcopy(WELFARE_CONFIG)
    res['date'] = today
    res['signed'] = []
    res['unsinged'] = []
    # 本月最后一天
    res['last_date'] = last_day_of_month()
    # 当前补签次数
    res['patchsign_times'] = redis.scard(WELFARE_USER_PATCH_SIGN % (account, month))

    # 今天是否签到`
    if redis.exists(WELFARE_USER_SIGN % (account, today)):
        res['issigned'] = 1
    else:
        res['issigned'] = 0

    while first <= last:
        if redis.exists(WELFARE_USER_SIGN % (account, first)):
            res['signed'].append(first.strftime('%d'))
        elif redis.sismember(WELFARE_USER_PATCH_SIGN % (account, first.strftime("%m")), first.strftime('%Y-%m-%d')):
            res['signed'].append(first.strftime('%d'))
        elif first != last:
            res['unsinged'].append(first.strftime('%d'))
        first += timedelta(1)

    # 补签+签到次数
    signTotal = len(res['signed'])

    # 七天奖励
    state = MESSION_STATUS_OK if signTotal >= 7 else MESSION_STATUS_NO
    hstate = redis.hget(GOLD_WELFARE_SIGN_7DAYS % month, account)
    if res['rewardlist'][0] :
        res['rewardlist'][0]['status'] = hstate if hstate else state

    # 十五天奖励
    state = MESSION_STATUS_OK if signTotal >= 15 else MESSION_STATUS_NO
    hstate = redis.hget(GOLD_WELFARE_SIGN_15DAYS % month, account)
    if res['rewardlist'][1]:
        res['rewardlist'][1]['status'] = hstate if hstate else state

    # 月奖励
    state = MESSION_STATUS_OK if signTotal >= int(last_day_of_month()) else MESSION_STATUS_NO
    hstate = redis.hget(GOLD_WELFARE_SIGN_MONTH % month, account)
    if res['rewardlist'][2]:
        res['rewardlist'][2]['status'] = hstate if hstate else state

    # 每日首冲奖励
    if not redis.sismember(DAILY_USER_GOLD2_SET % today, account):
        res['messionlist'][0]['status'] = MESSION_STATUS_NO
        res['messionlist'][0]['parent_mode'] = CHECK_MALL
    else:
        if redis.hget(GOLD_REWARD_DAY_BUY_GOLD_HASH % today, account) == MESSION_STATUS_OVER:
            res['messionlist'][0]['status'] = MESSION_STATUS_OVER
        else:
            res['messionlist'][0]['status'] = MESSION_STATUS_OK

    # 任务进度处理
    for msiData in res['messionlist']:
        if msiData['id'] == 1 :
            # 新手礼包
            if redis.hget(GOLD_REWARD_NEW_PRESENT_HASH, account) == MESSION_STATUS_OVER:
                msiData['status'] = MESSION_STATUS_OVER
            else:
                msiData['status'] = MESSION_STATUS_OK
        elif msiData['id'] == 2:
            # 破产补助
            key = WELFARE_USER_INSURANCE % (account, today)
            if not redis.exists(WELFARE_USER_INSURANCE % (account, today)):
                msiData['status'] = MESSION_STATUS_OK
                msiData['isOver'] = MESSION_STATUS_NO
            else:
                if redis.llen(key) >= SIGN_MAX:
                    msiData['status'] = MESSION_STATUS_OVER
                    msiData['isOver'] = MESSION_STATUS_OVER
                else:
                    msiData['status'] = MESSION_STATUS_OK
                    msiData['isOver'] = MESSION_STATUS_NO
        elif msiData['id'] == 3:
            key = GOLD_WELFARE_SHARE % account
            if redis.get(key) == today:
                msiData['status'] = MESSION_STATUS_OVER
        elif msiData['id'] == 6:
            key = WELFARE_USER_TICKET % (account,today)
            if redis.get(key) == MESSION_STATUS_OVER:
                msiData['status'] = MESSION_STATUS_OVER
            else:
                msiData['status'] = MESSION_STATUS_OK
    return res


def get_wechat_gold_records(redis,condition):
    """
        获取微信支付购买金币订单记录
        :params redis Redis实例
        :params condition 查询条件
    """
    deltaTime = timedelta(1)
    orderList = []
    roomCardCount,pendingMoney,successMoney,moneyCount = 0,0,0,0
    date_lists = convert_util.to_week_list(condition['startDate'],condition['endDate'])
    date_table = DAY_ORDER
    order_table = ORDER_TABLE

    pipe = redis.pipeline()
    for date in date_lists:
        orders = redis.lrange(date_table%(date),0,-1)
        for order in orders:
            orderInfo = {}
            if not order_table%(order):
                pipe.lrem(ORDER_NUM_LIST,orders)
                pipe.lrem(date_table%(date),order)
                continue
            orderDetail = redis.hgetall(order_table%(order))
            if not orderDetail:
                pipe.lrem(ORDER_NUM_LIST,orders)
                pipe.lrem(date_table%(date),order)
                continue

            """   过滤掉其他   """
            goodid = orderDetail.get('num')
            rType = redis.hget(GOODS_TABLE % goodid, 'type')
            if rType != '2':
                continue
            dateStr1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(orderDetail['time'])))
            moneyCount+=round(float(orderDetail['money']),2)
            if orderDetail['type'] == 'pending':
                pendingMoney+=round(float(orderDetail['money']),2)
            else:
                successMoney+=round(float(orderDetail['money']),2)
            user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE%(orderDetail['account']))
            group_id  = redis.hget(user_table,'parentAg')
            orderInfo['orderNo'] = order
            orderInfo['good_name'] = orderDetail['name']
            orderInfo['good_money'] = round(float(orderDetail['money'])*0.01,2)
            orderInfo['order_paytime'] = dateStr1
            orderInfo['good_count'] = orderDetail['roomCards']
            orderInfo['order_type'] = orderDetail['type']
            orderInfo['group_id'] = group_id if group_id else '-'
            orderInfo['memberId'] = user_table.split(':')[1]
            orderList.append(orderInfo)
    pipe.execute()
    return {'data':orderList,'orderCount':len(orderList),'moneyCount':moneyCount*0.01,'pendingMoney':pendingMoney*0.01,'successMoney':successMoney*0.01}

from bottle_mysql import get_mysql
def get_gold_operate_data(redis,condition):
        from bag.bag_config import bag_redis
#        hong_zhong_er_ren, hong_zhong_si_ren,pao_de_kuai,er_ren_ma_jiang,dou_di_zhu_jin_bi=\
#         444,445,559,449,560
#        game_id_list = [hong_zhong_er_ren, hong_zhong_si_ren,pao_de_kuai,er_ren_ma_jiang,dou_di_zhu_jin_bi]
        game_id_list = GOLD_GAME_LIST
        prredis = getPrivateRedisInst(redis, MASTER_GAMEID)
        sql = get_mysql()
        tool_price_map = get_tool_price()
        no_data = '0'
        #prredis = redis
        startDate = datetime.strptime(condition['startDate'], '%Y-%m-%d')
        endDate = datetime.strptime(condition['endDate'], '%Y-%m-%d')
        deltaTime = timedelta(1)
        res = []
        while startDate <= endDate:
                obj = {}
                dateStr = endDate.strftime('%Y-%m-%d')
                amount_of_recharge_gold_coin = -1
                amount_of_recharge_gold_coin = prredis.get(DAILY_GOLD2_SUM % dateStr)

                #从数据库中获取玩家当天拥有金币价值，玩家当天拥有元宝价值
                value_of_gold_that_players_own = 0
                value_of_yuanbao_that_players_own = 0
                tomorrow = (endDate + timedelta(days=1)).strftime('%Y-%m-%d')
                sql_str_tomorrow = 'select * from operate_data_record where data_date = "%s"' % tomorrow
                result, answers = sql.select_data_bywhere(sql_str_tomorrow)
                if result == True and len(answers) > 0:
                    if answers[0]['all_user_gold_sum']:
                        value_of_gold_that_players_own = answers[0]['all_user_gold_sum']
                        value_of_gold_that_players_own = transfer_into_RMB(tool_price_map,'gold',value_of_gold_that_players_own)
                    if answers[0]['all_user_yuanbao_sum']:    
                        value_of_yuanbao_that_players_own = answers[0]['all_user_yuanbao_sum']
                        value_of_yuanbao_that_players_own = transfer_into_RMB(tool_price_map,'yuanbao',value_of_yuanbao_that_players_own)

                # 1,金币场房费收入价值 这里只包括 红中二人、红中四人、跑得快、二人麻将、斗地主
                # 2,计算金币场人数
                income_total_value_from_golden_house_fee = 0
                total_population_golden_house = 0
                total_qty_of_games_in_golden_house = 0
                # gold_fee_list = [hong_zhong_er_ren,hong_zhong_si_ren,pao_de_kuai,er_ren_ma_jiang,dou_di_zhu_jin_bi]
                for gold_fee_type in game_id_list:
                    r_fee = prredis.hgetall(GOLD_OPERATE % (gold_fee_type, dateStr))
                    if r_fee:
                        if r_fee.has_key('fee_total'):
                            income_total_value_from_golden_house_fee = income_total_value_from_golden_house_fee + int(r_fee['fee_total'])
                        if r_fee.has_key('player_count'):
                            total_population_golden_house = total_population_golden_house + int(r_fee['player_count'])
                        if r_fee.has_key('game_count'):
                            total_qty_of_games_in_golden_house = total_qty_of_games_in_golden_house + int(r_fee['game_count'])

                # 比赛场报名费
                type_of_match_fee = ["roomCard","gold","yuanbao", "redpacket"]
                for fee_type in type_of_match_fee:
                    sql_str = 'select sum(playerFees) from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and FeeType = "%s" and GameId="451"' % (dateStr,fee_type)
                    fee_field = "income_total_value_from_competition_house_register_fee_%s" % fee_type
                    obj[fee_field] = 0
                    result, answers = sql.select_data_bywhere(sql_str)
                    if result == True:
                        if answers[0]['sum(playerFees)']:
                            obj[fee_field] = answers[0]['sum(playerFees)'].to_eng_string()

                # 比赛场目前只包括背包的元宝
                bag_info = bag_redis.hgetall(RED_ENVELOPE_DAY_INFO % (dateStr,))
                bag_yuanbao_fee = bag_info.get('roomCharge',0) 
                if bag_yuanbao_fee == 'None':
                    bag_yuanbao_fee = 0
                bag_yuanbao_fee = abs(int(bag_yuanbao_fee))
                obj['income_total_value_from_competition_house_fee_yuanbao'] =  bag_yuanbao_fee

                # 统计比赛场的人数 
                total_population_match_house = 0
                total_population_match_house_set = set()
                sql_str = 'select Accounts from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and GameId="451"' % dateStr
                result, answers = sql.select_data_bywhere(sql_str)
                if result == True:
                    for acc in answers:
                        if acc['Accounts']:
                            if '|' in acc['Accounts']:
                                acc_list =acc['Accounts'].split('|')
                                for acc_obj in acc_list:
                                    acc_uid = if_not_uid_return_uid(redis,acc_obj.strip())
                                    total_population_match_house_set.add(acc_uid)
                            else:
                                acc_uid = if_not_uid_return_uid(redis,acc['Accounts'].strip())
                                total_population_match_house_set.add(acc_uid)

                # 比赛场人数需要加上背包系统的
                acc_set = bag_redis.smembers(RED_ENVELOPE_PLAYER_SET % dateStr)
                if acc_set:
                    total_population_match_house_set = total_population_match_house_set.union(acc_set)
                total_population_match_house = len(total_population_match_house_set)

                # 比赛场总局数 = 2人麻将局数 + 跑得快局数
                total_qty_of_games_in_match_house = 0
                sql_str = 'select count(*) from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and GameId="451"' % dateStr
                result, answers = sql.select_data_bywhere(sql_str)
                if result == True:
                    total_qty_of_games_in_match_house = answers[0]['count(*)']

                bag_round = bag_redis.get(RED_ENVELOPE_ROUND % (dateStr))
                if bag_round:
                    if bag_round == 'None':
                        bag_round = 0
                    total_qty_of_games_in_match_house = total_qty_of_games_in_match_house + int(bag_round)

                # 兑换金币总额，兑换元宝总额
                amount_of_recharge_gold_coin = 0
                amount_of_recharge_yuan_bao = 0
                rtn_gold = bag_redis.get('exchange:1To2:date:%s' % dateStr)
                rtn_yuanbao = bag_redis.get('exchange:1To3:date:%s' % dateStr)
                if rtn_gold:
                    amount_of_recharge_gold_coin = transfer_into_RMB(tool_price_map,'diamond',int(rtn_gold))
                else:
                    amount_of_recharge_gold_coin = no_data
                if rtn_yuanbao:
                    amount_of_recharge_yuan_bao = transfer_into_RMB(tool_price_map,'diamond',int(rtn_yuanbao))
                else:
                    amount_of_recharge_yuan_bao = no_data

                # 福利支出
                query_str = 'welfare:daily:total_fee_%s*' % dateStr
                total_welfare_fee_gold = 0
                total_welfare_fee_vcoin = 0
                total_welfare_fee_bag = 0
                db8 = get_db(8)
                welfare_key_list = db8.keys(query_str)
                for welfare_key in welfare_key_list:
                    # 按照固定格式判断类型
                    try:
                        currency_type = welfare_key.split('_')[3]
                    except:
                        continue

                    obj_qty = int(db8.get(welfare_key))

                    if currency_type == 'gold':
                        total_welfare_fee_gold = total_welfare_fee_gold + obj_qty
                    elif currency_type == 'vcoin':
                        total_welfare_fee_vcoin = total_welfare_fee_vcoin + obj_qty
                    elif currency_type == 'bag':
                        total_welfare_fee_bag = total_welfare_fee_bag + obj_qty

                # 奖励支出
                fee_total_reward_expenditure_roomCard = 0
                fee_total_reward_expenditure_yuanbao = 0 
                fee_total_reward_expenditure_redpacket = 0
                fee_total_reward_expenditure_gold = 0
                type_of_match_fee = ["roomCard","gold","yuanbao", "redpacket"]
                for fee_type in type_of_match_fee:
                    mysql_field = "reward_%s" % fee_type
                    sql_str = 'select sum(%s) from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and GameId="451"' % (mysql_field,dateStr)
                    fee_field = "fee_total_reward_expenditure_%s" % fee_type

                    result, answers = sql.select_data_bywhere(sql_str)
                    if result == True:
                        if answers[0]['sum(%s)' % mysql_field]:
                            # obj[fee_field] = answers[0]["sum(%s)" % mysql_field].to_eng_string()
                            total_fee = answers[0]["sum(%s)" % mysql_field].to_eng_string()
                            exec('%s = %s' % (fee_field,total_fee))
                            
                # 奖励支出需要加上红包赛的数量
                info1 = bag_redis.hgetall(RED_ENVELOPE_DAY_INFO % (dateStr,))
                rp_fee_total_reward_expenditure_redpacket = abs(int(info1.get('30',0))) + abs(int(info1.get('60',0))) + abs(int(info1.get('120',0))) #当天发放红包
                rp_fee_total_reward_expenditure_yuanbao = abs(int(info1.get('3',0))) + abs(int(info1.get('6',0))) + abs(int(info1.get('12',0))) # 当天发放元宝

                fee_total_reward_expenditure_yuanbao = fee_total_reward_expenditure_yuanbao + rp_fee_total_reward_expenditure_yuanbao
                fee_total_reward_expenditure_redpacket = fee_total_reward_expenditure_redpacket + rp_fee_total_reward_expenditure_redpacket

                # 充值总价值金额
                total_cash_value_of_recharge = 0
                # total_value_of_players_recharge = 0
                orders = redis.lrange(DAY_ORDER%(dateStr),0,-1)
                for order in orders:
                    orderDetail = redis.hgetall(ORDER_TABLE%(order))
                    if orderDetail:
                        if orderDetail['type'] != 'pending':
                            total_cash_value_of_recharge += float(orderDetail['money']) * 0.01

                total_cash_value_of_recharge = round(total_cash_value_of_recharge,2)

                
                '''
                # 旧的代码
                # AI波动金币价值（赢-输的价值）
                income_value_of_AI_fluctuating_gold_coin = 0
                sql_str = 'select sum(playerGolds) from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and GameId="451"' % dateStr
                result, answers = sql.select_data_bywhere(sql_str)
                if result == True:
                    if answers[0]['sum(playerGolds)']:
                        income_value_of_AI_fluctuating_gold_coin -= int(answers[0]['sum(playerGolds)']
            
                # ai波动金额
                tool_id_map = {'yuanbao':3,'gold':2}
                robot_level = ['B' , 'D']

                redis_db8 = get_db(8)
                income_value_of_AI_fluctuating_gold_coin = 0
                today = dateStr

                #for day in day_list:
                for level in robot_level:
                    for tool in tool_id_map.items():
                        field = '%s_%s' % (level,tool[0])
                        sql_str = "RobotGather:%s:%s:%s" % (level,dateStr,tool[1])
                        exec('%s = 0' % field)
                        exec('rtn = redis_db8.get("%s")' % (sql_str))
                        if rtn:
                            exec('%s = int(rtn)' % field)

                        exec('rmb_value = transfer_into_RMB(tool_price_map,tool[0],%s)' % field)
                        exec('income_value_of_AI_fluctuating_gold_coin += rmb_value')
                income_value_of_AI_fluctuating_gold_coin = round(income_value_of_AI_fluctuating_gold_coin,2
                '''
                # AI波动金币价值（赢-输的价值）
                income_value_of_AI_fluctuating_gold_coin = 0
                next_date = endDate + deltaTime
                next_date_str = next_date.strftime('%Y-%m-%d')
                query_str = "SELECT SUM(quantity_change) from income_and_fee_detail WHERE \
                    create_time > '%s' and create_time < '%s' and game_id \
                    in (444,445,449,559,451,560) and user_id like '%%robot%%' and currency = 2 and type_id = 9;" \
                    % (dateStr,next_date_str)
                result, answers = sql.execute(query_str)
                if result == True:
                    if answers[0]['SUM(quantity_change)']:
                        income_value_of_AI_fluctuating_gold_coin = int(answers[0]['SUM(quantity_change)']) 
                income_value_of_AI_fluctuating_gold_coin = transfer_into_RMB(tool_price_map,'gold',income_value_of_AI_fluctuating_gold_coin)       
                income_value_of_AI_fluctuating_gold_coin = round(income_value_of_AI_fluctuating_gold_coin,2)

                # A档（AI）波动金币价值（暴击场)
                redis_db8 = get_db(8)
                income_value_of_AI_fluctuating_gold_coin_levelA_baoji = 0
                tool_id_map = {'yuanbao':3,'gold':2}
                for tool in tool_id_map.items():
                    sql_str = "RobotGather:%s:%s:%s" % ('A',dateStr,tool[1])
                    exec('rtn = redis_db8.get("%s")' % (sql_str))
                    if rtn:
                        exec('rmb_value = transfer_into_RMB(tool_price_map,tool[0],%s)' % int(rtn))
                        income_value_of_AI_fluctuating_gold_coin_levelA_baoji += rmb_value

                # 玩家波动金额
                tomorrow = (endDate + timedelta(days=1)).strftime('%Y-%m-%d')
                sql_str_today = 'select all_user_gold_sum from operate_data_record where data_date = "%s"' % dateStr
                sql_str_tomorrow = 'select all_user_gold_sum from operate_data_record where data_date = "%s"' % tomorrow
                result_today, answers_today = sql.select_data_bywhere(sql_str_today)
                result_tomorrow, answers_tomorrow = sql.select_data_bywhere(sql_str_tomorrow)
                if (result_today and result_tomorrow) and (len(answers_today) > 0 and len(answers_tomorrow) > 0):
                    gold_differ = answers_tomorrow[0]['all_user_gold_sum'] - answers_today[0]['all_user_gold_sum']
                    obj['volatility_of_gold_coin'] = transfer_into_RMB(tool_price_map,'gold',int(gold_differ))
                else:
                    obj['volatility_of_gold_coin'] = no_data


                # 金币场比赛场活跃人数总金币 和 金币场比赛场活跃人数金币波动
                total_value_of_active_in_gold_and_compete = 0
                total_value_of_active_in_gold_and_compete_tomorrow = 0
                total_value_of_active_in_gold_and_compete_today = 0
                total_wave_value_of_active_in_gold_and_compete = 0
                sql_str_today = 'select active_player_gold_sum_pre from operate_data_record \
                where data_date ="%s"' % tomorrow 
                sql_str_tomorrow = 'select active_player_gold_sum from operate_data_record \
                where data_date ="%s"' % tomorrow

                result, answers = sql.select_data_bywhere(sql_str_today)
                if result == True:
                    if len(answers)>0 and answers[0]['active_player_gold_sum_pre']:
                        total_value_of_active_in_gold_and_compete_today = int(answers[0]['active_player_gold_sum_pre'])

                result, answers = sql.select_data_bywhere(sql_str_tomorrow)
                if result == True:
                    if len(answers)>0 and answers[0]['active_player_gold_sum']:
                        total_value_of_active_in_gold_and_compete_tomorrow = int(answers[0]['active_player_gold_sum'])                        
                total_wave_value_of_active_in_gold_and_compete = total_value_of_active_in_gold_and_compete_tomorrow - \
                total_value_of_active_in_gold_and_compete_today
                total_value_of_active_in_gold_and_compete = total_value_of_active_in_gold_and_compete_tomorrow
                
                obj['total_wave_value_of_active_in_gold_and_compete'] = \
                transfer_into_RMB(tool_price_map,'gold',int(total_wave_value_of_active_in_gold_and_compete))
                obj['total_value_of_active_in_gold_and_compete'] = \
                transfer_into_RMB(tool_price_map,'gold',int(total_value_of_active_in_gold_and_compete))

                # 获取 特殊支出
                fee_special_fee = 0
                special_fee_sql = "select special_fee from operate_data_record where data_date = '%s'"  % dateStr
                result, answers = sql.select_data_bywhere(special_fee_sql)
                if result == True:
                   if len(answers)>0:
                            fee_special_fee = float(answers[0]['special_fee'])

                # 保险箱收入手续费

                income_from_insurance_box = 0
                insurance_tax_str =  "box:tax:date:%s" % dateStr
                insurance_tax = bag_redis.get(insurance_tax_str)
                if insurance_tax:
                    income_from_insurance_box = float(insurance_tax)
                    income_from_insurance_box = transfer_into_RMB(tool_price_map,'gold',income_from_insurance_box)
                obj['income_from_insurance_box'] = income_from_insurance_box

                # 计算流水 = 充值总价值金额 - 玩家兑换奖励价值总额
                # 玩家兑换奖励价值总额 目前没有计算，为0
                value_of_reward_that_player_redeem = 0
                obj['profit_of_journal'] = total_cash_value_of_recharge - value_of_reward_that_player_redeem

                obj['date'] = dateStr
                obj['value_of_gold_that_players_own'] = value_of_gold_that_players_own
                obj['value_of_yuanbao_that_players_own'] = value_of_yuanbao_that_players_own
                obj['value_of_reward_that_player_redeem'] = no_data
                obj['income_value_of_player_change'] = no_data
                obj['income_value_of_tool_that_activity_cost'] =no_data 
                obj['income_value_of_tool_that_purchase'] =no_data 
                obj['fee_value_back_to_creator_of_club'] =no_data 
                obj['fee_value_back_to_agent_level_1'] =no_data 
                obj['fee_value_back_to_relaship_between_updown'] =no_data 
                obj['fee_value_that_pay_commission_to_platform'] =no_data 

                obj['income_total_value_from_competition_house_register_fee_gold'] =  transfer_into_RMB(tool_price_map,'gold',int(obj['income_total_value_from_competition_house_register_fee_gold']))
                obj['income_total_value_from_competition_house_register_fee_yuanbao'] =  transfer_into_RMB(tool_price_map,'yuanbao',int(obj['income_total_value_from_competition_house_register_fee_yuanbao']))
                obj['income_total_value_from_competition_house_register_fee_roomCard'] =  transfer_into_RMB(tool_price_map,'diamond',int(obj['income_total_value_from_competition_house_register_fee_roomCard']))

                obj['income_total_value_from_competition_house_fee_yuanbao'] =  transfer_into_RMB(tool_price_map,'yuanbao',int(obj['income_total_value_from_competition_house_fee_yuanbao']))

                obj['income_total_value_from_golden_house_fee'] = transfer_into_RMB(tool_price_map,'gold',income_total_value_from_golden_house_fee)
                obj['total_value_from_competition_house_register_fee'] = 'no data'
                obj['fee_total_welfare_expenditure_gold'] =  transfer_into_RMB(tool_price_map,'gold',total_welfare_fee_gold)
                obj['fee_total_welfare_expenditure_vcoin'] = transfer_into_RMB(tool_price_map,'yuanbao',total_welfare_fee_vcoin)
                #  这个汇率没有
                obj['fee_total_welfare_expenditure_bag'] = 0 # total_welfare_fee_bag 暂时设为0
                obj['fee_total_reward_expenditure_gold'] = transfer_into_RMB(tool_price_map,'gold',fee_total_reward_expenditure_gold)
                obj['fee_total_reward_expenditure_roomCard'] =  transfer_into_RMB(tool_price_map,'room_card',fee_total_reward_expenditure_roomCard)
                obj['fee_total_reward_expenditure_yuanbao'] = transfer_into_RMB(tool_price_map,'yuanbao',fee_total_reward_expenditure_yuanbao)
                obj['fee_total_reward_expenditure_redpacket'] = transfer_into_RMB(tool_price_map,'redpacket',fee_total_reward_expenditure_redpacket)
                obj['total_population_golden_house'] = total_population_golden_house
                obj['total_qty_of_games_in_golden_house'] = total_qty_of_games_in_golden_house
                obj['total_population_match_house'] = total_population_match_house
                obj['total_qty_of_games_in_match_house']  = total_qty_of_games_in_match_house
                obj['total_cash_value_of_recharge'] = total_cash_value_of_recharge
                obj['income_value_of_AI_fluctuating_gold_coin'] = income_value_of_AI_fluctuating_gold_coin             
                obj['income_value_of_AI_fluctuating_gold_coin_levelA_baoji'] = income_value_of_AI_fluctuating_gold_coin_levelA_baoji
                obj['amount_of_recharge_yuan_bao'] =amount_of_recharge_yuan_bao  
                obj['amount_of_recharge_gold_coin'] =amount_of_recharge_gold_coin
                obj['fee_special_fee'] = fee_special_fee
                obj['profit_of_today'] = total_profit_of_the_day(obj)
                
                res.append(obj)

                endDate -= deltaTime
        sql.close_connect()
        return {'data':res}

def get_active_player_data(redis,condition):
    res = {}
    no_data = '0'
    startDate = datetime.strptime(condition['startDate'], '%Y-%m-%d')
    endDate = datetime.strptime(condition['endDate'], '%Y-%m-%d')
    from bag.bag_config import bag_redis
    gold_game_id_list = GOLD_GAME_LIST
    tool_price_map = get_tool_price()
    prredis = getPrivateRedisInst(redis, MASTER_GAMEID)    
    mysql = get_mysql()    
    deltaTime = timedelta(1)
    res = []
    while startDate <= endDate:
        obj = {}
        dateStr = endDate.strftime('%Y-%m-%d')
        # 金币场活跃人数
        gold_id_set = get_gold_user_id_set(redis,GOLD_GAME_LIST,dateStr)
        population_of_players_in_gold = len(gold_id_set)
        # 比赛场活跃人数
        compete_id_set = get_compete_user_id_set(redis,mysql,dateStr,bag_redis)
        population_of_players_in_match = len(compete_id_set)

        # 1,金币场总局数 这里只包括 红中二人、红中四人、跑得快、二人麻将、斗地主
        # 2,金币场房费
        total_round_in_gold = 0
        income_total_value_from_golden_house_fee = 0
        for gold_fee_type in gold_game_id_list:
            r_fee = prredis.hgetall(GOLD_OPERATE % (gold_fee_type, dateStr))
            if r_fee:
                if r_fee.has_key('fee_total'):
                   income_total_value_from_golden_house_fee = income_total_value_from_golden_house_fee + int(r_fee['fee_total'])
                if r_fee.has_key('game_count'):
                    total_round_in_gold = total_round_in_gold + int(r_fee['game_count'])        
        income_total_value_from_golden_house_fee = \
         transfer_into_RMB(tool_price_map,'gold',int(income_total_value_from_golden_house_fee))

        # 比赛场总局数 = 2人麻将局数 + 跑得快局数
        total_qty_of_games_in_match_house = 0
        sql_str = 'select count(*) from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and GameId="451"' % dateStr
        result, answers = mysql.select_data_bywhere(sql_str)
        if result == True:
            total_qty_of_games_in_match_house = answers[0]['count(*)']

        bag_round = bag_redis.get(RED_ENVELOPE_ROUND % (dateStr))
        if bag_round:
            if bag_round == 'None':
                bag_round = 0
            total_qty_of_games_in_match_house = total_qty_of_games_in_match_house + int(bag_round)

        # 金币场比赛场活跃人数总金币
        # 金币场比赛场活跃人数总金币 和 金币场比赛场活跃人数金币波动
        tomorrow = (endDate + timedelta(days=1)).strftime('%Y-%m-%d')
        total_value_of_active_in_gold_and_compete = 0
        total_value_of_active_in_gold_and_compete_tomorrow = 0
        total_value_of_active_in_gold_and_compete_today = 0
        total_wave_value_of_active_in_gold_and_compete = 0
        sql_str_today = 'select active_player_gold_sum_pre from operate_data_record \
        where data_date ="%s"' % tomorrow 
        sql_str_tomorrow = 'select active_player_gold_sum from operate_data_record \
        where data_date ="%s"' % tomorrow

        result, answers = mysql.select_data_bywhere(sql_str_today)
        if result == True:
            if len(answers)>0 and answers[0]['active_player_gold_sum_pre']:
                total_value_of_active_in_gold_and_compete_today = int(answers[0]['active_player_gold_sum_pre'])

        result, answers = mysql.select_data_bywhere(sql_str_tomorrow)
        if result == True:
            if len(answers)>0 and answers[0]['active_player_gold_sum']:
                total_value_of_active_in_gold_and_compete_tomorrow = int(answers[0]['active_player_gold_sum'])                        
        total_wave_value_of_active_in_gold_and_compete = total_value_of_active_in_gold_and_compete_tomorrow - \
        total_value_of_active_in_gold_and_compete_today
        total_value_of_active_in_gold_and_compete = total_value_of_active_in_gold_and_compete_tomorrow
                
        obj['total_wave_value_of_active_in_gold_and_compete'] = \
        transfer_into_RMB(tool_price_map,'gold',int(total_wave_value_of_active_in_gold_and_compete))
        obj['total_value_of_active_in_gold_and_compete'] = \
        transfer_into_RMB(tool_price_map,'gold',int(total_value_of_active_in_gold_and_compete))

        # 兑换金币总额，兑换元宝总额
        amount_of_recharge_gold_coin = 0
        amount_of_recharge_yuan_bao = 0
        rtn_gold = bag_redis.get('exchange:1To2:date:%s' % dateStr)
        rtn_yuanbao = bag_redis.get('exchange:1To3:date:%s' % dateStr)
        if rtn_gold:
            amount_of_recharge_gold_coin = transfer_into_RMB(tool_price_map,'diamond',int(rtn_gold))
        else:
            amount_of_recharge_gold_coin = no_data
        if rtn_yuanbao:
            amount_of_recharge_yuan_bao = transfer_into_RMB(tool_price_map,'diamond',int(rtn_yuanbao))
        else:
            amount_of_recharge_yuan_bao = no_data

        # 充值总价值金额
        total_cash_value_of_recharge = 0
        # total_value_of_players_recharge = 0
        orders = redis.lrange(DAY_ORDER%(dateStr),0,-1)
        for order in orders:
            orderDetail = redis.hgetall(ORDER_TABLE%(order))
            if orderDetail:
                if orderDetail['type'] != 'pending':
                    total_cash_value_of_recharge += float(orderDetail['money']) * 0.01
        total_cash_value_of_recharge = round(total_cash_value_of_recharge,2)        

        # 比赛场房费收入价值
        bag_info = bag_redis.hgetall(RED_ENVELOPE_DAY_INFO % (dateStr,))
        bag_yuanbao_fee = bag_info.get('roomCharge',0) 
        if bag_yuanbao_fee == 'None':
            bag_yuanbao_fee = 0
        bag_yuanbao_fee = abs(int(bag_yuanbao_fee))
        income_total_value_from_competition_house_fee_yuanbao =  \
         transfer_into_RMB(tool_price_map,'yuanbao',int(bag_yuanbao_fee))

        # 比赛场报名费
        type_of_match_fee = ["roomCard","gold","yuanbao", "redpacket"]
        for fee_type in type_of_match_fee:
            sql_str = 'select sum(playerFees) from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and FeeType = "%s" and GameId="451"' % (dateStr,fee_type)
            fee_field = "income_total_value_from_competition_house_register_fee_%s" % fee_type
            obj[fee_field] = 0
            result, answers = mysql.select_data_bywhere(sql_str)
            if result == True:
                if answers[0]['sum(playerFees)']:
                    obj[fee_field] = answers[0]['sum(playerFees)'].to_eng_string()        
            
         # 福利支出
        query_str = 'welfare:daily:total_fee_%s*' % dateStr
        total_welfare_fee_gold = 0
        total_welfare_fee_vcoin = 0
        total_welfare_fee_bag = 0
        db8 = get_db(8)
        welfare_key_list = db8.keys(query_str)
        for welfare_key in welfare_key_list:
            # 按照固定格式判断类型
            try:
                currency_type = welfare_key.split('_')[3]
            except:
                continue

            obj_qty = int(db8.get(welfare_key))

            if currency_type == 'gold':
                total_welfare_fee_gold = total_welfare_fee_gold + obj_qty
            elif currency_type == 'vcoin':
                total_welfare_fee_vcoin = total_welfare_fee_vcoin + obj_qty
            elif currency_type == 'bag':
                total_welfare_fee_bag = total_welfare_fee_bag + obj_qty           

        # 奖励支出
        fee_total_reward_expenditure_roomCard = 0
        fee_total_reward_expenditure_yuanbao = 0 
        fee_total_reward_expenditure_redpacket = 0
        fee_total_reward_expenditure_gold = 0
        type_of_match_fee = ["roomCard","gold","yuanbao", "redpacket"]
        for fee_type in type_of_match_fee:
            mysql_field = "reward_%s" % fee_type
            sql_str = 'select sum(%s) from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and GameId="451"' % (mysql_field,dateStr)
            fee_field = "fee_total_reward_expenditure_%s" % fee_type

            result, answers = mysql.select_data_bywhere(sql_str)
            if result == True:
                if answers[0]['sum(%s)' % mysql_field]:
                    # obj[fee_field] = answers[0]["sum(%s)" % mysql_field].to_eng_string()
                    total_fee = answers[0]["sum(%s)" % mysql_field].to_eng_string()
                    exec('%s = %s' % (fee_field,total_fee))
                    
        # 奖励支出需要加上红包赛的数量
        info1 = bag_redis.hgetall(RED_ENVELOPE_DAY_INFO % (dateStr,))
        rp_fee_total_reward_expenditure_redpacket = abs(int(info1.get('30',0))) + abs(int(info1.get('60',0))) + abs(int(info1.get('120',0))) #当天发放红包
        rp_fee_total_reward_expenditure_yuanbao = abs(int(info1.get('3',0))) + abs(int(info1.get('6',0))) + abs(int(info1.get('12',0))) # 当天发放元宝

        fee_total_reward_expenditure_yuanbao = fee_total_reward_expenditure_yuanbao + rp_fee_total_reward_expenditure_yuanbao
        fee_total_reward_expenditure_redpacket = fee_total_reward_expenditure_redpacket + rp_fee_total_reward_expenditure_redpacket

        # AI波动金币价值（赢-输的价值）
        income_value_of_AI_fluctuating_gold_coin = 0
        sql_str = 'select sum(playerGolds) from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and GameId="451"' % dateStr
        result, answers = mysql.select_data_bywhere(sql_str)
        if result == True:
            if answers[0]['sum(playerGolds)']:
                income_value_of_AI_fluctuating_gold_coin -= int(answers[0]['sum(playerGolds)'])




        # ai波动金额
        tool_id_map = {'yuanbao':3,'gold':2}
        robot_level = ['B' , 'D']

        redis_db8 = get_db(8)
        income_value_of_AI_fluctuating_gold_coin = 0
        today = dateStr

        #for day in day_list:
        for level in robot_level:
            for tool in tool_id_map.items():
                field = '%s_%s' % (level,tool[0])
                sql_str = "RobotGather:%s:%s:%s" % (level,dateStr,tool[1])
                exec('%s = 0' % field)
                exec('rtn = redis_db8.get("%s")' % (sql_str))
                if rtn:
                    exec('%s = int(rtn)' % field)

                exec('rmb_value = transfer_into_RMB(tool_price_map,tool[0],%s)' % field)
                exec('income_value_of_AI_fluctuating_gold_coin += rmb_value')
        income_value_of_AI_fluctuating_gold_coin = round(income_value_of_AI_fluctuating_gold_coin,2)

        # 获取 特殊支出
        fee_special_fee = 0
        special_fee_sql = "select special_fee_active from operate_data_record where data_date = '%s'"  % dateStr
        result, answers = mysql.select_data_bywhere(special_fee_sql)
        if result == True:
           if len(answers)>0:
                    fee_special_fee = float(answers[0]['special_fee_active'])        

        obj['date'] = dateStr
        obj['population_of_players_in_gold'] = population_of_players_in_gold
        obj['population_of_players_in_match'] = population_of_players_in_match        
        obj['total_round_in_gold'] = total_round_in_gold    
        obj['total_qty_of_games_in_match_house']  = total_qty_of_games_in_match_house
        obj['income_total_value_from_golden_house_fee'] = income_total_value_from_golden_house_fee 
        obj['amount_of_recharge_yuan_bao'] = amount_of_recharge_yuan_bao  
        obj['amount_of_recharge_gold_coin'] = amount_of_recharge_gold_coin
        obj['total_cash_value_of_recharge'] = total_cash_value_of_recharge
        obj['income_total_value_from_competition_house_fee_yuanbao'] =\
         income_total_value_from_competition_house_fee_yuanbao
        obj['income_total_value_from_competition_house_register_fee_gold'] =  transfer_into_RMB(tool_price_map,'gold',int(obj['income_total_value_from_competition_house_register_fee_gold']))
        obj['income_total_value_from_competition_house_register_fee_yuanbao'] =  transfer_into_RMB(tool_price_map,'yuanbao',int(obj['income_total_value_from_competition_house_register_fee_yuanbao']))
        obj['income_total_value_from_competition_house_register_fee_roomCard'] =  transfer_into_RMB(tool_price_map,'diamond',int(obj['income_total_value_from_competition_house_register_fee_roomCard']))
        obj['fee_total_welfare_expenditure_gold'] =  transfer_into_RMB(tool_price_map,'gold',total_welfare_fee_gold)
        obj['fee_total_welfare_expenditure_vcoin'] = transfer_into_RMB(tool_price_map,'yuanbao',total_welfare_fee_vcoin)
        #  这个汇率没有
        obj['fee_total_welfare_expenditure_bag'] = 0 # total_welfare_fee_bag 暂时设为0        
        obj['fee_total_reward_expenditure_gold'] = transfer_into_RMB(tool_price_map,'gold',fee_total_reward_expenditure_gold)
        obj['fee_total_reward_expenditure_roomCard'] =  transfer_into_RMB(tool_price_map,'room_card',fee_total_reward_expenditure_roomCard)
        obj['fee_total_reward_expenditure_yuanbao'] = transfer_into_RMB(tool_price_map,'yuanbao',fee_total_reward_expenditure_yuanbao)
        obj['fee_total_reward_expenditure_redpacket'] = transfer_into_RMB(tool_price_map,'redpacket',fee_total_reward_expenditure_redpacket)
        obj['income_value_of_AI_fluctuating_gold_coin'] = income_value_of_AI_fluctuating_gold_coin             
        obj['fee_special_fee'] = fee_special_fee 
        obj['profit_of_today'] = total_profit_of_the_day(obj)
        res.append(obj)
        endDate -= deltaTime
    return {'data':res}

def if_not_uid_return_uid(redis,account):
    try:
        obj = int(account)
        return account
    except:
        rtn = redis.get('users:account:%s' % account)
        if rtn:
            uid = rtn.split(':')[1]
            return uid
        else:
            return None

def get_tool_price():
    # 得到道具兑人民币的价格
    tool_price = {}
    toolName_id_map = {'gold':2,'yuanbao':3,'diamond':1,'room_card':6,'redpacket':4}
    from bag.bag_config import bag_redis
    for obj in toolName_id_map.items():
        item_id = obj[1]
        item_name = obj[0]
        dic = bag_redis.hgetall(ITEM_ATTRS%item_id)
        if dic:
            tool_price[item_name] = float(dic['price'])
    return tool_price

def transfer_into_RMB(tool_price_map,tool_type,amount):
    return round(amount * tool_price_map[tool_type] ,2)

def get_db(num):
    from bottle import default_app
    conf = default_app().config
    host = str(conf.get('redis.host'))
    port = conf.get('redis.port')
    database = num
    pwd = ""
    redisdb = redis.ConnectionPool(host=host, port=port, db=num, password=pwd)
    return redis.Redis(connection_pool=redisdb)

def total_profit_of_the_day(dic):
    total_fee = 0
    total_income = 0
    for obj in dic.items():
        if obj[0].split('_')[0] == 'income':
            if isinstance(obj[1],float):
                total_income += obj[1]
            else:
                try:
                    total_income += float(obj[1])
                except:
                    return 'error'

        elif obj[0].split('_')[0] == 'fee':
            if isinstance(obj[1],float):
                total_fee += obj[1]
            else:
                try:
                    total_fee += float(obj[1])
                except:
                    return 'error'
    profit = total_income - total_fee
    return round(profit,2)

def get_ai_config_value(redis,game_id):
    '''
    获取ai配置的值
    :param redis: 主库
    :param game_id: 游戏id
    :return: rtn_value 
    '''    
    rtn_value = {}
    format_str = 'RobotD:%s:gold:hesh'
    sql_str = format_str % game_id 
    hgetall_return = redis.hgetall(sql_str)
    if hgetall_return:
        for key_tmp in hgetall_return.keys():
            value_str = hgetall_return[key_tmp]
            value_lsit = value_str.split('|')
            for index in range(0,3):
                rtn_key = key_tmp+'_'+str(index)
                rtn_value[rtn_key] = value_lsit[index]
    return rtn_value

def get_gold_ai_accumulated_value(redis):
    '''
     获取累计调控值
    :param redis: 主库
    :return: rtn_value 
    '''
    robot_d_sql_str = 'RobotD:AddValue:hesh'
    robot_range_sql_str = 'RobotD:RangeValue:list'
    rtn_value = {}
    robot_d_return = redis.hgetall(robot_d_sql_str)
    rtn_value['Ai_B_Pct'] = '无数据'
    rtn_value['Ai_D_Pct'] = '无数据'
    rtn_value['Player_Pct'] = '无数据'
    rtn_value['Default_Pct'] = '无数据'
    if robot_d_return:
        if robot_d_return['Ai_B_Pct']:
            rtn_value['Ai_B_Pct'] = robot_d_return['Ai_B_Pct']
        if robot_d_return['Ai_D_Pct']:
            rtn_value['Ai_D_Pct'] = robot_d_return['Ai_D_Pct']
        if robot_d_return['Player_Pct']:
            rtn_value['Player_Pct'] = robot_d_return['Player_Pct']
        if robot_d_return['Default_Pct']:   
            rtn_value['Default_Pct'] = robot_d_return['Default_Pct']
           
    accumulated_value_list =  []
    accumulated_value_list = redis.lrange(robot_range_sql_str,0,-1)
    list_tem = []
    for i in range(0,len(accumulated_value_list)):
        list_tem.append(accumulated_value_list[i].split('|'))
    print(list_tem)
    rtn_value['accmulated_list'] = list_tem

    return rtn_value

def get_active_people(redis,mysql_ins,data_date):
    '''
     获取活跃人数的集合
    :param redis: 主库
    :return: 数据对应日期
    '''    
    pass

def get_compete_user_id_set(redis,mysql,data_date,bag_redis):
    # 获取当天参与比赛场用户ID的集合
    # 返回集合
    # 统计比赛场的人数 

    total_population_match_house = 0
    total_population_match_house_set = set()
    sql_str = 'select Accounts from MatchLog where DATE_FORMAT( StartTime, "%%Y-%%m-%%d") = "%s" and GameId="451"' % data_date
    result, answers = mysql.select_data_bywhere(sql_str)
    if result == True:
        for acc in answers:
            if acc['Accounts']:
                if '|' in acc['Accounts']:
                    acc_list =acc['Accounts'].split('|')
                    for acc_obj in acc_list:
                        acc_uid = if_not_uid_return_uid(redis,acc_obj.strip())
                        total_population_match_house_set.add(acc_uid)
                else:
                    acc_uid = if_not_uid_return_uid(redis,acc['Accounts'].strip())
                    total_population_match_house_set.add(acc_uid)
    # 比赛场人数需要加上背包系统的
    acc_set = bag_redis.smembers(RED_ENVELOPE_PLAYER_SET % data_date)
    if acc_set:
        total_population_match_house_set = total_population_match_house_set.union(acc_set)

    set_between_0_and_2000 = set()
    for uid in total_population_match_house_set:
        if int(uid) >=0 and int(uid) <= 2000:
            set_between_0_and_2000.add(uid)
    
    total_population_match_house_set = total_population_match_house_set - set_between_0_and_2000
    return total_population_match_house_set

def transfer_account_to_uid(redis,account):
    user_table = redis.get(FORMAT_ACCOUNT2USER_TABLE % account)
    if not user_table:
        return None
    uid =  user_table.split(':')[1]
    return uid

def update_special_fee_in_db(value,data_date,table_type):
    """
        param: table_type 0 表示运营总表  1 表示活跃玩家运营表
    """
    mysql = get_mysql()
    if '0' == table_type:
        sql_str = "insert into operate_data_record (data_date,special_fee) values ('%s',%s) \
                    on duplicate key update data_date=VALUES(data_date),special_fee = values(special_fee)"\
                    % (data_date,value)
    elif '1' == table_type:
        sql_str = "insert into operate_data_record (data_date,special_fee_active) values ('%s',%s) \
                    on duplicate key update data_date=VALUES(data_date),special_fee_active = values(special_fee_active)"\
                    % (data_date,value)
    result,answer = mysql.execute(sql_str)
    if result:
        print('update special_fee successfully')
        return True
    else:
        return False

def get_gold_user_id_set(r,game_id_list,data_date):
    # 获取当天参与金币场用户ID的集合
    # 返回集合

    account_set = set()
    uid_set = set()
    for game_id in game_id_list:
        game_redis = getPrivateRedisInst(r,game_id)
        if game_redis is None:
            game_redis = r
        player_set =  game_redis.smembers(GOLD_ACCOUNT_SET%(game_id,data_date))
        account_set = account_set.union(player_set)

    for account in account_set:
        uid = transfer_account_to_uid(r,account)
        if uid == None:
            continue
        # 排除uid是 0到2000的账户
        if int(uid) >=0 and int(uid) <= 2000:
            continue
        uid_set.add(uid)

    return uid_set

