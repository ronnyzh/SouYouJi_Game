#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
     server初始化
"""
from bottle import request,response,abort,hook
import bottle
from common.install_plugin import install_redis_plugin,install_session_plugin
from common import web_util,log_util
from i18n.i18n import initializeWeb
from config import config
import json
import logging
import os
import sys

class createWebServer(object):
    """ 创建server应用类 """
    def __init__(self,app):
        self.app = app
        self.check_urls = []
        self.redis_inst = None

    def _init_app(self):
        self._install_plugin()
        self._init_config()
        self._init_log()
        self._init_before()

    def _install_plugin(self):
        """ 初始化插件 """
        install_redis_plugin(self.app)
        install_session_plugin(self.app)

    def _init_config(self):
        """ 初始化配置 """
        with open(config.CONF_FILE) as f:
            self.app.config.load_dict(json.load(f))

        self.redis_inst = web_util.get_redis(1)

    def _init_log(self):
        """ 初始化日志文件 """
        #获取当前main.py文件所在服务器的绝对路径
        program_path = os.path.split(os.path.realpath(__file__))[0]
        #将路径添加的bottle变量中
        sys.path.append(program_path)
        #初始化日志目录路径
        log_path = os.path.join(program_path, 'log')
        #############################################
        # 如果日志目录log文件夹不存在，则创建日志目录
        if not os.path.exists(log_path):
            os.mkdir(log_path,0755)

        logging.basicConfig(
               level=logging.DEBUG,
               format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
               filename="%s/ds_info.log" % log_path,
               filemode='w+'
        )

    def _init_before(self):
        """ 请求前的钩子 (拦截器) """
        @hook('before_request')
        def before_request_check():
            req_path = request.path
            req_ip = web_util.get_ip()

            if req_path in self.check_urls:
                sid = request.params.sid
                log_util.debug('before req_ip[%s] request_path[%s] sid[%s] redis[%s]'%(req_ip,req_path,sid,self.redis_inst))
                # if not sid:
                #     """ 在接口请求中不携带SID的都是非法 """
                #     log_util.error('req_ip[%s] req_path[%s] sid[%s] is illg request...'%(req_ip,req_path,sid))
                #     bottle.abort(503,'Invalid Request')

                if not web_util.api_limit_checker(self.redis_inst,sid,req_ip,req_path):
                    """ 检查是否恶意访问 """
                    log_util.error('req_ip[%s] req_path[%s] sid[%s] is attack...'%(req_ip,req_path,sid))
                    bottle.abort(503,'Invalid Request')

    def set_memfile_max(self,value):
        """ 设置bottle的上传文件大小 """
        if value and isinstance(value,int):
            bottle.BaseRequest.MEMFILE_MAX = value

    def set_template_path(self,path):
        """ 添加bottle的模版路径 """
        if path:
            bottle.TEMPLATE_PATH.append(path)

    def add_check_urls(self,urls):
        """ 添加检查规则 """
        if isinstance(urls,str):
            self.check_urls.append(urls)
        elif isinstance(urls,list):
            self.check_urls.extend(urls)
        else:
            pass
