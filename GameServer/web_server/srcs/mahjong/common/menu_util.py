# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description:
    转换工具集合
"""
import datetime


def init_menus(lang,access,menus):
    """
    初始化后台菜单
    :params access 当前用户权限
    :params menus 菜单
    :return 返回生成好的菜单
    """
    mainModules = []
    # 一级菜单定位
    i= -1
    # 二级菜单定位
    j= -1
    for accessObj in menus:
        test = {}
        test['1'] = accessObj.url

        if accessObj.check and (accessObj.url in access):
            i+=1
            # 重置二级菜单定位
            j=-1
            mainModule = {}
            mainModule['url'] = accessObj.url
            mainModule['txt'] = accessObj.getTxt(lang)
            mainModule['subModules'] = []
            mainModules.append(mainModule)

        elif len(accessObj.tree) != 2 and (accessObj.url in access):
            j+=1
            subModule = {}
            subModule['url'] = accessObj.url
            subModule['txt'] = accessObj.getTxt(lang)
            subModule['subsubModules'] = []
            if not mainModules:
                continue
            mainModules[i]['subModules'].append(subModule)
        elif len(accessObj.tree) == 2 and (accessObj.url in access):
            if not mainModules:
                continue
            if j==-1:
                subModule = {}
                subModule['url'] = accessObj.url
                subModule['txt'] = accessObj.getTxt(lang)
                subModule['subsubModules'] = []
                mainModules[i]['subModules'].append(subModule)
            else:
                subsubModule = {}
                subsubModule['url'] = accessObj.url
                subsubModule['txt'] = accessObj.getTxt(lang)
                mainModules[i]['subModules'][j]['subsubModules'].append(subsubModule)
    return mainModules
