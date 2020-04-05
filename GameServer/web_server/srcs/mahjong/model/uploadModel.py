#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    上传工具模型
"""
from web_db_define import *
from admin  import access_module
from config.config import *
from datetime import datetime,timedelta
import random


class uploadFile(object):
    """
    上传工具模型
    """
    def __init__(self,filename,savePath):
        self._fileObj  = filename
        self._savePath = savePath
        self._fileName,self._fileExt = self._fileObj.split('.')

        if not self.check(self.fileExt):
            return False
            
        self.save()

    def save(self):
        """
        """
        self._fileObj.save(self.savePath,overwrite=True)

    def check(self):
        """
        """
        if self._fileExt not in FILES_ALLOW_EXTS:
            return False

        return True