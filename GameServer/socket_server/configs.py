# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
import pymysql

CONFIGS = {
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'dbNum': 1,
    },
    'mysql': {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "game_db",
        "maxConnections": 55,
        "minFreeConnections": 11,
    },
    'async_mysql': {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "root",
        "db": "game_db",
        "init_command": 'select count(*) from match_record',
    }
}
