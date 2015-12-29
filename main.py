from player import Player
from ball import Ball
from time import sleep
import client

cntdwn = 10
won = False
starting = 0
s = 5
target = 10

p1 = Player()
p2 = Player()

bl = Ball()


def bar(pos, x):
    p = [(x, y, 255) for y in range(pos - s, pos + s)]
    client.set_pixels(p)


def draw():
    client.clear()
    if won:
        # draw winner screen
        client.write(0, 0, 'Player 1: %d'.format(p1.score))
        client.write(0, 1, 'Player 2: %d'.format(p2.score))
        sleep(10)
    else:
        # draw ball
        p = [(x, y, 255) for x, y in []]
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
        client.clear()
        client.write('Waiting for players ...')
        starting = cntdwn
    elif starting > 0:
        # show "game starts in %d"
        client.clear()
        client.write('Game starts in %d'.format(starting))
        starting -= 1
    else:
        # game frame
        bl.updatePos()

        # bounce p1 or p2
        if ((p1.pos - s <= bl.pos.y and p1.pos + s >= bl.pos.y) or
           (p2.pos - s <= bl.pos.y and p2.pos + s >= bl.pos.y)):
            bl.speed.y = bl.speed.y * -1
        # bounce top or bot
        elif bl.pos.x <= 0 or bl.pos.x >= client.HEIGHT:
            bl.speed.x = bl.speed.x * -1
        # score p1
        elif bl.pos.x <= 0:
            p1.incScore()
        # score p2
        elif bl.pos.y >= client.WIDTH:
            p2.incScore()

        if p1.score >= target or p2.score >= target:
            won = True

        # draw update, draw() decides how long to sleep
        draw()

# we're done here.
