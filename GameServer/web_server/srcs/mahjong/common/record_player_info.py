# -*- coding:utf-8 -*-

def record_player_balance_change(redis_ins,user_table,currency_id,quantity_change,quantity_final,type_id,game_id=""):
    """
    记录账户每一笔变化
    params: redis_ins 存入数据的redis 请传入mahjong.bag.bag_config import bag_redis
    params: user_table 
            1,真实账户格式 'users:%s' % uid ,例子 users:123
            2,机器人账户格式 'users:robot:level:%s:%s|%s' % (arg,uid,level), 例子 users:robot:level:2:20000|A
    params: currency 货币类型 传入道具id。道具id可参照后台系统 背包系统->道具列表
    params: quantity_change 改变的数量 
    params: quantity_final 改变后的数量
    params: type_id 变化的类型：
             {0:签到,1:分享,2:破产,3:新手礼包,4:七天奖励,5:十五天奖励,6:月签到奖励,7:元宝低保,8:宝箱任务，9:游戏输赢,10:房费,11:记牌器
              ,12:钻石兑换金币(金币变化),13:钻石兑换元宝（元宝变化）,14:钻石兑换钻石（钻石变化）,15:钻石兑换金币(钻石变化)，
               16:钻石兑换元宝(钻石变化)，17:钻石兑换钻石(钻石变化),18:钻石兑换记牌器1局（记牌器变化） 19:钻石兑换记牌器10局（记牌器变化）,
               20:钻石兑换记牌器1天（记牌器变化）21:钻石兑换记牌器7天（记牌器变化）,22:钻石兑换记牌器1局（钻石器变化）,
               23:钻石兑换记牌器10局（钻石变化）,24:钻石兑换记牌器1天（钻石变化）,25:钻石兑换记牌器7天（钻石变化）,26:保险箱取款手续费,
               27:存入保险箱（账号金额变化），28:存入保险箱（保险箱金额变化），
               29:取出保险箱（账号金额变化），30:取出保险箱（保险箱金额变化）,
               31:充值钻石,32:报名费支出，33：报名费反还
               34,补签费用，35,补签奖励,36,每日领取门票
               }
    params: game_id 游戏的id} 
    调用例子：
    1， 用户9527玩跑得快，盈了1000金币，结算后金币是10000.
        record_player_balance_change(redis,'users:9527',2,1000,11000,9,"559")
    2， 用户9527玩跑得快，房费10金币，结算后金币是11000.
        record_player_balance_change(redis,'users:9527',2,10,11000,10)
    3， 用户9527玩跑得快，输了10元宝，结算后元宝数是110元宝.
        record_player_balance_change(redis,'users:9527',3,-10,110,9)
    """
    # currency_dic = {'gold':2,'yuanbao':3,'diamond':1,'room_card':6,'redpacket':4,'jipai_1s':9,'jipai_10s':10,'jipai_1day':11,'jipai_7days':12}
    # currency_id = currency_dic[currency]
    sql_str_format = 'insert into income_and_fee_detail' +\
                        ' (user_id,quantity_change,quantity_final,currency,type_id,game_id,create_time)' +\
                        " values ('{0}',{1},{2},{3},{4},'{5}','{6}');"
    import time
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    sql_str = sql_str_format.format(user_table,quantity_change,quantity_final,currency_id,type_id,game_id,now_time)
    redis_ins.lpush('player:balance_change',sql_str)