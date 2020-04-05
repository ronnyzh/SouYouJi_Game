#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    this is Description
"""

from bottle import response,request
import inspect
from web_db_define import *
from wechat.wechatData import *
from common.install_plugin import *
from datetime import datetime,timedelta
from config.config import *
from common.log import *
from common import log_util,convert_util
from model.agentModel import *
import time
import uuid
import xml.dom.minidom
import md5
import hashlib
import urllib2
import urllib
import socket
import redis

def pbAppendRank(rankList, rank, nickname, headImgUrl, score, level=None):
    _rankInfo = {}
    _rankInfo['rank'] = rank
    _rankInfo['nickname'] = nickname
    _rankInfo['headImgUrl'] = headImgUrl
    _rankInfo['score'] = score
    if level is not None:
        _rankInfo['level'] = level
    rankList.append(_rankInfo)
    return rankList

