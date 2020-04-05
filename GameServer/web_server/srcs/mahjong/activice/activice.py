#-*- coding:utf-8 -*-
#!/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    后台activice应用入口
"""

from bottle import Bottle
from common.install_plugin import install_redis_plugin,install_session_plugin

activice_app = Bottle()

install_redis_plugin(activice_app)
install_session_plugin(activice_app)


