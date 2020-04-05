# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/11
Revision: 1.0.0
Description: Description
"""

import inspect
import logging
import logging.handlers
import os
import stat
import time
import platform
import traceback

t_fmt = '%(asctime)s - %(message)s'
default_fmt = '%(asctime)s -[%(name)s][%(levelname)s] - %(message)s'
try:
    if platform.system() == 'Linux':
        default_dir = os.getcwd().split('/')
        default_dir = '/'.join(default_dir[:default_dir.index('socket_server') + 1])
    elif platform.system() == 'Windows':
        default_dir = os.getcwd().split('\\')
        default_dir = '\\'.join(default_dir[:default_dir.index('socket_server') + 1])
except:
    traceback.print_exc()
    default_dir = '.'


class close_log(object):
    def info(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass


class HourFileHandler(logging.handlers.BaseRotatingHandler):

    def __init__(self, filename, when='H', encoding='utf-8', delay=False, *args, **kwargs):
        logging.handlers.BaseRotatingHandler.__init__(self, filename, 'a', encoding, delay)
        self.when = when.upper()
        if self.when == 'S':
            self.suffix = "%Y-%m-%d_%H-%M-%S"
        elif self.when == 'M':
            self.suffix = "%Y-%m-%d_%H-%M"
        elif self.when == 'H':
            self.suffix = "%Y-%m-%d_%H"
        elif self.when == 'D':
            self.suffix = "%Y-%m-%d"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        self.timeLen = self.suffix.count('%')
        self.oldDate = self.toDate()
        if os.path.abspath(self.baseFilename):
            oldTime = os.stat(self.baseFilename)[stat.ST_MTIME]
            if self.toDate() > self.toDate(oldTime):
                self.oldDate = self.toDate(oldTime)

    def emit(self, record):
        try:
            if self.shouldRollover(record):
                self.doRollover()
            logging.FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)

    def shouldRollover(self, record):
        cur_date = self.toDate()
        if cur_date > self.oldDate:
            return True
        return False

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        suffix = self.getFileNameSuffix(oldDate=self.oldDate)
        default_name = '%s.%s' % (self.baseFilename, suffix)
        dfn = self.rotation_filename(default_name)
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()
        self.oldDate = self.toDate()

    def toDate(self, *args):
        return time.localtime(*args)[:self.timeLen]

    def getFileNameSuffix(self, oldDate=None):
        if not oldDate:
            oldDate = self.toDate()
        oldDate = list(oldDate)
        oldDateTuple = tuple(oldDate + [0] * (9 - len(oldDate)))
        return time.strftime(self.suffix, oldDateTuple)

    def rotate(self, source, dest):
        super(HourFileHandler, self).rotate(source, dest)
        print('[rotate] %s => %s' % (source, dest))


class Handler_Class():
    Null = 'Null'
    File = 'File'
    Stream = 'Stream'
    RotatingFile = 'RotatingFile'
    TimedRotatingFile = 'TimedRotatingFile'
    HourFile = 'HourFile'

    _Handler_Type_Map_ = {
        'Null': logging.NullHandler,
        'File': logging.FileHandler,
        'Stream': logging.StreamHandler,
        'RotatingFile': logging.handlers.RotatingFileHandler,
        'TimedRotatingFile': logging.handlers.TimedRotatingFileHandler,
        'HourFile': HourFileHandler,
    }
    _Handler_Type_Configs_ = {
        'File': dict(encoding='utf-8'),
        'RotatingFile': dict(maxBytes=0, backupCount=0, encoding='utf-8'),
        'TimedRotatingFile': dict(when='H', interval=1, backupCount=0, encoding='utf-8'),
        'HourFile': dict(when='H', encoding='utf-8'),
    }

    @classmethod
    def getHandler(cls, htype):
        return cls._Handler_Type_Map_[htype]

    @classmethod
    def getConfigs(cls, htype):
        return cls._Handler_Type_Configs_.get(htype, {})


def getHandlerLogger(fileLabel='test', loggerLabel=None, handler_type=None, handler_types=None, onlyGetHandler=False,
                     formatter=default_fmt, level=logging.DEBUG, **HandlerConfigs):
    assert not handler_types or isinstance(handler_types, list)
    assert not handler_type or isinstance(handler_type, str)
    if not handler_types:
        handler_types = []
    if handler_type:
        handler_types.append(handler_type)
    assert handler_types
    handlers = []
    for _htype_ in handler_types:
        handler = Handler_Class.getHandler(_htype_)
        defaultConfigs = Handler_Class.getConfigs(_htype_)
        if _htype_ not in [Handler_Class.Null, Handler_Class.Stream]:
            log_file = '%s/logs/%s.log' % (default_dir, fileLabel)
            defaultConfigs['filename'] = log_file
        defaultConfigs.update(HandlerConfigs)
        args = inspect.getfullargspec(handler).args
        for _key in list(defaultConfigs.keys()):
            if _key not in args:
                del defaultConfigs[_key]
        handler = handler(**defaultConfigs)
        handler.setFormatter(logging.Formatter(formatter))
        handlers.append(handler)
    if onlyGetHandler:
        return handlers
    logger = logging.getLogger(loggerLabel)
    for _handler_ in handlers:
        logger.addHandler(_handler_)
    level and logger.setLevel(level=level)
    return logger


if __name__ == '__main__':
    logger = getHandlerLogger(fileLabel='testLog', handler_type=Handler_Class.HourFile,
                              level=logging.DEBUG, when='M')
    # while True:
    #     # logger.debug('debug')
    #     logger.info('info')
    #     # logger.warning('warn')
    #     # logger.error('error')
    #     time.sleep(0.1)
