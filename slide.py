#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# simple pyglet animation
# http://www.github.com/msarch/slide

import math
import pyglet
from pyglet.gl import *

DEG2RAD = 2* math.pi/360
OMEGA = 360.0 * 0.5 # angular velocity (rev/s) : 1/2 rev/s
ORIGIN = [1280/2,800/2,0]   # x,y of screen center, rotation = 0
alpha = 0.0                 # initial angle
vis = 1                     # visibility switch
#---------------------------------- SKETCH ------------------------------------
class Sketch(pyglet.graphics.Group): # subclass with position/rotation ability
    def __init__(self,pos=ORIGIN):
        super(Sketch, self).__init__()
        self.pos=pos

    def set_state(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glRotatef(self.pos[2], 0, 0, 1) # rot. in degrees; x,y,z of rot. axis

    def unset_state(self):
        glPopMatrix()

# vertex_list modifier function -----------------------------------------------
def translate(vtx,pos): # modifying a list of vertices at once to new pos
    return(reduce(tuple.__add__, zip([x+pos[0] for x in vtx[0::2]],
    [y+pos[1] for y in vtx[1::2]])))

#--------------------------------- PYGLET STUFF -------------------------------
batch = pyglet.graphics.Batch()  # holds all graphics
canvas = pyglet.window.Window(fullscreen=True)
canvas.set_mouse_visible(False)

glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable(GL_BLEND)                                  # transparency
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # transparency
black   =(  0,   0,   0, 255)
glClearColor(*black)  # background color

@canvas.event
def on_key_press(symbol, modifiers):
    global vis
    if symbol == pyglet.window.key.I:
        vis=not(vis)  # visibility switch
        toggle(vis)
    else: pyglet.app.exit()

@canvas.event
def draw():
    canvas.clear()
    batch.draw()

def update(dt):  # updates an uniform circular motion then calls custom actions
    global alpha
    alpha+= dt * OMEGA % 360 # stay within [0,360°]
    updates(dt)
    draw()

def toggle(vis):
    for e in [vr, hr]: e.colors = (200,200,200,255*vis)*5
    dot.colors = (255,0,0,255*vis)*5

#-------------------------------- SCENE STUFF ---------------------------------
still  = Sketch()  # 'default' still sketch
wheel  = Sketch()  # 'default' revolving sketch
hslide = Sketch()
vslide = Sketch()

# dot -------------------------------------------------------------------------
dot=batch.add(5, pyglet.gl.GL_LINE_STRIP, wheel,'v2i/static', 'c4B/static')
dot.colors = (255,0,0,255*vis)*5  # vertex list color data, rgba format
dot.vertices = translate([-3, 0, 3, 0, 0, 0, 0, 3, 0, -3], (400-10,0))

# recs ------------------------------------------------------------------------
def rec(w=100, h=100, color=(255,255,255,255), pos=ORIGIN, sk=still):
    rec=batch.add(6, pyglet.gl.GL_TRIANGLES, sk, 'v2f/static', 'c4B/static')
    rec.colors = color*6
    rec.vertices = translate((0,0,0,h,w,h,w,h,w,0,0,0), pos)
    return(rec) # batch.add() returns a vertex_list

gu = int(800/85)  # overall drawing V size is 85 gu and just fits into screen
len, wth, thk = 33 * gu, 11 * gu, 6 * gu  # proportions of the kapla block
white = (255, 255, 255, 255)

# four + 1 horizontal rects
r1 = rec(w=len, h=thk, color=white, pos=(wth/2 + thk, wth/2))
r2 = rec(w=len, h=thk, color=white, pos=(wth/2 + thk, -wth/2-thk))
r3 = rec(w=len, h=thk, color=white, pos=(-len-thk-wth/2, wth/2))
r4 = rec(w=len, h=thk, color=white, pos=(-len-thk-wth/2, -wth/2-thk))
s1 = rec(w=len, h=wth, color=white, pos=(-len/2, -wth/2, 0, 0), sk=hslide)
# four vertical rects
r5 = rec(w=thk, h=len, color=white, pos=(wth/2, wth/2+thk))
r6 = rec(w=thk, h=len, color=white, pos=(-wth/2-thk, wth/2+thk))
r7 = rec(w=thk, h=len, color=white, pos=(wth/2, -len-thk-wth/2))
r8 = rec(w=thk, h=len, color=white, pos=(-wth/2 - thk, -len-thk-wth/2))
s2 = rec(w=wth, h=len, color=white, pos=(-wth/2, -len/2, 0.1, 0), sk=vslide)

vr=batch.add(5, pyglet.gl.GL_LINE_STRIP, vslide, 'v2f/static', 'c4B/static')
vr.colors = (200,200,200,255*vis)*5  # vis = true/false visibility switch
vr.vertices = (-640,-len/2,640,-len/2,640,len/2,-640,len/2,-640, -len/2)

hr=batch.add(5, pyglet.gl.GL_LINE_STRIP, hslide, 'v2f/static', 'c4B/static')
hr.colors = (200,200,200,255*vis)*5  # vis = true/false visibility switch
hr.vertices = (-len/2,-400,len/2,-400,len/2,400,-len/2,400,-len/2, -400)

# updates ---------------------------------------------------------------------
from itertools import cycle
previous_hdir, previous_vdir = 1, 1
BOW = pyglet.media.load('bow.wav', streaming=False)
BOW1 = pyglet.media.load('bow1.wav', streaming=False)
# kapla_colors
redk =(255, 69,   0,   255)  # red kapla
bluk =(  0,  0, 140,   255)  # blue kapla
grnk =(  0, 99,   0,   255)  # green kapla
yelk =(255, 214,  0,   255)  # yellow kapla

target_h = cycle((r2,r1,r3,r4,s1))
target_v = cycle((r5,r6,r8,r7,s2))
h_color = cycle((redk, grnk, bluk, yelk))
v_color = cycle((redk, grnk, bluk, yelk))

def updates(dt):
    global previous_hdir, previous_vdir
    wheel.pos = [wheel.pos[0],wheel.pos[1], alpha]

    cosa = math.cos(alpha*DEG2RAD)
    previous_h_pos = hslide.pos[0]
    hslide.pos = [640+cosa*(640-len/2), hslide.pos[1], 0]
    new_hdir = cmp( previous_h_pos, hslide.pos[0])
    if new_hdir + previous_hdir == 0:
        BOW.play()
        target_h.next().colors = h_color.next()*6
        previous_hdir=new_hdir

    sina = math.sin(alpha*DEG2RAD)
    previous_vslide_pos1 = vslide.pos[1]
    vslide.pos = [vslide.pos[0], 400+sina*(400-len/2), 0]
    new_vdir = cmp( previous_vslide_pos1, vslide.pos[1])
    if new_vdir + previous_vdir == 0:
        BOW1.play()
        target_v.next().colors = v_color.next()*6
        previous_vdir=new_vdir

#---------------------------------- MAIN --------------------------------------
if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
