# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description:
    邮件工具函数
"""

import smtplib
from email.mime.text import MIMEText
from traceback import format_exc
from config import config

#初始化邮件参数
smtp = config.SMTP
port = config.SMTP_PORT
user = config.EMAIL_USER
passwd = config.EMAIL_PWD
email_list = config.EMAIL_LIST
err_title = config.EMAIL_ERR_TITLE

def send_email(subject,context,to_list):
    '''
    发送邮件
    接收参数
    subject 邮件主题
    context 邮件内容
    to_list 接收者邮件列表，每个邮箱地址用,分割
    '''
    if not subject or not context or not to_list:
        return '发送邮件失败,邮件主题,邮件内容,邮件接收人都是必填项'

    #初始化邮件相关参数
    email = MIMEText(context,'html','utf-8')
    email['To'] = to_list
    email['Subject'] = subject
    email['From'] = user

    #qq邮箱改为ssl发送
    s = smtplib.SMTP_SSL(smtp)
    try:
        s.login(user,passwd)
        s.sendmail(user,email_list,email.as_string())
        s.closr()
    except Exception,e:
        s.close()
        stacktrace = format_exc()
        return '邮件内容发送失败,出现异常' + str(e.args) + stacktrace + '\n'


def send_error_mail(context):
    '''
    发送错误邮件
    接收参数
    context 邮件内容
    '''
    if not context:
        return '邮件内容不能为空'

    send_email(err_title,context,email_list)

import unittest
from except_util import *

class MailUtilTest(unittest.TestCase):
    """邮件操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        send_mail('test', 'test', '514303208@qq.com')
        except_info = except_util.detail_trace()
        mail_helper.send_error_mail('出现异常，堆栈信息：' + except_info)

if __name__ == '__main__':
    unittest.main()
