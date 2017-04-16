#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
"""
simple pyglet animation
msarch - march 2017
http://www.github.com/msarch/py
"""
import math
import pyglet
from pyglet.gl import *

SCREEN = 1280, 800
ORIGIN = [640,400,0]           # x,y = screen center, rotation = 0
RADIUS = 390
PI, TWOPI = math.pi, math.pi * 2
RAD2DEG = 360 / TWOPI
OMEGA = TWOPI * 0.5            # angular velocity (rev/s) : TWOPI/2 = 1/2 rev/s
alpha = 0.0                    # start angle
BLIP = [-3, 0, 3, 0, 0, 0, 0, 3, 0, -3]  # list of vtx for a point (blip style)
#--------------------------------- PYGLET STUFF -------------------------------
batch = pyglet.graphics.Batch()
canvas = pyglet.window.Window(fullscreen=True)
canvas.set_mouse_visible(False)
pyglet.clock.set_fps_limit(60)

glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glClearColor(0,0,0,0)                               # background color

@canvas.event
def on_key_press(symbol, modifiers):
    pyglet.app.exit()

@canvas.event
def on_draw():
    canvas.clear()
    batch.draw()

#------------------------------- DRAWING STUFF --------------------------------
class Sketch(pyglet.graphics.Group):
    def __init__(self,pos=ORIGIN):
        super(Sketch, self).__init__()
        self.pos=pos

    def set_state(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glRotatef(self.pos[2], 0, 0, 1) # degrees,around x, y, z axis

    def unset_state(self):
        glPopMatrix()

wheel= Sketch()

#------------------------------- ACTION STUFF ---------------------------------
def update(dt, *args, **kwargs):
    # yelds sine and cosine values from an uniform circular motion
    global alpha
    alpha += dt * OMEGA
    alpha = alpha % (TWOPI)  # stay within [0,2*Pi]
    rotate_wheel(alpha)

def rotate_wheel(alpha):
        wheel.pos[2] = alpha*RAD2DEG

# dot -------------------------------------------------------------------------
pt=batch.add(5, pyglet.gl.GL_LINE_STRIP, wheel, 'v2i/static', 'c4B/static')
pt.colors = (255,0,0,255)*5
# modifying vertices to reposition dot
pt.vertices = reduce(tuple.__add__, zip( [x+RADIUS for x in BLIP[0::2]],
    [y for y in BLIP[1::2]]))

#----------------------------------- GO ---------------------------------------
if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
