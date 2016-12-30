#!/usr/bin/env python2

import client

class Framebuffer:
    def __init__(self, posx, posy, client, height=None, width=None):
        self._posx = posx
        self._posy = posy
        self._client = client
        if height is None:
            self._height = client.HEIGHT - posy
        else:
            self._height = height
        if width is None:
            self._width = client.WIDTH - posx
        else:
            self._width = width

        self._old = self._newBuffer()
        self._new = self._newBuffer()

    def _newBuffer(self):
        return [0] * self._width * self._height

    def drawPixel(self, x, y, intensity=255):
        if x >= 0 and y >= 0 and int(x) + int(y)*self._width < len(self._new):
            self._new[int(x) + int(y)*self._width] = intensity

    def drawRect(self, x, y, width, height, intensity=255):
        for xi in range(int(width)):
            for yi in range(int(height)):
                self.drawPixel(int(x)+xi, int(y)+yi, intensity)

    def output(self):
        # create list of changes between both framebuffers
        self._client.blit(self._posx, self._posy, self._width, self._height, self._new)
#        pixels = list()
#        for i in range(len(self._new)):
#            if self._new[i] != self._old:
#                xi = i % int(self._width)
#                yi = i / self._width
#                pixels.append((self._posx+xi, self._posy+yi, self._new[i]))
#        self._client.set_pixels(pixels)
#        self._old = self._new
        self._new = self._newBuffer()

