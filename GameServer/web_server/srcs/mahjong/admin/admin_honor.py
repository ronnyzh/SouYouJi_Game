# coding:utf-8
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    金币场
"""
from bottle import *
from admin import admin_app
from config.config import STATIC_LAYUI_PATH, STATIC_ADMIN_PATH, BACK_PRE, RES_VERSION
from common.utilt import *
from common.log import *
from datetime import datetime
from web_db_define import *
from access_module import *
from common import encrypt_util, convert_util, json_util, web_util

import hashlib
import json

@admin_app.get('/honor/getAPI1')
@checkAccess
def getAPI1(redis, session):
    lang = getLang()

    info  =  {
        "title"                  :   '荣誉场接口',
        'STATIC_LAYUI_PATH'      :   STATIC_LAYUI_PATH,
        'STATIC_ADMIN_PATH'      :   STATIC_ADMIN_PATH
    }
    return template('admin_honor_api1', info=info, lang=lang, RES_VERSION=RES_VERSION)