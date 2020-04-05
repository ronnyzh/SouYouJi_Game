#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description:
    翻译文本
"""
MAHJONG_TITLE_TXT = '搜集游棋牌后台管理系统'
MAHJONG_LOGIN_TITLE_TXT = '搜集游棋牌后台系统登录'
COPY_RIGHT_TXT    = '2019 后台管理系统'

SELF_INFO_TXT = '个人信息'
LOUT_TXT = '退出'

INPUT_LABEL_ACCOUNT_COUNT_TXT = '创建账号个数:'
INPUT_LABEL_ACCOUNT_TXT = '账号:'
INPUT_LABEL_ACCOUNT_TYPE_TXT = '账户类型:'
INPUT_LABEL_LOGIN_TIME_TXT = '最近登录时间:'
INPUT_LABEL_LOGIN_IP_TXT = '最近登录IP:'
INPUT_LABEL_AG_LEVEL_TXT = '代理级别:'
INPUT_LABEL_AG_ACOUNT_TXT = '下线数:'
INPUT_LABEL_NAME_TXT = '名字:'
INPUT_LABEL_CREDIT_TXT = '信用余额:'
INPUT_LABLE_CREDIT_LIMIT_TXT = '信用额度'
INPUT_LABEL_EMAIL_TXT = '电子邮件:'
INPUT_LABEL_PHONE_TXT = '电话:'
INPUT_LABEL_SHARE_TXT = '占成比例:'
INPUT_LABEL_ODDS_PUMPING_TXT = '赔率抽水比例:'
INPUT_LABEL_ODDS_MIN_TXT = '最小赔率因子:'
INPUT_LABEL_STATUS_TXT = '状态:'
INPUT_LABEL_OLD_PASSWD_TXT = '旧密码'
INPUT_LABEL_PASSWD_TXT = '密码'
INPUT_LABEL_VALIDATE_CODE_TXT = '验证码:'
INPUT_LABEL_PASSWD1_TXT = '新密码'
INPUT_LABEL_PASSWD2_TXT = '确认密码'
INPUT_LABEL_AGID_TXT = '代理ID:'
INPUT_LABEL_CURRENCY_TXT = '货币:'
INPUT_LABEL_SELF_PASSWD_TXT = '你的密码:'
INPUT_LABEL_PARENT_AG_TXT = '上线代理:'
INPUT_LABEL_DEPOSIT_CREDIT_TXT = '存款金额'
INPUT_LABEL_WITHDRAW_CREDIT_TXT = '取款金额'
INPUT_LABEL_REMARK_TXT = '备注:'
INPUT_LABEL_OPERATOR_CACHE_EXIST_SEC_TXT = '转登录cache持续时间(秒):'
INPUT_LABEL_API_REQUEST_COUNT_TXT = 'API请求最大次数:'
INPUT_LABEL_API_URL_TXT = 'API URL:'
INPUT_LABEL_CAGENT_TXT = '总代标识:'
INPUT_LABEL_ORDER_NO_TXT = '订单流水编号:'
INPUT_LABEL_IN_MD5_KEY_TXT = '接收数据 MD5密钥:'
INPUT_LABEL_IN_DES_KEY_TXT = '接收数据 DES密钥:'
INPUT_LABEL_OUT_MD5_KEY_TXT = '发送数据 MD5密钥:'
INPUT_LABEL_OUT_DES_KEY_TXT = '发送数据 DES密钥:'
INPUT_LABEL_ODDS_UP_DELTA_TXT = '升水赔率比例:'
INPUT_LABEL_ODDS_UP_USER_COUNT_TXT = '每次升水玩家比例:'
INPUT_LABEL_ODDS_UP_SWITCH_SEC_TXT = '升水转换时间间隔（秒）:'
INPUT_LABEL_BROADCAST_CONTENT_TXT = '广播内容:'
INPUT_LABEL_BROADCAST_TYPE_TXT = '广播类型:'
INPUT_LABEL_BROADCAST_REPEAT_COUNT_TXT = '广播重复次数:'
INPUT_LABEL_BROADCAST_REPEAT_INTERVAL_TXT = '广播间隔(秒):'
INPUT_LABEL_COUNT_DOWN_TXT = '倒计时:'
INPUT_LABEL_TOTAL_TXT = '总计:'
INPUT_LABLE_LAST_LOGIN_TIME_TXT = '上次登录时间:'
INPUT_LABLE_LAST_LOGIN_IP_TXT = '上次登录IP:'
INPUT_LABLE_MARQUEE_TXT = '公告内容:'
INPUT_LABLE_PARENT_TXT = '父账号:'
INPUT_LABLE_SUB_ACCOUNT_ID_TXT = '子账号ID：'
LABLE_MAX_ONLINE_COUNT = '最高同时在线人数：'


INPUT_LABEL_START_DATE_TXT = '开始时间'
INPUT_LABEL_END_DATE_TXT = '结束时间'
INPUT_TIPS_START_DATE_TXT = '请选择查询开始日期'
INPUT_TIPS_END_DATE_TXT = '请选择查询结束日期'
INPUT_LABEL_PREV_MONTH = '上月'
INPUT_LABEL_CURR_MONTH = '今月'
INPUT_LABEL_PREV_WEEK = '上周'
INPUT_LABEL_CURR_WEEK = '本周'
INPUT_LABEL_PREV_DAY = '昨天'
INPUT_LABEL_CURR_DAY = '今天'
INPUT_LABEL_QUERY = '查询'
INPUT_LABEL_CHECK_ENABLE = '是否可用'
INPUT_LABEL_CASH_TYPE = '账类筛选'

MEMBER_NOT_EXISTES_TXT = '会员[%s]不存在'


BTN_LOGIN = '登录'
BTN_START_GAME = '启动游戏'
BTN_CLOSE_GAME = '关闭游戏'
BTN_SUBMIT_TXT = '提交'
BTN_CREATE_TXT = '生成规则'
BTN_BACK_TXT = '返回'
BTN_PARENT_CASH_TXT = '(%s)(%s) 输赢报表'
BTN_PARENT_TOTAL_CASH_TXT = '(%s)(%s) 输赢总报表'
BTN_PARENT_AG_TXT = '(%s)(%s) 成员列表'


TYPE_2_ADMINTYPE = {
        '0'           :       '超级管理员',
        '1'           :       '省级代理',
        '2'           :       '市级代理',
        '3'           :       '市级代理2'
}


AGENT_OP_LOG_TYPE = {
        'openAgent'        :       '创建代理[%s]',
        'modifyAgent'        :       '修改代理[%s]信息',
        'freezeAgent'        :       '冻结代理[%s]',
        'unfreezeAgent'      :       '解冻代理[%s]',
        'modifyHall'         :       '更正大厅配置[%s]',
        'createGame'         :       '新建游戏[%s]',
        'modifyGame'         :       '修改游戏[%s]',
        'deleteGame'         :       '删除游戏[%s]',
        'createFishRoom'     :       '创建捕鱼[%s]房间',
        'modifyFishRoom'     :       '修改捕鱼[%s]房间',
        'rechargeMember'     :       '向玩家[%s]充值了钻石[%s]张',
        'checkMember'        :       '审核玩家[%s]加入公会',
        'uncheckMember'      :       '移除玩家[%s]出公会',
        'rejectMember'       :       '拒绝玩家[%s]加入公会',
        'modifyMember'       :       '修改玩家[%s]信息',
        'removeRoomCard'     :       '从玩家[%s]移除了钻石[%s]个',
        'addRoomCard'        :       '向玩家[%s]补充了钻石[%s]个',
        'kickGm'             :       '移除玩家[%s]gm权限',
        'addGm'              :       '给玩家[%s]设置gm权限',
        'createGameRule'     :       '生成游戏[%s]规则',
        'trailAgent'         :       '设置公会[%s]及其下线公会为试玩公会',
        'unTrailAgent'       :       '设置公会[%s]及其下线公会为正式公会',
        'rechargeAg'         :       '开启公会[%s]及其下线公会的线上充卡功能',
        'unRechargeAg'       :       '关闭公会[%s]及其下线公会的线上充卡功能',
        'autocheck'          :       '开启公会[%s]及其下线公会的自动审核',
        'unAutocheck'        :       '关闭公会[%s]及其下线公会的自动审核',
        'createAuth'         :       '允许公会[%s]及其子公会创建三级代理',
        'unCreateAuth'       :       '禁止公会[%s]及其子公会创建三级代理',
        'openAuth'           :       '设置公会[%s]及其子公会有权限的玩家可以代开房间',
        'unOpenAuth'         :       '设置公会[%s]及其子公会所有玩家可以代开房间',
        'openMemberAuth'     :       '开启会员[%s]的代开房间权限',
        'unOpenMemberAuth'   :       '关闭会员[%s]的代开房间权限',
        'goodsDel'           :       '删除商品ID[%s]的物品',
        'goodsModify'        :       '操作接口[%s] 修改商品ID[%s]的物品',
        'reward_create'      :       '操作接口[%s] 创建奖品[%s]成功',
        'reward_modify'      :       '操作接口[%s] 修改奖品[%s]成功',
}

LABEL_PARENT_ACCOUNT = '上级代理名称'
LABEL_PARENT_ID = '上级代理ID'
LABEL_MEMBER_TOTAL   = '总用户数'
LABEL_REGIST_DAY     = '当日注册数'
LABEL_LOGIN_DAY      = '当日活跃数'
LABEL_PLAYROOM_DAY   = '当日耗钻数'
LABEL_RECHARGE_DAY   = '当日充值金额'
LABEL_ROOMCARD_TITLE = '钻石数'
LABEL_AGENTID_TXT    = '代理ID'
LABEL_AGENTROLE_TXT  = '角色'
LABEL_LOGOUT_TXT     = '退出'
LABEL_LASTLOIN_TIME_TXT = '上次登录时间'
LABEL_LASTLOIN_IP_TXT = '上次登录IP'

MENU_PRIMARY_TXT = '主菜单'
MENU_SYS_TXT = '系统设置'
MENU_GAME_PAY_LIST_TXT = '支付设置'
MENU_FISH_SETTING_TXT = '捕鱼大厅配置'
MENU_HOT_UPDATE_LIST_TXT = '大厅更新设置'
MENU_TASK_LIST_TXT = "任务系统"
MENU_TASK_STETS_TXT = "宝箱系统"

MENU_HOT_DATA_QUERY_TXT = '数据查询'
MENU_GAME_MODULE_LIST_TXT = '游戏模块列表'
MENU_GAME_TXT = '游戏管理'
MENU_GAME_LIST_TXT = '游戏列表'
MENU_GAME_BROAD_LIST_TXT = '广播列表'
MENU_GAME_BROADCAST_TXT = '游戏广播发布'
MENU_GAME_NOTICE_LIST_TXT = '游戏公告列表'
MENU_NOTIC_TXT = '信息公告管理'
MENU_NOTIC_TEMP_TXT = '信息模板设置'
MENU_NOTIC_LIST_TXT = '系统公告列表'
MENU_NOTIC_AD_TXT = '广告列表'
MENU_NOTIC_MAIL_LIST_TXT = '邮件列表'
MENU_SHOPMALL_TXT = '商城兑换'
MENU_SHOPMALL_COCOGC_TXT = '椰云商城'
MENU_SHOPMALL_CYGSE_TXT = '创盈商城'
MENU_GOODS_TXT = '商品管理'
MENU_GOODS_LIST_TXT = '商品列表'
MENU_GOODS_REWARD_LIST_TXT = '兑换奖品管理'
MENU_GOODS_EXCHANGE_LIST_TXT = '奖品兑换记录'
MENU_AGENT_TXT = '代理管理'
MENU_AGENT_LIST_TXT = '下线代理关系'
MENU_AGENT_ROLE_LIST_TXT = '下线代理查看'
MENU_AGENT_ACTIVE_TXT = '代理活跃统计'
MENU_AGENT_ROOM_LIST_TXT = '玩家房间列表'
MENU_AGENT_RESET_PWD_TXT = '代理密码重置'
MENU_MEMBER_TXT = '会员管理'
MENU_AGENT_MEMBER_CURONLINE_TXT = '会员在线'
MENU_AGENT_MEMBER_DEFAULTCARD_TXT = '会员默认钻石记录'
MENU_AGENT_MEMBER_SHARE_TXT = '会员分享记录'
MENU_AGENT_MEMBER_DAYUSE_TXT = '会员钻石消耗'
MENU_MEMBER_SEARCH_GAMEPOINT_TXT = '会员积分兑换记录'
MENU_MEMBER_SEARCH_TXT = '会员充钻'
MENU_MEMBER_SEARCH_COIN_TXT = '会员充金币'
MENU_MEMBER_LIST_TXT = '会员列表'
MENU_MEMBER_GM_SET_TXT = 'GM列表'
MENU_MEMBER_COMPENSATE_TXT = '钻石/积分增减记录'
MENU_MEMBER_JOINLIST_TXT = '公会申请列表'
MENU_ORDER_TXT = '我的订单'
MENU_ORDER_BUY_TXT = '购买钻石'
MENU_ORDER_WECHAT_TXT = '商城售钻记录'
MENU_ORDER_BUY_RECORD_TXT = '购买钻石记录'
MENU_ORDER_SALE_RECORD_TXT = '售卖钻石记录'
MENU_ACCOUNTS_TXT = '数据统计'
MENU_REPORT_TXT = '订单/报表'
MENU_STATISTICS_SALEREPORT_TXT = '我的售钻报表'
MENU_STATISTICS_BUYREPORT_TXT = '我的购钻报表'
MENU_STATISTICS_AGENT_SALEREPORT_TXT = '下线代理售钻报表'
MENU_STATISTICS_AGENT_BUYREPORT_TXT = '下线代理购钻报表'
MENU_STATISTICS_RATEREPORT_TXT = '利润占成报表'
MENU_STATISTICS_RATEREPORT2_TXT = '利润占成报表2'
MENU_STATISTICS_REG_TXT = '注册人数统计'
MENU_STATISTICS_LOGIN_TXT = '登录人数统计'
MENU_STATISTICS_ACTIVE_TXT = '活跃人数统计'
MENU_STATISTICS_DAILY_TXT = '每日数据统计'
MENU_STATISTICS_USER_SAVE_TXT = '用户留存统计'
MENU_STATISTICS_GAME_PLAY_TXT = '游戏玩法统计'
MENU_STATISTICS_MATCH_TXT = '赛事数据统计'
MENU_STATISTICS_MATCH_PLAYER_TXT = '赛事玩家统计'
MENU_STATISTICS_OVERALL_DATA_TXT = '总体数据'
MENU_STATISTICS_CARD_TXT = '钻石消耗统计'
MENU_STATISTICS_COUNT_TXT = '局数统计'
MENU_PERSON_TXT = '个人信息'
MENU_SELF_MODIFYPASSWD_TXT = '密码修改'
MENU_SELF_SYSLOG_TXT = '操作记录'
MENU_SELF_LOGINLOG_TXT = '登录日志'

MENU_FISH_TXT = '捕鱼游戏'
MENU_FISH_DATA_TXT = '捕鱼游戏数据'
MENU_FISH_ROOM_LIST_TXT = '捕鱼房间列表'
MENU_FISH_BET_LIST_TXT = '玩家数据统计'
MENU_FISH_DATA_MODIFY_TXT = '数据调整'
MENU_FISH_BET_REPORT_TXT = '玩家数据统计'
MENU_FISH_RECHARGE_LIST_TXT = '充值明细'
MENU_FISH_ONLINE_LIST_TXT = '捕鱼在线'
MENU_FISH_ONLINE_REAL_TXT = '捕鱼玩家实时在线'
MENU_FISH_DATA_REAL_TXT = '捕鱼系统数据统计'
MENU_FISH_AGENT_REPORT_TXT = '胜负统计'

MEMBER_ONLINE_TITLE_TXT = '会员实时在线'
MEMBER_LIST_TITLE_TXT = '会员列表'
MEMBER_INPUT_TXT = '请输入会员编号'
MEMBER_DIOMAN_INPUT_TXT = '请填写移除的钻石数'
MEMBER_DIOMAN_INPUT_NUM_TXT = '请填写正确的整数'
MEMBER_DIOMAN_LT_TXT = '钻石数不能小于等于0'
MEMBER_DIOMAN_GT_TXT = '钻石不等大于会员现有的钻石数'
MEMBER_DIOMAN_REMOVE_SUCCESS = '移除会员[%s] %s个钻石成功'
MEMBER_COIN_REMOVE_SUCCESS = '移除会员[%s] %s个金币成功'
MEMBER_DIOMAN_ADD_SUCCESS = '补充会员[%s] %s个钻石成功'
MEMBER_COIN_ADD_SUCCESS   = '补充会员[%s] %s个金币成功'

WECHAT_RECORD_TITLE = '商城售钻记录'
WECHAT_FISH_RECORD_TITLE = '捕鱼微信金币充值记录'
# 列表权限
LIST_AGENT_CREATE_TXT = '创建代理'
LIST_AGENT_MODIFY_TXT = '修改'
LIST_AGENT_INFO_TXT = '查看'
LIST_AGENT_FREEZE_TXT = '冻结'
LIST_AGENT_TRAIL_TXT  = '设置为试玩'
LIST_AGENT_RECHARGE_TXT  = '线上充卡'
LIST_AGENT_CHECK_TXT  = '自动审核'
LIST_AGENT_AUTH_TXT  = '开启三级公会'
LIST_AGENT_PRODUCE_INVITE_TXT = '生成邀请码'
LIST_AGENT_MANAGERS_SET_TXT = '设置公会管理'
LIST_AGENT_OPEN_AUTH_TXT  = '权限者代开房'
LIST_MEMBER_KICK_TXT = '移出公会'
LIST_MEMBER_REMOVECARD_TXT = '移除钻石数'
LIST_MEMBER_MODIFY_TXT = '修改信息'
LIST_MEMBER_FREEZE_TXT = '冻结'
LIST_MEMBER_CHARGE_TXT = '补钻石'
LIST_MEMBER_CHANGECARD_TXT = '增减钻石'
LIST_MEMBER_CHANGEGAMEPOINT_TXT = '增减积分'
LIST_MEMBER_OPEN_TXT = '开启代开权限'
LIST_MEMBER_CHANGE_AGENT_TXT = '转移公会'
LIST_GAME_NOTICE_MODIFY = '修改'
LIST_GAME_NOTICE_DEL = '删除'
LIST_GAME_NOTICE_PUSH = '推送'
LIST_ROOM_DISSOLVE_TXT = '强制解散房间'
LIST_ROOM_DISSOLVE2_TXT = '强制解散房间2'
#商品管理
GOODS_LIST_TXT  =  '商品列表'
GOODS_CREATE_TXT = '创建新商品'
GOODS_REWARD_CREATE_TXT = '添加新奖品'
GOODS_NAME_TXT  = '商品名称'
GOODS_NOTE_TXT = '商品介绍'
GOODS_TYPE_TXT  = '商品类型'
GOODS_CARD_TXT  = '商品钻石数'
GOODS_COIN_TXT  = '商品金币数'
GOODS_CARD_PRESENT_TXT = '赠送钻石数'
GOODS_COIN_PRESENT_TXT = '赠送金币数'
GOODS_PRICE_TXT = '商品价格(单位:元)'
GOODS_NOT_EMPTY_TXT = '商品名称不能为空'
GOODS_CARD_NOT_EMPTY_TXT = '商品钻石数不能为空'
GOODS_PRICE_NOT_EMPTY  =  '商品价格不能为空'
GOODS_CREATE_SUCCESS_TXT = '商品[%s]创建成功'
GOODS_CREATE_ERROR_TXT = '商品[%s]创建失败'
GOODS_MODIFY_TXT  = '商品[%s]修改'
GOODS_MODIFY_SUCCESS_TXT  = '商品[%s]修改成功'
GOODS_MODIFY_ERROR_TXT  = '商品[%s]修改失败'
GOODS_SETTING_TXT  =  '商品设置'
GOODS_PRICE_SETTING_TXT = '商品单价设置为[%s]'
GOODS_SETTING_TXT_ERROR  = '商品单价设置失败'

#钻石
CARD_SALER_TXT = '卖钻石方'
CARD_PACK_CHOOSE_TXT = '充值钻石数'
CARD_BUY_ONLINE_TXT = '线上购钻[上级代理:%s]'
CARD_SALER_NOT_EXISTS = '售钻方不存在'
CARD_REMARK_TXT = '备注信息'
CARD_RECHARGE_NUMS_REQUEST = '请选择充值钻石数'
CARD_RECHARGE_PASSWD_REQ = '请填写你的登录密码'
CARD_HANDLE_TIPS_TXT = '请输入正确的密码,才能进行此操作'
CARD_APPLY_SUCCESS_TXT = '申请购买钻石成功,订单号[%s]'
CARD_APPLY_ERROR_TXT = '申请购买钻石失败,订单号[%s]'
CARD_BUY_RECORD_TXT = '购钻记录'
CARD_SALE_RECORD_TXT = '售钻记录'
CARD_ORDER_NOT_EXISTS = '订单[%s]不存在'
CARD_NOT_ENGOUGHT_TXT = '钻石不足,是否前往购买钻石'
CARD_COMFIRM_ERROR_TXT = '订单确认失败'
CARD_COMFIRM_SUCCESS_TXT = '订单[%s]确认成功'
CARD_DETAIL_TXT  = '订单[%s]详情'
CARD_CANCEL_SUCCESS_TXT = '订单[%s]取消成功'
CARD_CANCEL_ERROR_TXT = '订单取消失败'
CARD_APPLY_RECHARGE_TXT = '申请充值'

COMFIRM_ALREADY_TXT = '已确认'
COMFIRM_NOT_TXT  = '未确认'

#[游戏]
GAME_LIST_TXT  =  '游戏列表'
GAME_CREATE_TXT = '创建新游戏'
GAME_SET_DEFAULT_TXT = '设置/解除默认游戏'
GAME_NAME_NOT_EMPTY_TXT = '游戏名称不能为空'
GAME_VER_NOT_EMPTY_TXT = '游戏版本号不能为空'
GAME_CREATE_SUCCESS_TXT = '游戏[%s]创建成功'
GAME_CREATE_ERROR_TXT   = '游戏[%s]创建失败'
GAME_MODIFY_SUCCESS_TXT = '游戏[%s]修改成功'
GAME_MODIFY_ERROR_TXT = '游戏[%s]修改失败'
GAME_MODIFY_TXT = '[%s]游戏修改'
GAME_BROCAST_TXT = '全游戏广播'
GAME_BROCAST_CON_TXT = '请填写广播内容'
GAME_BROCAST_SEND_SUCCESS = '发布广播成功'
GAME_BROCAST_SEND_ERROR = '发布广播失败'
GAME_DISSOLVE_ROOM_SUCCESS = '解散房间成功'
GAME_BROCAST_REPEAT_ERR_TXT = '重复次数错误'
GAME_BROCAST_SEC_ERR_TXT = '重复秒数错误'
GAME_ID_REPEAT_TXT = '游戏ID[%s]已存在'
GAME_NOTIFY_LIST_TXT = '游戏公告列表'
GAME_BROAD_LIST_TXT = '广播列表'
GAME_NOTIFY_CREATE_TXT = '创建新公告'
GAME_BROAD_CREATE_TXT = '创建新广播'
GAME_NOTIFY_SEND_TXT = '发布游戏公告'
GAME_NOTIFY_REQ_TXT = '请填写游戏公告'
GAME_NOTIFY_SEND_SUCCESS_TXT = '发布公告成功'
GAME_NOTIFY_DEL_TXT = '删除公告'
GAME_NOTIFY_DEL_SUCCESS_TXT = '删除公告成功'
GAME_NOTIFY_DEL_ERR_TXT = '删除公告失败'
GAME_NOTIFY_MODIFY_TXT = '公告信息修改'
GAME_EDIT_DESC = '[%s]游戏规则'
GAME_INTRO_TITLE = '游戏规则'
GAME_INTRO_TXT = '(规则内容用于游戏客户端显示)'
GAME_INTRO_CREATE_SUCCESS = '生成游戏[%s]规则成功'
GAME_INTRO_CREATE_ERROR = '生成游戏[%s]规则失败'
GAME_ID_ERROR_TXT = 'gameId错误'
GAME_INTRO_NOT_EMPTY = '游戏规则描述不能为空'
GAME_NOTIFY_MODIFY_SUC_TXT = '公告修改成功'
GAME_NOTIFY_MODIFY_ERR_TXT = '公告修改失败'

FISH_ROOM_LIST_TXT = '捕鱼房间列表'
FISH_ROOM_CREATE_TXT = '创建新房间'
FISH_ROOM_MODIFY_TXT = '修改房间信息'
FISH_ROOM_NAME_EMPTY_TXT = '房间名称不能为空'
FISH_ROOM_ID_EMPTY_TXT = '房间编号(ID)不能为空'
FISH_ROOM_BASE_EMPTY_TXT = '房间最小底分不能为空'
FISH_ROOM_MAX_BASE_EMPTY_TXT = '房间最大底分不能为空'
FISH_ROOM_STEP_BASE_EMPTY_TXT = '房间步长底分不能为空'

MSG_TYPE_ONE   = '系统公告'
MSG_TYPE_TWO   = '活动消息'
MSG_TYPE_THREE = '玩家邮件'
#[系统设置]
SYSTEM_SETTING_TITLE_TXT = '系统设置'


CLINET_KIND_TXTS = {
    '0'     :   'Web Browser',
    '1'     :   'Android',
    '2'     :   'IOS',
}

getBroadType = {

        '0'         :       '游戏广播',
        '1'         :       '大厅广播',
        '2'         :       '游戏/大厅广播'
}

GROUP_NOT_EXISTS_TXT = '公会[%s]不存在'
GROUP_STATUS_SETTING_SUCCESS = '设置公会[%s]状态成功'
GROUP_RECHARGE_SETTING_SUCCESS = '设置公会[%s]商城状态成功!'
GROUP_CHECK_SETTING_SUCCESS = '操作成功'


""" 配置相关提示 """
SETTING_TIPS_SUCCESS = '配置成功'
SETTING_TIPS_ERROR   = '配置失败'
SETTING_WECHAT_SWITCH_TXT = '微信支付开关值只能为0或1'
SETTING_HOT_UPDTAE_TIPS = '热更新配置'


'''
        竞技场&金币场模块
'''
MENU_PARTY_MODEL_TXT = "竞技/金币/比赛场"
MENU_PARTY_ONE = "竞技场"
PARTY_COMPETITION_SETTING = "竞技场配置"
PARTY_COMPETITION_JOURNAL = "竞技场流水表"
PARTY_COMPETITION_OPERATE = "竞技场运营表"
PARTY_COMPETITION_SETTING_SUCCESS = "竞技场配置成功"
PARTY_COMPETITION_SETTING_ERROR = "竞技场配置成功"
MENU_PARTY_TWO = "金币场"
PARTY_COMPETITION_OPEN_SUCCESS = "竞技场开启成功"
PARTY_COMPETITION_OPEN_ERROR = "竞技场开启失败"
PARTY_COMPETITION_CLOSE_SUCCESS = "竞技场关闭成功"
PARTY_COMPETITION_CLOSE_ERROR = "竞技场关闭失败"
GOLD_USER_DATA = "总用户数据表"
GOLD_OPERATE = "总运营表"
GOLD_AI_DATA = "AI数据表"
GOLD_OPERATE_DATA = "运营数据表"
GOLD_ACTIVE_PLAYER_DATA = "活跃玩家运营表"
GOLD_AI_CONFIG = "修改AI配置"
GOLD_ROBOT_GOOD_HAND = "C档AI转换及好牌概率配置"
ACCUMULATED_VALUE_SETTING = "累计值调控"
MENU_GOLD_WECHAT_TXT = '商城金币记录'

MENU_PARTY_THREE = "比赛场"
MENU_MATCH_SETTING = '比赛场设置'
MENU_MATCH_LIST = '比赛设置'
MENU_MATCH_RUN_LIST = '比赛列表'
MENU_MATCH_MODIFY = '修改比赛场设置'
MENU_MATCH_LOG = '二人麻将统计表'
MENU_MATCH_LOG_2 = '跑得快统计表'

MENU_HONOR_TITLE = "荣誉场"
MENU_HONOR_API1 = "荣誉场接口"

# 背包模块
BAG_CREATE_ITEM = "创建道具"
BAG_LIST = "道具列表"
BAG_MODEL_TXT = "背包系统"
BAG_EMAIL_TXT = "邮件系统"
BAG_SEND_MAIL = "发送邮件"
BAG_ENCLOSURE_MAIL = "附件领取记录"
BAG_VCOIN_DAY = "当天元宝信息"
BAG_VCOIN_SUM = "元宝总表"
BAG_EXCHANGE_LIST = "商城兑换列表"
BAG_EXCHANGE_CREATE_LIST = "创建兑换套餐"


#商城兑换类型
REWARD_TYPE_2_DESC = {
        0       :       '手机',
        1       :       '话费',
        2       :       '家用电器',
        3       :       '生活用品',
        4       :       '电子产品'
}

######################################################################################
#捕鱼接口
######################################################################################
EXCHANGE_REAL_TIPS = '兑换成功,奖品将在3-5个工作日内发出,请注意查收'


#活动模块
MENU_ACTIVICE_TXT = '活动'
MENU_ACTIVE_TXT = '活动'
MENU_ACTIVICE_SETTING = '活动设置'
MENU_ACTIVICE_LIST = '活动列表'
MENU_RESOURCE_LIST = "资源列表"
MENU_REWARD_LIST = "奖品管理"

ACTIVICE_TITLE = '活动标题'
ACTIVICE_MISSION = '活动任务'
ACTIVICE_TEMPLATE = '活动模板'
ACTIVICE_CREATE_TXT = '增加活动'
ACTIVICE_TIME = '起止时间'
ACTIVICE_AGENT_LIST = '限定开启工会'


LIST_GAME_ACTIVICE_ADD = '增加'
LIST_GAME_ACTIVICE_MODIFY = '修改'
LIST_GAME_ACTIVICE_DEL = '删除'
LIST_GAME_ACTIVICE_READ = '查看'
LIST_GAME_ACTIVICE_CHECK = '提交'
LIST_GAME_ACTIVICE_START = '开启'
LIST_GAME_ACTIVICE_CLOSE = '关闭'


ACTIVICE_TEMPLATE_TYPE_NONE  = '无'
ACTIVICE_TEMPLATE_TYPE_ONE   = '红包雨'
ACTIVICE_TEMPLATE_TYPE_TWO   = '风车'
ACTIVICE_TEMPLATE_TYPE_THREE = '转盘'

ACTIVICE_CREATE_SUCCESS = '活动设置成功'
ACTIVICE_CREATE_ERROR = '活动设置失败'

ACTIVICE_READ_TXT= '查看活动'
ACTIVICE_CONFIRM_TXT= '审核活动'
ACTIVICE_MODIFY= '修改活动'

ACTIVICE_LIST_SUCCESS = '获取活动列表成功'
ACTIVICE_LIST_ERROR = '获取活动列表成功'

ACTIVICE_REWARD_LIST_INDEX = '活动奖品管理'
ACTIVICE_REWARD_LIST_TXT = '活动奖品列表'
ACTIVICE_REWARD_LIST_ADD = '增加活动奖品'
ACTIVICE_REWARD_LIST_EDIT = '修改活动奖品'
ACTIVICE_REWARD_LIST_ADD_SUCCESS = '增加活动奖品成功'
ACTIVICE_REWARD_LIST_SUCCESS = '获取奖品列表成功'
ACTIVICE_REWARD_LIST_ERROR = '无法获取奖品列表'
ACTIVICE_REWARD_LIST_ADD_FAIL = '增加活动奖品失败'
RESOURCE_LIST_SUCCESS = "资源列表获取成功"
RESOURCE_LIST_ERROR = "资源列表获取成功"
RESOURCE_ADD_TEXT = "新增资源"
RESOURCE_ADD_SUCCESS = "新增资源成功"
RESOURCE_ADD_ERROR = "新增资源失败"
RESOURCE_DEL_SUCCESS = "资源删除成功"
RESOURCE_DEL_ERROR = "资源删除失败"
RESOURCE_EDIT_TEXT = "修改资源信息"
RESOURCE_EDIT_SUCCESS = "资源修改成功"
RESOURCE_EDIT_ERROR = "资源修改失败"

ACTIVICE_STATIS_RECORD = "全部奖品记录"
ACTIVICE_STATIS_SPECIAL = "实物奖品记录"
