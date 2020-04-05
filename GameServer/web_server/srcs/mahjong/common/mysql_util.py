#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
@Author: $Author$
@Date: $Date$
@version: $Revision$

Description:
    mysql
"""
import time, datetime
import traceback
import pymysql
from configs import CONFIGS

DB_CONFIG = CONFIGS.get('mysql')

class MysqlInterface(object):
    """mysql"""
    @staticmethod
    def getConn():
        try:
            the_conn = pymysql.connect(host=DB_CONFIG['host'], user=DB_CONFIG['user'], passwd=DB_CONFIG['password'],
                                       port=DB_CONFIG['port'], db=DB_CONFIG['database'], charset='utf8')
            the_conn.autocommit(1)
            return the_conn
        except Exception as err:
            traceback.print_exc()

    @classmethod
    def excute_sql(cls, conn, sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        return cls.get_mysql_result(cursor)

    @classmethod
    def get_mysql_result(cls, cursor, size=10000):
        """每次获取10000条记录"""
        while True:
            result = cursor.fetchmany(size)
            if not result:
                cursor.close()
                break
            for line in result:
                yield line

    @classmethod
    def query(cls, sql='', fetchmany=False):
        results = []
        try:
            if sql:
                the_conn = cls.getConn()
                if fetchmany:
                    results = cls.excute_sql(the_conn, sql)
                else:
                    cursor = the_conn.cursor()
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    cursor.close()
                the_conn.close()
        except Exception as err:
            traceback.print_exc()
        finally:
            return results

    @classmethod
    def query_one(cls, sql='', fetchmany=False):
        results = []
        try:
            if sql:
                the_conn = cls.getConn()
                if fetchmany:
                    results = cls.excute_sql(the_conn, sql)
                else:
                    cursor = the_conn.cursor()
                    cursor.execute(sql)
                    results = cursor.fetchone()
                    cursor.close()
                the_conn.close()
        except Exception as err:
            traceback.print_exc()
        finally:
            return results