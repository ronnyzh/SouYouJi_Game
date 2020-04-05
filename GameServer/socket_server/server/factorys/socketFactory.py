# -*- coding:utf-8 -*-
# !/bin/python

"""
Author: Winslen
Date: 2019/11/5
Revision: 1.0.0
Description: Description
"""
from pprint import pformat

from define.define_consts import *
from proto import hall_match_pb2
from public.public_protoMgr import *
from .matchServer import MatchServer


class SocketFactory(MatchServer):
    def __init__(self, *args, **kwargs):
        super(SocketFactory, self).__init__(*args, **kwargs)
        self.uidSocketMgrs = {}
        self.senderMgr = SendManager(self)
        self.recverMgr = RecvManager(self)
        self.registerProtocolResolver()

    def addSocket(self, socket):
        self.log('[addSocket] %s' % socket.__str__())
        assert socket.uid
        uid = socket.uid
        if uid in self.uidSocketMgrs:
            oldSocket = self.uidSocketMgrs[uid]
            self.log('[addSocket] oldSocket=>%s' % oldSocket)
            oldSocket.close(code=1000, reason=u'被新的websocket连接覆盖')
        self.uidSocketMgrs[uid] = socket
        self.log('[addSocket] %s' % pformat(self.uidSocketMgrs))
        self.afterAddSocket(socket)

    def afterAddSocket(self, socket):
        pass

    def removeSocket(self, socket):
        self.log('[removeSocket] %s' % socket.__str__())
        if socket.uid and socket.uid in self.uidSocketMgrs:
            oldSocket = self.uidSocketMgrs[socket.uid]
            if oldSocket == socket:
                del self.uidSocketMgrs[socket.uid]
            else:
                self.log('[removeSocket] %s %s' % (socket, oldSocket))
        self.log('[removeSocket] %s' % (pformat(self.uidSocketMgrs)))
        self.afterRemoveSocket(socket)

    def afterRemoveSocket(self, socket):
        pass

    def registerProtocolResolver(self):
        pass
        # unpacker = Unpacker
        # self.recverMgr.registerCommands((
        #     unpacker(interface_pb2.C_S_PING, interface_pb2.C_S_Ping, self.onPing),
        # ))
        # packer = Packer
        # self.senderMgr.registerCommands((
        #     packer(interface_pb2.S_C_PING, interface_pb2.S_C_Ping),
        # ))

    def resolveMsg(self, socket, msgData):
        recvMgr = self.recverMgr
        recvMgr.unpackCall(socket, msgData)

    def sendData(self, peer, data):
        peer.sendMessage(data)

    def getPeersAttr(self, peers, attrName, toStr=False):
        data = [str(getattr(peer, attrName, '未知')) for peer in peers]
        if toStr:
            return ','.join(data)
        return data

    def send(self, peers, protocol_obj, excludes=()):
        try:
            msg_name = protocol_obj.__class__.__name__
            data = self.senderMgr.pack(protocol_obj)
        except:
            traceback.print_exc()
        else:
            self.log('[send] to [%s] the [%s]' % (self.getPeersAttr(peers, 'uid', toStr=True), msg_name))
            if excludes:
                self.log('[send] excludes [%s]' % (self.getPeersAttr(excludes, 'uid', toStr=True)))
            for peer in peers:
                if peer not in excludes:
                    try:
                        self.sendData(peer, data)
                    except:
                        traceback.print_exc()

    def sendOne(self, peer, protocol_obj):
        self.send([peer], protocol_obj)

    def sendAll(self, protocol_obj):
        self.send(self.uidSocketMgrs.values(), protocol_obj)
