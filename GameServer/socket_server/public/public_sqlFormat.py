# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/10/15
Revision: 1.0.0
Description: Description
"""
import re


class FormatSql(object):
    PARAMERTS_REG = re.compile(r':([_0-9]*[_A-z]+[_0-9]*[_A-z]*)')

    def __init__(self, tableName, **kwargs):
        self.kwargs = kwargs
        self.tableName = tableName
        self.columnNames = kwargs.get('columnNames', [])

        self.formatKeyNum = 0
        self.formatDict = {}
        self.whereStr = ''
        self.orderStr = ''
        whereParams = kwargs.get('whereParams', {})
        if whereParams and whereParams.get('data', {}):
            whereData = whereParams['data']
            joinStr = whereParams.get('joinStr', 'AND')
            sign = whereParams.get('sign', '=')
            tmpWhereStr = self.getWhereStr_ByDatas(whereDatas=whereData, joinStr=joinStr, sign=sign)
            self.setWhereStr(tmpWhereStr)

    def getNextTmpValueName(self, incr=1):
        self.formatKeyNum += incr
        return 'value_%s' % (self.formatKeyNum)

    def setWhereStr(self, whereStr):
        self.whereStr = whereStr

    def addWhereStr(self, whereStr, joinStr='AND'):
        self.whereStr += ' %s %s' % (joinStr, whereStr)

    def insertWhereData(self, key, value, sign='='):
        '''sign: =,>,<,Like'''
        tmpValueName = self.getNextTmpValueName()
        if isinstance(value, str):
            value = value.replace("'", "\\'").replace('"', '\\"')
        elif isinstance(value, (tuple, list)) and sign == 'in':
            value = tuple(value)
            # value = repr(value).replace(",)", ")")
        self.formatDict[tmpValueName] = value
        return "`%s` %s :%s" % (key, sign, tmpValueName)

    def getWhereStr_ByDatas(self, whereDatas, joinStr='AND', sign='='):
        whereStr = ''
        for _key, _value in whereDatas.items():
            str_ = self.insertWhereData(key=_key, value=_value, sign=sign)
            whereStr += '%s %s ' % (str_, joinStr)
        whereStr = whereStr.strip().strip(joinStr).strip()
        return whereStr

    def joinWhereStr(self, joinStr='AND', *args):
        whereStr = ''
        for _arg in args:
            whereStr += '(%s) %s ' % (_arg, joinStr)
        whereStr = whereStr.strip().strip(joinStr).strip()
        return whereStr

    def fiterSqlStr(self):
        sqlStr = ''
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr

    def tryGetAllSql(self):
        '''可以获取sql数据拼接后的语句,但是此处只是预览'''
        sqlStr = self.fiterSqlStr()
        for _key, _value in self.formatDict.items():
            if isinstance(_value, str):
                _value = "'%s'" % _value
            sqlStr = sqlStr.replace(':%s' % _key, str(_value))
        return sqlStr

    def getSqlStrAndArgs(self):
        return self.fiterSqlStr(), self.formatDict


class FormatSql_Insert(FormatSql):
    def __init__(self, **kwargs):
        super(FormatSql_Insert, self).__init__(**kwargs)
        self.datasDict = kwargs.get('datasDict', {})

    def fiterSqlStr(self):
        keyStr = []
        valueStr = []
        for _key, _value in self.datasDict.items():
            tmpValueName = self.getNextTmpValueName()
            self.formatDict[tmpValueName] = _value
            keyStr.append(_key)
            valueStr.append(':%s' % tmpValueName)
        sqlStr = 'INSERT INTO %s (`%s`) VALUES (%s)' % (self.tableName, '`,`'.join(keyStr), ','.join(valueStr))
        sqlStr = sqlStr.replace('  ', ' ')
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr


class FormatSql_Select(FormatSql):

    def getTableSql(self):
        '''获取主要的sql语句'''
        columnNames = self.kwargs.get('columnNames')
        if columnNames:
            keysStr = '`,`'.join(columnNames)
            tableSql = 'SELECT `%s` FROM %s' % (keysStr, self.tableName)
        else:
            tableSql = 'SELECT * FROM %s' % (self.tableName)
        return tableSql

    def doJoinTable(self):
        joinType = self.kwargs.get('joinType', 'JOIN')
        joinTableName = self.kwargs.get('joinTableName', '')
        onStr = self.kwargs.get('onStr', '')
        if not joinTableName:
            return ''
        if onStr:
            joinTableStr = '%s %s ON %s' % (joinType, joinTableName, onStr)
        else:
            joinTableStr = '%s %s' % (joinType, joinTableName)
        return joinTableStr

    def doOrderBy(self):
        orderBy = self.kwargs.get('orderBy', '')
        orderType = self.kwargs.get('orderType', 'DESC')
        if not orderBy:
            return ''
        return 'ORDER BY `%s` %s' % (orderBy, orderType)

    def fiterSqlStr(self):
        sqlStr = self.getTableSql()
        joinSql = self.doJoinTable()
        if joinSql:
            sqlStr += ' ' + joinSql
        if self.whereStr:
            sqlStr += ' WHERE ' + self.whereStr
        orderStr = self.doOrderBy()
        if orderStr:
            sqlStr += ' ' + orderStr
        sqlStr = sqlStr.replace('  ', ' ')
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr


class FormatSql_Update(FormatSql):

    def __init__(self, **kwargs):
        super(FormatSql_Update, self).__init__(**kwargs)
        self.datasDict = kwargs.get('datasDict', {})

    def getSetDataStr(self):
        setDataStr = self.getWhereStr_ByDatas(self.datasDict, joinStr=',')
        return setDataStr

    def fiterSqlStr(self):
        setData = self.getSetDataStr()
        sqlStr = 'UPDATE %s SET %s' % (self.tableName, setData)
        if self.whereStr:
            sqlStr += ' WHERE ' + self.whereStr
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr


class FormatSql_Delete(FormatSql):
    def fiterSqlStr(self):
        sqlStr = 'DELETE FROM %s' % (self.tableName)
        if self.whereStr:
            sqlStr += ' WHERE ' + self.whereStr
        sqlStr = self.PARAMERTS_REG.sub(r'%(\1)s', sqlStr)
        return sqlStr


if __name__ == '__main__':
    VIDEO_SQL_KEY_1 = ['ym_video.id', 'ym_video.create_time', 'image_url', 'video_url', 'title', 'praiseCount',
                       'watchCount', 'content', 'director_id', 'nickname', 'user_id', 'avatar_url']
    pass
    # a = FormatSql_Select(
    #     **dict(
    #         tableName='ym_video',
    #         joinTableName='ym_users',
    #         onStr='ym_video.user_id = ym_users.id',
    #         whereParams={
    #             'data': {'ym_video.id': '123'},
    #             'joinStr': 'AND',
    #             'sign': '=',
    #         },
    #         columnNames=VIDEO_SQL_KEY_1,
    #         joinType='LEFT JOIN',
    #         orderBy='create_time',
    #     )
    # )
    # # print(a.fiterSqlStr())
    # # print('#' * 50)
    # a1 = a.getWhereStr_ByDatas({'ym_video.id': 37, 'title': 'ass'})
    # a2 = a.getWhereStr_ByDatas({'ym_video.id': 38, 'title': 'hahahah'}, joinStr='AND')
    # a3 = a.getWhereStr_ByDatas({'ym_video.id': [39, 40], 'title': ['hahahah', 'hahahahasdsa']}, joinStr='AND', sign='in')
    # print('a1=>', a1)
    # print('a2=>', a2)
    # print('a3=>', a3)
    # a4 = a.joinWhereStr(joinStr='OR', a1, a2, a3)
    # print('a4=>', a4)
    # a.addWhereStr(a4)
    # print(a.fiterSqlStr())
    # print(a.tryGetAllSql())

    # a4 = a.joinWhereStr(joinStr='OR', a1, a2, a3)
    # print('a4=>', a4)
    # print('#' * 50)
    # a5 = a.getWhereStr_ByDatas({'ym_video.id': 43, 'title': '1231'})
    # print('a5=>', a5)
    #
    # a6 = a.joinWhereStr(joinStr='OR', a4, a5)
    # print('a6=>', a6)
    # a.setWhereStr(a6)
    # print(a.formatDict)
    # a7 = a.fiterSqlStr()
    # print('a7=>', a7)

    # a = FormatSql_Insert(**dict(
    #     tableName='ym_video',
    #     datasDict={'id': 2, 'name': '你好'}
    # ))
    # print(a.fiterSqlStr())
    # print(a.tryGetAllSql())

    # a = FormatSql_Update(**dict(
    #     tableName='ym_video',
    #     datasDict={'id': 2, 'name': '你好'},
    #     whereParams={
    #         'data': {'ym_video.id': '123', 'name': '你好'},
    #         'joinStr': 'AND',
    #         'sign': '=',
    #     },
    # ))
    # print(a.fiterSqlStr())
    # print(a.tryGetAllSql())
    #
    # a = FormatSql_Delete(**dict(
    #     tableName='ym_video',
    #     whereParams={
    #         'data': {'ym_video.id': '123', 'name': '你好'},
    #         'joinStr': 'AND',
    #         'sign': '=',
    #     },
    # ))
    # print(a.fiterSqlStr())
    # print(a.tryGetAllSql())
