# -*- coding:utf-8 -*-
# !/usr/bin/python
"""
Author:$Author$
Date:$Date$
Revision:$Revision$

Description:
    消消乐游戏逻辑类
"""

import numpy as np
import copy
import traceback

def getZeros():
    return np.zeros((8, 8))


def Rprint(str):
    # print(str)
    pass

WIDTH = 8
HEIGHT = 8

TYPECount = 5


class xiaoxiaoleMgr(object):
    def __init__(self):
        self.canvas = []
        self.table = getZeros()
        self.numObjs = [None] * TYPECount

    def run(self):
        self.canvas = self.setCanvas()
        self.numObjs = [xiaoxiaoleNumObj(self, num=n) for n in xrange(1, TYPECount + 1)]
        Rprint(self.canvas)
        results = self.getResults()
        return results

    def getCanvas(self):
        return self.canvas

    def getResults(self):
        results = []
        for _numobj in self.numObjs:
            _results = _numobj.getResult()
            if _results:
                results.extend(_results)
        return results

    def setCanvas(self):
        return np.random.random_integers(low=1, high=TYPECount, size=HEIGHT * WIDTH).reshape((HEIGHT, WIDTH))

class xiaoxiaoleNumObj(object):
    def __init__(self, xiaoxiaoleMgr, num):
        self.mgr = xiaoxiaoleMgr
        self.canvas = self.mgr.canvas
        self.num = num
        self.table = getZeros()
        self.pointList = []
        self.copyPointList = []
        # self.copyPointList = [[(5, 2), (5, 3), (5, 4)], [(6, 4), (6, 5), (6, 6)], [(4, 2), (5, 2), (6, 2)], [(3, 4), (4, 4), (5, 4), (6, 4)]]
        self.resultLists = []
        self.filter()
        Rprint(self.table)
        self.relevance(datas_points=self.copyPointList, isfirst=True)
        Rprint('结果为%s' % (self.resultLists))

    def getResult(self):
        result = []
        import json
        for _result in self.resultLists:
            # print '_result'
            # print _result
            # print type(_result)
            # for _r in _result:
            #     print _r
            #     print type(_r)
            #     for _i in _r:
            #         print _i
            #         print type(_i)

            rep = {
                'len':len(_result),
                'coordinates':_result,
                'type':self.num,
            }
            result.append(rep)
        return result

    def relevance(self, sample_points=None, datas_points=None, tmp_point_lists=None, isfirst=False):
        '''
        查找重合点
        :param sample_points:  样本
        :param datas_points:    数据集
        :param isfirst: 是否主函数,False为递归函数
        :param tmp_point_lists:
        :return:无
        '''
        if not datas_points:
            return
        if not tmp_point_lists:
            tmp_point_lists = []
        if not sample_points and datas_points:
            sample_points = datas_points[0]
        for _sample_point in sample_points:
            if _sample_point not in tmp_point_lists:
                tmp_point_lists.append(_sample_point)
        Rprint('查看%s是否与%s有重合 isfirst[%s]' % (sample_points, datas_points, isfirst))
        if sample_points not in datas_points:
            return
        datas_points.remove(sample_points)

        if datas_points:
            relevance_list = []
            for _point in sample_points:
                for _pointlist in datas_points:
                    if _point in _pointlist and _pointlist not in relevance_list:
                        relevance_list.append(_pointlist)
            Rprint('重合点为%s' % (relevance_list))
            for _relevance in relevance_list:
                Rprint('_relevance = %s' % _relevance)
                self.relevance(sample_points=_relevance, datas_points=datas_points, tmp_point_lists=tmp_point_lists)
        if isfirst:
            self.resultLists.append(tmp_point_lists)
            if datas_points:
                Rprint('tmp_point_lists = %s' % tmp_point_lists)
                return self.relevance(datas_points=datas_points, isfirst=True)
            else:
                Rprint('tmp_point_lists = %s' % tmp_point_lists)
                Rprint('结束')

    def filter(self):
        ''''找到该号码所有连续的点'''
        Rprint('准备查找%s的点' % (self.num))
        for row in xrange(0, HEIGHT):
            row_indexs = np.reshape(np.argwhere(self.canvas[row] == self.num), (-1))
            row_indexs = [int(_row_index) for _row_index in row_indexs]
            results = self.checkIncrease(row_indexs)
            # print '第%s行,结果为%s'%(row,results)
            for _result in results:
                Rprint(zip([row] * len(_result), _result))
                self.pointList.append(zip([row] * len(_result), _result))
                for _y in _result:
                    self.table[row, _y] = 1
                    self.mgr.table[row, _y] = 1
        for col in xrange(0, WIDTH):
            col_indexs = np.reshape(np.argwhere(self.canvas[:, col] == self.num), (-1))
            col_indexs = [int(_row_index) for _row_index in col_indexs]
            results = self.checkIncrease(col_indexs)
            # print '第%s列,结果为%s'%(col,results)
            for _result in results:
                Rprint(zip([col] * len(_result), _result))
                self.pointList.append(zip(_result, [col] * len(_result)))
                for _x in _result:
                    self.table[_x, col] = 1
                    self.mgr.table[_x, col] = 1
        Rprint('pointList = %s' % self.pointList)
        self.copyPointList = copy.deepcopy(self.pointList)

    def checkIncrease(self, index_list):
        ''''找多连续的列表'''
        results = []
        tmp_list = []
        len_array = len(index_list)
        for index, value in enumerate(index_list):
            if not tmp_list:
                tmp_list = [value]
            if index + 1 < len_array and value + 1 != index_list[index + 1]:
                if len(tmp_list) >= 3 and tmp_list not in results:
                    results.append(tmp_list)
                tmp_list = []
                continue
            else:
                if index + 1 < len_array:
                    tmp_list.append(value + 1)
        if len(tmp_list) >= 3 and tmp_list not in results:
            results.append(tmp_list)
        return results


if __name__ == '__main__':
    count = 10000
    from datetime import datetime
    start = datetime.now()
    print 'start',start
    while count:
        a = xiaoxiaoleMgr()
        try:
    #         # print a.run()
            a.run()
        except Exception as error:
            traceback.print_exc()
            print(a.canvas)
        count -= 1
    end = datetime.now()
    print 'end',end
    print end-start