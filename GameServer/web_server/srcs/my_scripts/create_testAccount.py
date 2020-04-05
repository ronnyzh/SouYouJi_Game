# -*- coding:utf-8 -*-

# import redis_instance
import datetime
import md5
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from redis_instance import getInst
from server_common.web_db_define import *

FORMAT_REG_DATE_TABLE = "reg:date:account:%s"
FORMAT_USER_COUNT_TABLE = "users:count"
FORMAT_USER_TABLE = "users:%s"
FORMAT_ACCOUNT2USER_TABLE = "users:account:%s"
redis = getInst(1)

'''-----配置区(开始)-----'''
PingNumStart = 300
PingNumEnd = 500
agentId = '000000'
# 新增的用户账号的uid是否用自增ID,否则使用ping后缀的数字作为ID,比如ping22就是22
incrUid = False
# 存在uid相同.是否覆盖
existsCover = True
# 默认钻石
defaultCard = 88
'''-----配置区(结束)-----'''

if agentId:
    if not redis.exists(AGENT_TABLE % (agentId)):
        raise Exception('代理号[%s]不存在' % (agentId))


def initAccount(account):
    curTime = datetime.datetime.now()
    curRegDateTable = FORMAT_REG_DATE_TABLE % (curTime.strftime("%Y-%m-%d"))
    # 创建新的用户数据
    if incrUid:
        id = redis.incr(FORMAT_USER_COUNT_TABLE)
    else:
        id = account.split('ping')[1]
    table = FORMAT_USER_TABLE % (id)
    if redis.exists(table):
        if not existsCover:
            print('用户[%s]已存在,忽略' % (id))
            return False
        print('用户[%s]已存在,将被覆盖' % (id))

    pipe = redis.pipeline()
    pipe.hmset(table, {
        'account': account,
        'password': md5.new('ping').hexdigest(),
        'nickname': account,
        'name': account,
        'currency': 'CNY',  # 国家需要做微信到数据库的变换映射
        'money': 0.0,
        'wallet': 0.0,
        'vip_level': 0,
        'exp': 0,
        'level': 0,
        'charge': 0.0,
        'charge_count': 0,
        'game_count': 0,
        'coin_delta': 0,
        'parentAg': '',  # 上线代理需要获得
        'email': '',
        'phone': '',
        'valid': 1,
        'last_join_ip': '',
        'last_join_date': '',
        'last_exit_ip': '',
        'last_exit_date': '',
        'last_login_ip': '',
        'last_login_date': '',
        'last_logout_ip': '',
        'last_logout_date': '',
        'last_present_date': '',
        'newcomer_present_date': '',
        'reg_ip': '192.168.0.1',
        'reg_date': curTime.strftime("%Y-%m-%d %H:%M:%S"),
        'coin': 0,
        'accessToken': '',  # 以下新增
        'refreshToken': '',
        'openid': '',
        'sex': 0,  # 性别
        'headImgUrl': '',  # 头像
        'unionID': '',
        'province_id': 0,
        'playCount': 0,
        'like_qty': 0
    })
    # 加公会
    if agentId:
        pipe.hset(table, 'parentAg', agentId)
        pipe.sadd(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE % (agentId), id)
        pipe.set(USER4AGENT_CARD % (agentId, id), int(defaultCard))

    # pipe.set(WEIXIN2ACCOUNT%(openID), account) #微信ID到账号映射
    # pipe.sadd(ACCOUNT4WEIXIN_SET, account) #微信账号集合
    account2user_table = FORMAT_ACCOUNT2USER_TABLE % (account)
    pipe.set(account2user_table, table)
    # pipe.sadd(FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE%('CHNWX'), id) #上线代理需要获得
    pipe.sadd(curRegDateTable, account)
    pipe.execute()
    return True


def getAccount(account):
    account2user_table = FORMAT_ACCOUNT2USER_TABLE % (account)
    table = redis.get(account2user_table)
    print table
    print redis.hgetall(table)


def do():
    # 批量创建和查看账号
    for num in range(PingNumStart, PingNumEnd + 1):
        if num <= 0:
            continue
        account = 'ping' + str(num)
        if initAccount(account):
            print('创建%s成功' % account)
        # getAccount(account)


if __name__ == '__main__':
    do()
