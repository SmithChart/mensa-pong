#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import client
import bitmapfont

class Framebuffer:
    """Provides a framebuffer for the mensadisplay
    Uses the client.py for output of frame and the geometry of the display.
    Every framebuffer blits only the part of the mensadisplay that it is initialized to.
    Thus an application can use multiple framebuffer.
    """

    def __init__(self, posx, posy, client, height=None, width=None):
        """Create a new Framebuffer

        Arguments:
        posx   - x-coordinate (long side) on which the framebuffer starts
        posy   - y-coordinate (short side) on which the framebuffer starts
        client - the zmq-client to use
        height - height (y, short side) of the framebuffer in pixels. If None: Uses all available space
        width  - width (x, long side) of the framebuffer in pixels. If None: uses all available space
        """

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

        self._new = self._newBuffer()

    def _newBuffer(self):
        """Internal function to create a new blank buffer"""
        return [0] * self._width * self._height

    def drawPixel(self, x, y, intensity=255):
        """Sets a single pixel

        Arguments:
        x - x-position
        y - y-position
        intensity - intensity of the pixel"""

        if x >= 0 and y >= 0 and int(x) + int(y)*self._width < len(self._new):
            self._new[int(x) + int(y)*self._width] = intensity


    def drawRect(self, x, y, width, height, intensity=255):
        """Draws a rectangle

        Arguments:
        x         - x-position
        y         - y-position
        width     - width of the rectangle
        height    - height of the rectangle
        intensity - intensity of the rectangle
        """

        for xi in range(int(width)):
            for yi in range(int(height)):
                self.drawPixel(int(x)+xi, int(y)+yi, intensity)

    def output(self):
        """Blits the current framebuffer to the mensadisplay"""
        self._client.blit(self._posx, self._posy, self._width, self._height, self._new)
        self._new = self._newBuffer()

    def _char_to_pixel_segment(self, c):
        """return array of size PWIDTH * PHEIGHT (indexed by row, then column)"""
        pixels = [0] * self._client.PWIDTH * self._client.PHEIGHT

        if(c not in bitmapfont.FONT.keys()):
            c = u"☐";

        for x in xrange(0, self._client.PWIDTH):
            for y in xrange(0, self._client.PHEIGHT):
                pix = (bitmapfont.FONT[c][x] & (1<<y)) >> y
                pixels[y * self._client.PWIDTH + x] = pix * 255
        return pixels

    def write(self, x, y, string):
        """write string, starting at segment x,y. Tabs are expanded to 8 spaces, new
        lines always begin at the given x position. No boundary checks are done, text
        may be clipped at the border, in this case the function returns.
        This function returns a tuple (x,y,success) where (x,y) gives the position of
        the last character written, and success is set to False if the function
        returned because of clipped text.
        """
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
