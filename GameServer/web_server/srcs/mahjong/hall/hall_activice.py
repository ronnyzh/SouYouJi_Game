#-*- coding:utf-8 -*-
#!/usr/bin/python

from common.log import *
from hall import hall_app
from hall_func import *
from bottle import request, Bottle, abort, redirect, response, template,static_file
from model.activeModel import *
from common.utilt import *
from model.niuniuModel import *
from config.config import STATIC_LAYUI_PATH, STATIC_ADMIN_PATH, BACK_PRE,RES_VERSION, STATIC_ACTIVICE_PATH,AC_TYPE_NIUNIU
from datetime import *
from model.hallModel import getHotSettingAll
import time



@hall_app.get('/activice/check')
@allow_cross
def do_getHallServer(redis,session):
    """
        查看活动列表
    """
    sid = request.GET.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}

    online_ac = []
    data = []
    province_agentid = getProvinceAgentId(redis,groupId)
    online_ac.extend(get_online_activices(redis,province_agentid))
    online_ac.extend(get_online_activices(redis,systemId))

    for info in online_ac:
        if info.get('allowAgent',''):
            allowAgent = info['allowAgent']
            if province_agentid in [allow.get('allowAgentId','') for allow in allowAgent]:
                data.append(info)
        else:
            data.append(info)

    # 插入牛牛活动
    niuniulist = getActiviceNiuniuList(redis, groupId, request)
    data = data + niuniulist

    # 写入默认配置，如果有这个字段则不覆盖
    # 用于写入一些默认配置比如 海报图
    urlParts = request.urlparts
    rootUrl = "{0}://{1}".format(urlParts.scheme, urlParts.netloc)
    for key,acData in enumerate(data):
        type = acData.get('type','')
        if type == "turnlate"  :
            defaultOption = {
                            'posterUrl': rootUrl + STATIC_ACTIVICE_PATH +'/admin/turnlate_poster.jpg',
                            'iconUrl':  rootUrl + STATIC_ACTIVICE_PATH +'/admin/turnplate-icon.png'
                        }
            data[key]=dict(defaultOption, **acData)
    return {'code': 0, 'msg': '', 'data': data}


@hall_app.get('/activice/niuniuShare')
@allow_cross
def getActiviceNiuniuShare(redis,session):
    """
    牛牛分享朋友圈回调
    """
    sid = request.GET.get('sid', '').strip()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code': -5, 'msg': '该用户不存在'}
    picUrl, gender, groupId, isVolntExitGroup, maxScore, baseScore = \
        redis.hmget(userTable, ('headImgUrl', 'sex', 'parentAg', 'isVolntExitGroup', 'maxScore', 'baseScore'))
    if not groupId:
        return {'code': -7, 'msg': '您已被移出公会，请重新加入公会'}
    return process_niuniu_share(redis, account)


@hall_app.get('/activice/route')
@allow_cross
def getActiviceByAcId(redis, session):
    sid = request.GET.get('sid', '').strip()
    agentId = request.GET.get('agentId', '').strip()
    ac_type = request.GET.get('type', '').strip()
    acid = request.GET.get('id', '').strip()
    getJson = request.GET.get('getJson', '').strip()
    lang = getLang()
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    userTable = getUserByAccount(redis, account)
    groupId = redis.hget(userTable,'parentAg')
    # 牛牛活动
    if ac_type == AC_TYPE_NIUNIU:
        return getActiviceNiuniuInfo(redis)

    #其他活动
    activice_info = getActiciveInfo(redis,acid)

    if not check_activice_isonline(redis, acid):
        return {'code': 301, 'msg': "活动已关闭"}

    # 获取用户进度
    user_schedule = get_user_schedule(redis,acid,account)
    if not user_schedule:
        user_schedule = init_user_schedule(redis,activice_info["missionList"])
    # 获取奖品详细信息
    for ind,reward in enumerate(activice_info["rewardList"]):
        searchId = reward["rewardId"]
        detailInfo = get_rewardList2(redis,agentId,searchId,lang, searchType = '')
        reward_infos = detailInfo["data"][0]
        activice_info["rewardList"][ind] = dict(reward, **reward_infos)


    # 获奖人列表
    awardee = get_awardees(redis,groupId,acid)
    # log_debug('********************5555555555555555555555555555555555555{0}'.format(awardee))
    # 获取用户抽奖次数
    drawCount = get_lottery_num(redis,acid,account)
    serverCount = get_lottery_server_count(redis)

    # 获取h5网页
    htmlList = [
        {"type":"turnlate","template":"turnlate"},
        {"type":"redpack","template":"redpack"},
    ]
    for htmlInfo in htmlList:
        if htmlInfo["type"] == activice_info["type"]:
            htmlTemplate = htmlInfo["template"]

    # 获取根目录
    urlParts = request.urlparts
    rootUrl = "{0}://{1}".format(urlParts.scheme, urlParts.netloc)

    setting = {
        "activice"  : activice_info,
        "drawCount" : drawCount,
        "awardee"   : awardee,
        "serverCount": serverCount,
        "user_schedule" : user_schedule,
        "rootUrl"   : rootUrl,
        "resourceUrl" : "http://niuniu.dongshenggame.cn:9798"
    }

    info = {
        'title': "活动",
        'STATIC_ADMIN_PATH': "%s/%s" % (STATIC_ACTIVICE_PATH, "turnlate"),
        'submitUrl': "/hall/activice/draw?id=%s_%s" % (sid,acid)
    }

    if getJson == '1' :
        data = dict(setting, **info)
        return {'code':0,'msg':'获取活动数据成功','data':data}
    else:
        return template(htmlTemplate,info = info, lang = lang,setting = setting)


def get_meet_confidion(redis,acid,plans):
    """
        查看是否满足特殊条件
    """
    total = int(get_lottery_activice_count(redis,acid)) + 1
    ret_dict = {}
    for plan in plans:
        plan_type = plan['planNeedType']
        plan_num = int(plan['planNeedNum'])
        plan_level = int(plan['planNeedLevel'] or 0)
        if (plan_type == 'multiple' and total>=plan_num and total%plan_num==0) or \
            (plan_type == 'equal' and total == plan_num):
            ret_dict[plan_level] = plan

        log_debug('total ********************  {0} {1}'.format(total,plan_num))

    if not ret_dict:
        return
    return ret_dict[max(ret_dict.keys())]


@hall_app.get('/activice/draw')
@hall_app.post('/activice/draw')
@allow_cross
def drawReward(redis,session):
    """
        抽奖
    """
    type = request.GET.get('type', '').strip()
    times = request.GET.get('times', '').strip()
    Ids = request.GET.get('id', '').strip().split('_')
    # 牛牛抽奖
    if type == AC_TYPE_NIUNIU:
        sid = request.GET.get('sid', '').strip()
        _, account, _, _ = getInfoBySid(redis, sid)
        return getActiviceNiuniuDraw(redis, times)
    sid = Ids[0]
    acid = Ids[1]
    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)
    if verfiySid and sid != verfiySid:
        return {'code':-4,'msg':'账号已在其他地方登录', 'osid':sid}
    if not redis.exists(SessionTable):
        return {'code':-3,'msg':'sid 超时'}

    userTable = getUserByAccount(redis, account)
    if not redis.exists(userTable):
        return {'code':-5,'msg':'该用户不存在'}
    groupId= redis.hget(userTable, 'parentAg')
    nickname = redis.hget(userTable, 'nickname')

    if get_lottery_num(redis, acid, account) <= 0:
        log_debug('玩家{0}没有足够的抽奖次数'.format(account))
        return {'code':1, 'msg':'抽奖失败'}

    if not check_activice_isonline(redis,acid):
        return {'code':301, 'msg':'活动已关闭'}

    activice_info = getActiciveInfo(redis, acid)
    probabilitys = []  # 概率
    rewards = {}
    special_flag = False
    # 特殊概率
    # 查看是否满足条件
    if activice_info.get('specialPlan',[]):
        plan = get_meet_confidion(redis,acid,activice_info['specialPlan'])
        if plan:
            special_flag = True
            log_debug('达到特殊概率条件  {0}'.format(plan))
            for side,reward in enumerate(plan["specialRate"]):
                searchId = reward["planRewardId"]
                # 库存判断
                if get_active_reward_num(redis,acid,searchId) <= 0:
                    continue
                rate = int(float(reward["planRewardRate"])*100)
                rewards[side] = searchId
                probabilitys.extend([side] * rate)

    if special_flag == False:
        for reward in activice_info["rewardList"]:
            searchId = reward["rewardId"]
            # 库存判断
            if get_active_reward_num(redis, acid, searchId) <= 0:
                continue
            rate = int(float(reward["rewardRate"])*100)
            side = int(reward["rewardSide"])
            rewards[side] = searchId
            probabilitys.extend([side]*rate)

    set_lottery_activice_count(redis, acid)

    if not probabilitys:
        return {'code': 1, 'msg': "没有库存了"}

    pos = random.choice(probabilitys)

    ret_reward_list = []

    reward_info = getRewardInfo(redis,rewards[pos])
    if reward_info:

        pipe = redis.pipeline()
        # 会员ID
        id = userTable.split(':')[1]

        isRecord = False

        # 奖励钻石
        if reward_info.get('type','') == 'diamonds':
            cardNums = int(reward_info.get('baseRewardCount', '0'))
            log_debug('应奖励钻石 {0}'.format(cardNums))
            if cardNums > 0:
                pipe.incrby(USER4AGENT_CARD % (groupId, id), cardNums)
                ret_reward_list.append(reward_info)

        # 礼包发放部分
        elif reward_info.get('type','') == 'pack':
            log_debug('应奖励礼包')

            price_total = int(reward_info['priceTotal'])
            reward_num = 0

            for singleData in reward_info['singleData']:
                mincount = int(singleData['minCount'])
                reward = getRewardInfo(redis, singleData['singleId'])
                price = int(reward['priceTotal'])
                if price_total - price*mincount < 0:
                    break
                price_total -= price*mincount
                if reward.get('type', '') == 'diamonds':
                    reward_num += int(reward.get('baseRewardCount', '0'))*mincount
                ret_reward_list.extend([reward]*mincount)

            if price_total > 0:
                for singleData in reward_info['singleData'][:-1]:
                    mincount = int(singleData['minCount'])
                    maxcount = int(singleData['maxCount'])
                    reward = getRewardInfo(redis, singleData['singleId'])
                    price = int(reward['priceTotal'])
                    count = (maxcount-mincount if (price_total/price)>(maxcount-mincount) else price_total/price)
                    if count <= 0:
                        continue
                    real_count = random.choice(xrange(count+1))
                    price_total -= price*real_count
                    if reward.get('type', '') == 'diamonds':
                        reward_num += int(reward.get('baseRewardCount', '0'))*real_count
                    ret_reward_list.extend([reward] * real_count)

                if price_total > 0:
                    singleData = reward_info['singleData'][-1]
                    mincount = int(singleData['minCount'])
                    maxcount = int(singleData['maxCount'])
                    reward = getRewardInfo(redis, singleData['singleId'])
                    price = int(reward['priceTotal'])
                    count = (maxcount - mincount if (price_total / price) > (maxcount - mincount) else price_total / price)
                    real_count = count
                    price_total -= price * real_count
                    if reward.get('type', '') == 'diamonds':
                        reward_num += int(reward.get('baseRewardCount', '0')) * real_count
                    ret_reward_list.extend([reward] * real_count)

                if price_total >= 0:
                    pipe.incrby(USER4AGENT_CARD % (groupId, id), reward_num)

        elif reward_info.get('type', '') == 'goods':
            if reward_info['isRecord'] == '1':
                isRecord = True
        else:
            ret_reward_list.append(reward_info)

        decr_active_reward_num(redis, acid, reward_info['id'])

        # 获奖人信息
        info = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "id": id,
            "name": nickname if nickname else account,
            "rewardTitle": reward_info['title'],
            "rewardId": reward_info['id'],
            "rewardNum": int(reward_info.get('baseRewardCount', '1')),
            "type": reward_info.get('type', ''),
        }
        if isRecord:
            info['record'] = 1

        reid = set_awardees(redis,groupId,acid,info)

        if isRecord:
            reward_info['recordId'] = reid
            reward_info['acid'] = acid
            reward_info['jumpUrl'] = HALL_PRE + '/activice/draw/phone'
            ret_reward_list.append(reward_info)
            # 写入未领取列表
            set_noreward_awardees(redis, account,acid, reid, ret_reward_list)

        desc_lottery_num(redis,acid,account)
        pipe.execute()

    return {'code':0, 'msg':"", 'data':{'pos':pos,'content':ret_reward_list}}


@hall_app.post('/activice/draw/phone')
@allow_cross
def drawReward(redis, session):
    recordId = request.POST.get('recordId', '').strip()
    phone = request.POST.get('phone', '').strip()
    acid = request.POST.get('acid', '').strip()
    name = request.POST.get('realName', '').strip()
    sid =  request.POST.get('sid', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    checkNullFields = [
            {'field':name,'msg':'请输入你的姓名'},
            {'field': phone, 'msg': '请输入你的手机号'},
    ]
    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}


    info = {
        'phone': phone,
        'name': name
    }
    modify_awardees(redis,recordId,acid,info)

    # 从未领取列表中删除
    remove_noreward_awardees(redis,account, acid, recordId)

    return {'code': 0, 'msg': ""}


@hall_app.post('/activice/checkNoreward')
@allow_cross
def checkNoReward(redis, session):
    """检查该玩家未领取实物列表
    sid = request.POST.get('sid', '').strip()

    SessionTable, account, uid, verfiySid = getInfoBySid(redis, sid)

    ret = check_noreward_awardees(redis,account)
    """

    return {'code':0,'msg':"",'data':[]}


@hall_app.get('/activice/niuniu/cash')
@allow_cross
def getNiuniuCash(redis, session):
    return {'code': 0, 'msg': u"请联系客服，微信：{0}".format(KEFU_WEIXIN)}


@hall_app.get('/activice/inviteNiuniu')
def getInviteNiuniuPage(redis,session):
    """
    邀请页面链接
    """
    ip = request.remote_addr
    rid = request.GET.get('rid','').strip()

    HALL2VERS = getHotSettingAll(redis)

    log_debug('[HALL][url:/invite][info] requestIp[%s] rid[%s] versionInfo[%s]'%(ip,rid,HALL2VERS))

    # links = {
    #         'scheme_android'        :       'dsmj://com.dsmj/invite?rid=%s'%(rid),
    #         'scheme_ios'            :       'com.DSYL://invite?rid=%s'%(rid),
    #         'download_ios'          :        HALL2VERS['IPAURL'],
    #         'download_android'      :       'https://fir.im/5xtp'
    # }

    links = {
        'scheme_android': 'dsmj://com.dsmj/invite?rid=%s' % (rid),
        'scheme_ios': 'com.DSYL://invite?rid=%s' % (rid),
        'download_ios': HALL2VERS['IPAURL'],
        'download_android': 'http://a.app.qq.com/o/simple.jsp?pkgname=com.dsmj'
    }

    info = {
        'entry_title'           :           '搜集游棋牌牛牛完美归来',
        'scheme_ios'            :           links['scheme_ios'],
        'scheme_android'        :           links['scheme_android'],
        'ios_download'          :           links['download_android'],
        'android_download'      :           links['download_android'],
        'ifr_src'               :           '',
        'timeout'               :           1000,
    }

    response.add_header("Expires", 0)
    response.add_header( "Cache-Control", "no-cache" )
    response.add_header( "Cache-Control", "no-store" )
    response.add_header( "Cache-Control", "must-revalidate" )
    #是否限制IP
    return template('inviteNiuniu',info=info)