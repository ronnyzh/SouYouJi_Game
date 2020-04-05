# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/29
Revision: 1.0.0
Description: Description
"""

import os
import shutil
import zipfile
from datetime import datetime
from pprint import pprint
import time

basePath = os.getcwd()
if basePath.split('\\')[-1] == 'socket_server':
    os.chdir('./logs')
elif basePath.split('/')[-1] == 'socket_server':
    os.chdir('./logs')
basePath = os.getcwd()
today = datetime.now().strftime('%Y-%m-%d')


def timestampToDate(timestamp, fmt='%Y-%m-%d'):
    return datetime.fromtimestamp(timestamp).strftime(fmt)


def pastFileMoveToBackupsDir():
    print(u'开始整理日志,并转移去备份目录')
    date_fileMap = {}

    for _fileName_ in os.listdir('.'):
        if 'log' not in _fileName_:
            print('[%s]不是log文件' % (_fileName_))
            continue
        nameList = _fileName_.split('.')
        if nameList[-1] == 'log':
            print('[%s]正在写入的过滤' % (_fileName_))
            continue
        if 'server' in _fileName_:
            date = nameList[-1].split('_')[0]
        elif 'mysql' in _fileName_:
            date = 'mysql'
        else:
            print('[%s]未知的文件' % (_fileName_))
            continue
        if date == today:
            print('[%s]今日的文件过滤' % (_fileName_))
            continue
        date_fileMap.setdefault(date, set())
        date_fileMap[date].add(_fileName_)
    pprint(date_fileMap)

    for _date, _files in date_fileMap.items():
        # dirName : 备份的文件夹名字
        # dirPath : 备份的文件夹路径
        targetDirName = 'backups_%s' % (_date)
        targetDirPath = './%s' % (targetDirName)
        if not os.path.exists(targetDirName):
            os.mkdir(targetDirName)

        for _file in _files:
            if _date == 'mysql':
                fmt = '%Y-%m-%d-%H-%M'
                tagetFilePath = '%s/%s_%s_%s' % (targetDirPath, _file, timestampToDate(os.path.getctime(_file), fmt),
                                                 timestampToDate(os.path.getmtime(_file), fmt))
            else:
                tagetFilePath = '%s/%s' % (targetDirPath, _file)
            if os.path.exists(tagetFilePath):
                print('存在文件%s' % (tagetFilePath))
                os.remove(tagetFilePath)
            shutil.move(_file, tagetFilePath)


def backupsDirToZip(rmSourceFile=False):
    def toZip(targetDirName):
        targetZipFileName = '%s.zip' % targetDirName

        backupsFilesPath = []
        for path, dirnames, filenames in os.walk(targetDirName):
            for filename in filenames:
                backupsFilesPath.append(os.path.join(path, filename))

        print('backupsFilesPath', backupsFilesPath)

        if not backupsFilesPath:
            print('当前文件夹[%s]为空,不需要压缩' % (targetDirName))
            return
        else:
            print('文件%s,将要备份去[%s]' % (backupsFilesPath, targetZipFileName))
        with zipfile.ZipFile(targetZipFileName, "a", zipfile.ZIP_DEFLATED) as zip:
            print('压缩包[%s]写入开始' % (targetZipFileName))
            for filePath in backupsFilesPath:
                zip.write(filePath)
                print('--->[%s]写入成功' % (filePath))
            print('压缩包[%s]写入完成' % (targetZipFileName))
            if rmSourceFile:
                shutil.rmtree(targetDirName)
                print('删除已备份的目录[%s]' % (targetDirName))

    print('备份开始')
    for _fileName_ in os.listdir('.'):
        isDir = os.path.isdir(_fileName_)
        if not isDir or 'backups' not in _fileName_:
            continue
        toZip(_fileName_)
    print('备份完成')


if __name__ == '__main__':
    print('basePath', basePath)
    print('today', today)
    pastFileMoveToBackupsDir()
    backupsDirToZip(True)
    time.sleep(3)
