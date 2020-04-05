# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
from model.model_mysqlPool import *


class MySQLdb(object):
    """mysql 的数据库操作类，支持连接池"""

    def __init__(self, cfg):
        self.config = cfg
        self._pool = PooledConnection(self.config,
                                      self.config.get('maxConnections'),
                                      self.config.get('minFreeConnections', 1))

    def execute(self, sql, args=None):
        """执行 sql"""

        cursor = None
        conn = None
        try:
            try:
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
            except pymysql.err.OperationalError:
                log.error('execute error ready to retry:',
                          traceback.format_exc())
                conn and conn.drop()
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
            except RuntimeError:
                log.error('execute error ready to retry:',
                          traceback.format_exc())
                conn and conn.drop()
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
        except pymysql.err.InterfaceError:
            raise
        except pymysql.err.IntegrityError:
            raise
        except:
            log.error('execute error ready to retry:', traceback.format_exc())
            traceback.print_exc()
            conn and conn.drop()
            conn = None
        finally:
            conn and conn.release()

        return cursor

    def insert(self, sql, args=None):
        """插入记录"""

        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_id = cursor.lastrowid
            return row_id
        except:
            raise
        finally:
            cursor and cursor.close()

    def update(self, sql, args=None):
        """更新记录"""

        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_count = cursor.rowcount
            return row_count
        except:
            raise
        finally:
            cursor and cursor.close()

    def delete(self, sql, args=None):
        """删除记录"""

        cursor = None
        try:
            cursor = self.execute(sql, args)
            row_count = cursor.rowcount
            return row_count
        except:
            raise
        finally:
            cursor and cursor.close()

    def query(self, sql, args=None):
        """查询"""

        cursor = None
        try:
            cursor = self.execute(sql, args)
            return cursor.fetchall()
        except:
            raise
        finally:
            cursor and cursor.close()

    def query_one(self, sql, args=None):
        """查询返回一条数据"""

        cursor = None
        try:
            cursor = self.execute(sql, args)
            return cursor.fetchone()
        except:
            traceback.print_exc()
            print('[query_one] [Error] %s' % (sql))
            raise
        finally:
            cursor and cursor.close()

    def begin(self):
        """开启并返回一个事务"""

        tran = Transaction(self._pool.get_connection())
        tran.begin()

        return tran

    def commit(self, tran):
        """提交事务"""
        return tran.commit()

    def rollback(self, tran):
        """回滚事务"""
        return tran.rollback()


class Transaction(object):
    """事务类"""

    def __init__(self, conn):
        self.__isBegan = False
        self.conn = conn
        self.__old_autocommit = self.conn._conn.get_autocommit()
        self.conn._conn.autocommit(False)

    def begin(self):
        """开启事务"""

        if not self.__isBegan:
            self.conn._conn.begin()
            self.__isBegan = True

    def commit(self):
        """提交事务"""

        self.conn._conn.commit()
        self.__isBegan = False
        self._finished()

    def rollback(self):
        """回滚事务"""

        self.conn._conn.rollback()
        self.__isBegan = False
        self._finished()

    def _finished(self):
        self.__reset_autocommit()
        self.conn.release()

    def __reset_autocommit(self):
        """将连接的自动提交设置重置回原来的设置"""
        self.conn._conn.autocommit(self.__old_autocommit)

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()


if __name__ == "__main__":
    db = MySQLdb({
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "imqq",
        "maxConnections": 55,
        "minFreeConnections": 11,
    })

    dat = db.query("show databases;")
    tables = db.query("show tables;")
    print(dat)
    print(tables)
