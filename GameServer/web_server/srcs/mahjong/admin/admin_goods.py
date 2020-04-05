#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    商品管理模块
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH,STATIC_ADMIN_PATH,BACK_PRE,RES_VERSION
from common.utilt import *
from common.log import *
from common import encrypt_util,web_util,log_util,convert_util
from datetime import datetime
from web_db_define import *
from model.goodsModel import *
from model.agentModel import *
from access_module import *
import hashlib
import json
import md5
import time

#奖品字段俞
reward_fields = (
            'token',
            'reward_id',
            'img_path1',
            'reward_name',
            'reward_stock',
            'img_path',
            'reward_need_ticket',
            'reward_pos',           #奖品位置
            'reward_nums',          #奖品总期数
            'reward_now_nums',      #奖品当前期数
            'reward_cost',          #奖品成本
            'reward_type',          #奖品类型
            'reward_status',        #奖品状态
            'reward_auto_charge',        #奖品自动续期开关
            'reward_card_no',           #奖品卡号
            'reward_card_pwd',          #奖品密码
            'reward_per_stock',        #每期奖品库存
            'reward_coin'               #奖品金币
)

@admin_app.get('/goods/list')
@admin_app.get('/goods/list/<action>')
def getGoodList(redis,session,action="hall"):
    """
    商品列表视图
    """
    lang = getLang()
    action = action.upper()

    fields = ('isList','sys')
    for field in fields:
        exec("%s=request.GET.get('%s','').strip()"%(field,field))

    if not sys: #默认访问棋牌后台
        if action:
            sys = action
        else:
            sys = 'HALL'

    if isList:
        if action == 'HALL':
            res = get_goods_list(redis,goods_type='0',action='hall')
        else:
            res = get_goods_list(redis,goods_type='1',action='fish')
        return json.dumps(res)
    else:
        info = {
                'title'         :     lang.GOODS_LIST_TXT,
                'addTitle'      :     lang.GOODS_CREATE_TXT,
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'tableUrl'      :     BACK_PRE+'/goods/list/{}?isList=1'.format(sys)
        }
        #info['createAccess'] = True if BACK_PRE+'/game/create' in accesses else False
        info['createUrl']   = BACK_PRE+'/goods/create/{}'.format(sys)
        return template('admin_good_list',system=sys,info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/goods/fish/reward/list')
def getGoodList(redis,session):
    """
    捕鱼奖品兑换设置页面
    """
    lang = getLang()

    isList = request.GET.get('list','').strip()

    info = {
            'title'         :     '兑换奖品列表',
            'addTitle'      :     lang.GOODS_REWARD_CREATE_TXT,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'exchang_record_list_url' :     BACK_PRE+'/goods/reward/exchange/list',
            'tableUrl'      :     BACK_PRE+'/goods/fish/reward/list?list=1'
    }

    if isList:
        res = get_fish_reward_list(redis)
        return json.dumps(res)
    else:
        #info['createAccess'] = True if BACK_PRE+'/game/create' in accesses else False
        info['createUrl']   = BACK_PRE+'/goods/reward/create'
        return template('admin_goods_reward',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.get('/goods/reward/create')
def getGoodsCreate(redis,session):
    """
    创建捕鱼兑换奖品视图
    """
    lang = getLang()

    page_token = encrypt_util.to_md5(str(time.time()))
    info = {
            'title'             :       lang.GOODS_CREATE_TXT,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'back_pre'          :       BACK_PRE,
            'backUrl'           :       BACK_PRE+'/goods/fish/reward/list',
            'submitUrl'         :       BACK_PRE+'/goods/reward/create',
            'upload_url'        :       BACK_PRE+'/goods/reward/upload',
            'token'             :       page_token

    }
    #recordLastURL(session,BACK_PRE+'/game/list')
    return template('admin_goods_reward_create',message='',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/goods/reward/create')
def do_reward_create(redis,session):
    """
    创建捕鱼兑换奖品视图
    """
    lang = getLang()
    curTime = datetime.now()

    for reward_field in reward_fields:
        exec("%s = request.forms.get('%s','').strip()"%(reward_field,reward_field))

    check_null_fields = [
                {'fields':reward_name,'msg':'奖品名称不能为空'},
                {'fields':reward_stock,'msg':'奖品初始库存不能为空'},
                {'fields':reward_need_ticket,'msg':'奖品所需兑换卷不能为空'},
                {'fields':reward_nums,'msg':'奖品总期数不能为空'},
                {'fields':reward_now_nums,'msg':'奖品当前期数不能为空'}
    ]

    for check_field in check_null_fields:
        if not check_field['fields']:
            return {'code':1,'msg':check_field['msg']}

    log_debug('[try do_reward_create] reward_id[%s] reward_name[%s] reward_stock[%s] reward_img_path[%s]'\
                    %(reward_id,reward_name,reward_stock,img_path))

    reward_id = redis.incr(FISH_REWARD_ID_COUNT)
    reward_info = {
            'reward_id'            :      reward_id,
            'reward_name'          :      reward_name,
            'reward_stock'         :      reward_stock,
            'reward_img_path'      :      img_path[14:],
            'reward_need_ticket'   :      reward_need_ticket,
            'reward_pos'           :      reward_pos,           #奖品位置
            'reward_nums'          :      reward_nums,          #奖品总期数
            'reward_now_nums'      :      reward_now_nums,      #奖品当前期数
            'reward_cost'          :      reward_cost,          #奖品成本
            'reward_type'          :      reward_type,          #奖品类型
            'reward_status'        :      reward_status if reward_status else 0,        #奖品状态
            'reward_auto_charge'   :      0,
            'reward_card_no'       :      reward_card_no if reward_card_no else '',           #奖品卡号
            'reward_card_pwd'      :      reward_card_pwd if reward_card_pwd else '',        #奖品密码
            'reward_per_stock'     :      reward_per_stock if reward_per_stock else 0,         #奖品密码
            'reward_coin'          :      reward_coin if reward_coin else 0

    }

    try:
        do_create_reward(redis,reward_info)
    except Exception,e:
        return {'code':1,'msg':'创建奖品失败错误代码:[%s]'%(e)}

    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
            'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['reward_create']%('/goods/reward/create',reward_name)}
    #记录日志
    writeAgentOpLog(redis,session['id'],logInfo)
    return {'code':0,'msg':'创建奖品[%s]成功!'%(reward_name),'jumpUrl':BACK_PRE+'/goods/fish/reward/list'}

@admin_app.get('/goods/reward/modify')
def get_reward_modify(redis,session):
    """
    捕鱼奖品修改视图
    """

    curTime = datetime.now()
    lang    = getLang()
    reward_id  = request.GET.get('reward_id','').strip()

    reward_info  =  get_reward_info(redis,reward_id)
    page_token = md5.new(str(time.time())).hexdigest()
    info = {
                'title'     :       lang.GOODS_MODIFY_TXT%(reward_info['reward_name']),
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'back_pre'          :       BACK_PRE,
                'backUrl'           :       BACK_PRE+'/goods/fish/reward/list',
                'submitUrl'         :       BACK_PRE+'/goods/reward/modify',
                'upload_url'        :       BACK_PRE+'/goods/reward/upload',
                'token'             :       page_token
    }

    return template('admin_goods_reward_modify',info=info,reward=reward_info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/goods/reward/modify')
def do_reward_modify(redis,session):
    """
    修改捕鱼奖品接口
    """
    lang = getLang()
    curTime = datetime.now()

    for reward_field in reward_fields:
        exec("%s = request.forms.get('%s','').strip()"%(reward_field,reward_field))

    check_null_fields = [
                {'fields':reward_id,'msg':'奖品ID不能为空'},
                {'fields':reward_name,'msg':'奖品名称不能为空'},
                {'fields':reward_stock,'msg':'奖品初始库存不能为空'},
                {'fields':reward_need_ticket,'msg':'奖品所需兑换卷不能为空'},
                {'fields':reward_nums,'msg':'奖品总期数不能为空'},
                {'fields':reward_now_nums,'msg':'奖品当前期数不能为空'}
    ]

    for check_field in check_null_fields:
        if not check_field['fields']:
            return {'code':1,'msg':check_field['msg']}

    log_debug('[try do_reward_modify] reward_id[%s] reward_name[%s] reward_stock[%s] reward_img_path[%s]'\
                    %(reward_id,reward_name,reward_stock,img_path))

    if img_path.startswith("mahjong/static"):#去掉头部
        ori_file_name = "mahjong/static"+img_path1
        if os.path.exists(ori_file_name):
            #删除原来的图片。
            try:
                os.remove(ori_file_name)
            except Exception,e:
                log_debug('[try do_reward_modify] delete file[%s] error reason[%s]'%(ori_file_name,e))
        #生成新的路径
        img_path = img_path[14:]

    reward_info = {
            'reward_id'            :      reward_id,
            'reward_name'          :      reward_name,
            'reward_stock'         :      reward_stock,
            'reward_img_path'      :      img_path,
            'reward_need_ticket'   :      reward_need_ticket,
            'reward_pos'           :      reward_pos,           #奖品位置
            'reward_nums'          :      reward_nums,          #奖品总期数
            'reward_now_nums'      :      reward_now_nums,      #奖品当前期数
            'reward_cost'          :      reward_cost,          #奖品成本
            'reward_type'          :      reward_type,          #奖品类型
            'reward_status'        :      0,               #奖品状态
            'reward_card_no'       :      reward_card_no if reward_card_no else '',            #奖品卡号
            'reward_card_pwd'      :      reward_card_pwd if reward_card_pwd else '',          #奖品密码
            'reward_per_stock'     :      reward_per_stock if reward_per_stock else 0,         #每期库存
            'reward_coin'          :      reward_coin if reward_coin else 0
    }

    try:
        do_modify_reward(redis,reward_info)
    except Exception,e:
        return {'code':1,'msg':'修改奖品失败错误代码:[%s]'%(e)}

    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
            'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['reward_modify']%('/goods/reward/modify',reward_name)}
    #记录日志
    writeAgentOpLog(redis,session['id'],logInfo)
    return {'code':0,'msg':'修改奖品[%s]成功!'%(reward_name),'jumpUrl':BACK_PRE+'/goods/fish/reward/list'}

@admin_app.post('/goods/reward/delete')
def do_reward_deleteCall(redis,session):
    """
    删除奖品信息接口
    :params reward_id 兑换奖品ID
    """
    fields = {
            ('reward_id','奖品ID','')
    }
    for field in fields:
        exec('%s = web_util.get_form("%s","%s","%s")'%(field[0],field[0],field[1],field[2]))

    reward_table = FISH_REWARD_TABLE%(reward_id)
    if not redis.exists(reward_table):
        return web_util.do_response(1,'商品不存在.')

    reward_status = convert_util.to_int(redis.hget(reward_table,'reward_status'))
    if reward_status == REWARD_ONLINE:
        return web_util.do_response(1,'不能删除已上架的商品.')

    try:
        do_reward_delete(redis,reward_id)
    except Exception,e:
        log_util.error('[do_reward_delete] reward_id[%s] delete error.reason[%s]'%(reward_id,e))
        return web_util.do_response(1,msg="删除奖品失败!")

    return web_util.do_response(0,msg="删除奖品成功",jumpUrl=BACK_PRE+'/goods/fish/reward/list')

@admin_app.post('/goods/reward/upload')
def do_file_upload(redis,session):
    '''
    奖品图片上传接口
    @params:
    '''
    files = request.files.get('files')
    try:
        file_name,file_ext = files.filename.split('.')
    except:
        return json.dumps({'error':'文件名称不符合规范,请不要包含特殊字符!'})
    #文件新名称
    new_file_name = file_name+md5.new(str(file_name)+str(time.time())).hexdigest()+"."+file_ext
    #文件上传路劲
    file_save_path = FILES_REWARD_UPLOAD_PATH+"/"+new_file_name
    log_util.debug('[try do_file_upload] file_name[%s] file_path[%s]'%(new_file_name,file_save_path))
    #保存文件
    if not os.path.exists(FILES_REWARD_UPLOAD_PATH):
        os.mkdir(FILES_REWARD_UPLOAD_PATH,0755)
    files.save(file_save_path)

    return json.dumps({'path':file_save_path})

@admin_app.post('/goods/reward/auto_charge')
def do_auto_charge(redis,session):
    """
    开启关闭自动续期接口
    """
    curTime = datetime.now()
    fields = ('reward_id',)
    for field in fields:
        exec("%s=request.forms.get('%s','').strip()"%(field,field))

    if not reward_id:
        return {'code':1,'msg':'参数错误'}

    checkDesc = {
             1      :     '关闭奖品ID为[%s]的自动续期成功',
             0      :     '开启奖品ID为[%s]的自动续期成功'
    }

    reward_table = FISH_REWARD_TABLE%(reward_id)
    reward_auto_charge = redis.hget(reward_table,'reward_auto_charge')
    if not reward_auto_charge:
        reward_auto_charge = 0
    reward_auto_charge = int(reward_auto_charge)

    pipe = redis.pipeline()
    auto_charge_set = redis.smembers(FISH_REWARD_AUTO_CHARGE)
    if reward_auto_charge == 1:
        if reward_id in auto_charge_set:
            pipe.srem(FISH_REWARD_AUTO_CHARGE,reward_id)
        pipe.hset(reward_table,'reward_auto_charge',0)
    else:
        pipe.hset(reward_table,'reward_auto_charge',1)
        pipe.sadd(FISH_REWARD_AUTO_CHARGE,reward_id)

    pipe.execute()
    return {'code':0,'msg':checkDesc[reward_auto_charge]%(reward_id),'jumpUrl':BACK_PRE+'/goods/fish/reward/list'}

@admin_app.post('/goods/reward/status')
def do_auto_charge(redis,session):
    """
    奖品上架接口
    """
    curTime = datetime.now()
    fields = ('reward_id',)
    for field in fields:
        exec("%s=request.forms.get('%s','').strip()"%(field,field))

    if not reward_id:
        return {'code':1,'msg':'参数错误'}

    checkDesc = {
             1      :     '奖品ID为[%s]的商品下架成功',
             0      :     '奖品ID为[%s]的商品上架成功'
    }

    reward_table = FISH_REWARD_TABLE%(reward_id)
    reward_status,reward_now_nums,reward_nums,reward_type = redis.hmget(reward_table,('reward_status','reward_now_nums','reward_nums','reward_type'))
    reward_status = convert_util.to_int(reward_status)
    reward_now_nums = convert_util.to_int(reward_now_nums)
    reward_nums = convert_util.to_int(reward_nums)


    pipe = redis.pipeline()
    #auto_charge_set = redis.smembers(FISH_REWARD_AUTO_CHARGE)
    if reward_status == 1:
        pipe.hset(reward_table,'reward_status',0)
        pipe.lrem(FISH_REWARD_ON_SHOP_LIST,reward_id)
        pipe.lrem(FISH_REWARD_ON_SHOP_TYPE_LIST%(reward_type),reward_id)
    else:
        if reward_now_nums > reward_nums:
            return web_util.do_response(1,'该奖品期数已过期,不能上架!')
        pipe.hset(reward_table,'reward_status',1)
        pipe.lpush(FISH_REWARD_ON_SHOP_LIST,reward_id)
        pipe.lpush(FISH_REWARD_ON_SHOP_TYPE_LIST%(reward_type),reward_id)

    #更新版本号
    pipe.hincrby(FISH_CONSTS_CONFIG,'exchange_shop_ver',1)
    pipe.execute()
    return {'code':0,'msg':checkDesc[reward_status]%(reward_id),'jumpUrl':BACK_PRE+'/goods/fish/reward/list'}


@admin_app.get('/goods/reward/exchange/list')
def get_reward_exchange_list(redis,session):
    """
    奖品兑换记录接口
    """
    lang = getLang()
    fields = ('isList','start_date','end_date','user_id','sort_name','sort_method','pageSize','pageNumber')
    for field in fields:
        log_debug('%s = request.GET.get("%s",'').strip()'%(field,field))
        exec('%s = request.GET.get("%s","").strip()'%(field,field))

    log_util.debug('[try get_reward_exchange_list] isList[%s] start_date[%s] end_date[%s] user_id[%s] sort_name[%s] sort_method[%s]'\
                %(isList,start_date,end_date,user_id,sort_name,sort_method))

    if sort_method == 'asc':
        sort_method = True
    if sort_method == 'desc':
        sort_method = False

    if isList:
        exchange_infos = get_exchange_infos(redis,start_date,end_date,user_id,sort_name,sort_method,pageSize,pageNumber)
        return json.dumps(exchange_infos)
    else:
        info = {
                'title'     :       '奖品兑换记录',
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'tableUrl'               :       BACK_PRE+'/goods/reward/exchange/list?isList=1&sort_name=exchange_reward_status&sort_method=asc',
                'searchTxt'              :       '请输入玩家编号',
                'batch_url'              :       BACK_PRE+'/goods/reward/exchange/status',
                'submitUrl'              :       BACK_PRE+'/goods/reward/modify',
                'upload_url'             :       BACK_PRE+'/goods/reward/upload'
        }
        return template('admin_goods_reward_exchange',info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/goods/reward/exchange/status')
@checkLogin
def do_auto_charge(redis,session):
    """
    奖品发货状态变更接口
    """
    curTime = datetime.now()
    fields = ('exchange_id','exchangeIds')
    for field in fields:
        exec("%s=request.forms.get('%s','').strip()"%(field,field))

    if exchangeIds:
        """ 批量发货设置 """
        batch_ids = exchangeIds.split(',')
        pipe = redis.pipeline()
        for batch_id in batch_ids:
            exchange_table = FISH_EXCHANGE_TABLE%(batch_id)
            exchange_info = eval(redis.get(exchange_table))
            exchange_info['exchange_reward_status'] = convert_util.to_int(exchange_info['exchange_reward_status'])
            if exchange_info['exchange_reward_status'] == 0:
                exchange_info['exchange_reward_status'] = 1
                pipe.set(exchange_table,exchange_info)
            else:
                pass
        pipe.execute()
        return {'code':0,'msg':'批量发货成功,请注意商品状态!','jumpUrl':BACK_PRE+'/goods/reward/exchange/list'}
    else:
        """ 单个商品发货 """
        if not exchange_id:
            return {'code':1,'msg':'参数错误'}

        exchange_table = FISH_EXCHANGE_TABLE%(exchange_id)
        exchange_info = eval(redis.get(exchange_table))

        exchange_info['exchange_reward_status'] = convert_util.to_int(exchange_info['exchange_reward_status'])
        log_debug('[exchange_info][%s]'%(exchange_info))
        pipe = redis.pipeline()
        #auto_charge_set = redis.smembers(FISH_REWARD_AUTO_CHARGE)
        if exchange_info['exchange_reward_status'] == 0:
            exchange_info['exchange_reward_status'] = 1
            pipe.set(exchange_table,exchange_info)
        else:
            return {'code':1,'msg':'该奖品已经发货'}
            #pipe.lrem(FISH_REWARD_ON_SHOP_LIST,exchange_id)

        pipe.execute()
        return {'code':0,'msg':'兑换ID为[%s]的商品发货状态更改成功'%(exchange_id),'jumpUrl':BACK_PRE+'/goods/reward/exchange/list'}

@admin_app.get('/goods/create')
@admin_app.get('/goods/create/<action>')
@checkLogin
def getGoodsCreate(redis,session,action='hall'):
    """
    创建商品视图
    """
    lang = getLang()
    action = action.upper()

    action_2_type = {
            'HALL'      :   '0',
            'FISH'      :   '1'
    }

    info = {
            'title'             :       lang.GOODS_CREATE_TXT,
            'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
            'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
            'back_pre'          :       BACK_PRE,
            'backUrl'           :       BACK_PRE+'/goods/list?sys={}'.format(action),
            'submitUrl'         :       BACK_PRE+'/goods/create/{}'.format(action),
    }

    return template('admin_good_create',system=action,goods_type=action_2_type[action],info=info,lang=lang,RES_VERSION=RES_VERSION)

@admin_app.post('/goods/create')
@admin_app.post('/goods/create/<action>')
@checkLogin
def do_goodsCreate(redis,session,action="hall"):
    """
    创建商品控制器
    """
    curTime = datetime.now()
    lang    = getLang()
    action = action.upper()

    fields = ('name', 'note', 'cards','present_cards','price','goods_type', 'attribute', 'goods')
    for field in fields:
        exec("%s = request.forms.get('%s','').strip()"%(field,field))

    if goods:
        cards = goods
    checkNullFields = [
        {'field':name,'msg':lang.GOODS_NOT_EMPTY_TXT},
        {'field':cards,'msg':lang.GOODS_CARD_NOT_EMPTY_TXT},
        {'field':price,'msg':lang.GOODS_PRICE_NOT_EMPTY}
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    try:
        argv = map(int, [cards, present_cards, price])
    except Exception as err:
        return {'code': 1, 'msg': '请输入正确的参数'}

    #print
    log_util.debug('[try do_goodsCreate]name[%s] cards[%s] present_cards[%s] price[%s]'\
                    %(name,cards,present_cards,price))

    goodsInfo = {

            'name'          :       name,
            'note'          :       note, # 商品介绍
            'type'          :       goods_type, # 0-钻石 1-金币
            'cards'         :       cards,
            'present_cards' :       present_cards,
            'price'         :       price,
            'attribute'     :       attribute,
    }
    try:
        do_create_goods(redis,goodsInfo)
    except:
        return {'code':1,'msg':lang.GOODS_CREATE_ERROR_TXT%(name)}

    return {'code':0,'msg':lang.GOODS_CREATE_SUCCESS_TXT%(name),'jumpUrl':BACK_PRE+'/goods/list?sys={}'.format(action)}

@admin_app.get('/goods/modify')
@admin_app.get('/goods/modify/<action>')
@admin_app.get('/goods/info/<good_id:int>')
@checkLogin
def getGoodsModify(redis,session,action='hall',good_id=None):
    """
    商品信息修改接口
    """
    goodsId = request.GET.get('goodsId','').strip()
    curTime = datetime.now()
    lang    = getLang()
    action = action.upper()

    action_2_type = {
            'HALL'   :   '0',
            'FISH'   :   '1'
    }

    if good_id:
        """ 通过接口获取数据 """
        goods_info = get_goods_info(redis,good_id)
        goods_info['goodsType'] = {'0': '钻石', '2': '金币场金币', '4': '其他'}[goods_info['type']]
        return {'goods_info':goods_info}
    else:
        """ 模板渲染 """
        info = {
                    'title'     :       lang.GOODS_MODIFY_TXT % (goodsId),
                    'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                    'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                    'back_pre'          :       BACK_PRE,
                    'backUrl'           :       BACK_PRE+'/goods/list/{}'.format(action),
                    'submitUrl'         :       BACK_PRE+'/goods/modify/{}'.format(action),
                    'api_url'           :       BACK_PRE+'/goods/info',
                    'type'              :       redis.hget(GOODS_TABLE%(goodsId), 'type')
        }
        return template('admin_good_modify',system=action,info=info,lang=lang,goodsId=goodsId,RES_VERSION=RES_VERSION)

@admin_app.post('/goods/modify')
@admin_app.post('/goods/modify/<action>')
@checkLogin
def do_goodsModify(redis,session,action="hall"):
    """
    商品信息修改控制器
    """
    action  = action.upper()
    curTime = datetime.now()
    lang    = getLang()

    fields = ('goodsId','note', 'name','cards','goods_type','present_cards','price',  'attribute')
    for field in fields:
        exec('%s = request.forms.get("%s","").strip()'%(field,field))

    checkNullFields = [
        {'field':name,'msg':lang.GOODS_NOT_EMPTY_TXT},
        {'field':cards,'msg':lang.GOODS_CARD_NOT_EMPTY_TXT},
        {'field':price,'msg':lang.GOODS_PRICE_NOT_EMPTY}
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    #print
    log_util.debug('[try goodsModify] name[%s] cards[%s] present_cards[%s] price[%s]'\
                    %(name,cards,present_cards,price))

    goodsInfo = {

            'name'          :       name,
            'note'          :       note,
            'cards'         :       cards,
            'type'          :       goods_type,
            'present_cards' :       present_cards,
            'price'         :       price,
            'attribute'     :       attribute,
    }
    try:

        do_goods_modify(redis,goodsId,goodsInfo)
        logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['goodsModify']%('/goods/modify',goodsId)}
        #记录日志
        writeAgentOpLog(redis,session['id'],logInfo)
    except:
        return {'code':1,'msg':lang.GOODS_MODIFY_ERROR_TXT%(name)}

    return {'code':0,'msg':lang.GOODS_MODIFY_SUCCESS_TXT%(name),'jumpUrl':BACK_PRE+'/goods/list?sys={}'.format(action)}

@admin_app.post('/goods/del')
@admin_app.post('/goods/del/<action>')
@checkLogin
def do_goodsModify(redis,session,action='hall'):
    """
    删除商品接口
    """
    action = action.upper()
    curTime = datetime.now()
    lang    = getLang()

    goodsId  =  request.forms.get('id','').strip()

    checkNullFields = [
        {'field':goodsId,'msg':'商品ID不存在'},
    ]

    for check in checkNullFields:
        if not check['field']:
            return {'code':1,'msg':check['msg']}

    pipe = redis.pipeline()
    try:
        pipe.lrem(GOODS_TYPE_LIST%('0'),goodsId)
        pipe.lrem(GOODS_TYPE_LIST%('2'), goodsId)
        pipe.lrem(GOODS_TYPE_LIST%('1'),goodsId)
        pipe.lrem(GOODS_LIST,goodsId)
        pipe.delete(GOODS_TABLE%(goodsId))
    except Exception,e:
        log_util.debug('[try do_goodsModify] delete goods[%s] faield. reason[%s]'%(goodsId,e))
        return {'code':1,'msg':'删除商品失败'}

    logInfo = {'datetime':curTime.strftime('%Y-%m-%d %H:%M:%S'),\
                'ip':request.remote_addr,'desc':lang.AGENT_OP_LOG_TYPE['goodsDel']%(goodsId)}
    #记录日志
    writeAgentOpLog(redis,session['id'],logInfo)
    pipe.execute()
    return {'code':0,'msg':'删除商品成功','jumpUrl':BACK_PRE+'/goods/list?sys={}'.format(action)}

@admin_app.get('/goods/setting')
@checkLogin
def getGoodsSetting(redis,session):
    """
    获取商品价格设置
    """
    curTime  =  datetime.now()
    lang     =  getLang()

    goodsPrice = getGoodsPrice(redis)

    info = {
                'title'                  :       lang.GOODS_SETTING_TXT,
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'back_pre'          :       BACK_PRE,
                'backUrl'           :       BACK_PRE+'/goods/setting',
                'createUrl'         :       BACK_PRE+'/goods/setting'
    }

    return template('admin_good_setting',info=info,lang=lang,goodsPrice=goodsPrice,RES_VERSION=RES_VERSION)

@admin_app.post('/goods/setting')
def do_GoodsSetting(redis,session):
    """
    设置商品价格
    """
    curTime = datetime.now()
    lang    = getLang()

    goodsPrice = request.forms.get('goodsPrice','').strip()

    if not goodsPrice:
        return {'code':1,'msg':lang.GOODS_PRICE_NOT_EMPTY}

    #print
    print '[%s][goods setting][info] goodsPrice[%s]'%(curTime,goodsPrice)

    info = {
                'title'                  :       lang.GOODS_SETTING_TXT,
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'back_pre'          :       BACK_PRE,
                'backUrl'           :       BACK_PRE+'/goods/setting',
                'createUrl'         :       BACK_PRE+'/goods/setting'
    }

    if setGoodsPrice(redis,goodsPrice):
        return {'code':0,'msg':lang.GOODS_PRICE_SETTING_TXT%(goodsPrice),'jumpUrl':BACK_PRE+"/goods/setting"}

    return {'code':1,'msg':lang.GOODS_SETTING_TXT_ERROR}

@admin_app.get('/shopmall/cocogc')
def getGoodList(redis,session):
    """
    商品列表视图
    """
    curTime = datetime.now()
    lang = getLang()
    islist = request.GET.get('isList', '').strip()

    if islist:
        res = 1
        res = get_goods_list(redis,goods_type='0',action='hall')
        return json.dumps(res)
    else:
        info = {
                'title'         :     lang.MENU_SHOPMALL_COCOGC_TXT,
                'addTitle'      :     '创建新兑换',
                'STATIC_LAYUI_PATH'      :       STATIC_LAYUI_PATH,
                'STATIC_ADMIN_PATH'      :       STATIC_ADMIN_PATH,
                'tableUrl'      :     BACK_PRE+'/goods/list/{}?isList=1',
                'submitUrl': BACK_PRE + '/shopmall/cocogc/create/{}',
        }
        info['createUrl']   = BACK_PRE+'/shopmall/cocogc/create'
        return template('admin_shop_cocogc_list',system=sys,info=info,lang=lang,RES_VERSION=RES_VERSION)


@admin_app.get('/shopmall/cocogc/create')
def getShopCocogcCreate(redis, session):
    """
    创建商品视图
    """
    lang = getLang()
    curTime = datetime.now()

    info = {
        'title': '创建椰云兑换',
        'STATIC_LAYUI_PATH': STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH': STATIC_ADMIN_PATH,
        'back_pre': BACK_PRE,
        'backUrl': BACK_PRE + '/shopmall/cocogc/list?sys={}',
        'submitUrl': BACK_PRE + '/shopmall/cocogc/create/{}'
    }

    return template('admin_shop_cocogc_create',  info=info, lang=lang, RES_VERSION=RES_VERSION)