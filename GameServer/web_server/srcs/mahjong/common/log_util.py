# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description:
    日志工具函数
"""

import logging
import logging.handlers
import traceback

from common import mail_util,except_util

def info(content):
    """ 记录日志信息 """
    if content:
        logging.info(content)

def debug(content):
    """ 调试日志信息 """
    if content:
        logging.debug(content)

def error(content,is_send_mail = False):
    """ 记录错误日志信息 """
    if content:
        content = content + "\n" + traceback.format_exc()+"\n"

    #获取程序当前的堆栈信息
    detail_trace = except_util.detail_trace()
    content = content + "progress take log" + detail_trace + "\n"

    logging.error(content)
    if is_send_mail:
        info = mail_util.send_error_mail(context=content)
        logging.error(info)
