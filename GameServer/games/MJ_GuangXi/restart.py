# coding=utf-8

import psutil
import traceback
import os
from run_servers import NAME

def removeLog():
    basePath = '%s\log'%os.getcwd()
    logs = os.listdir(basePath)
    for _log in logs:
        if _log == '.gitignore':
            continue
        filePath = '%s\%s'%(basePath,_log)
        try:
            os.remove(filePath)
        except:
            print(u'[删除日志文件] [%s] 失败' % _log)
            traceback.print_exc()
        else:
            print(u'[已删除日志文件] [%s]'%_log)

def close_server():
    mainPids = []
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
            if p.name() != 'python.exe' or NAME not in p.cmdline():
                continue
            # print p.name()
            # print p.cmdline()
            mainPids.append(pid)
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
        except:
            traceback.print_exc()
    if mainPids:
        print(u'当前进程%s' % mainPids)
        os.system('python close_server.py')
        print(u'开始关闭服务')
        while mainPids:
            for _pid in mainPids[:]:
                try:
                    p = psutil.Process(_pid)
                except psutil.NoSuchProcess:
                    mainPids.remove(_pid)
                    print(u'移除pid[%s]'%_pid)
        print(u'进程已全部关闭')
    else:
        print(u'当前无进程在运行')

def run_server():
    os.system('python run_servers.py')
    print(u'已启动服务')
if __name__ == '__main__':
    close_server()
    removeLog()
    run_server()