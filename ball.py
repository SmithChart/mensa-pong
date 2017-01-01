#!/usr/bin/env python2

import client
import random
import math

class Ball:
  """Balls are square. Deal with it."""
  # start position
  posx = 200.0
  posy = 45.0
  # movement speed, multiplied onto the coordinates with every frame
  speed = 4

  # in order to match the logic for the bar, size is added to the ball twice
  size = 1

  pixels = [(x, y) for x in range(size * -1, size + 1) for y in range(size * -1, size + 1)]

  def __init__(self):
    angle = float(random.randrange(-30, 30))
    if random.random() >= 0.5:
      angle += 180
    self.speedy = math.sin(angle / 180 * math.pi)
    self.speedx = math.cos(angle / 180 * math.pi)

  def updatePos(self):
    self.posx += self.speedx * self.speed
    self.posy += self.speedy * self.speed

  def getPixels(self):
    return [(int(self.posx + x), int(self.posy + y)) for x,y in self.pixels]

