#!/usr/bin/env python2

import socket
from time import sleep
import thread

class Player:
    "Mensadisplay-Pong Networking Layer"

    connected = False
    pos = 0

    pos_min = 0
    pos_max = 69

    inc = 3

    port = 0

    score = 0

    def tcpserver(self):
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.bind(('0.0.0.0', self.port))
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ss.listen(1)
        while not self._stop:
            (cs, addr) = ss.accept()
            self.connected = True
            print "Connected"
            while not self._stop:
                c = cs.recv(1)
                if(c == ''):
                    self.connected = False
                    print "Disconnected"
                    break
                if c == 'k':
                    self.pos -= self.inc
                if c == 'j':
                    self.pos += self.inc
                if self.pos < self.pos_min:
                    self.pos = self.pos_min
                if self.pos > self.pos_max:
                    self.pos = self.pos_max
            cs.close()
            self.connected = False
        ss.close()

    def __init__(self, port):
        self.port = port
        thread.start_new_thread(self.tcpserver,())
        self._stop = False

    def incScore(self):
        self.score += 1

    def stop(self):
        self._stop = True
