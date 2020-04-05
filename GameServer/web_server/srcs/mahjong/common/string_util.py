# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description:
    字符串工具函数
"""

import re

STRING_CHECK_PATTER = { #常用的检查格式
    'phone'     :   '\(?0\d{2,3}[) -]?\d{7,8}$',
    'mobile'    :   '^1[3578]\d{9}$|^147\d{8}$',
    'email'     :   '[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$',
    'letter'    :   '^[a-zA-Z]+$'
}

def check_string(value,pattern):
    """
    检查字符串是否符合规则
    :params value 需要检查的字符串
    :params pattern 检查的规则
    :return 含有指定字符时返回真，否则返回假
    """
    match = re.search(pattern,value)
    if match:
        return True
    else:
        return False

def is_pattern(value,patters):
    """
    验证字符串是否是邮箱
    :params : 待验证字符串
    :patters : string phone email ...
    :return 符合返回True 否则返回False
    """
    return check_string(value,STRING_CHECK_PATTER[patter])

def filter_str(value,filter='\||<|>|&|%|~|\^|;|\''):
    """
    过滤字符串
    :params value 需要过滤的字符串
    :params filter 过滤内容（正则表达式）
    """
    if value:
        return re.subn(filter,'',value)[0]
    else:
        return ''

def filter_tag(htmlstr):
    """
    过滤html字符串标签
    :params htmlstr html内容
    """
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释

    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释

    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

def replaceCharEntity(htmlstr):
    """
    替换常用HTML字符
    :param htmlstr: 要替换的字符
    :return:
    """
    CHAR_ENTITIES={     'nbsp'  :       ' ',
                        '160'   :       ' ',
                        'lt'    :       '<',
                        '60'    :       '<',
                        'gt'    :       '>',
                        '62'    :       '>',
                        'amp'   :       '&',
                        '38'    :       '&',
                        'quot'  :       '"',
                        '34'    :       '"',
    }
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr

def format_credit(credit):
    """
    将金币格式转化为money的模式 000,000,00
    :params credit 输入的金币
    :return 格式化好的金钱格式
    """
    
    credit_str = '%.2f'%(float(credit))
    l = credit_str.split('.')
    s = ''
    _end = -len(l[0])-1
    for i in xrange(-1, _end, -1):
        char = l[0][i]
        if char.isdigit() and i % 3 == 2 and i != -1:
            s = ',' + s
        s = char + s

    return s + '.' + l[1]
