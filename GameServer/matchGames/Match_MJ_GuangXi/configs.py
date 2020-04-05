# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/26
Revision: 1.0.0
Description: Description
"""
CONFIGS = {
    'redis': {
        'host': "127.0.0.1",
        'port': 6379,
        'db': 1,
        'password': '',
    },
    'mysql': {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "root",
        "db": "game_db",
        'charset': 'utf8',
        "init_command": 'select count(*) from match_record',
        'cp_min': 3,
        'cp_max': 5,
    }
}
