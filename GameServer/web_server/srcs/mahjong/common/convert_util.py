# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description:
    转换工具集合
"""

import decimal
import datetime
from datetime import timedelta

#######################
# 转换功能函数
#######################

def to_int(value):
    """ 将字符串安全转换为整形 """
    try:
        return int(value)
    except:
        return 0

def to_int0(value):
    """ 将字符串安全转换为0，小与0则返回0 """

    result = to_int(value)

    if not result or result < 0 :
        return 1
    else:
        return result

def to_float(value):
    """ 将字符串安全转换为float类型 """
    try:
        return float(value)
    except:
        return 0.0

def to_decimal(value):
    """ 将字符串安全转换为 int类型 """
    try:
        return decimal.Decimal(value)
    except:
        return 0

def to_dateStr(value,format_str="%Y-%m-%d"):
    """ 将日期转换为字符串 """
    try:
        return value.strftime(format_str)
    except:
        return None

def to_week_list(start_date,end_date):
    '''
    返回一段时间的对象列表
    '''
    startDate = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    endDate   = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    date_list = []
    one_del_time = timedelta(1)
    while startDate<=endDate:
        dateStr = datetime.datetime.strftime(startDate,'%Y-%m-%d')
        date_list.append(dateStr)

        startDate+=one_del_time

    return date_list

#############################################
# 日期转换函数
#############################################

def to_datetime(value):
    """  字符串转换为时间 """
    if not value:
        return None

    time_dict = {
        1   :   '%Y-%m-%d %H:%M:%S',
        2   :   '%Y-%m-%d %H:%M',
        3   :   '%Y-%m-%d'
    }

    try:
        if str(value).find('.') > -1:
            return datetime.datetime.strptime(value,time_dict[1])
        elif ':' in value:
            time_list = value.split(':')
            return datetime.datetime.strptime(value,time_dict[len(time_list)])
        else:
            return datetime.datetime.strptime(value,time_dict[3])
    except:
        return None

def to_date(value):
    """ 字符串转换为日期 """
    d = to_datetime(value)
    if d:
        return d.date()

def to_timestamp10(value):
    """ 将时间格式的字符串转换为长度为10位的时间戳 """
    d = to_datetime(value)
    if d:
        return int(d.timestamp()*1000)
    else:
        return 0
