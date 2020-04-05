#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
    牛牛消息处理
"""
import time
import functools
from datetime import datetime, timedelta
from model.serviceModle import MSG_NIUNIU_BALANCE, MSG_NIUNIU_SHARE
from model.niuniu_db_define import *
from model.niuniu_active_db_define import *
from model.niuniuModel import getPrivateRedisInst, check_account_in_try_play_groups
from tsconfig import log_debug, str2timestamp2, config, get_pub_inst

redis = getPrivateRedisInst(get_pub_inst(), NIUNIU_GAMEID)
ActiveTable = NIUNIU_ACTIVI_CONFIG_TABLE


def _get_next_day(baseday, n):
    return datetime.strptime(baseday, '%Y-%m-%d') + timedelta(days=n)


def on_niuniu_balance(table, data):
    """
        牛牛活动前三天每拿到一手牛牛及以上的牌型
        即获得一次抽奖机会
    """
    if not is_niuniu_active_openning(redis):
        log_debug(u'牛牛活动还没开始或已经结束')
        return
    date = time.strftime('%Y-%m-%d', time.localtime(data['start_time']/1000))
    # date = datetime.now().strftime('%Y-%m-%d')
    cur_date = datetime.strptime(date, '%Y-%m-%d')
    nday = functools.partial(_get_next_day, redis.hget(ActiveTable, 'start_date')[:10])
    if cur_date >= nday(4):
        log_debug(u'活动已经进行三天以上 开始时间{0}'.format(nday(0)))
        return
    pipe = redis.pipeline()
    accounts = data['accounts'].split('|')
    niuniu_accounts = []
    for index, account in enumerate(accounts):
        if check_account_in_try_play_groups(get_pub_inst(), account):
            continue
        bull = int(data['bull_info'].split('|')[index])
        if bull < 10:
            continue
        if bull == 10:
            niuniu_accounts.append(account)
            # account牛牛次数+1
            pipe.hincrby(NIUNIU_ACCOUNT_STACTICS_TABLE % account, 'niuniu_count')
        # # 一天内不得多次获得抽奖机会
        # if redis.hexists(NIUNIU_COUNT_LARGE_TABLE_BY_DAY % date, account):
        #    continue
        pipe.hincrby(NIUNIU_COUNT_LARGE_TABLE_BY_DAY % date, account)
        # 抽奖次数+1
        pipe.hincrby(NIUNIU_ACCOUNT_STACTICS_TABLE % account, 'draw_times')
        # 总剩余抽奖次数+1
        pipe.hincrby(NIUNIU_GAME_OPERATE_TABLE, 'draw_last_count')
    pipe.execute()
    return {'result': True, 'data': niuniu_accounts, 'content': u'恭喜您获得一次抽奖机会！！！'}


def on_niuniu_share(table, data):
    """
        牛牛活动期间分享即可获得抽奖机会
        即获得一次抽奖机会
    """
    if not is_niuniu_active_openning(redis):
        log_debug(u'牛牛活动还没开始或已经结束')
        return
    account = data['account']
    if check_account_in_try_play_groups(get_pub_inst(), account):
        return {'code': 1, 'msg': '您是试玩工会玩家'}
    today = datetime.now().strftime('%Y-%m-%d')
    if account in redis.smembers(NIUNIU_GAME_SHARE_ACCOUNTS_SET % today):
        return {'code': 1, 'msg': '您已经分享过'}

    pipe = redis.pipeline()
    pipe.sadd(NIUNIU_GAME_SHARE_ACCOUNTS_SET % today, account)
    pipe.hincrby(NIUNIU_ACCOUNT_STACTICS_TABLE % account, 'share_count')
    pipe.hincrby(NIUNIU_ACCOUNT_STACTICS_TABLE % account, 'draw_times')
    pipe.hincrby(NIUNIU_GAME_OPERATE_TABLE, 'draw_last_count')
    pipe.execute()
    return {'code': 0, 'msg': '分享成功'}


"""
    事件处理定义
"""
niuniu_handles = {
    MSG_NIUNIU_BALANCE: on_niuniu_balance,
    MSG_NIUNIU_SHARE: on_niuniu_share,
}


def clear_db():
    pipe = redis.pipeline()
    for key in redis.keys('niuniu:game:*'):
        pipe.delete(key)
    for key in redis.keys('mpniuniu:game:*'):
        pipe.delete(key)
    return pipe.execute()


def set_niuniu_active():
    """ 
        设置牛牛活动时间 
    """
    redis.hmset(ActiveTable, config['niuniu_active'])
    print '活动信息:{0}'.format(redis.hgetall(ActiveTable))


def check_niuniu_active():
    """ 
        监听牛牛活动状态
    """
    if not redis.exists(ActiveTable):
        log_debug('当前没有牛牛活动')
        return
    info = redis.hgetall(ActiveTable)
    if not info:
        return
    start_time = str2timestamp2(info['start_date'])
    end_time = str2timestamp2(info['end_date'])
    if end_time <= start_time:
        return
    cur_time = time.time()
    status = info.get('status', '')
    if status == '0':
        log_debug('牛牛活动未开始')
    if cur_time - start_time > 0 and status == '0':
        redis.hset(ActiveTable, 'status', 1)
        log_debug('牛牛活动开始')
    if end_time - cur_time < 0 and status == '1':
        redis.hset(ActiveTable, 'status', 2)
        log_debug('牛牛活动结束')


def register_handles(worker):
    """ 
        注册事件
    """
    worker.appendServiceProtocols(niuniu_handles)



