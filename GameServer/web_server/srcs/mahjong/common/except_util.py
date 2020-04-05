# -*- coding:utf-8 -*-
#!/bin/python

"""
Author: $Author$
Date: $Date$
Revision: $Revision$

Description:
    异常工具函数
"""

import os
import sys

def detail_trace():
    """ 打印当前堆栈信息 """
    res_str = ""
    f = sys._getframe()
    f = f.f_back

    while hasattr(f,"f_code"):
        co = f.f_code
        res_str = "%s(%s:%s) ->"%(os.path.basename(co.co_filename),co.co_name,f.f_lineno)+res_str
        f = f.f_back

    return res_str


if __name__ == '__main__':
    print detail_trace()
