#!/usr/bin/env python2

""" This is a two-player pong game for the mensadisplay:
https://stratum0.org/wiki/Mensadisplay
"""

import sys
sys.path.append("/home/chris/mensactrl/python")
from player import Player
from ball import Ball
from time import sleep
import client
import clearscreen
import framebuffer

cntdwn = 10
won = False
starting = 0
s = 5
target = 10

p1 = Player(13371)
p2 = Player(13372)

bl = Ball()


def bar(pos, x):
    p = [(x, y, 255) for y in range(pos - s, pos + s)]
    client.set_pixels(p)


def draw():
    if won:
        # draw winner screen
        client.write(0, 0, 'Player 1: {0}'.format(p1.score))
        client.write(0, 1, 'Player 2: {0}'.format(p2.score))
        sleep(10)
    else:
        # draw ball
        fb.drawRect(bl.posx-bl.size, bl.posy-bl.size, bl.size*2+1, bl.size*2+1)
        # draw scores?
        client.write(10, 0, "{}".format(p1.score))
        client.write(80, 0, "{}".format(p2.score))

        # draw bar
        fb.drawRect(0, p1.pos-p1.size, 2, p1.size*2)
        fb.drawRect(client.WIDTH-2, p2.pos-p2.size, 2, p2.size*2)

        fb.output()
        sleep(0.1)


try:
    fb = framebuffer.Framebuffer(0,0, client)

    clearscreen.clear()
    # determine game state
    while not won:
        # waiting for players
        if not p1.connected or not p2.connected:
            # show "waiting for player"
            #clearscreen.clear()
            client.write(0,0,'Waiting for players ...')
            if p1.connected:
                client.write(0, 4, "Player 1 connected                                ")
            else:
                client.write(0,4, "Player 1: 'stty -icanon && netcat localhost 13371'")
            if p2.connected:
                client.write(0, 5, "Player 2 connected                                ")
            else:
                client.write(0,5, "Player 2: 'stty -icanon && netcat localhost 13372'")
            starting = cntdwn
        elif starting > 0:
            # show "game starts in %d"
            clearscreen.clear()
            client.write(0,0,'Game starts in {0}'.format(starting))
            starting -= 1
            sleep(0.5)
        elif starting == 0:
            clearscreen.clear()
            starting = -1
        else:
            # game frame
            bl.updatePos()

            # bounce p1 or p2
            if (bl.posx <= 2 and p1.checkCollision(bl)) or (bl.posx >= client.WIDTH -2 and p2.checkCollision(bl)):
                bl.speedx = bl.speedx * -1.0
            # bounce top or bot
            elif bl.posy <= 0 or bl.posy >= client.HEIGHT:
                bl.speedy = bl.speedy * -1.0
            # score p1
            elif bl.posx <= 0:
                p2.incScore()
                bl = Ball()
            # score p2
            elif bl.posx >= client.WIDTH:
                p1.incScore()
                bl = Ball()

            if p1.score >= target or p2.score >= target:
                won = True

            # draw update, draw() decides how long to sleep
            draw()

    # we're done here.
except KeyboardInterrupt as e:
    p1.stop()
    p2.stop()

