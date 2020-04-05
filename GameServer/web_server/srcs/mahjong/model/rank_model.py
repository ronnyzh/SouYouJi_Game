# -*- coding:utf-8 -*-

from hall_db_define import  HALL_MONEY_RANK_WITH_AGENT_ZSET,HALL_ACTIVE_RANK_WITH_AGENT_ZSET,HALL_HONOR_RANK_WITH_AGENT_ZSET,\
    LIKE_INFO

# 邮箱表
EMAIL_HASH = "email:id:%s:hash"
# 用户邮箱集合表
USER_EMAIL_SET = "user:uid:%s:email:set"
from bag.bag_config import bag_redis
from goldModel import get_user_info
from goldModel import getPrivateRedisInst
import time
from datetime import datetime
import uuid


def get_rank_info(redis,rank_type,groupid,player_uid,begin_pos,end_pos):
    """
        param rank_type 需要获取的排行榜的类型。
    """
    redis_ins = bag_redis
    rank_type_dic = {0:HALL_MONEY_RANK_WITH_AGENT_ZSET,1:HALL_ACTIVE_RANK_WITH_AGENT_ZSET,2:HALL_HONOR_RANK_WITH_AGENT_ZSET}
    zset_format = rank_type_dic[rank_type]
    res = {}
    res['rank'] = []
    my_user_info = redis.hgetall('users:%s' % player_uid)
    # 金币排行榜
    rank = begin_pos
    try:
        for uid, value in redis_ins.zrevrange(zset_format % groupid, begin_pos, end_pos, True):
            rank += 1
            value = int(value)
            user_info = redis.hgetall('users:%s'% uid)
            if not user_info:
                continue
            # 是否点赞
            is_like =  is_like_today(redis,player_uid,uid)
            res['rank'].append({'rank': rank, 'nickname': user_info['nickname'], 'value': value,
                                     'account': user_info['account'], 'headImgUrl': user_info['headImgUrl'],
                                     'like': int(user_info['like_qty']),'sex':user_info['sex'],'is_like':is_like,'like_uid':uid})                        

    except Exception as err:
        print('exception: ',err)
        return {-1:'获取排行榜错误'}

    try:
        myrank = redis_ins.zrevrank(zset_format % groupid, player_uid)
        myvalue = redis_ins.zscore(zset_format % groupid, player_uid)
        like_qty = int(my_user_info['like_qty']) if my_user_info.has_key('like_qty') else 0
        if  myrank != None:
            res['rank'].append({'rank': int(myrank)+1, 'nickname': my_user_info['nickname'], 'value': myvalue,
                                    'account': my_user_info['account'], 'headImgUrl': my_user_info['headImgUrl'], 
                                    'like': like_qty,'self': '1','sex':my_user_info['sex'],'is_like':True,'like_uid':player_uid})
        else:
            return {-2:'获取排行榜失败，无法获取账号信息'}

    except Exception as err:
        print('..........................................exception: ',err)
        return {-3:'获取排行榜失败，账户异常'}
    return res

def update_rank_info(redis,rank_type,agentid,uid,qty):
    """
        这个方法用于更新排行榜的数据
        param redis 主库 db1
        param rank_type 排行的类型  {0:金币排行，1:活跃排行，2:荣耀排行} 
        param agent_id 工会id 
        param account 账号
        param qty 变化的数量
        例子：
            1，uid 是123 的 客户 玩了跑得快 赢了2000万。

    """
    rank_type = {0:HALL_MONEY_RANK_WITH_AGENT_ZSET,1:HALL_ACTIVE_RANK_WITH_AGENT_ZSET,2:HALL_HONOR_RANK_WITH_AGENT_ZSET}
    zset_format = rank_type[rank_type]
    redis.zadd(zset_format % agentid, uid, qty)

def is_like_today(redis,uid1,uid2):
    """
        判断uid1 今天是否点赞了 uid2
    """
    redis_ins = bag_redis
    today_str = datetime.strftime(datetime.now(),'%Y-%m-%d')
    like_field = LIKE_INFO % (today_str,uid2)
    return_vle = redis_ins.sismember(like_field,uid1)
    if 1 == return_vle:
        return True
    else:
        return False

def set_like_info(redis,uid,like_uid):
    """
        这个方法用于处理点赞
        param redis 主库 db1
        param uid 用户的uid
        param account 被点赞的账号的uid        
    """
    # 还没定用哪个redis 
    redis_ins = bag_redis
    today_str = datetime.strftime(datetime.now(),'%Y-%m-%d')
    like_field = LIKE_INFO % (today_str,like_uid)
    return_vle = redis_ins.sismember(like_field,uid)
    if uid == like_uid:
        return {-1:'不能为自己点赞'}    
    if 1 == return_vle:
        return {-2:'今日已经点赞过了'}
    redis_ins.sadd(like_field,uid)
    redis.hincrby('users:%s' % like_uid,'like_qty',1) 
    is_show_info = redis.hget('users:%s' % uid,'is_show_info')
    # 显示个人信息，才发送邮件
    if is_show_info == '1':
        send_like_email(redis,uid,like_uid)
    return {0:'点赞成功'}

def send_like_email(redis,uid,like_uid):
    redis_ins = bag_redis
    user_table = redis.hgetall("users:%s"%uid)
    title = '%s 为您点赞' % (user_table['account'])
    email_type = 1
    body = ''
    like_info = {}
    like_info_list = ['wechat','qq','phone','uid','like_qty','user_title']
    for obj in like_info_list:
        try:
            like_info[obj] = user_table[obj]
        except:
            if obj == 'like_qty':
                like_info['like_qty'] = 0
            else:   
                like_info[obj] = ''
    try:
        province_dic = redis.hgetall('province')
        like_info["province"] = province_dic[user_table['province_id']]
    except:
        like_info["province"] = ''
    email_id = uuid.uuid4().hex
    redis_ins.hmset(EMAIL_HASH % email_id,{
        "title":title ,
        "body": body,
        "send_time": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
        "read": 0,
        "timestamp": str(time.time()),
        "email_type": 1,
        "like_info": like_info,
        "awards": ''
    })
    redis_ins.sadd(USER_EMAIL_SET % like_uid, email_id)    