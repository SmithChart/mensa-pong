#!/usr/bin/env python2

import client

class Ball:
  posx = 200.0
  posy = 45.0

  speedx = 0.8
  speedy = 0.2

  speed = 10

  pixels = [(0,0), (-1,-1), (1,1), (1,-1), (-1,1)]

  def updatePos(self):
    self.posx += self.speedx*self.speed
    self.posy += self.speedy*self.speed

  def getPixels(self):
    return [(int(self.posx+x),int(self.posy+y)) for x,y in self.pixels]
    
