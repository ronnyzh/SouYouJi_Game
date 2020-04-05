# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/5
Revision: 1.0.0
Description: Description
"""

# -*- coding: utf-8 -*-
"""
B{[公共]}指令解包/封包模块。
"""
import struct
import traceback


class Packer(object):
    def __init__(self, msg_code, msg_cls):
        self.msg_code = msg_code
        self.msg_cls = msg_cls

    def pack(self, protocol_object):
        assert isinstance(protocol_object, self.msg_cls)
        _data = struct.pack('>I', self.msg_code) + protocol_object.SerializeToString()
        return _data


class Unpacker(object):
    def __init__(self, msg_code, msg_cls, callback):
        assert callable(callback), "resolver[%s] is not a callable object" % (str(callback))
        self.msg_code = msg_code
        self.msg_cls = msg_cls
        self.callback = callback

    def unpack(self, data):
        obj = self.msg_cls()
        obj.ParseFromString(data)
        return obj


class SendManager(object):
    def __init__(self, factory=None):
        self._cmds = {}
        self.factory = factory

    def log(self, msg='', level='info'):
        try:
            if self.factory:
                self.factory.log(msg=msg, level=level)
            else:
                print('[%s] %s' % (level, msg))
        except:
            traceback.print_exc()
            print('[%s] %s' % (level, msg))

    def registerComand(self, cmd_inst):
        assert isinstance(cmd_inst, Packer) and (cmd_inst.msg_cls.__name__ not in self._cmds)
        self._cmds[cmd_inst.msg_cls.__name__] = cmd_inst

    def registerCommands(self, commands):
        for cmd_inst in commands:
            self.registerComand(cmd_inst)

    def pack(self, protocol_object):
        msg_name = protocol_object.__class__.__name__
        if msg_name not in self._cmds:
            raise Exception('%s not in %s' % (msg_name, self._cmds))
        cmd_inst = self._cmds[msg_name]
        self.log("[SendManager] pack [%s] => %s" % (msg_name, protocol_object))
        msg = cmd_inst.pack(protocol_object)
        return msg

    def hasCmd(self, msg_name):
        return msg_name in self._cmds


class RecvManager(object):
    def __init__(self, factory=None):
        self._cmds = {}
        self.factory = factory

    def log(self, msg='', level='info'):
        try:
            if self.factory:
                self.factory.log(msg=msg, level=level)
            else:
                print('[%s] %s' % (level, msg))
        except:
            traceback.print_exc()
            print('[%s] %s' % (level, msg))

    def registerCommand(self, cmd_inst):
        assert (isinstance(cmd_inst, Unpacker) and (cmd_inst.msg_code not in self._cmds))
        self._cmds[cmd_inst.msg_code] = cmd_inst

    def registerCommands(self, commands):
        for cmd_inst in commands:
            self.registerCommand(cmd_inst)

    def unpackCall(self, peer, msg):
        try:
            _log = self.log
            if peer:
                _log = peer.log
            msg_code, = struct.unpack('>I', msg[:4])
            if msg_code not in self._cmds:
                raise Exception('msg_code[%s] is not existed.' % (msg_code))
            _log("[unpackCall] recv %s, %s" % (msg_code, self._cmds[msg_code].msg_cls.__name__))
            cmd_inst = self._cmds[msg_code]
            proto_obj = cmd_inst.unpack(msg[4:])
            _log("[unpackCall] proto_obj => %s" % (proto_obj))
        except:
            traceback.print_exc()
            return False
        params = [proto_obj]
        if peer is not None:
            params.insert(0, peer)
        cmd_inst.callback(*params)
        return cmd_inst.msg_code, cmd_inst.callback, params

    def clientUnpackCall(self, msg):
        return self.unpackCall(None, msg)

    def hasCmd(self, msg_header):
        return msg_header in self._cmds
