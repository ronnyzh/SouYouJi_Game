#coding:utf-8
from bag_config import bag_redis,Mysql_instance
from bottle import request, Bottle, abort, redirect, response, template,static_file
from common import web_util
from common.log import *
from common.utilt import *
from datetime import datetime,timedelta
from web_db_define import *
from bag_log import *
from common.record_player_info import record_player_balance_change
import json
import time
import uuid

bag_app = Bottle()

# 时限道具映射
LIMIT_ITEM_MAP = {
    "9":"jipaiqi",
    "10":"jipaiqi",
    "11":"jipaiqi",
    "12":"jipaiqi",
    "8":"good_card",
}

def get_remain_time(rc,uid,key):
    now = datetime.now()
    end_time = rc.split('|')[1]
    end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    if end < now:
        bag_redis.hdel('user:%s:buff' % uid,key)
        return ""
    remains = str(end - now).split(' ')
    if len(remains) == 3:
        r_day, r_time = remains[0], remains[2].split(':')
        hour, min, sec = r_time[0], r_time[1], r_time[2][:2]
    else:
        r_day = 0
        r_time = remains[0].split(':')
        hour, min, sec = r_time[0], r_time[1], r_time[2][:2]
    return "剩余时间为%s天%s小时%s分%s秒"%(r_day,hour,min,sec)

@bag_app.post('/single/detail')
@web_util.allow_cross_request
def get_all_item_by_uid(redis,session):
    """
        根据uid获取所拥有的所有道具id和数量
    """
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    item_id = request.forms.get('item_id', '').strip()

    key = None
    limit_msg = ""
    if item_id in LIMIT_ITEM_MAP.keys():
        key = LIMIT_ITEM_MAP[item_id]
    rc = bag_redis.hget('user:%s:buff' % uid, key)
    if rc:
        rl = rc.split('|')
        if rl[0] == 'times':
            limit_msg = "当前剩余%s次"%rl[1]
        else:
            limit_msg = get_remain_time(rc,uid,key)

    title,des,can_use = bag_redis.hmget(ITEM_ATTRS%item_id,'title','des','can_use')
    can_use = int(can_use if can_use else 0)
    num = get_player_item(item_id,uid)

    if item_id == '6':
        groupId = redis.hget('users:%s'%uid,'parentAg')
        num =  redis.get(USER4AGENT_CARD % (groupId, uid))

    """
    
    hint = None
    if item_id in LIMIT_ITEM_MAP.keys():
        buff_sts = bag_redis.hget('user:%s:buff',LIMIT_ITEM_MAP[item_id])
        if buff_sts:
            blist = buff_sts.split(':')
            if blist[0] == 'times':
                hint = "剩余次数:%s次"%blist[1]
            else:
                datetime.strptime(blist[1])
    """
    #  加入兑奖价格列表
    price_list = []

    mysql = Mysql_instance()
    sql = "select price from reward_course_config where item_id = '%s'"%item_id
    mysql.cursor.execute(sql)
    res = mysql.cursor.fetchall()
    for row in res:
        price_list.append(row[0])

    res = json.dumps({"code":0,"title":title,'des':des,'num':num,'can_use':can_use,'limit_msg':limit_msg,'price_list':price_list})
    return res

@bag_app.post('/all/items')
@web_util.allow_cross_request
def get_all_item_by_uid(redis,session):
    """
        根据uid获取所拥有的所有道具id和数量
    """
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    items = bag_redis.hgetall(PLAYER_ITEM_HASH%uid)

    # 必显示道具列表
    for iid in ["3","5","13","14"]:
        if iid not in items.keys():
            items[iid]  = 0
    data = []
    for item_id,num in items.items():
        title,des,can_use,bag_show,unit,can_reward = bag_redis.hmget(ITEM_ATTRS%item_id,'title','des','can_use','bag_show','unit','can_reward')
        if bag_show != '1':
            continue
        if int(item_id) == 6:
            # 钻石特殊获取
            groupId = redis.hget('users:%s'%uid,'parentAg')
            num =  redis.get(USER4AGENT_CARD % (groupId, uid)) or 0

        data.append({
            "item_id":item_id,
            "num":num,
            "title":title,
            "unit":int(unit or 0),
            "can_reward":int(can_reward or 0),
        })

    res = json.dumps({"code":0,"data":data})
    return res

@bag_app.post('/item/num')
@web_util.allow_cross_request
def get_num_of_item(redis,session):
    """
        根据uid和道具id获取道具的数量
    """
    item_id = request.forms.get('item_id', '').strip()
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    num = bag_redis.hget(PLAYER_ITEM_HASH%uid,item_id)

    if num:
        return {"code":0,"num":num}
    else:
        return {"code":0,"num":0}

def give_player_item(item_id,uid,num):
    """
        给予玩家num数量的道具
    """
    try:
        if bag_redis.hexists(PLAYER_ITEM_HASH%uid,item_id):
            cur_num = bag_redis.hget(PLAYER_ITEM_HASH%uid,str(item_id))
            if not cur_num:
                cur_num = 0
            new_num = str(int(cur_num) + int(num))
            bag_redis.hset(PLAYER_ITEM_HASH%uid,item_id,new_num)

        else:
            new_num = num
            bag_redis.hset(PLAYER_ITEM_HASH%uid,str(item_id),num)
    except Exception as e:
        log_debug(e)
        return None
    else:
        return new_num

# 消耗玩家道具
def cost_player_item(item_id,uid,num):
    if bag_redis.hexists(PLAYER_ITEM_HASH%uid,item_id):
        cur_num = bag_redis.hget(PLAYER_ITEM_HASH%uid,str(item_id))
        if not cur_num:
            return False
        new_num = (int(cur_num) - int(num))
        if new_num < 0:
            return False
        else:
            bag_redis.hset(PLAYER_ITEM_HASH%uid,item_id,new_num)
            return True
    else:
        return False

#获取玩家道具数量
def get_player_item(item_id,uid):
    cur_num = bag_redis.hget(PLAYER_ITEM_HASH%uid,str(item_id))
    if cur_num:
        return int(cur_num)
    else:
        return 0

def buyItem(redis,sid,item_id,num):
    num = int(num)
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    gold = redis.hget(FORMAT_USER_TABLE%uid,'gold')
    if gold:
        gold = int(gold)
    else:
        return {"code":1,"msg":'no gold'}

    item_id = int(item_id)
    price = bag_redis.hget(ITEM_ATTRS%item_id,"price")
    price = int(price)
    cost = price

    if gold < cost:
        return {"code":1,"msg":'is not enough'}

    res_gold = gold - cost
    redis.hset(FORMAT_USER_TABLE%uid,'gold',res_gold)
    give_player_item(item_id,uid,num)
    return {"code":0,"msg":'ok'}

# 大厅新增商品
def hall_add_bag_goods(goodsInfo,choice_type,_type):
    data = goodsInfo
    cids = bag_redis.smembers("currency:change:course:set")
    for cid in cids:
        name, cost, gain,cost_type,gain_type = bag_redis.hmget("currency:change:course:%s:hesh" % cid, 'name', 'cost', 'gain','cost_type','gain_type')
        if gain_type == choice_type:
            data.append({
                "id": cid,
                "price": cost,
                "name": name,
                "cards": gain,
                "type":_type,
                "c_change":1
            })
    return data

@bag_app.post('/use')
@web_util.allow_cross_request
def use_player_item(redis,session):
    """
        使用玩家num数量的道具
    """
    item_id = request.forms.get('item_id', '').strip()
    sid = request.forms.get('sid', '').strip()
    num = request.forms.get('num', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    mysql = Mysql_instance()
    sql = "select distinct(item_id) from reward_course_config"
    mysql.cursor.execute(sql)
    res = mysql.cursor.fetchall()
    rewards = []
    for row in res:
        rewards.append(row[0])
    mysql.close()

    if item_id in rewards:
        return getRewardCode(redis,uid,item_id,num)

    if bag_redis.hexists(PLAYER_ITEM_HASH%uid,item_id):
        cur_num = get_player_item(item_id,uid)
        if int(cur_num) == 0:
            return {"code":1,"msg":"道具数量不足！"}
        new_num = int(cur_num) - int(num)
        if new_num < 0:
            return {"code":2,"msg":"道具数量不足。"}
        else:
            bag_redis.hset(PLAYER_ITEM_HASH%uid,item_id,new_num)
            if new_num == 0:
                bag_redis.hdel(PLAYER_ITEM_HASH%uid,item_id)
            #res = use_item_effect(item_id,num)
            log_bag(uid,item_id,num)
            return {"code":0,"msg":"ok","type":item_id}
    else:
        return {"code":1,"msg":"道具数量不足！"}

@bag_app.post('/send/mail')
@web_util.allow_cross_request
def send_mail(redis,session):
    """
        发送邮件接口
    """
    title = request.forms.get('title', '').strip()
    uid = request.forms.get('uid', '').strip()
    body = request.forms.get('body', '').strip()
    awards = request.forms.get('awards', '').strip()

    email_id = uuid.uuid4().hex
    bag_redis.hmset(EMAIL_HASH%email_id,{"title":title,"body":body,"awards":awards,"send_time":datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'),"read":0,"timestamp":int(time.time()*1000)})
    bag_redis.sadd(USER_EMAIL_SET%uid,email_id)
    return {"code":0,"msg":"ok"}

def inner_send_mail(title,uid,body,awards):
    """
        内部发送邮件接口
    """
    email_id = uuid.uuid4().hex
    e_num = bag_redis.scard(USER_EMAIL_SET%uid)
    if e_num >= 200:
        return {"code":1,"msg":"mail num more than 200"}
    bag_redis.hmset(EMAIL_HASH%email_id,{"title":title,"body":body,"awards":awards,"send_time":datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'),"read":0,"timestamp":int(time.time()*1000)})
    bag_redis.sadd(USER_EMAIL_SET%uid,email_id)
    return {"code":0,"msg":"ok"}

def check_user_mail_num(uid):
    num = bag_redis.scard(USER_EMAIL_SET%uid)
    if num >= 100:
        return False
    else:
        return True

@bag_app.post('/see/mail')
@web_util.allow_cross_request
def use_player_item(redis,session):
    """
        查看邮件列表
    """
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}

    if not redis.exists(SessionTable):
        return {'code':-3,'msg':'sid 超时'}
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code':-5,'msg':'该用户不存在'}

    nowTime = int(time.time()*1000)
    eids = bag_redis.smembers(USER_EMAIL_SET%uid)
    data = []
    for eid in eids:
        dic = {}
        if not bag_redis.exists(EMAIL_HASH % eid):
            bag_redis.srem(USER_EMAIL_SET % uid, eid)
            continue
        title,body,read,timestamp,valid_time,read_time,awards,is_get = bag_redis.hmget(EMAIL_HASH % eid,"title","body","read",'timestamp', 'valid_time', 'read_time', 'awards', 'is_get')
        if valid_time and read_time:
            if float(nowTime) - float(read_time) > float(valid_time) * 86400 * 1000:
                bag_redis.srem(USER_EMAIL_SET % uid, eid)
                continue
        dic['email_id'] = eid
        dic['timestamp'] = timestamp if timestamp else 0
        dic['read'] = read
        dic['title'] = title
        dic['is_get'] = is_get
        dic['body'] = body
        dic['has_awards'] = True if awards else False
        data.append(dic)
    data = sorted(data,key=lambda x:float(x['timestamp']), reverse=True)
    return {"code":0,"data":data}

@bag_app.post('/open/mail')
@web_util.allow_cross_request
def use_player_item(redis,session):
    """
        打开特定邮件
    """
    eid = request.forms.get('eid', '').strip()
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code': -4, 'msg': '账号已在其他地方登录', 'osid': sid}

    if not redis.exists(SessionTable):
        return {'code': -3, 'msg': 'sid 超时'}
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}

    data = bag_redis.hgetall(EMAIL_HASH%eid)
    if not data:
        return {'code': -1, 'msg': '该邮件不存在'}

    if uid != data.get('userId'):
        return {'code': -1, 'msg': '您不能打开该邮件'}

    bag_redis.hset(EMAIL_HASH%eid,'read',1)
    valid_time, read_time, award_time = bag_redis.hmget(EMAIL_HASH % eid, ('valid_time', 'read_time', 'award_time'))
    nowTime = int(time.time()*1000)
    # 判断邮件类型
    if data.get('email_type') == '':
        data['email_type'] = 0
    elif data.get('email_type') == '1':
        data['like_info'] = eval(data['like_info'])
        data['awards'] = []
    else:
        data['email_type'] = 0

    if not data.get("awards"):
        if not valid_time and not read_time:
            bag_redis.hmset(EMAIL_HASH % eid, {'valid_time': EMAIL_RETENTION_TIME, 'read_time': nowTime})
    else:
        if not read_time:
            bag_redis.hmset(EMAIL_HASH % eid, {'read_time': nowTime})

        awards = data['awards']
        aws = awards.split('|')
        awards_list = []
        for aw in aws:
            dic = {}
            item_id = aw.split(',')[0]
            num = aw.split(',')[1]
            dic['num'] = num
            dic['item_id'] = item_id
            awards_list.append(dic)
        data['awards'] = awards_list
    data['eid'] = eid
    return {"code":0, "data":data}

@bag_app.post('/get/awards')
@web_util.allow_cross_request
def use_player_item(redis,session):
    """
        获取附件
    """
    eid = request.forms.get('eid', '').strip()
    sid = request.forms.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}

    if not redis.exists(SessionTable):
        return {'code':-3,'msg':'sid 超时'}
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code':-5,'msg':'该用户不存在'}

    if not redis.exists(EMAIL_HASH%eid):
        return {'code':-1, 'msg': '该邮件不存在'}

    userTable = FORMAT_USER_TABLE % uid
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d")
    dateTime =  curTime.strftime("%Y-%m-%d %H:%M:%S")
    awards, award_time, euid, read_time = bag_redis.hmget(EMAIL_HASH%eid, ("awards", "award_time", "userId", "read_time"))
    groupId = redis.hget('users:%s' % uid, 'parentAg')
    if euid != uid:
        return {'code': -1, 'msg': '您不能领取该邮件'}
    if not read_time:
        bag_redis.hmset(EMAIL_HASH % eid, {'read_time': int(time.time() * 1000), 'read': 1})
    if not awards:
        return {"code": 0, "msg": "ok"}
    try:
        if not award_time:
            item_nums = awards.split('|')
        else:
            return {"code": 0, "msg": "ok"}
    except Exception as e:
        item_nums = [awards]
    for item_num in item_nums:
        item_id = item_num.split(',')[0]
        num = item_num.split(',')[1]
        # 附件为钻石
        if int(item_id) == 1:
            before_card = redis.get(USER4AGENT_CARD % (groupId, uid))
            if not before_card:
                before_card = 0
            redis.incrby(USER4AGENT_CARD % (groupId, uid), int(num))
            bag_redis.hmset(EMAIL_HASH % eid, {'before_card': before_card, 'now_card': int(before_card) + int(num)})
        # 附件为游戏积分
        if int(item_id) == 3:
            before_card = redis.hget(userTable, 'gamePoint')
            if not before_card:
                before_card = 0
            redis.hincrby(userTable, 'gamePoint', int(num))
        enclosure = MATCH_AWARDS_TYPE_TABLE.get(item_id)
        redis.lpush(ENCLOSURE_MAIL_DAY % date, '%s|%s|%s|%s|%s|%s|%s' % (uid, groupId, before_card, num, dateTime, enclosure, eid))
    bag_redis.hmset(EMAIL_HASH % eid, {'is_get': '1', 'award_time': int(time.time()*1000), 'valid_time': EMAIL_RETENTION_TIME})

    # bag_redis.delete(EMAIL_HASH%eid)
    # bag_redis.srem(USER_EMAIL_SET%uid,eid)

    return {"code":0,"msg":"ok"}

@bag_app.post('/safe/box/push')
@web_util.allow_cross_request
def safeBoxPush(redis,session):
    """
        存入金币入保险箱
    """
    sid = request.forms.get('sid', '').strip()
    push_num = request.forms.get('push_num', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    gold = redis.hget(FORMAT_USER_TABLE%uid,'gold')
    if not gold:
        gold = 0

    gold = int(gold)
    p_num = int(push_num)
    if p_num > gold:
        return {"code":1,"msg":"gold is not enough"}

    remain_gold = gold -  p_num
    redis.hset(FORMAT_USER_TABLE%uid,'gold',remain_gold)
    box_gold = bag_redis.hget(SAVE_BOX_HASH,uid)
    if box_gold:
        box_gold = int(box_gold)
    else:
        box_gold = 0
    res_num = p_num + box_gold
    bag_redis.hset(SAVE_BOX_HASH,uid,res_num)
    record_box_change_into_mysql(uid,'save',remain_gold,res_num,p_num)
    return {"code":0,"user_gold":remain_gold}


@bag_app.post('/safe/box/take')
@web_util.allow_cross_request
def safeBoxPush(redis,session):
    """
        取金币从保险箱
    """
    sid = request.forms.get('sid', '').strip()
    take_num = request.forms.get('take_num', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    take_num = int(take_num)

    box_gold = bag_redis.hget(SAVE_BOX_HASH,uid)
    if box_gold:
        box_gold = int(box_gold)
    else:
        box_gold = 0

    if take_num > box_gold:
        return {"code":1,"msg":"gold is not enough"}

    remain_gold = box_gold - take_num
    bag_redis.hset(SAVE_BOX_HASH,uid,remain_gold)

    gold = redis.hget(FORMAT_USER_TABLE%uid,'gold')
    if gold:
        gold = int(gold)
    else:
        gold = 0

    res_gold = gold + take_num
    # 手续费千分之五
    res_gold = int(res_gold) - int(take_num*0.005)
    # 记录每天手续费总额
    tax = int(take_num*0.005)
    now_day = str(datetime.now())[:10]
    bag_redis.incrby('box:tax:date:%s'%now_day,tax)

    redis.hset(FORMAT_USER_TABLE%uid,'gold',res_gold)
    record_box_change_into_mysql(uid,'get',res_gold,remain_gold,take_num,tax=tax,balance_origin=gold)
    return {"code":0,"user_gold":res_gold}

def record_box_change_into_mysql(uid,getOrsave,account_balance,box_balance,balance_change,tax=0,balance_origin=0):
    """
        这个方法用于统计存取保险箱记录
    """
    user_table = 'users:%s' % uid
    if 'save' == getOrsave:
        record_player_balance_change(bag_redis,user_table,2,-balance_change,account_balance,27)
        record_player_balance_change(bag_redis,user_table,2,balance_change,box_balance,28)
    elif 'get' == getOrsave:
        record_player_balance_change(bag_redis,user_table, 2,-tax,balance_origin-tax,26)
        record_player_balance_change(bag_redis,user_table, 2,balance_change,account_balance,29)
        record_player_balance_change(bag_redis,user_table, 2,-balance_change,box_balance,30)


# 显示保险箱金额
@bag_app.get('/safe/box/show')
@web_util.allow_cross_request
def safeBoxShow(redis,session):
    sid = request.GET.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    num = bag_redis.hget(SAVE_BOX_HASH,uid)
    if not num:
       num = 0
    return {"code":0,"num":num}

# 删除邮件
@bag_app.post('/delete/mail')
@web_util.allow_cross_request
def deleteMail(redis,session):
    sid = request.forms.get('sid', '').strip()
    eids = request.forms.get('eids', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    eids = eids.split(',')
    for eid in eids:
        # bag_redis.delete(EMAIL_HASH%eid)
        bag_redis.srem(USER_EMAIL_SET%uid,eid)
    num = len(eids)

    return {"code":0,"del_num":num}

# 商城货币兑换
@bag_app.post('/currency/exchange')
@web_util.allow_cross_request
def CurrencyChange(redis,session):
    sid = request.forms.get('sid', '').strip()
    cid = request.forms.get('id', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    return exchange_dispatcher(redis,uid,cid)

def cost_dispatcher(redis,uid,cost_type,cost):
    cost = int(cost)
    # 消耗搜集游棋牌钻石
    if cost_type == '1':
        cur_ds = redis.hget('users:%s'%uid,'DSdiamond')
        cur_ds = int(cur_ds or 0)
        res_ds = cur_ds - cost
        if res_ds < 0:
            return False
        else:
            redis.hset('users:%s'%uid,'DSdiamond',res_ds)
    # 消耗金币
    elif cost_type == '2':
        cur_gold = redis.hget('users:%s'%uid,'gold')
        cur_gold = int(cur_gold or 0)
        res_gold =  cur_gold - cost
        if res_gold < 0:
            return False
        else:
            redis.hset('users:%s'%uid,'gold',res_gold)

    # 消耗钻石
    elif cost_type == '6':
        parentAg = redis.hget('users:%s'%uid,'parentAg')
        cur_roomcard = redis.get(USER4AGENT_CARD%(parentAg,uid))
        cur_roomcard = int(cur_roomcard or 0)
        res_roomcard = cur_roomcard - cost
        if res_roomcard:
            return False
        else:
            redis.set(USER4AGENT_CARD%(parentAg,uid),res_roomcard)
    else:
        return cost_player_item(cost_type,uid,cost)

    return True

def gain_dispatcher(redis,uid,gain_type,gain,cost,cost_type):
    cur_day = str(datetime.now())[:10]
    gain = int(gain)
    exchange_day_table = "exchange:" + cost_type + "To" + gain_type + ":date:%s"
    # 获得搜集游棋牌钻石
    if gain_type == '1':
        redis.hincrby('users:%s'%uid,'DSdiamond',gain)
    # 获得金币
    elif gain_type == '2':
        redis.hincrby('users:%s'%uid,'gold',gain)
    # 获得钻石
    elif gain_type == '6':
        parentAg = redis.hget('users:%s'%uid,'parentAg')
        redis.incrby(USER4AGENT_CARD%(parentAg,uid),gain)
    # 获得其他道具
    else:
        give_player_item(gain_type,uid,int(gain))

    res_gold = redis.hget('users:%s'%uid,'gold')
    res_gold = int(res_gold) if res_gold else 0
    res_DSdiamond = redis.hget('users:%s'%uid,'DSdiamond')
    res_DSdiamond = int(res_DSdiamond) if res_DSdiamond else 0
    bag_redis.incrby(exchange_day_table%cur_day,cost)
    record_exchange_into_mysql(redis,uid,gain_type,gain,cost,cost_type)
    return {"code":0,"msg":'兑换成功！','res_gold':res_gold,'res_DSdiamond':res_DSdiamond}

def exchange_dispatcher(redis,uid,cid):
    cost,gain,gain_type,cost_type,cost_title = bag_redis.hmget("currency:change:course:%s:hesh"%cid,'cost','gain','gain_type','cost_type','cost_title')
    cost,gain = int(cost),int(gain)
    # 非默认公会不允许兑换钻石
    parentAg = redis.hget('users:%s'%uid,'parentAg')
    if gain_type == '6' and parentAg != '000000':
        return {'code':-1,'msg':'兑换失败！非默认公会无法兑换钻石！'}
    if cost_dispatcher(redis,uid,cost_type,cost):
        return gain_dispatcher(redis,uid,gain_type,gain,cost,cost_type)
    else:
        return {'code':-1,'msg':'兑换失败！%s不足！'%cost_title}

def record_exchange_into_mysql(redis,uid,gain_type,gain,cost,cost_type):
    """
        这个方法用于统计商城购买记录
    """

    res_gold = redis.hget('users:%s'%uid,'gold')
    res_gold = int(res_gold) if res_gold else 0
    res_DSdiamond = redis.hget('users:%s'%uid,'DSdiamond')
    res_DSdiamond = int(res_DSdiamond) if res_DSdiamond else 0
    res_yuanbao = bag_redis.hget(PLAYER_ITEM_HASH%uid,'3')
    res_yuanbao = int(res_yuanbao) if res_yuanbao else 0
    parentAg = redis.hget('users:%s'%uid,'parentAg')
    res_roomcard = redis.get(USER4AGENT_CARD%(parentAg,uid))
    res_roomcard = int(res_roomcard) if res_roomcard else 0
    jipai_1s = bag_redis.hget(PLAYER_ITEM_HASH%uid,'9')
    jipai_10s = bag_redis.hget(PLAYER_ITEM_HASH%uid,'10')
    jipai_1day = bag_redis.hget(PLAYER_ITEM_HASH%uid,'11')
    jipai_7days = bag_redis.hget(PLAYER_ITEM_HASH%uid,'12')


    # 将兑换记录存入mysql edit by hzs
    # 钻石1 金币2 元宝3 钻石6 记牌器 (10局)10 记牌器 (1天)11 记牌器 (7天) 12
    user_table = 'users:%s' % uid
    exchange_type = cost_type + '_' + gain_type
    if '1_2' == exchange_type:
        record_player_balance_change(bag_redis,user_table,2,gain,res_gold,12)
        record_player_balance_change(bag_redis,user_table,1,-cost,res_DSdiamond,15)
    if '1_3' == exchange_type:
        record_player_balance_change(bag_redis,user_table,3,gain,res_yuanbao,13)
        record_player_balance_change(bag_redis,user_table,1,-cost,res_DSdiamond,16)
    if '1_6' == exchange_type:
        record_player_balance_change(bag_redis,user_table,6,gain,res_roomcard,14)
        record_player_balance_change(bag_redis,user_table,1,-cost,res_DSdiamond,17)
    if '2_9' == exchange_type:
        record_player_balance_change(bag_redis,user_table,9,gain,jipai_1s,18)
        record_player_balance_change(bag_redis,user_table,2,-cost,res_gold,22)
    if '1_10' == exchange_type:
        record_player_balance_change(bag_redis,user_table,10,gain,jipai_10s,19)
        record_player_balance_change(bag_redis,user_table,1,-cost,res_DSdiamond,23)
    if '1_11' == exchange_type:
        record_player_balance_change(bag_redis,user_table,11,gain,jipai_1day,20)
        record_player_balance_change(bag_redis,user_table,1,-cost,res_DSdiamond,24)
    if '1_12' == exchange_type:
        record_player_balance_change(bag_redis,user_table,12,gain,jipai_7days,21)
        record_player_balance_change(bag_redis,user_table,1,-cost,res_DSdiamond,25)


@bag_app.post('/buy/item')
@web_util.allow_cross_request
def buyItem(redis,session):
    sid = request.forms.get('sid', '').strip()
    item_id = request.forms.get('item_id', '').strip()
    num = request.forms.get('num', '').strip()
    num = int(num)
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    gold = redis.hget(FORMAT_USER_TABLE%uid,'gold')
    if gold:
        gold = int(gold)
    else:
        return {"code":1,"msg":'no gold'}

    item_id = int(item_id)
    price = bag_redis.hget(ITEM_ATTRS%item_id,"price")
    price = int(price)
    cost = price

    if gold < cost:
        return {"code":1,"msg":'is not enough'}

    res_gold = gold - cost
    redis.hset(FORMAT_USER_TABLE%uid,'gold',res_gold)
    give_player_item(item_id,uid,num)
    return {"code":0,"msg":'ok'}

# 跑马灯数据保存
def save_marquee_data(body,type):
    date_str = datetime.strftime(datetime.now(),'%Y-%m-%d')
    min_str = datetime.strftime(datetime.now(),'%M')
    bag_redis.incr('accumulate:marquee:sum',1)

    # 比赛
    if int(type) == 1:
        bag_redis.hset("match:marquee:hesh",str(datetime.now()),body)
        bag_redis.rpush("match:marquee:list:%s"%min_str,body)
        bag_redis.expire("match:marquee:list:%s"%min_str,600)
        bag_redis.incr('match:marquee:sum',1)
        bag_redis.incr('match:marquee:sum:date:%s'%date_str,1)
    # 红包兑奖
    elif int(type) == 2:
        bag_redis.hset("reddraw:marquee:hesh",str(datetime.now()),body)
        bag_redis.rpush("reddraw:marquee:list:%s"%min_str,body)
        bag_redis.expire("reddraw:marquee:list:%s"%min_str,600)
        bag_redis.incr('reddraw:marquee:sum',1)
        bag_redis.incr('reddraw:marquee:sum:date:%s'%date_str,1)
    # 活动中奖
    elif int(type) == 3:
        bag_redis.hset("actpong:marquee:hesh",str(datetime.now()),body)
        bag_redis.rpush("actpong:marquee:list:%s"%min_str,body)
        bag_redis.expire("actpong:marquee:list:%s"%min_str,600)
        bag_redis.incr('actpong:marquee:sum',1)
        bag_redis.incr('actpong:marquee:sum:date:%s'%date_str,1)
    # 活动兑奖
    elif int(type) == 4:
        bag_redis.hset("actdraw:marquee:hesh",str(datetime.now()),body)
        bag_redis.rpush("actdraw:marquee:list:%s"%min_str,body)
        bag_redis.expire("actdraw:marquee:list:%s"%min_str,600)
        bag_redis.incr('actdraw:marquee:sum',1)
        bag_redis.incr('actdraw:marquee:sum:date:%s'%date_str,1)

# 检查跑马灯信息是否存在
def check_marquee_have():
    min = datetime.strftime(datetime.now(),'%M')
    for i in range(1,4):
        min_str = str(int(min)-1)
        marquee_list = ["match:marquee:list:%s","reddraw:marquee:list:%s","actpong:marquee:list:%s","actdraw:marquee:list:%s"]
        res_list = []
        for ml in marquee_list:
            res = bag_redis.exists(ml%min_str)
            res_list.append(res)
    if not all(res_list):
        return False
    else:
        return True


# 将跑马灯数据放入播放广播列表
def put_marquee_into_broad(broad_list):
    min = datetime.strftime(datetime.now(),'%M')
    for i in range(1,4):
        min_str = str(int(min)-i)
        marquee_list = ["match:marquee:list:%s","reddraw:marquee:list:%s","actpong:marquee:list:%s","actdraw:marquee:list:%s"]
        for ml in marquee_list:
            m_list = bag_redis.lrange(ml%min_str,0,-1)
            for mbody in m_list:
                broadDetail = {}
                broadDetail['content'] = mbody
                broadDetail['repeatInterval'] = 10
                broad_list.append(broadDetail)

    return broad_list

# ----------------------------测试跑马灯接口----------------------------------
@bag_app.post('/test/marquee')
def testMarquee():
    nickname = request.forms.get('nickname', '').strip()
    type = request.forms.get('type', '').strip()
    award = request.forms.get('award', "").strip()
    active = request.forms.get('active', '').strip()
    game = request.forms.get('game', '').strip()
    rank = request.forms.get('rank', 1).strip()
    produce_marquee_info(type,nickname,award,active,game,rank)
    return {"code":0,"msg":"ok"}
# ----------------------------测试跑马灯接口----------------------------------

# 处理跑马灯body信息
def produce_marquee_info(type,nickname,award="",active="",game="",rank=1):
    if int(type) == 1:
        body = "恭喜玩家%s赢得%s比赛第%s名，获得%s"%(nickname,game,rank,award)
        save_marquee_data(body,type)
    elif int(type) == 2:
        body = "恭喜玩家%s兑换%s"%(nickname,award)
        save_marquee_data(body,type)
    elif int(type) == 3:
        body = "恭喜玩家%s在%s活动中获得%s"%(nickname,active,award)
        save_marquee_data(body,type)
    elif int(type) == 4:
        body = "恭喜玩家%s在%s活动中兑换%s"%(nickname,active,award)
        save_marquee_data(body,type)

def getRewardCode(redis,uid,item_id,num):
    cur_num = get_player_item(item_id,uid)
    yuan = num
    key_num = int(yuan)*100

    title = bag_redis.hget(ITEM_ATTRS%item_id,'title')
    reward_table = 'reward:%s:user:%s:keycode'%(item_id,uid)
    print '-'*77
    print reward_table
    print '-'*77

    try_code = bag_redis.hget(reward_table,key_num)
    if try_code:
        res_num = get_player_item(item_id,uid)
        return {"code":0,"msg":'ok',"res_num":res_num,'key_code':try_code}

    if cur_num < key_num:
        return {"code":1,"msg":'当前'+title+'余额不足！'}
    else:
        # 消耗道具
        cost_player_item(item_id,uid,key_num)

        # 兑换码
        key_code = uuid.uuid4().hex
        this_time = str(datetime.now())[:19]
        bag_redis.hset(reward_table,key_num,key_code)
        nickname = redis.hget('users:%s'%uid,'nickname')
        try:
            mysql = Mysql_instance()
            sql = "select cost,reward_name from reward_course_config where item_id = '%s' and price = '%s'"%(item_id,key_num)
            mysql.cursor.execute(sql)
            res = mysql.cursor.fetchone()
            reward_cost = res[0]
            reward_name = res[1]
            print '----------------------------------------------'
            print '----------------------------------------------'
            print sql
            print res
            print '----------------------------------------------'
            print '----------------------------------------------'
            mysql.close()
        except:
            reward_cost = yuan
            reward_name = str(yuan) + "元" + title

        sql = "insert into reward_record(uid,nickname,key_code,reward_cost,reward_value,reward_time,reward_name,item_id)"+\
              "values('%s','%s','%s','%s','%s','%s','%s','%s')"%(uid,nickname,key_code,reward_cost,key_num,this_time,reward_name,item_id)

        print '='*56
        print sql
        print '='*56

        mysql = Mysql_instance()
        mysql.cursor.execute(sql)
        mysql.commit()
        mysql.close()

        res_num = get_player_item(item_id,uid)
        produce_marquee_info(2,nickname,award=title+str(yuan)+"元")
        return {"code":0,"msg":'ok',"res_num":res_num,'key_code':key_code}

    res_num = get_player_item(4,uid)
    return {"code":2,"msg":'获取兑换码失败！',"res_num":res_num}

# 获取红包兑换码
def getRedbagKey(redis,uid,key_num):
    cur_num = get_player_item(4,uid)
    yuan =  key_num
    key_num = int(key_num)*100

    try_code = bag_redis.hget('redbag:user:%s:keycode'%uid,key_num)
    if try_code:
        res_num = get_player_item(4,uid)
        return {"code":0,"msg":'ok',"res_num":res_num,'key_code':try_code}

    if cur_num < key_num:
        return {"code":1,"msg":'当前红包余额不足！'}
    else:
        cost_player_item(4,uid,key_num)
        key_code = uuid.uuid4().hex
        bag_redis.set('redbag:keycode:%s:value'%key_code,str(key_num)+"|"+uid)
        bag_redis.hset('redbag:user:%s:keycode'%uid,key_num,key_code)
        res_num = get_player_item(4,uid)
        nickname = redis.hget('users:%s'%uid,'nickname')
        produce_marquee_info(2,nickname,award="红包"+str(yuan)+"元")
        date_str = datetime.strftime(datetime.now(),'%Y-%m-%d')
        bag_redis.incrby("redbag2cash:date:%s"%date_str,yuan)
        return {"code":0,"msg":'ok',"res_num":res_num,'key_code':key_code}

    res_num = get_player_item(4,uid)
    return {"code":2,"msg":'获取兑换码失败！',"res_num":res_num}

def getUserByAccount(redis, account):
    """
    通过account获取玩家数据
    """
    account2user_table = FORMAT_ACCOUNT2USER_TABLE%(account)
    userTable = redis.get(account2user_table)
    return userTable

def check_vcoin_baselive(uid,threshold):
    cur_vcoin = get_player_item(3, uid)
    today_str = datetime.strftime(datetime.now(), '%Y-%m-%d')
    if int(cur_vcoin) >= threshold:
        return 0
    elif int(cur_vcoin) < threshold and uid in bag_redis.smembers('vcoin:baselive:date:%s:set'% today_str):
        return 1
    else:
        # 不足则领取低保
        give_player_item(3, uid, 12)
        bag_redis.sadd('vcoin:baselive:date:%s:set' % today_str, uid)
        bag_redis.incrby('vcoin:present:date:%s:sum' % today_str, 12)
        bag_redis.incrby('vcoin:present:sum', 12)
        res_num = get_player_item(3, uid)

        # user_table = 'users:%s' % uid
        # cur_vcoin = get_player_item(3, uid)
        # record_player_balance_change(bag_redis, user_table, 3, 12, cur_vcoin, 7)
        return 2

@bag_app.get('/get/buff/status')
@web_util.allow_cross_request
def get_buff_status(uid,key,game_id):
    #key = game_id + LIMIT_ITEM_MAP[item_id]
    rc = bag_redis.hget('user:%s:buff'%uid,key)
    if rc:
        btype = rc.split(':')[0]
        sts = rc.split(':')[0]
        return {"code":0,"buff_type":btype,btype:sts}
    else:
        return {"code":"1","msg":"无状态"}

# 使用时限或次数道具
@bag_app.post('/use/limit/item')
@web_util.allow_cross_request
def useLimitItem(redis,session):

    sid = request.forms.get('sid', '').strip()
    item_id = request.forms.get('item_id', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    atimes,adays,title = bag_redis.hmget('attrs:itemid:%s:hash'%item_id,'times','days','title')
    adays = int(adays or 0)
    if int(item_id) in [9,10,11,12]:
        title = "记牌器"
    # 使用次数道具
    key = LIMIT_ITEM_MAP[item_id]
    rc = bag_redis.hget('user:%s:buff'%uid,key)
    num = int(get_player_item(item_id,uid) or 0)
    if num < 1:
        return {"code":2,"msg":"数量不够"}
    if atimes:
        # buff状态中
        if rc:
            # 已有次数
            if rc.startswith('times'):
                cost_player_item(item_id,uid,1)
                times = rc.split('|')[1]
                res_times = int(times) + int(atimes)
                res = "times|"+str(res_times)
                bag_redis.hset('user:%s:buff'%uid,key,res)
                return {"code":0,"msg":"ok"}
            # 已有时间
            else:
                now = datetime.now()
                end_time = rc.split('|')[1]
                end = datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S')
                remains = str(end - now).split(' ')
                if len(remains) == 3:
                    r_day,r_time = remains[0],remains[2].split(':')
                    hour,min,sec = r_time[0],r_time[1],r_time[2][:2]
                else:
                    r_day = 0
                    r_time = remains[0].split(':')
                    hour,min,sec = r_time[0],r_time[1],r_time[2][:2]
                return {"code":1,"msg":"已有使用中的%s，剩余时间为%s天%s小时%s分%s秒"%(title,r_day,hour,min,sec)}
        # buff无状态中
        else:
            res = "times|"+str(atimes)
            bag_redis.hset('user:%s:buff'%uid,key,res)
            cost_player_item(item_id,uid,1)
            return {"code":0,"msg":"ok"}
    # 使用天数道具
    else:
        # buff状态中
        if rc:
            # 已有次数
            if rc.startswith('times'):
                r_times = rc.split('|')[1]
                return {"code":1,"msg":'已有使用中的%s,剩余次数为%s次'%(title,r_times)}
            # 已有时间
            else:
                r_time = rc.split('|')[1]
                cur_remain = datetime.strptime(r_time,'%Y-%m-%d %H:%M:%S')
                res = cur_remain + timedelta(adays)
                res = 'days|' + str(res)[:19]
                bag_redis.hset('user:%s:buff'%uid,key,res)
                cost_player_item(item_id,uid,1)
                return {"code":0,"msg":"ok"}
        # buff 无状态
        else:
            end_time = datetime.now() + timedelta(int(adays))
            res = 'days|' + str(end_time)[:19]
            bag_redis.hset('user:%s:buff'%uid,key,res)
            cost_player_item(item_id,uid,1)
            return {"code":0,"msg":"ok"}

def do_send_mail(redis, session, uid, title, body, enclosure=0, enclosure_num=0):
    """
    发送邮件方法
    """
    curTime = datetime.now()
    date = curTime.strftime("%Y-%m-%d")

    awards = ''
    if enclosure and enclosure_num:
        awards = '%s,%s' % (enclosure, enclosure_num)

    uid_list = uid.split(',')
    for uid in uid_list:
        email_id = uuid.uuid4().hex
        bag_redis.sadd(USER_EMAIL_DATE_SET % date, email_id)
        bag_redis.sadd(USER_EMAIL_SET % uid, email_id)
        bag_redis.hmset(EMAIL_HASH % email_id,
                        {"title": title, "body": body, "awards": awards,
                         "send_time": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                         "read": 0, "timestamp": int(time.time()) * 1000, 'email_type': '',
                         'userId': uid})
