from player import Player
from ball import Ball
from time import sleep
import client
import clearscreen

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
    clearscreen.clear()
    if won:
        # draw winner screen
        client.write(0, 0, 'Player 1: {0}'.format(p1.score))
        client.write(0, 1, 'Player 2: {0}'.format(p2.score))
        sleep(10)
    else:
        # draw ball
        p = [(x, y, 255) for x, y in bl.getPixels()]
        client.set_pixels(p)
        # draw scores?

        # draw bar
        bar(p1.pos, 0)
        bar(p2.pos, client.WIDTH - 1)

        sleep(1)


# determine game state
while not won:
    # waiting for players
    if not p1.connected or not p2.connected:
        # show "waiting for player"
        clearscreen.clear()
        client.write(0,0,'Waiting for players ...')
        starting = cntdwn
    elif starting > 0:
        # show "game starts in %d"
        clearscreen.clear()
        client.write(0,0,'Game starts in {0}'.format(starting))
        starting -= 1
    else:
        # game frame
        bl.updatePos()

        # bounce p1 or p2
        if ((p1.pos - s <= bl.posx and p1.pos + s >= bl.posx) or
           (p2.pos - s <= bl.posx and p2.pos + s >= bl.posx)):
            bl.speedx = bl.speedx * -1.0
        # bounce top or bot
        elif bl.posy <= 0 or bl.posy >= client.HEIGHT:
            bl.speedy = bl.speedy * -1.0
        # score p1
        elif bl.posx <= 0:
            p1.incScore()
        # score p2
        elif bl.posy >= client.WIDTH:
            p2.incScore()

        if p1.score >= target or p2.score >= target:
            won = True

        # draw update, draw() decides how long to sleep
        draw()

# we're done here.
