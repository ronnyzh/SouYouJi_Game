#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    web数据表及关系对应
"""
# 日志保存时间
LOG_TABLE_TTL = 60 * 60 * 24 * 8

"""
agent
  {
        id          :    代理的ID
        account     :    账号
        passwd      :    密码
        name        :    昵称
        shareRate   :    占成
        valid       :    是否有效 0-冻结 1-有效
        isCreate    :    是否允许创建下级代理 0-不允许 1-允许
        roomcard_id :    当前货币ID
        parent_id   :    上线代理id
        roomcard    :    钻石数
        regIp       :    注册IP
        regDate     :    注册日期
        lastLoginIP :    注册IP
        lastLoginDate :  注册日期
        unitPrice   ：   每张钻石数
        defaultRoomCard : 给新用户默认钻石数(张)
  }
"""
AGENT_COUNT         =     'agents:id:count'
AGENT_TABLE         =     'agents:id:%s'
AGENT_CHILD_TABLE   =     'agents:id:%s:child'
AGENT_ID_TABLE      =     'agents:ids:set'
AGENT_ACCOUNT_TO_ID =     'agents:account:%s:to:id'

'''
生成代理日期索引
代理ID表 : AGENT_ID_TABLE
代理创建日期表 : AGENT_ID_CREATE_DATE
'''
AGENT_CREATE_DATE = "agent:create:date:%s"

"""
agent2accessban
代理id对应父id映射表
set
"""
AGENT2PARENT     =    'agents:id:%s:parent'




# 代理的通过账号映射id

"""
Game 游戏表
{
       id        :     游戏ID
       name      :     游戏名称
       version   :     游戏版本号
       web_tag   :     web启动地址
       ipa_tag   :     ios启动标志
       apk_tag   :     android启动标志
       minVersion  :   android版本号
       iosVersion  :   ios版本号
       pack_name   :   游戏包名称
       downloadUrl  :   游戏包下载地址
       maxRoomCount :   每个游戏最大房间数
       IPAURL       :
       apk_size     :   apk大小
       apk_md5      :   apkmd5验证
       game_rule    :   游戏规则(创建房间时使用)
       module_id    :   游戏模块ID

}
"""
GAME_COUNT      =       'games:id:count'
GAME_LIST       =       'games:list'
GAMEID_SET      =       'games:id:set'
GAME_TABLE      =       'games:id:%s'
# 游戏ID的规则描述
GAME2DESC       =       'games:id:%s:desc'

"""
gameModule
游戏模块表
{
    id      :    游戏模块ID
    path    :    游戏路径
    remart  :    备注
    name    :    游戏模块名称
}
"""
GAMEMODULE_COUNT   =   'gameModule:id:count'
GAMEMODULE_TABLE   =   'gameModule:id:%s'

"""
系统默认绑定游戏集合
gameserver:url
"""
GAME_DEFAULT_BIND = 'games:default:bind:set'

"""
agent_own_game
代理游戏映射
agent:ID:own:games  list
"""
AGENT_OWN_GAME     =    'agent:%s:own:games'


"""
agent2access
代理权限表
agent:ID:accesses  set
"""
AGENT2ACCESS     =    'agent:%s:accesses'

"""
agent2accessban
代理禁用权限表
agent:ID:ban:accesses  set
"""
AGENT2ACCESSBAN     =    'agent:%s:ban:accesses'

"""
user4AgentCard
agent:ID:user:ID:cards
"""
USER4AGENT_CARD = 'agent:%s:user:%s:card'

"""
user4AgentRechargeCard
agent:ID:user:ID:recharge:total
"""
USER4AGENT_RECHARGE = 'agent:%s:user:%s:recharge:total'

'''
agent:$1:buy:his:total
'''
AGENT_BUY_TOTAL = 'agent:%s:buy:total'

'''
agent:$1:sale:his:total
'''
AGENT_SALE_TOTAL = 'agent:%s:sale:total'

"""
agent_op_log
代理操作日志
{
    'id'            :       日志ID
    'datetime'      :       操作时间
    'desc'          :       操作描述
}
"""
AGENT_OP_COUNT              = 'agent:op:count'
AGENT_OP_LOG_TABLE          = 'agent:%s:op:log'
AGENT_OP_LOG_DATESET_TABLE  = 'agent:%s:op:log:dateset:%s'

"""
管理员操作日志
{
    'account'           :   登录账号,
    'type'              :   1：正常,2密码错误
    'description'       :   操作描述,
    'datetime'          :   登录时间,
    'ip'                :   登录IP
}
"""
#日志流水号
FORMAT_AGENT_OP_LOG_COUNT_TABLE = "agent:op:log:count"
FORMAT_AGENT_OP_LOG_TABLE = "agent:op:log:%s"
FORMAT_AGENT_OP_LOG_DATESET_TABLE = "agent:op:log:dateset:%s"


"""
游戏大厅公告列表
notice:day1:ID:list
"""
FORMAT_GAMEHALL_NOTIC_LIST_TABLE = "notice:list"
"""
捕鱼大厅公告表
"""
FORMAT_FISHHALL_NOTIC_LIST_TABLE = "notice:fish:list"
FORMAT_GAMEHALL_NOTIC_COUNT_TABLE = "notice:count"
"""
公告内容表
{   'id'            ：      公告Id
    'content'       :       公告内容
    'date'          :       公告时间
    'status'        :       公告状态  1 已推送 0 未推送
    'read'          :       是否阅读
    'type'          :       公告类型  0-系统消息 1-活动信息 2-玩家邮件
}
"""
FORMAT_GAMEHALL_NOTIC_TABLE = "notice:%s"
"""
联系方式公告
"""
FORMAT_NOTIC_INOF_TABLE = 'notic:contact:info:hash'
"""
玩家信息已读列表
"""
FORMAT_MSG_READ_SET = "notices:%s:read:set"

"""
管理员发送公告列表
"""
FORMAT_MGR_SEND_MESSAGE_LIST = "agent:%s:send:message:list"

"""
玩家消息box表
"""
FORMAT_USER_MESSAGE_LIST = "user:%s:messages:list"
FORMAT_USER_MSG_FISH_LIST = "user:%s:fish:msg:list"

"""
玩家收获地址表
"""
FORMAT_USER_ADDRESS_TABLE = "user:%s:addr:info"

"""
agent_op_log
代理占成表
{
    'number'         :       销售张数
    'rate'           :       每张分成数
    'unitPrice'      :       每张单价
    'rateTotal'      :       总分成(实际赚的钱) = 上级分给自己的占额 - 自付给下级的占额
    'meAndNextTotal' :       上级应该分给自己的总占额
    'superRateTotal' :      上级的总占额
}
"""
AGENT_RATE_DATE  = 'agent:%s:rate:%s:price:%s:date:%s'

"""
agent_op_log
总公司占成表
{
    'number'        :       销售张数
    'rate'          :       每张分成数
    'unitPrice'     :       每张单价
    'rateTotal'     :       总分成
}
"""
AGENT_COMPAY_RATE_DATE ='agent:%s:date:%s'

# 代理占成值集合表
AGENT_RATE_SET = 'agent:%s:rate:set'
# 钻石单价集合表
AGENT_ROOMCARD_PER_PRICE = 'agent:%s:roomcard:per:price'
#



"""
order
订单表
{
        'id'            :       订单ID
        'orderNo'       :       订单编号
        'card_nums'     :       购卡数
        'card_present'  :       赠送卡数
        'apply_date'    :       申请购卡日期
        'finish_date'   :       确认订单信息
        'note'          :       备注
        'type'          :       充卡类型 0-代理充卡 1-会员充卡
        'price'         :       每张钻石价格
        'status'        :       0-等待卖卡房确认 1-卖卡房已确认
        'applyAccount'  :       购卡方账号
        'saleAccount'   :       售卡方账号
        'name'          :       name1, #商品名
        'body'          :       body1,
        'count'         :       detail1, #商品数量
        'money'         :       money1, #总价
        'startTime'     :       time1, #下单时间
        'account'       :       account1, #微信账号
        'time'          :       timeStamp2, #支付时间戳
        'sign'          :       sign1, #支付签名
        'nonceStr'      :       nonceStr1, #支付字符串
        'prepayID'      :       prepayID1, #支付ID
        'endTime'       :       time2, #成交时间
        'type'          :       type1, #状态
        'orderNum'      :       num1, #微信支付订单号
        'costMoney'     :       money2, #支付金额
        'currency'      :       currency1, #货币种类
        'bank'          :       bank1, #银行
        'errReason'     :       reason1, #错误原因
        'num'           :       商品编号
        'roomCards'     :       钻石数
}
"""
ORDER_LIST      =    'orders:list'
ORDER_COUNT     =    'orders:count'
ORDER_TABLE     =    'orders:id:%s'
ORDER_TABLE4FISH     =    'orders4fish:id:%s'

"""
待处理订单
pendingGoods:ID1:set
"""
PENDING_ORDER = 'pendingGoods:101:set'
PENDING_ORDER4FISH = 'pendingGoods4fish:set'

"""
成功订单
succeedGoods:ID1:set
"""
SUCCEED_ORDER = 'succeedGoods:101:set'
SUCCEED_ORDER4FISH = 'succeedGoods4fish:set'

"""
失败订单
failedGoods:ID1:set
"""
FAILED_ORDER = 'failedGoods:101:set'

"""
订单列表
orderNumList:ID1:list
"""
ORDER_NUM_LIST = 'orderNumList:101:list'
ORDER_NUM_LIST4FISH = 'orderNumList4fish:list'

"""
账号、物品、价格到订单的映射，用来检测重复订单
pending4account:account1:money1:name1:ID1:key
"""
PENDING4ACCOUNT = 'pending4account:%s:%s:%s:101:key'

"""
每日的订单
dayOrder:day1::ID1:list
日期格式：2015-01-01
"""
DAY_ORDER = 'dayOrder:%s:101:list'
DAY_ORDER4FISH = 'dayOrder4fish:%s:list'

"""
每日成功的订单
daySucceedOrder:day1::ID1:list
日期格式：2015-01-01
"""
DAY_SUCCEED_ORDER = 'daySucceedOrder:%s:101:list'
DAY_SUCCEED_ORDER4FISH = 'daySucceedOrder4fish:%s:list'

"""
每日等待的订单
dayPendingOrder:day1::ID1:list
日期格式：2015-01-01
"""
DAY_PENDING_ORDER = 'dayPendingOrder:%s:101:list'
DAY_PENDING_ORDER4FISH = 'dayPendingOrder4fish:%s:list'

"""
账号下的订单
playerOrder:account1:ID1:set
"""
PLAYER_ORDER = 'playerOrder:%s:101:set'
PLAYER_ORDER4FISH = 'playerOrder4fish:%s:set'

"""
buy_order_list
代理订单列表
agent:ID:order:list
"""
AGENT_BUY_ORDER_LIST = 'agent:%s:order:list'

"""
buy_order_success_date
代理成功列表
agent:ID:buySuccess:datestr
"""
AGENT_BUY_ORDER_LIST         = 'agent:%s:buy:order:%s'
AGENT_BUYSUCCESS_ORDER_LIST  = 'agent:%s:buySuccess:%s'
AGENT_BUYPENDING_ORDER_LIST  = 'agent:%s:buyPending:%s'

AGENT_SALE_ORDER_LIST         = 'agent:%s:sale:order:%s'
AGENT_SALESUCCESS_ORDER_LIST  = 'agent:%s:saleSuccess:%s'
AGENT_SALEPENDING_ORDER_LIST  = 'agent:%s:salePending:%s'


"""
agent_buyOrder_card_date
代理购卡报表统计
{
    date
    cardNums
}
agent:ID:buy:card:%s:dateStr
"""
AGENT_BUY_CARD_DATE = 'agent:%s:buy:card:%s'


"""
agent_buyOrder_card_date
代理售卡报表统计
{
   date
   cardNums
}
agent:ID:sale:card:%s:dateStr
"""
AGENT_SALE_CARD_DATE = 'agent:%s:sale:card:%s'


"""
roomcard_info
钻石信息
{
            id     :  钻石ID
            money  :  钻石单价
            date   :  设置日期
}
roomcard:id:%s
"""
ROOMCARD_COUNT    = 'roomcard:count'
ROOMCARD_TABLE    = 'roomcard:id:%s'


"""
agent2roomcard
代理对应钻石列表
agent:%s:roomcard:list
"""
AGENT2ROOMCARD     =    'agent:%s:roomcard:list'

"""
大厅游戏登录session
"""
#time -> userTable
FORMAT_USER_HALL_SESSION = 'hall:session:%s'

"""
平台session
"""
#$account
FORMAT_USER_PLATFORM_SESSION = 'session:%s'

"""
代理子会员id集合
"""
FORMAT_ADMIN_ACCOUNT_MEMBER_TABLE = "agent:%s:member:children"

"""
UID到玩家表名的映射：users:account:$账号名
users:uid:test      ->      账号test所在的数据表
"""
FORMAT_ACCOUNT2USER_TABLE = "users:account:%s"
"""
手机登录验证码
"""
USERS_LOGIN_PHONE_VCODE_TABLE = 'users:login:phone:%s:vcode'
"""
用户手机更绑验证码
"""
USERS_BIND_PHONE_VCODE_TABLE = 'users:bind:phone:%s:vcode'
"""
用户账号绑定的手机号码
"""
USERS_ACCOUNT_PHONE_TABLE = 'users:account:%s:phone'
"""
微信标示ID到账号的映射
unionid2account:weixin:ID1:key
"""
WEIXIN2ACCOUNT = 'unionid2account:weixin:%s:key'
WEIXIN2ACCOUNT4FISH = 'unionid2account4fish:weixin:%s:key'

"""
微信账号集合
account4weixin:set
"""
ACCOUNT4WEIXIN_SET = 'account4weixin:set'
ACCOUNT4WEIXIN_SET4FISH = 'account4weixin4fish:set'

"""
房间号到服务器的映射
room2server:room1:hesh
{
    'ip'           :       房间所在ip,
    'port'         :       房间所在port,
    'ag'           :       房间所属ag,
    'gameid'       :       房间所属游戏,
    'type'         :       房间类型,
    'gameName'     :       房间名,
    'dealer'       :       房主,
    'playerCount'  :       玩家数,
    'maxPlayer'    :       最大玩家数,
}
"""
ROOM2SERVER = 'room2server:%s:hesh'

"""
代理房间列表
ag2room:ag:agID:set
"""
AG2SERVER = 'ag2room:ag:%s:set'

"""
服务器下房间列表
server2room:server:server1:set
"""
SERVER2ROOM = 'server2room:server:%s:set'

"""
游戏服务配置表
{
    'playerCount'       :   #玩家个数
    'roomCount'         :   #房间个数
}
"""
#gameid:currency:ip:port
FORMAT_GAME_SERVICE_TABLE = "service:game:%s:%s"
FORMAT_GAME_SERVICE_SET = "services:game:%s"

"""
web服务器配置表
"""
FORMAT_HALL_SERVICE_SET = "services:hall:set"

"""
大厅商品表
{
    id    :
    name         :      商品名称
    cards        :      钻石数
    present_card :      赠送钻石数
    price        :      钻石价格
    body         :      商品描述
    detail       :      商品详情
}
goods:id
"""
GOODS_COUNT = 'goods:count'
GOODS_TABLE = 'goods:id:%s'
GOODS_LIST  = 'goods:list'
GOODS_TYPE_LIST = 'goods:type:%s:list'
GOODS_ROOMCARD_PRICE = 'goods:cards:price:list'

GOODS_TABLE4FISH = 'goods4fish:id:%s'

"""
商品名字到编号(id)的映射
goodsName2Num:%s:ID1:key
"""
GOODS_NAME2NUM = 'goodsName2Num:%s:101:key'

"""
所有商品的集合
goodsSet:ID1:set
"""
GOODS_SET = 'goodsSet:101:set'

"""
商品编号(id)对应的订单编号(id)
goodsId:goodsName1:ID1:key
"""
GOODS_NUM = 'goodsNum:%s:101:key'
GOODS_NUM4FISH = 'goodsNum4fish:%s:key'

"""
支付开关
order2weixin:ID:key
"""
ORDER2WEIXIN_SWITCH = 'order2weixin:101:key'
ORDER2WEIXIN_SWITCH4FISH = 'order2weixin4fish:101:key'

"""
游戏服务地址
gameserver:url
"""
GAME_SERVER_URL = 'gameserver:url'

"""
房间规则
rules:gameID:list
"""
GAME2RULE = 'rules:%s:list'

"""
房间规则详细
ruleDatas:gameID:ruleNum:hesh
{
    title   :   规则名
    type    :   单选1复选0
    rule    :   选项
}
"""
GAME2RULE_DATA = 'ruleDatas:%s:%s:hesh'

"""
房间依赖规则
ruleDatas:gameID:ruleNum:depend
{
    type : 3
    rule : 选项
}
"""
GAME2RULE_DATA_DEPEND = 'ruleDats:%s:%s:depend'

"""
消耗钻石数设置
useRoomCardsRule:gameID:list
['描述:消耗钻石数', '1局:1']
"""
USE_ROOM_CARDS_RULE = 'useRoomCardsRule:%s:list'


#总在线账号
ONLINE_ACCOUNTS_TABLE = "online:accounts"
ONLINE_GAME_ACCOUNTS_TABLE = "online4game:accounts:game:%s"

"""
玩家每个游戏的在线情况
user:$account:online:$gameId
"""
FORMAT_CUR_USER_GAME_ONLINE = "user:%s:online"

"""
退出的玩家记录
player:account:exitPlayer:gameID1:hash
{
    'ip'            :       ip,
    'port'          :       port1,
    'game'          :       gameNum1,
    'side'          :       side1
}
"""
EXIT_PLAYER = 'player:%s:exitPlayer:hash'

"""
玩家玩过的房间列表
player:account1:player2game:gameID1:list
"""
PLAYER_PLAY_ROOM = 'player:%s:player2game:list'

"""
一轮中包含的每局
game:gameNum1:startTime:time1:game2room:list
"""
GAME2ROOM = 'game:%s:startTime:%s:game2room:list'

"""
房间信息（一整轮）
game:gameNum1:startTime:time1:playGame:hash
{
    'player'                    :   side1:account1;side2:account2,
    'startTime'                 :   time1,
    'endTime'                   :   time2,
    'win:account1'              :   win1,
    'hu:account1'               :   huCount1,
    'kong:account1'             :   kongCount1,
    'giveKong:account1'         :   giveKongCount1,
    'concealedKong:account1'    :   concealedKong1
}
"""
PLAY_GAME_DATA = 'game:%s:startTime:%s:playGame:hash'

"""
某个房间（一局）的游戏信息
game:gameNum1:time:time1:playRoom:hash
{
    'startTime'                 :   time1,
    'endTime'                   :   time2,
    'action'                    :   side1:action1:mahjongs1;side2:action2:mahjongs2,
    'win:account1'              :   win1:win2:win3,
    'kong:account1'             :   kongCount1,
    'concealedKong:account1'    :   concealedKong1,
    'giveKong:account1'         :   giveKongCount1
}
action:rool,get,put,pong(1),kong(2),hu(4),concealed_kong(5),end
"""
GAME_ROOM_DATA = 'game:%s:time:%s:playRoom:hash'

"""
回放集合
playerReplaySet:ID1:zset
"""
PLAYER_REPLAY_SET = 'playerReplaySet:zset'

"""
等待加入公会的玩家列表
joinGroup:$admin:list
"""
JOIN_GROUP_LIST = 'joingroup:%s:list'

"""
加入公会状态
joinGroupResult:$account:key
工会号:状态:申请时间
0等待，1成功，2失败
"""
JOIN_GROUP_RESULT = 'joinGroupResult:%s:key'

"""
玩家数据表：users:$id(从1开始递增）

"""
FORMAT_USER_TABLE = "users:%s"
FORMAT_USER_COUNT_TABLE = "users:count"

"""
服务协议表队列表
"""
#service:protocols:game:$gameId:$channelId:$IP:$PORT
FORMAT_SERVICE_PROTOCOL_TABLE = "service:protocols:game:%s:%s"

HEAD_SERVICE_PROTOCOL_GAME_CLOSE = "close"
HEAD_SERVICE_PROTOCOL_GAME_CONFIG_REFRESH = "configRefresh"
#operatorRefresh|$account
HEAD_SERVICE_PROTOCOL_OPERATOR_REFRESH = "operatorRefresh|%s"
HEAD_SERVICE_PROTOCOL_AGENT_REFRESH = "agRefresh|%s"
#currencyRefresh|$cur
HEAD_SERVICE_PROTOCOL_CURRENCY_REFRESH = "currencyRefresh|"
#memberRefresh|$account
HEAD_SERVICE_PROTOCOL_MEMBER_REFRESH = "memberRefresh|%s"
#noticeRefresh|$noticCount
HEAD_SERVICE_PROTOCOL_GAMEHALL_NOTICE = "noticeRefresh|%s"
#broadcast|$ag|$content|$repeatTimes|$repeatInterval|$bid
HEAD_SERVICE_PROTOCOL_AGENT_BROADCAST = "broadcast|%s|%s|%s|%s|%s"
#reSession|$memberAccount|$sessionId
HEAD_SERVICE_PROTOCOL_OPERATOR_RESESSION = "reSession|%s|%s"
#kickMember|$memberAccount
HEAD_SERVICE_PROTOCOL_KICK_MEMBER = "kickMember|%s"
#joinPartyRoom|$memberAccount|$ag|$rule
HEAD_SERVICE_PROTOCOL_JOIN_PARTY_ROOM = "joinPartyRoom|%s|%s|%s"
#cancelJoinPartyRoom|$memberAccount|$ag|$rule
HEAD_SERVICE_PROTOCOL_CANCEL_JOIN_PARTY_ROOM = "cancelJoinPartyRoom|%s|%s|%s"
#cancelJoinPartyRoom|$memberAccount|$ag|$rule
HEAD_SERVICE_PROTOCOL_DISSOLVE_ROOM = "dissolveRoom|%s"
#createRoom4Other|$memberAccount|$ag|$rule|$ruleText
HEAD_SERVICE_PROTOCOL_CREATE_OTHER_ROOM = "createRoom4Other|%s|%s|%s|%s"
#kickMember4repeat|$memberAccount|$sid
HEAD_SERVICE_PROTOCOL_KICK_MEMBER4REPEAT = "kickMember4repeat|%s|%s"

"""
等待加入娱乐模式列表
'testWaitJoinPartyRoomPlayers:ag:gameID:rule:list'
"""
WAIT_JOIN_PARTY_ROOM_PLAYERS = 'testWaitJoinPartyRoomPlayers:%s:%s:%s:list'

"""
取消加入娱乐模式列表
'testCancelJoinPartyRoomPlayers:list'
"""
CANCEL_JOIN_PARTY_ROOM_PLAYERS = 'testCancelJoinPartyRoomPlayers:list'

"""
账号到所在等待加入娱乐模式列表表名的映射
'testAccount2waitJoinPartyTable:account:str'
"""
ACCOUNT2WAIT_JOIN_PARTY_TABLE = 'testAccount2waitJoinPartyTable:%s:str'

"""
判断娱乐模式匹配是否完成
'testIsMatchFinished:account:str'
"""
IS_MATCH_FINISHED = 'testIsMatchFinished:%s:str'

"""
娱乐模式account到玩家个数的映射
'testPartyAccount2PlayerCount:account:str'
"""
PARTY_ACCOUNT2PLAYER_COUNT = 'testPartyAccount2PlayerCount:%s:str'

"""
广播表
{
    'id'            :   #广播ID
    'agent'         :   #代理商名
    'content'       :   #广播内容
    'repeatTimes'   :   #重播次数
    'repeatInterval':   #重播间隔秒数
}
"""
FORMAT_BROADCAST_COUNT_TABLE = "broadcast:count"
FORMAT_BROADCAST_TABLE = "broadcast:%s"
FORMAT_BROADCAST_LIST_TABLE = "broadcast:list"
FORMAT_BROADCAST_SAVE_TIME = 5 * 60 #过期时间

"""
日广播列表
broadcast:date:list
"""
DAY_BROADCAST_LIST = "broadcast:%s:list"

"""
大厅广播
"""
HALL_BROADCAST_LIST = "broadcast:hall:list"


"""
日注册玩家
redis set,记录每日注册玩家账号
login:date:account:2015-01-01
记录2015-01-01的不重复注册玩家账号
"""
FORMAT_REG_DATE_TABLE = "reg:date:account:%s"
FORMAT_REG_DATE_TABLE4FISH = "reg4fish:date:account:%s"

"""
gameid到redis库映射关系
{
       ip        :     redis的ip
       port      :     redis的port
       num       :     redis的数据库编号
       passwd    :     redis数据库密码，没有则为空字符串
}
"""
GAME2REDIS = 'gameRedisDatas:%s:hesh'

"""
gameid到redis库映射关系，此库为读取用的分库
{
       ip        :     redis的ip
       port      :     redis的port
       num       :     redis的数据库编号
       passwd    :     redis数据库密码，没有则为空字符串
}
"""
GAME2REDIS4READ = 'gameRedisDatas4Read:%s:hesh'

"""
大厅更新配置表
hotSetting
{
    resVersion    :     ///
}
"""
HOTUPDATE_TABLE = 'hotUpdate:table:hesh'
FISH_HOTUPDATE_TABLE = 'fish:hotupdate:hesh'

"""
APPLE PAY订单表
"""
APP_PAY_ORDER_ITEM = 'receptslist:%s'
APP_PAY_ORDER_ITEM4FISH = 'receptslist4fish:%s'

"""
每日玩家数据
playerData4day:$uid:$day:hesh
{
    'playCount'       :       #局数
    'roomCard'        :       #钻石数
}
"""
PLAYER_DAY_DATA = 'playerData4day:%s:%s:hesh'
PLAYER_DAY_DATA_SAVE_TIME = 60 * 24 * 60 * 60

"""
每日总钻石数
allRoomCard4day:day1:key
"""
DAY_ALL_PLAY_ROOM_CARD = 'allRoomCard4day:%s:key'

"""
每日代理总钻石数
allRoomCard4ag4day:ag1:day1:key
"""
DAY_AG_PLAY_ROOM_CARD = 'allRoomCard4ag4day:%s:%s:key'

"""
每日总活跃数
allLogin4day:day1:key
"""
DAY_ALL_LOGIN_COUNT = 'allLogin4day:%s:key'

"""
代理下每日总活跃数
allLogin4ag4day:ag1:day1:key
"""
DAY_AG_LOGIN_COUNT = 'allLogin4ag4day:%s:%s:key'

"""
日登录玩家
redis set,记录每日登录玩家账号
login:date:account:2015-01-01
记录2015-01-01的不重复登录玩家账号
"""
FORMAT_LOGIN_DATE_TABLE = "login:date:account:%s"
FORMAT_LOGIN_DATE_TABLE4FISH = "login4fish:date:account:%s"

"""
开给别人的房间
myRoom4Other:account:$account:list
"""
MY_OTHER_ROOMS = 'myRoom4Other:account:%s:list'

"""
开给别人的房间数据
{
       roomId        :     房间号,
       name          :     房间名称,
       gameType      :     游戏是否开始结束,
       minNum        :     分子,
       maxNum        :     分母,
       time          :     时间戳,
       rule          :     规则字符串,
       accountList   :     玩家账号列表，用;隔开,
}
otherRoomData:account:$account:time:$time:roomId:$roomId:hesh
"""
OTHER_ROOM_DATA = 'otherRoomData:account:%s:time:%s:roomId:%s:hesh'

"""
房间下玩家账号列表
room2accountList:roomId:$roomId:list
"""
ROOM2ACCOUNT_LIST = 'room2accountList:roomId:%s:list'

"""
代理每日总局数
allPlayCount4day:$day:$agId:key
"""
DAY_ALL_PLAY_COUNT = 'allPlayCount4day:%s:%s:key'
DAY_ALL_PLAY_COUNT_SAVE_DAY = 30 * 24 * 60 *60

"""
代理总局数
allPlayCount:$agId:key
"""
ALL_PLAY_COUNT = 'allPlayCount:%s:key'


"""
登录接口映射池
login:pools:set
"""
FORMAT_LOGIN_POOL_SET = "login:pools:set"

"""
游戏数据
playerUseCardData:player:$uid:day:$day:list
&useRoomCard;&type;&playerRoomCard;&roomId;$;others1$;others2
使用钻石数;类型;总钻石数;房间号;其他
type:1普通开房，2代开房间，3解散代开房间，4addRoomCard2Member，5onAppleStorePay，6buyCard
"""
PLAYER_DAY_USE_CARD = 'playerUseCardData:player:%s:day:%s:list'
SAVE_PLAYER_DAY_USE_CARD_TIME = 91 * 24 * 60 * 60

TOKEN2_JSAPI_TICKET = 'token2JsapiTicket:token:%s'

UNIONID2GROUP = 'unionId2Group:unionId:%s'
"""
玩家补偿钻石记录
"""
COMPENSATE_CARD_DAY = "compensate:roomcard:day:%s:list"
"""
玩家补偿积分记录
"""
COMPENSATE_POINT_DAY = "compensate:point:day:%s:list"
"""
邮件补偿记录
"""
COMPENSATE_MAIL_DAY = "compensate:mail:day:%s:list"
"""
邮件附件领取记录
"""
ENCLOSURE_MAIL_DAY = "enclosure:mail:day:%s:list"
"""
捕鱼ID集合
fish:room:id:set
"""
FISH_ROOM_ID_SETS = 'fish:room:id:set'

"""
捕鱼房间列表
"""
FISH_ROOM_LIST = 'fish:room:lists'

"""
捕鱼频道表
{
    room_id     :   房间ID
    room_name   :   房间名
    min_coin    :   最小携带金币
    max_coin    :   最大携带金币
    base_coin   :   最小底分
    max_base_coin : 最大底分
    step_base_coin : 步长底分
    isTrail     :   是否试玩
    max_player_count : 房间最大人数
    status      :   房间状态
    ip_mask     :   IP掩码做同IP判断用
}
fish:channel:$id:info
"""
FISH_ROOM_TABLE = "fish:channel:%s:info"

"""
捕鱼玩家总投注收益情况
playerFishBetAllData:player:$uid:hesh
{
    bet     :       $bet
    profit  :       &profit
}
"""
PLAYER_FISH_BET_DATA4ALL = 'playerFishBetAllData:player:%s:hesh'

"""
捕鱼玩家日投注收益情况
playerFishBetDayData:player:$uid:day:$day:hesh
{
    bet     :       $bet
    profit  :       &profit
}
"""
PLAYER_FISH_BET_DATA4DAY = 'playerFishBetDayData:player:%s:day:%s:hesh'
PLAYER_FISH_BET_DATA4DAY_SAVE_TIME = 91 * 24 * 60 * 60

"""
捕鱼玩家收益明细
playerFishBetDataDetail:player:$uid:list
每次登陆的bet和profit，内为json串
"""
PLAYER_FISH_BET_DATA_DETAIL = 'playerFishBetDataDetail:player:%s:list'
PLAYER_FISH_BET_DATA_DETAILL_MAX_LEN = 100

"""
捕鱼玩家日收益明细
playerFishBetDataDetail:player:$uid:day:$day:list
内为json串
"""
PLAYER_FISH_BET_DATA_DETAIL4DAY = 'playerFishBetDataDetail:player:%s:day:%s:list'
PLAYER_FISH_BET_DATA_DETAIL4DAY_SAVE_TIME = 91 * 24 * 60 * 60
PLAYER_FISH_BET_DATA_DETAIL4DAY_MAX_LEN = 100

"""
捕鱼代理总投注收益情况
agentFishBetAllData:agent:$agentUid:hesh
{
    bet     :       $bet
    profit  :       &profit
}
"""
AGENT_FISH_BET_DATA4ALL = 'agentFishBetAllData:agent:%s:hesh'

"""
捕鱼代理日投注收益情况
agentFishBetDayData:agent:$agentUid:day:$day:hesh
{
    bet     :       $bet
    profit  :       &profit
}
"""
AGENT_FISH_BET_DATA4DAY = 'agentFishBetDayData:agent:%s:day:%s:hesh'
AGENT_FISH_BET_DATA4DAY_SAVE_TIME = 91 * 24 * 60 * 60

"""
捕鱼代理收益明细
agentFishBetDataDetail:agent:$agentUid:day:$day:list
每次登陆的bet和profit，内为json串
"""
AGENT_FISH_BET_DATA_DETAIL = 'agentFishBetDataDetail:agent:%s:day:%s:list'
AGENT_FISH_BET_DATA_DETAIL_SAVE_TIME = 91 * 24 * 60 * 60
AGENT_FISH_BET_DATA_DETAILL_MAX_LEN = 100

"""
捕鱼总投注收益情况
allFishBetAllData:hesh
{
    bet     :       $bet
    profit  :       &profit
}
"""
ALL_FISH_BET_DATA4ALL = 'allFishBetAllData:hesh'

"""
捕鱼日投注收益情况
allFishBetDayData:day:$day:hesh
{
    bet     :       $bet
    profit  :       &profit
}
"""
ALL_FISH_BET_DATA4DAY = 'allFishBetDayData:day:%s:hesh'
ALL_FISH_BET_DATA4DAY_SAVE_TIME = 91 * 24 * 60 * 60

"""
捕鱼收益明细
allFishBetDataDetail:day:$day:list
每次登陆的bet和profit，内为json串
"""
ALL_FISH_BET_DATA_DETAIL = 'allFishBetDataDetail:day:%s:list'
ALL_FISH_BET_DATA_DETAILL_MAX_LEN = 100
ALL_FISH_BET_DATA_DETAILL_SAVE_TIME = 91 * 24 * 60 * 60

"""
捕鱼房间投注收益情况
fishBetAllData4Room:room:$roomId:hesh
{
    bet     :       $bet
    profit  :       &profit
}
"""
FISH_BET_DATA4ROOM = 'fishBetAllData4Room:room:%s:hesh'

"""
捕鱼日房间投注收益情况
fishBetDayData4Room:room:$roomId:day:$day:hesh
{
    bet     :       $bet
    profit  :       &profit
}
"""
FISH_BET_DATA4DAY4ROOM = 'fishBetDayData4Room:room:%s:day:%s:hesh'
FISH_BET_DATA4DAY4ROOM_SAVE_TIME = 91 * 24 * 60 * 60

"""
捕鱼房间收益明细
fishBetDataDetail4Room:room:$roomId:day:$day:list
每次登陆的bet和profit，内为json串
"""
FISH_BET_DATA_DETAIL4ROOM = 'fishBetDataDetail4Room:room:%s:day:%s:list'
FISH_BET_DATA_DETAILL4ROOM_MAX_LEN = 100
FISH_BET_DATA_DETAILL4ROOM_SAVE_TIME = 91 * 24 * 60 * 60

"""
捕鱼在线列表
"""
ONLINE_ACCOUNTS_TABLE4FISH = "online4Fish:accounts"

"""
GM操作记录
GMControlData:uid:$uid:list
记录gm功能操作记录，为json串，包含：时间，gameid，操作命令，房间号
"""
GM_CONTROL_DATA = 'GMControlData:uid:%s:list'
GM_CONTROL_DATA_MAX_LEN = 100


"""
新大厅广播内容表 (与原广播不冲突)
记录广播信息
{
    broad_id   :   广播编号
    per_sec    :   间隔/s
    content    :   广播内容
    start_date :   开始时间
    end_date   :   结束时间
    broad_type :   广播类型 0,1,2,3
    parent_ag  :   发送广播公会
}
"""
HALL_BRO_COUNT = "hall:broadcast:count"
HALL_BRO_TABLE = "hall:broadcast:%s:info"
HALL_BRO_LIST  = "hall:broadcast:list:all"
HALL_BRO_AG_LIST = "hall:broadcast:list:ag:%s"

FISH_BRO_LIST  = "fish:broadcast:list:all"
"""
广播列表分类
hall:broacast:type:%s:list
$type 0-全服维护广播 1-全服循环广播 2-地区维护广播 3-地区循环广播
"""
HALL_BRO_CONTAIN_ALL_LIST = "hall:broadcast:type:%s:list"
FISH_BRO_CONTAIN_ALL_LIST = "fish:broadcast:type:%s:list"

"""
代理下的广播分类
hall:broacast:type:%s:list
$type 0-全服维护广播 1-全服循环广播 2-地区维护广播 3-地区循环广播
"""
HALL_BRO_CONTAIN_AG_LIST = "hall:broadcast:type:%s:ag:%s:list"

"""
待播放广播队列
hall:broacast:play:queue
"""
HALL_BRO_PLAY_QUEUE = "hall:brocast:play:queue"

"""
过期的广播集合
hall:broadcast:out:set
"""
HALL_BRO_OUT_SET = "hall:bro:out:set"

"""
正在播放的广播集合
hall:broadcast:out:set
"""
HALL_BRO_PLAY_SET = "hall:bro:play:set"

"""
捕鱼奖票表
{
    rate        :   击中概率
    need_coin   :   金币保底
    coin        :   金币价值
}
fish:ticket:$id:info
"""
FISH_TICKET_TABLE = "fish:ticket:%s:info"

"""
捕鱼奖品表
{
    'reward_id' : 奖品ID
    'reward_name' : 奖品名称
    'reward_stock' : 每期指定库存
    'reward_per_stock':每期当前库存
    'reward_need_ticket' : 奖品兑换所需奖券
    'reward_img_path' : 奖品图片地址
    'reward_pos'      : 奖品位置
    'reward_nums'      : 奖品总期数
    'reward_now_nums'  : 当前期数
    'reward_cost'      : 商品成本
    'reward_type'      : 奖品类型  0-实物奖品，1-卡密奖品,
    'reward_status'    : 奖品状态  0-下架 1-上架 默认为下架
    'reward_auto_charge' : 奖品自动续期开关 0-关闭 1-开启
    'reward_card_no'   : '虚拟卡号',
    'reward_card_pwd'  : '虚拟卡密'
}
"""
FISH_REWARD_ID_COUNT = "fish:reward:id:count"
FISH_REWARD_ID_SET = "fish:reward:id:sets"
FISH_REWARD_LIST   = "fish:reward:id:list"
FISH_REWARD_TABLE  = "fish:reward:%s:info"
'''
奖品自动续期表
'''
FISH_REWARD_AUTO_CHARGE = "fish:reward:auto:charge:set"
'''
已上架商品集合
上架商品存放到已上架奖品列表
'''
FISH_REWARD_ON_SHOP_LIST = "fish:reward:onshop:list"
'''
已上架商品按分类存放
'''
FISH_REWARD_ON_SHOP_TYPE_LIST = "fish:reward:onshop:type:%s:list"

"""
捕鱼玩家兑换记录表
{
    'exchange_id'     :   兑换ID
    'exchange_user_id'         :   兑换玩家ID
    'exchange_reward_id'     :   兑换商品ID
    'exchange_reward_name'     :   兑换商品名称
    'exchange_reward_img_path' :   兑换商品图片
    'exchange_time'         :   兑换时间
    'exchange_use_ticket'  : 兑换使用卷
    'exchange_leave_ticket' : 兑换后剩余卷
}
"""
FISH_EXCHANGE_ID_COUNT = "fish:exchange:id:count"
FISH_EXCHANGE_LIST = "fish:exchange:list"
FISH_EXCHANGE_TABLE = "fish:exchange:item:%s:info"
'''
用户兑换索引
'''
FISH_USER_EXCHANGE_LIST = "fish:exchange:user:%s:list"
'''
兑换记录时间索引
'''
FISH_USER_EXCHANGE_DATE = 'fish:exchange:%s:date:list'
'''
兑换记录状态索引
0-未发货 1-已发货
'''
FISH_USER_EXCHANGE_STATUS_LIST = "fish:exchange:%s:status:list"

'''
分享领取金币相关
'''
FISH_FISH_SHARE_ID = 'fish:first:share:count'
FISH_FISH_SHARE_TABLE = 'fish:first:share:%s:table'
FISH_SHARE_TOTAL = "fish:first:share:total"

FISH_FIRST_SHARE_PER_DAY_SET = "fish:first:share:sets"
'''
待领取金币的玩家ID集合
'''
FISH_SHARE_NOT_TAKE_SETS = "fish:share:not:take:sets"
'''
已领取金币的玩家ID集合
'''
FISH_SHARE_TAKE_SETS = "fish:share:take:sets"
'''
捕鱼配置表
{
        share_coin  :   每日分享获得金币
        exchange_shop : 兑换商店状态  0-不开放 1-开放
        fish_shop   :   捕鱼商城状态  0-不开放 1-开放
}
'''
FISH_CONSTS_CONFIG = "fish:config:setting:hesh"

WAIT_JOIN_GAME_ROOMID_PLAYERS = 'WaitJoinGame:%s'
WAIT_JOIN_GAME_GROUPID_PLAYERS = 'WaitJoinGroup:%s'
ACCESS_TOKEN_API =  'AccessToken:api'
ACCESS_TOKEN_JSAPI =  'AccessToken:jsapi'

"""
捕鱼系统金币充值总额
FISH_SYSTEM_RECHARGE_TOTAL
"""
FISH_SYSTEM_RECHARGE_TOTAL = "fish:sys:recharge:total"
"""
每日充值人数和充值总额
{
    recharge_money_total
    recharge_user_total
}
"""
FISH_RECHARGE_USER_DAY_IDS = "fish:recharge:user:id:sets"
FISH_SYSTEM_DATE_RECHARGE_TOTAL = "fish:sys:date:%s:recharge:total"
"""
防访问次数table
"""
USER_API_ACCESS_TABLE = "user:%s:api:limit:table"
API_BLACK_SET = "api:limit:black:sets"
USER_API_EXPIRE = 60


# 金币场充值相关
"""
    日充值金币数
"""
DAILY_GOLD2_SUM = 'gold2:date:%s:sum'
"""
    日充值金币金额
"""
DAILY_GOLD2_MONEY_SUM = 'gold2:money:date:%s:sum'
"""
    日充值人数集合
"""
DAILY_USER_GOLD2_SET = 'gold2:user:date:%s:set'
"""
    用户日充值金币数
"""
DAILY_ACCOUNT_GOLD2_SUM = 'gold2:account:%s:date:%s:sum'
"""
    用户日充值金币金额数
"""
DAILY_ACCOUNT_GOLD2_MONEY_SUM = 'gold2:account:%s:money:date:%s:sum'

"""
金币排行榜表
表项：
[($uid, coin),...]
"""
FORMAT_USER_COIN_TABLE = "users:coin:day:%s:zset"
FORMAT_USER_COINDELTA_TABLE = "users:coinDelta:day:%s:zset"
TMP_FORMAT_USER_COINDELTA_TABLE = "users:coinDeltaTmp:zset"
FROMAT_USER_FISHCOUNT_TABLE = "users:game:%s:fishCount"
FROMAT_USER_TICKETCOUNT_TABLE = "users:ticketCount"
FISH_LEVEL_SHIFT_MASK = 0xFF000000
FISH_COUNT_SHIFT_MASK = 0x00FFFFFF
RANK_COUNT = 10
MY_MAX_RANK = 50
NOT_RANK_USE_NUM = 10000
RANK_SAVE_TIME = 7 * 24 * 60 * 60
TMP_TABLE_SAVE_TIME = 2 * 24 * 60 * 60


"""
    背包系统
"""

# 用户道具数量表
PLAYER_ITEM_HASH = "player:item:uid:%s:hash"
# 用户道具数量过期时间表 已废弃
ITEM_ENDTIME_NUM = "num:endtime:uid:%s:itemid:%s::hash"
# 道具属性表
ITEM_ATTRS = "attrs:itemid:%s:hash"
# 邮箱表
EMAIL_HASH = "email:id:%s:hash"
# 用户邮箱集合表
USER_EMAIL_SET = "user:uid:%s:email:set"
# 道具id列表
ITEM_ID_SET = "item:id:set"
# 保险箱金币表
SAVE_BOX_HASH = "save:box:hash"
# 当天发送邮箱集合表
USER_EMAIL_DATE_SET = "user:email:date:%s:set"
# 邮件有效期
EMAIL_RETENTION_TIME = 1
# 任务列表

TASK_LIST = "gold:title:task:set"
"""
编号: 

"""

TASK_CONTENT = "gold:title:task:attribute:%s:hset"
"""
id: 任务编号
description: 说明
gameType: 0=金币场 1=比赛场 2=大厅
where: {"gold": {}, "win": {}, "lost": {}, "sports": {}, "continueWin": {},  "other": {}} # 获得条件
results: [{"type": }] # 返回奖励
title: 获得称号名称
status: 状态 0=关闭 1= 开启
"""
# WHERE说明
"""
# 金币场金币数量
gold: {
    type: 1=指定天金币数量最多， 2=当前金币数量
    value: 天数或者金币数 
    week : 指定周期开放进行领取。 [0,1,2,3,4,5,6] 不填写则是每天
    date : 指定日期开房进行领取。 不填写则是每天
}
# 胜场数量
win: {
    type: 1=普通胜场 2=连续胜场 
    value: 次数 
    week : 指定周期开放进行领取。 [0,1,2,3,4,5,6] 不填写则是每天
    date : 指定日期开房进行领取。 不填写则是每天
}
# 失败数量
lost: {
    type: 1=普通敗场 2=连续敗场 3=特殊失败(连续点炮)
    value: 次数 
    week : 指定周期开放进行领取。 [0,1,2,3,4,5,6] 不填写则是每天
    date : 指定日期开房进行领取。 不填写则是每天
}
# 竞技
sports: {
    type: 1=获得竞技场名次奖励 
    rank: 名次 绝对等于
    value: 次数
    week : 指定周期开放进行领取。 [0,1,2,3,4,5,6] 不填写则是每天
    date : 指定日期开房进行领取。 不填写则是每天
}
# 其他
other: {
    type: 1=俱乐部创建者成员数量, 2=分享次数 3=抽奖内容 4=游戏时常 5=连续登录 6=钻石消费
    value: 
    week : 指定周期开放进行领取。 [0,1,2,3,4,5,6] 不填写则是每天
    date : 指定日期开房进行领取。 不填写则是每天
}

"""
# results说明
"""
[
{
    "type": 0=金币, 1=钻石
    "value": 数量
}
]
"""


CHETS_TASK_GAME = "task:chets:game:%(gameId)s:%(level)s:hesh"
"""
number: 要求对局次数
level : 奖励等级
result: [{"type": 1=道具， 2=金币， 3=钻石， "value": 道具ID， 金币数量， 钻石数量}]

"""
CHETS_TASK_WIN_GAME = "task:chets:win:game:%(gameId)s:%(level)s:hesh"
"""
number: 连胜次数
level : 奖励等级
result: [{"type": 1=道具， 2=金币， 3=钻石， "value": 道具ID， 金币数量， 钻石数量}]

"""


PLAYER_CHETS_TASK_GAME = "task:player:game:%(gameId)s:%(level)s:hesh"
"""
account: number ("账户"："次数")

"""

PLAYER_CHETS_TASK_WIN_GAME = "task:player:win:game:%(gameId)s:%(level)s:hesh"
"""
account: number ("账户"："次数")

"""

# 活动设置相关
ACTIVICE_TABLE = "activice:setting:%s"
ACTIVICE_LIST_TABLE = "activice:setting:%s:list"
ACTIVICE_COUNT_TABLE = "activice:setting:count"
ONLINE_ACTIVICE_LIST = "activice:setting:%s:list:online"

"""
    活动奖品库存
    activice:setting:活动ID:奖品ID:reward:num
"""
ACTIVICE_REWARD_NUM = "activice:setting:%s:%s:reward:num"

PLAYER_BUFF_TABLE = 'user:%s:buff'

"""
    比赛场
"""
MATCH_SET = "match:game:ids:set"  # 比赛游戏ID集合
MATCH_GAME_SET = 'match:game:%s:set'  # 比赛游戏ID对应场次ID集合
MATCH_GAME_ID_TABLE = 'match:game:%s:id:%s'  # 比赛游戏场次信息
MATCH_GAME_COUNT = "match:game:%s:count"  # 场次ID自增长
MATCH_GAME_ID_DESC = 'match:game:%s:id:%s:desc' # 游戏规则
MATCH_AWARDS_NAME_TABLE = {'roomCard': '钻石', 'gamePoint': '积分'}  # 比赛场奖励
MATCH_AWARDS_TYPE_TABLE = {'1': 'roomCard', '3': 'gamePoint'}  # 比赛场奖励

"""
广告
"""
NOTIC_AD_ID_SET = "notic:ad:id:set"
NOTIC_AD_TABLE  = "notic:ad:%s:hesh"
NOTIC_AD_ID_COUNT = "notic:ad:id:count"
NOTIC_AD_UPLOAD_PATH = 'mahjong/static/assest/default/image/ad'

"""
支付宝
"""
ALIPAY_APP_ID = "2019012363096631"
ALIPAY_WAP_METHOD = "alipay.trade.wap.pay"
ALIPAY_FORMAT = "JSON"
ALIPAY_CHARSET = "utf-8"
ALIPAY_SIGN_TYPE = "RSA2"
ALIPAY_VERSION = '1.0'
ALIPAY_NOTIFY_URL = "http://testinterface.soujiyou168.com/hall/alipay/NotifyServer"
ALIPAY_RETURN_URL = "http://testinterface.soujiyou168.com/invite"
ALIPAY_APPLICATION_PRIVATE_KEY = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCw8NfWpIiNBx7K52gMY+LQ5bW5FwBFG0NHqUYegVDpHfDRCszrWYotsVmXY1t1VjBeTxB3p/rzQync6Yc3cSt8CY+DBqPZEyEpE+Ta+SP+ZJxv19Rvjl2R2RjO2APrPxNTldaVATTYMmnNHC3b6J3oqKVc6ka1ct3HQdsMXCAXEo+R4dBiKhJPszwcevExWPL5W2hDBtLbAcfxjn6S0mR4jUDybFvggQeM73v2eafEIca7XowOjDFY+Vaw6Wt5L5fnqzk6SBoOHAatN4or64n4OD3MsYrAzFYixiiPvJHoNBX2qJDkuLBxiCZ/5W0d9gg/K2ActfZ8CyEMjLjKhaqpAgMBAAECggEAdF9CpbH6+T4Im4yMmzGKuLeLyFr/W3Qt0NDdBC0q6Nc/Tk1bLyLpxVmSQgYf3dE86Jn5i6kYXKv8uYWB4A33epHTKGrSkm+JbLnf18DqUmMbnFeIKYKpucXeEhRyp2MJs/ylb8SmW9b0TOlOpAae7KkWcUDIFoigom+GwN9KX8FD1D3oAF9PdiTZPymnuZoyW0YVr6mB/8XSvcGTOUFLu9AlaEI0813BhgVsP0WIESltMvYz45HwSMz5m8bt/eZ3glRNaDGURkTtBd0cPnrKHHxjFR/omghygeyY+f5beL+cmI1DuhJVFSvW/zU92QEgPLCed0+hxNPOb5rjX6EqcQKBgQDzpxedtyER46Zs+dWMEkXB9Ek9YklyOs09w16YwYKsdwgQf/HQ3TRzAXOffTfOwf+DDZimDM5jPOr2MyOVTYeJY73eSl/QaQ29Rz9yacMCJGrtv9C32x6A66164b98BxIUB8iDB+iRGm7SXie3n0+z/1mXl6c/Y3cMYqHnTxPrXQKBgQC56EwCy8bGICHuyRy+wVSDAKlSasRdMPU989aBikZVtePy6Hho2lBk149mWXi6+zMlxbY5w3yzJZreI0p3tqmD7INDhYkH8Ilk3NrCFkagkxpIOy/LOt2WVwmBFAXtH6MbdAEs/oGNDyUuskQAU/VeC1K8UKMQzMWwlzZs2y0TvQKBgGscB0uz13vPwbeiVHgRCE1tIE01yefHZbZDDnDEkLdUVF08gYc51va/qp5wI3pm2fY4oeRNOOVzQC8e6AOYY37INA1mUJyDsiCFE6UuTSXB8Ke3bP+F+fDeqhKc7tqNGStpCIJhlaFEJ3efIIKeLCGKnU4AwusgxJLTQS04HB+ZAoGBAKkOAPEZ9Wv9lF3cLHOawwtN8qurw10rRBhOQGYUI9mVSfB+TeCrhiftjc141zzRabWTkR3+EsumCqquVO2AAa6hyMwCBpZdudMqsxODxj4HBwNgLxoUMaShCVeDqc/z0RMJ7nfICG8JsrpACW5y6tHWYio0+dQxIiRvnWJn/RnRAoGAM63wfTjDCnM9T680V4JHQsA7rpVbzm4Um4kOAi5uX3kRNqXO8RcnPRMtOb0rHdHIXt9o/d9v97XDmzCpwbwBaCW+IgOag8dZ9dRpeS9Sm4bZri0ldltXF2BEjKX6qffR5/zZjgmjw8zC5b5kgB9sslF49m5K5u/4aZ0lsbca+as="
ALIPAY_APPLICATION_PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsPDX1qSIjQceyudoDGPi0OW1uRcARRtDR6lGHoFQ6R3w0QrM61mKLbFZl2NbdVYwXk8Qd6f680Mp3OmHN3ErfAmPgwaj2RMhKRPk2vkj/mScb9fUb45dkdkYztgD6z8TU5XWlQE02DJpzRwt2+id6KilXOpGtXLdx0HbDFwgFxKPkeHQYioST7M8HHrxMVjy+VtoQwbS2wHH8Y5+ktJkeI1A8mxb4IEHjO979nmnxCHGu16MDowxWPlWsOlreS+X56s5OkgaDhwGrTeKK+uJ+Dg9zLGKwMxWIsYoj7yR6DQV9qiQ5LiwcYgmf+VtHfYIPytgHLX2fAshDIy4yoWqqQIDAQAB"
ALIPAY_PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqFAlMkUp9OlHwg3fa+cc5Wg0OxOrP6AbFusHb43IJCa50gpK28N39LHpYoKqEYQQqG4vlT0DJVVxF8KMR6R7Qyzpr2vv/mm6LinURkl3nhue339jFiKwi1w0RESTv6x1BhQdSDJ7T6CcoqNxDwVsazLPDhXK7JetU1pPQNqzXUXfNu/Cl2tZL1QV3V77IFwG6BMwGZJglWcvnzMPE/UAsHTqcm+0H3oPr40O9/HjWfjffXf5Gz7810TpcwU19Dub3Hgk0+9sGOvGumEJ5s0/AHJUh8NLeaqsu0gWEF8RF2mW4W7ImVq/bEIUTTbxEzIkVSo6bTW+Kap9/ysMCQ6VQwIDAQAB"

"""
椰子竞技
"""
COCOGC_TIME = 5  # 查询接口隔秒数
COCOGC_POINT_PROPORTION = 100  # 椰云积分兑换比例
COCOGC_ORDER_USER_LIST = 'cocogc:orders:%s:list'  # 椰云用户兑换积分订单记录
COCOGC_ORDER_TABLE = 'cocogc:orders:id:%s'        # 椰云订单详情
COCOGC_ORDER_KEY = 'cocogc:orders:101:key'        # 椰云订单ID
COCOGC_MERCHANTID = "920064062e4e407fb7660c8193d0113b"  # 商户ID
COCOGC_PRIVATE_KEY = "7ccb85a101d64abbd2d28a3b0eb7ad42"  # 椰子密钥
COCOGC_BINDUSER = "https://tapi.cocogc.cn/api/bindUser"  # 用户绑t定接口
COCOGC_GETTOKEN = "https://tapi.cocogc.cn/api/getToken"  # 用户登录
COCOGC_GETUSERINFO = "https://tapi.cocogc.cn/api/userInfo"  # 用户积分查询
COCOGC_POINTINCOME = "https://tapi.cocogc.cn/api/pointIncome"  # 用户积分收入接口
COCOGC_SEARCHORDERS = "https://tapi.cocogc.cn/api/searchOrders"  # 用户积分收入接口
COCOGC_POINT_INCOME_USER_TIME= 'cocogc:point:income:%s:time'  # 用户兑换积分时间
COCOGC_POINT_SEARCH_USER_TIME= 'cocogc:point:search:%s:time'  # 用户查询积分时间
COCOGC_ORDER_SEARCH_USER_TIME= 'cocogc:order:search:%s:time'  # 用户兑换订单时间
COCOGC_PLAYER_DAY_DATA = 'cocogc:playerData4day:%s:%s:hesh'  # 用户兑换总数记录
COCOGC_LOGIN_DATE_TABLE = "cocogc:date:account:%s" # w 玩家兑换名单
"""
创盈商城
"""
CYGSE_TIME = 5  # 查询接口隔秒数
CYGSE_POINT_PROPORTION = 100  # 椰云积分兑换比例
CYGSE_ORDER_USER_LIST = 'cygse:orders:%s:list'  # 椰云用户兑换积分订单记录
CYGSE_ORDER_TABLE = 'cygse:orders:id:%s'        # 椰云订单详情
CYGSE_ORDER_KEY = 'cygse:orders:101:key'        # 椰云订单ID
CYGSE_MERCHANTID = "1574041494365"  # 创盈商户ID
CYGSE_PRIVATE_KEY = "7a062de3fa3e5c9118f3c63f317055a0"  # 创盈密钥
CYGSE_BINDUSER = "http://ntmall.cygse.com/api/bind_user"  # 用户绑定接口
CYGSE_GETTOKEN = "http://ntmall.cygse.com/api/get_token"  # 用户登录
CYGSE_POINTINCOME = "http://ntmall.cygse.com/api/exchange_coin"  # 用户积分兑换
CYGSE_GETPOINT = "http://ntmall.cygse.com/api/get_user_coin_num" # 用户积分查询
CYGSE_POINT_INCOME_USER_TIME= 'cygse:point:income:%s:time'  # 用户兑换积分时间
CYGSE_POINT_SEARCH_USER_TIME= 'cygse:point:search:%s:time'  # 用户查询积分时间
CYGSE_ORDER_SEARCH_USER_TIME= 'cygse:order:search:%s:time'  # 用户兑换订单时间
CYGSE_PLAYER_DAY_DATA = 'cygse:playerData4day:%s:%s:hesh'  # 用户兑换总数记录
CYGSE_LOGIN_DATE_TABLE = "cygse:date:account:%s" # w 玩家兑换名单

"""
比赛场缓存数据
"""
MATCH_CACHE_TIME = 60
MATCH_LOGIN_DATE_KEY = 'match:login:date:%s:%s:set'  # 比赛场登录人数
MATCH_RECORD_DATE_SET = 'match:record:date:%s:%s:set'  # 比赛场数据总和
MATCH_RECORD_GAME_DATE_SET = 'match:record:game:date:%s:%s:set'  # 比赛场数据总和

"""
分享获取钻石数
"""
SHARE_ROOMCARD = 2 # 分享获取钻石数
SHARE_TIME_INTERVAL = 7200 * 1000  # 分享间隔时间
SHARE_GAME_DATE_ZSET = 'share:game:date:%s:set' # 用户分享时间集合
SHARE_GAME_USER_ZSET = 'share:game:user:%s:zset' # 用户分享时间集合
SHARE_GAME_DATE_TOTAL_KEY = 'share:game:date:%s:total' # 当天分享钻石总数

"""
用户领取默认公会钻石
"""
AGENT_DEFAULTCARD_SET = 'agent:default:roomcard:%s:set' # 当天领取公会默认钻石
AGENT_DEFAULTCARD_TOTAL_HASH = 'agent:default:roomcard:hash' # 公会被领取默认钻石总数
