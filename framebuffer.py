#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import client
import bitmapfont

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
        self._new = self._newBuffer()

    # return array of size PWIDTH * PHEIGHT (indexed by row, then column)
    def _char_to_pixel_segment(self, c):
        pixels = [0] * self._client.PWIDTH * self._client.PHEIGHT

        if(c not in bitmapfont.FONT.keys()):
            c = u"☐";

        for x in xrange(0, self._client.PWIDTH):
            for y in xrange(0, self._client.PHEIGHT):
                pix = (bitmapfont.FONT[c][x] & (1<<y)) >> y
                pixels[y * self._client.PWIDTH + x] = pix * 255
        return pixels

    # write string, starting at segment x,y. Tabs are expanded to 8 spaces, new
    # lines always begin at the given x position. No boundary checks are done, text
    # may be clipped at the border, in this case the function returns.
    # This function returns a tuple (x,y,success) where (x,y) gives the position of
    # the last character written, and success is set to False if the function
    # returned because of clipped text.
    def write(self, x, y, string):
        orig_x = x
        string = string.replace("\t", " "*8)
        for c in string:
            if c == "\n":
                y += 1
                x = orig_x
            if ord(c) < 0x1f:
                pass
            else:
                pixels = self._char_to_pixel_segment(c)
                # copy pixels to framebuffer
                i0 = x*self._client.PWIDTH + y*self._client.PHEIGHT*self._client.WIDTH
                for j in range(len(pixels)):
                    row = j / self._client.PWIDTH
                    off = j % self._client.PWIDTH
                    i = i0 + row*self._client.WIDTH + off
                    self._new[i] = pixels[j]
                x += 1

            if(x > self._client.NUM_SEG_X):
                return (x,y,False)

        return (x,y,True)
