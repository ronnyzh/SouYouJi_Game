#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
创建市级代理
'''

import requests

'''-----配置区(开始)-----'''
# 服务器地址
Url = 'http://127.0.0.1:9798'
# 省级Id
parentAg = '111111'
# 代理登录账户名
account = 'winslen0'
passwd = '123456'
# 当前代理的代理id,不设置则随机生成
agentId = '000000'
'''-----配置区(结束)-----'''


def do():
    r = requests.post('%s/admin/agent/create/%s' % (Url, parentAg), data={
        'parentAg:': parentAg,
        'agentId': agentId,
        'account': account,
        'passwd': passwd,
        'comfirPasswd': passwd,
        'myRate': 1,
        'shareRate': 1,
    })
    if r.status_code != 200:
        print(r.text)
    else:
        data = r.json()
        # print(data)
        for _key, _val in data.iteritems():
            print(_key),
            print(_val)


if __name__ == '__main__':
    do()
