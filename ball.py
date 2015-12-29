#!/usr/bin/env python2

class Ball:
  posx = 0.0
  posy = 0.0

  speedx = 0.0
  speedy = 0.0

  speed = 1

  pixels = [(0,0), (-1,-1), (1,1), (1,-1), (-1,1)]

  def updatePos(self):
    self.posx += self.speedx*self.speed
    self.posy += self.speedy*self.speed

  def getPixels(self):
    return [(posx+x,posy+y) for x,y in pixels]
    
