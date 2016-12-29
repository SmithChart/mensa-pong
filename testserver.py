import pygame
import struct
import time
import zmq

P = 3
red_fg = (255,0,0)
red_bg = (114,42,42)
green_fg = (0,255,0)
green_bg = (102,144,102)
yellow_fg = (255,255,0)
yellow_bg = (155,155,56)
COLORS = [red_bg]*3+[green_bg]*3+[yellow_bg]*3+[red_bg]
SPLIT_N = 1
SPLIT_I = 0
NUM_SEG_X = 96
NUM_SEG_Y = 10
PWIDTH = 5
WIDTH = PWIDTH*NUM_SEG_X/SPLIT_N
WOFFSET = WIDTH*SPLIT_I
PHEIGHT = 7
PPAD = 5
HEIGHT = PHEIGHT*NUM_SEG_Y
PADDED_HEIGHT = HEIGHT + PPAD * (NUM_SEG_Y - 1)

pygame.init()
screen = pygame.display.set_mode((WIDTH*P,PADDED_HEIGHT*P))

def set_pixel(x,y,s):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return
    row = int(y/PHEIGHT)
    bg = COLORS[row]
    fg = fg_for_bg(bg)
    col = color_interpolate(fg, bg, s)
    real_y = row * (PHEIGHT+PPAD) + y % PHEIGHT
    pygame.draw.rect(screen, col, (x*P,real_y*P,P,P), 0)

CACHE = dict([(red_fg,[None]*256),(green_fg,[None]*256),(yellow_fg,[None]*256)])
def color_interpolate(fg, bg, s):
    l = s / 255.0
    assert 0 <= l and l <= 1
    if CACHE[fg][s]:
        col = CACHE[fg][s]
    else:
        col = tuple([int(bg[i] + l*(fg[i]-bg[i])) for i in range(3)])
        CACHE[fg][s] = col
    return col

def fg_for_bg(col):
    if col == red_bg:
        return red_fg
    if col == green_bg:
        return green_fg
    if col == yellow_bg:
        return yellow_fg

if __name__ == '__main__':
    for i in range(NUM_SEG_Y):
        top = i*(PHEIGHT+PPAD)
        pygame.draw.rect(screen, COLORS[i], (0,top*P,WIDTH*P,PHEIGHT*P), 0)
    pygame.display.update()

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % 5556)

    while True:
        #  Wait for next request from client
        message = socket.recv_multipart()
        for m in filter(None,message):
            t = ord(m[0])
            if t == 0: #single pixel
                _,x,y,v = struct.unpack('<BiiB', m)
                set_pixel(x,y,v)
            elif t == 1: #blit
                _,x,y,w,h = struct.unpack('<Biiii', m[:17])
                vals = [ord(s) for s in m[17:]]
                assert len(vals) == w*h
                for i in range(h):
                    for j in range(w):
                        set_pixel(x+j, y+i, vals[i*w+j])
        pygame.display.update()
        socket.send(' ')

