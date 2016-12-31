#!/usr/bin/env python2

import time

class waiter:
    def __init__(self, period):
        self._period = period
        self._next = float(time.time())+period

    def wait(self):
        n = float(time.time())
        if n > self._next:
            self._next = n + self._period
        else:
            d = self._next - n
            time.sleep(d)
            self._next = self._next + self._period
