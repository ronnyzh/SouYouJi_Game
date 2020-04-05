#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
创建省级代理
'''

import requests

'''-----配置区(开始)-----'''
# 服务器地址
Url = 'http://127.0.0.1:9798'
# 代理登录账户名
account = 'winslen'
passwd = '123456'
# 当前代理(省级Id)的代理id,不设置则随机生成
agentId = '111111'
# 新用户默认钻石数(个)
defaultRoomCard = 0
'''-----配置区(结束)-----'''


def do():
    r = requests.post('%s/admin/agent/create/1' % (Url), data={
        'parentAg:': 1,
        'agentId': agentId,
        'account': account,
        'passwd': passwd,
        'comfirPasswd': passwd,
        # 钻石单价:
        'unitPrice': 1,
        # 当前代理占额(元):
        'shareRate': 1,
        'defaultRoomCard': defaultRoomCard,
    })
    if r.status_code != 200:
        print('----访问失败----')
        print(r.text)
    else:
        print('----访问成功----')
        print('----请根据以下信息判断是否创建成功!----')
        data = r.json()
        for _key, _val in data.iteritems():
            print('%s => %s' % (_key, _val))


if __name__ == '__main__':
    do()
