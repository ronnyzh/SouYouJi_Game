# -*-coding:utf8-*-

#!/usr/bin/env python
#-*-coding:utf-8 -*-

"""
@Author: $Author$
@Date: $Date$
@version: $Revision$

Description:
     Description
"""
from bottle import default_app
import pymysql
import traceback

class MysqlPlugin(object):
    name = 'mysql'

    def __init__(self,host="127.0.0.1",port=3306,user="root",password="root",db="Match_db",charset="utf8mb4",keyword="mysql"):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.db = db
        self.keyword = keyword
        self.charset = charset
        self.cursorclass = pymysql.cursors.DictCursor
        self.conn = self.connect_sql()

    '''连接数据库'''
    def connect_sql(self):
        conn = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,db=self.db,charset=self.charset,
                               cursorclass=self.cursorclass)
        print '连接数据库成功'
        return conn

    '''关闭数据库'''
    def close_connect(self):
        print '关闭数据库成功'
        self.conn.close()

    '''创建游标'''
    def create_cursor(self):
        return self.conn.cursor()

    '''关闭游标'''
    def close_cursor(self,cursor):
        cursor.close()

    def execute(self,cmd,fetchall = True):
        '''
        执行一条语句
        :param cmd: sql语句
        :param fetchall: 是否获取全部结果(或一个结果)
        :return:执行结果
        '''
        print '[execute] cmd[%s] fetchall[%s]'%(cmd,fetchall)
        cursor = self.create_cursor()
        try:
            total = cursor.execute(cmd)
            self.conn.commit()
        except Exception,error:
            print '[execute] error[%s]'%(error)
            traceback.print_exc()
            self.conn.rollback()
            self.close_cursor(cursor)
            print '[execute] result[False] error[%s]'%(error)
            return False,error
        else:
            if fetchall:
                answer = cursor.fetchall()
            else:
                answer = cursor.fetchone()
            self.close_cursor(cursor)
            if answer:
                print '[execute] result[True] answer[%s] is %s'%(len(answer),answer)
            else:
                print '[execute] result[True] no answer'
            return True,answer

    def executemany(self,cmd,data_list,fetchall = True):
        '''
        执行多条相似语句
        :param cmd: sql语句
        :param data_list: 数据列表[[],[]],[(),()]
        :param fetchall: 是否获取全部结果(或一个结果)
        :return:执行结果
        '''
        print '[executemany] cmd[%s] fetchall[%s]' % (cmd, fetchall)
        cursor = self.create_cursor()
        try:
            cursor.executemany(cmd, data_list)
            self.conn.commit()
        except Exception,error:
            print '[executemany] error[%s]' % (error)
            traceback.print_exc()

            self.conn.rollback()
            self.close_cursor(cursor)
            return False,error
        else:
            if fetchall:
                answer = cursor.fetchall()
            else:
                answer = cursor.fetchone()
            if answer:
                print '[execute] result[True] answer[%s] is %s' % (len(answer), answer)
            else:
                print '[executemany] result[True] no answer'
            self.close_cursor(cursor)
            return True, answer

    #######################简单封装############################
    def select_data(self,cmd_table, cmd_key, cmd_where={}):
        '''
        查询数据
        :param cmd_key: 字段
        :param cmd_table: 表名
        :param cmd_where: 限制条件(字典)
        :return:查询结果
        '''
        cmd = "select %s from %s" % (cmd_key, cmd_table)
        if cmd_where:
            if not isinstance(cmd_where, dict):
                print '参数错误'
                return False,
            where_str = " and ".join(map(lambda x, y: '%s = %s' % (x, y) if isinstance(y, int) else ('%s = "%s"' % (x, y)), cmd_where.keys(), cmd_where.values()))
            cmd += ' where %s' % (where_str)
        result, answer = self.execute(cmd)
        return result, answer

    def select_data_bywhere(self,cmd):
        result, answer = self.execute(cmd)
        return result, answer

    def insert_data(self,cmd_table,cmd_data):
        '''
        插入一条数据
        :param cmd_table:表名
        :param cmd_data: 数据(字典),{'字段','值'}
        :return:执行结果
        '''
        key_str,value_str = self.format_part_data(cmd_data)
        if not key_str or not value_str:
            print '参数错误'
            return False,False
        cmd = "insert into %s(%s) values(%s)" % (cmd_table,key_str,value_str)
        print(cmd)
        result, answer = self.execute(cmd)
        return result,answer

    def insert_datas(self,cmd_table,cmd_keys,cmd_datas):
        '''
        同时插入多条数据(具有相似度)
        :param cmd_table: 表名
        :param cmd_keys: 字段名(list)
        :param cmd_datas: 数据 [(),()] or [[],[]]
        :return: 执行结果
        '''
        if not isinstance(cmd_keys,(list,)) or not isinstance(cmd_datas,(list,set)):
            print '[insert_datas]1参数错误'
            return False,
        cmd = "insert into %s(%s) values("% (cmd_table,','.join(cmd_keys))
        cmd += "%s"%(','.join(['%s']*len(cmd_keys)))
        cmd += ")"
        result, answer = self.executemany(cmd,cmd_datas)
        return result,answer

    def format_part_data(self,cmd_data):
        '''
        格式化分离数据
        :param cmd_data:数据(字典),{'字段','值'}
        :return: keys列表字符串("key1,key2,key3"),values列表字符串("value1,'value2',value3")
        '''
        if not isinstance(cmd_data,dict):
            print '[update_insert_data]参数错误'
            return False,False
        key_list = []
        value_list = []
        for _key,_value in cmd_data.iteritems():
            key_list.append(_key)
            if isinstance(_value,(int,float)):
                _value = "%s"%(_value)
            else:
                _value = "'%s'" % (_value)
            value_list.append(_value)
        return ','.join(key_list), ','.join(value_list)

def get_mysql(host="120.79.141.135", user="root", password="root"):
    return MysqlPlugin(host=host,user=user,password=password)

if __name__ == '__main__':
    sql = get_mysql()
    sql.select_data('MatchLog','*',cmd_where={'id': '1'})
    sql.close_connect()
