# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/12/6
Revision: 1.0.0
Description: Description
"""
'''mysql数据补存脚本'''
from model.model_asyn_mysql import *
import asyncio

mysql_configs = {
    "host": "112.74.45.160",
    "port": 3306,
    "user": "winslen",
    "password": "AAbb@1212",
    "db": "game_db",
}


async def test():
    mysql_db = Async_Mysql(mysql_configs)
    await mysql_db.createPool_async()
    result = await mysql_db.update(
        '''UPDATE match_record SET `match_number` = %(value_2)s , `total_award_num` = %(value_3)s , `end_time` = %(value_4)s , `dismissReason` = %(value_5)s , `balance_datas` = %(value_6)s , `total_award_type` = %(value_7)s , `matchState` = %(value_8)s , `update_time` = %(value_9)s , `fee_type` = %(value_10)s WHERE `match_number` = %(value_1)s''',
        args={'value_9': 1575595910, 'value_8': 10, 'value_5': '', 'value_4': 1575595910, 'value_7': 3, 'value_6': '{\\"1\\": {\\"702-2-1575595392423-1-464983\\": {\\"ghostTile\\": null, \\"players\\": {\\"0\\": {\\"isHu\\": false, \\"account\\": \\"hHfiv121\\", \\"score\\": 0, \\"uid\\": 121, \\"descs\\": \\"\\", \\"isDealer\\": true, \\"chair\\": 0, \\"b_tiles\\": [\\"3;b7,b7,b7\\", \\"a2,b1,b1,b2,b2,b2,b5,b5,b6,b9\\", \\"\\"], \\"nickname\\": \\"\\u9648\\u5c0f\\u6021\\", \\"tiles\\": [\\"a2\\", \\"b1\\", \\"b1\\", \\"b2\\", \\"b2\\", \\"b2\\", \\"b5\\", \\"b5\\", \\"b6\\", \\"b9\\"]}, \\"1\\": {\\"isHu\\": false, \\"account\\": \\"BtRDU117\\", \\"score\\": 0, \\"uid\\": 117, \\"descs\\": \\"\\", \\"isDealer\\": false, \\"chair\\": 1, \\"b_tiles\\": [\\"a1,a1,a4,a5,a5,a5,a7,a8,a9,c2,c4,c4,c9\\", \\"\\"], \\"nickname\\": \\"C\\u3002\\", \\"tiles\\": [\\"a1\\", \\"a1\\", \\"a4\\", \\"a5\\", \\"a5\\", \\"a5\\", \\"a7\\", \\"a8\\", \\"a9\\", \\"c2\\", \\"c4\\", \\"c4\\", \\"c9\\"]}, \\"2\\": {\\"isHu\\": false, \\"account\\": \\"MUixJ119\\", \\"score\\": -4, \\"uid\\": 119, \\"descs\\": \\"\\u653e\\u70aeX2\\", \\"isDealer\\": false, \\"chair\\": 2, \\"b_tiles\\": [\\"3;a2,a2,a2\\", \\"3;a6,a6,a6\\", \\"3;a4,a4,a4\\", \\"a3,a7,a8,b9\\", \\"\\"], \\"nickname\\": \\"\\u641c\\u96c6\\u6e38\\", \\"tiles\\": [\\"a3\\", \\"a7\\", \\"a8\\", \\"b9\\"]}, \\"3\\": {\\"isHu\\": true, \\"account\\": \\"ZmKPQ114\\", \\"score\\": 4, \\"uid\\": 114, \\"descs\\": \\"\\u63a5\\u70aeX2,\\u95e8\\u6e05X2\\", \\"isDealer\\": false, \\"chair\\": 3, \\"b_tiles\\": [\\"a7,a7,b3,b3,b4,b4,b5,b6,b6,b6,b7,b8,b9,b5\\", \\"\\"], \\"nickname\\": \\"\\u732b\\u5357\\u5317\\ud83d\\udca4\\", \\"tiles\\": [\\"a7\\", \\"a7\\", \\"b3\\", \\"b3\\", \\"b4\\", \\"b4\\", \\"b5\\", \\"b6\\", \\"b6\\", \\"b6\\", \\"b7\\", \\"b8\\", \\"b9\\"]}}, \\"endTime\\": 1575595613406, \\"startTime\\": 1575595412994, \\"gameNumber\\": \\"702-2-1575595392423-1-464983\\"}}, \\"2\\": {\\"702-2-1575595392423-2-282867\\": {\\"ghostTile\\": null, \\"players\\": {\\"0\\": {\\"isHu\\": false, \\"account\\": \\"hHfiv121\\", \\"score\\": -2, \\"uid\\": 121, \\"descs\\": \\"\\u653e\\u70ae\\", \\"isDealer\\": true, \\"chair\\": 0, \\"b_tiles\\": [\\"a1,a2,a4,a5,a7,a8,a9,a9,b3,b5,b5,b6,b9\\", \\"\\"], \\"nickname\\": \\"\\u9648\\u5c0f\\u6021\\", \\"tiles\\": [\\"a1\\", \\"a2\\", \\"a4\\", \\"a5\\", \\"a7\\", \\"a8\\", \\"a9\\", \\"a9\\", \\"b3\\", \\"b5\\", \\"b5\\", \\"b6\\", \\"b9\\"]}, \\"1\\": {\\"isHu\\": true, \\"account\\": \\"MUixJ119\\", \\"score\\": -1, \\"uid\\": 119, \\"descs\\": \\"\\u5e73\\u80e1,\\u63a5\\u70ae,\\u653e\\u70ae\\", \\"isDealer\\": false, \\"chair\\": 1, \\"b_tiles\\": [\\"3;b7,b7,b7\\", \\"2;a2,a2,a2\\", \\"a6,a7,a8,a9,a9,b3,b3,b3\\", \\"\\"], \\"nickname\\": \\"\\u641c\\u96c6\\u6e38\\", \\"tiles\\": [\\"a6\\", \\"a7\\", \\"a8\\", \\"a9\\", \\"a9\\", \\"b3\\", \\"b3\\"]}, \\"2\\": {\\"isHu\\": true, \\"account\\": \\"ZmKPQ114\\", \\"score\\": 4, \\"uid\\": 114, \\"descs\\": \\"\\u63a5\\u70aeX2,\\u4e2d\\u5f20X2\\", \\"isDealer\\": false, \\"chair\\": 2, \\"b_tiles\\": [\\"3;b2,b2,b2\\", \\"a5,a6,a7,a8,b6,b6,b6,b8,b8,b8,a5\\", \\"\\"], \\"nickname\\": \\"\\u732b\\u5357\\u5317\\ud83d\\udca4\\", \\"tiles\\": [\\"a5\\", \\"a6\\", \\"a7\\", \\"a8\\", \\"b6\\", \\"b6\\", \\"b6\\", \\"b8\\", \\"b8\\", \\"b8\\"]}, \\"3\\": {\\"isHu\\": false, \\"account\\": \\"BtRDU117\\", \\"score\\": -1, \\"uid\\": 117, \\"descs\\": \\"\\u653e\\u70ae\\", \\"isDealer\\": false, \\"chair\\": 3, \\"b_tiles\\": [\\"2;b1,b1,b1,b1\\", \\"a3,a4,a6,a7,b4,b5,b5,b8,b9,b9\\", \\"\\"], \\"nickname\\": \\"C\\u3002\\", \\"tiles\\": [\\"a3\\", \\"a4\\", \\"a6\\", \\"a7\\", \\"b4\\", \\"b5\\", \\"b5\\", \\"b8\\", \\"b9\\", \\"b9\\"]}}, \\"endTime\\": 1575595895005, \\"startTime\\": 1575595648794, \\"gameNumber\\": \\"702-2-1575595392423-2-282867\\"}}}', 'value_1': '702-2-1575595392423', 'value_3': 4, 'value_2': '702-2-1575595392423', 'value_10': 1}

    )
    print(result)


asyncio.get_event_loop().run_until_complete(test())
