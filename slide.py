#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# simple pyglet animation
# http://www.github.com/msarch/slide

import math
import pyglet
from pyglet.gl import *

SCREEN = 1280, 800
ORIGIN = [640,400,0]             # x,y = screen center, rotation = 0
PI, TWOPI = math.pi, math.pi * 2
RAD2DEG = 360 / TWOPI
OMEGA = TWOPI * 0.5              # angular velocity (rev/s) : TWOPI/2=1/2 rev/s
RADIUS = 390
alpha = 0.0                      # start angle

#--------------------------------- PYGLET STUFF -------------------------------
batch = pyglet.graphics.Batch()
canvas = pyglet.window.Window(fullscreen=True)
canvas.set_mouse_visible(False)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glClearColor(0,0,0,0)  # background color

@canvas.event
def on_key_press(symbol, modifiers):
    pyglet.app.exit()

@canvas.event
def draw():
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

wheel= Sketch()  # 'default' sketch
#------------------------------- ACTION STUFF ---------------------------------
def update(dt, *args, **kwargs):
    # yelds sine and cosine values from an uniform circular motion
    global alpha
    alpha = (alpha + (dt * OMEGA)) % TWOPI  # stay within [0,2*Pi]
    wheel.pos[2] = alpha*RAD2DEG
    draw()

def translate(vtx,dx,dy): # modifying all vertices at once
    return(reduce(tuple.__add__, zip([x+dx for x in vtx[0::2]],
    [y+dy for y in vtx[1::2]])))

#---------------------------------- MAIN --------------------------------------
if __name__ == "__main__":
    # dot ---------------------------------------------------------------------
    pt=batch.add(5, pyglet.gl.GL_LINE_STRIP, wheel,'v2i/static', 'c4B/static')
    pt.colors = (255,0,0,255)*5  # inaccessible color data
    pt.vertices = translate([-3, 0, 3, 0, 0, 0, 0, 3, 0, -3], RADIUS,0)
    # go ----------------------------------------------------------------------
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
