#!/usr/bin/env python2

""" This is a two-player pong game for the mensadisplay:
https://stratum0.org/wiki/Mensadisplay
"""

# hack to make loading of the mensadisplay-client possible
# this assumes that this repo is checked out inside the mensadisplay-repository: https://gitli.stratum0.org/stratum0/mensactrl
import sys
sys.path.append("../python/")

from player import Player
from ball import Ball
from time import sleep
import client
import clearscreen
import framebuffer
import wait
import argparse

# Get the IP to bind to
parser = argparse.ArgumentParser()
parser.add_argument("bindTo", help="The IP to bind the players to")
args = parser.parse_args()

# this stuff represents the game's state
cntdwn = 10
won = False
starting = 0
s = 5
target = 10

# Init objects on the canvas
p1 = Player(13371, args.bindTo)
p2 = Player(13372, args.bindTo)
bl = Ball()

# Init framebuffer and time-logic
fb = framebuffer.Framebuffer(0,0, client)
wt = wait.waiter(1.0/20.0)

# this is a legacy-way to draw a players bar
#def bar(pos, x):
#    p = [(x, y, 255) for y in range(pos - s, pos + s)]
#    client.set_pixels(p)


def draw():
    """Draws a frame of the game"""
    if won:
        # draw winner screen
        fb.write(0, 0, 'Player 1: {0}'.format(p1.score))
        fb.write(0, 1, 'Player 2: {0}'.format(p2.score))
        fb.output()
        sleep(10)
    else:
        # draw ball
        fb.drawRect(bl.posx-bl.size, bl.posy-bl.size, bl.size*2+1, bl.size*2+1)
        # draw scores
        fb.write(10, 0, "{}".format(p1.score))
        fb.write(80, 0, "{}".format(p2.score))

        # draw bar
        fb.drawRect(0, p1.pos-p1.size, 2, p1.size*2)
        fb.drawRect(client.WIDTH-2, p2.pos-p2.size, 2, p2.size*2)

        fb.output()
        wt.wait()


# this is the main game-logic
try:
    # determine game state
    while not won:
        # waiting for players
        if not p1.connected or not p2.connected:
            # show "waiting for player"
            #clearscreen.clear()
            fb.write(0,0,'Waiting for players ...')
            if p1.connected:
                fb.write(0, 4, "Player 1 connected                                ")
            else:
                fb.write(0,4, "Player 1: 'stty -icanon && netcat {} 13371'".format(args.bindTo))
            if p2.connected:
                fb.write(0, 5, "Player 2 connected                                ")
            else:
                fb.write(0,5, "Player 2: 'stty -icanon && netcat {} 13372'".format(args.bindTo))
            fb.output()
            starting = cntdwn
        elif starting > 0:
            # show "game starts in %d"
            fb.write(0,0,'Game starts in {0}'.format(starting))
            starting -= 1
            fb.output()
        elif starting == 0:
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

