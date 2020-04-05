#-*- coding:utf-8 -*-
#!/usr/bin/env python

"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    平台入口
"""
import bottle
from create_server import createWebServer
from i18n.i18n import initializeWeb
#实例化语言包
initializeWeb()
#需要检查的url
check_urls = [
            '/hall/refresh',
            '/hall/extendSession',
            '/fish/refresh',
            '/fish/extendSession'
]
#初始化应用
ds_server = createWebServer(bottle.default_app())#bottle.default_app()
#设置bottle的最大文件上传内容
ds_server.set_memfile_max(1024*1024*2)
ds_server.set_template_path('mahjong/template/%s'%('default'))
#添加监测的URL
ds_server.add_check_urls(check_urls)
#初始化app
ds_server._init_app()

@ds_server.app.error(404)
def get_error_404(code):
    """ 返回404 """
    return 'Not Found'

@ds_server.app.error(500)
def get_error_500(code):
    """ 返回500 """
    return "Server Error"

@ds_server.app.get('/<res_path:path>')
def content_path(res_path):
    '''
     @description: 设置资源文件路径
    '''
    #支持跨域请求
    bottle.response.add_header('Conten-Type','application/octet-stream')
    return bottle.static_file(res_path,root='mahjong/static/')

if ds_server.app.config.get('download_view', 1):
    """ 是否开放下载 """
    @ds_server.app.get('/download/<res_path:path>')
    def download_path(res_path):
        '''
        @description:               是否允许下载
        '''
        return bottle.static_file(res_path,root='mahjong/static/download', download=True)


if ds_server.app.config.get('admin_view', 1):
    #是否允许访问后台
    from admin import admin_app
    ds_server.app.mount('/admin',admin_app)

if ds_server.app.config.get('bag_view',1):
    from bag import bag_app
    ds_server.app.mount('/hall/bag',bag_app)
    ds_server.app.mount('/bag',bag_app)

if ds_server.app.config.get('hall_view',1):
    from hall import hall_app
    ds_server.app.mount('/hall',hall_app)

if ds_server.app.config.get('fish_view',1):
    from fish import fish_app
    ds_server.app.mount('/fish',fish_app)

