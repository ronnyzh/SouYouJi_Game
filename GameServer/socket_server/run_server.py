# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/25
Revision: 1.0.0
Description: Description
"""
from server.factorys import matchFactory

from tornado import options

options.define('address', default='192.168.50.2', type=str)
options.define('port', default=9797, type=int)
options.define('checkDoMysqlJob', default=True, type=bool)
options.define('zipLogs', default=True, type=bool)
options.parse_command_line()

if __name__ == '__main__':
    server = matchFactory.MatchFactory(address=options.options.address, port=options.options.port)
    server.run_server()
