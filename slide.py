#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# simple pyglet animation
# http://www.github.com/msarch/slide

import math
import pyglet
from pyglet.gl import *

PI, TWOPI = math.pi, math.pi * 2
DEG2RAD = TWOPI/360
OMEGA = 360.0 * 0.5 # angular velocity (rev/s) : 1/2 rev/s
ORIGIN = [1280/2,800/2,0]             # x,y = screen center, rotation = 0
RADIUS = 390                          # large circle fitting into screen
status = {'alpha' :0.0, 'revs' : 1 }  # start angle, rev count

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
        glRotatef(self.pos[2], 0, 0, 1) # rot. in degrees; x,y,z of rot. axis

    def unset_state(self):
        glPopMatrix()

wheel= Sketch()  # 'default' sketch

#------------------------------- ACTION STUFF ---------------------------------
def update(dt): # updates an uniform circular motion then calls list of actions
    status['alpha'] += dt * OMEGA
    if status['alpha'] > 360:
        status['alpha'] -= 360  # stay within [0,360°]
        status['revs'] +=1      # another revolution
        print status['revs']
    updates(dt)
    draw()

def updates(dt):
    wheel.pos[2] = status['alpha']
    still.pos[2] = 0

def translate(vtx,dx,dy): # modifying all vertices at once
    return(reduce(tuple.__add__, zip([x+dx for x in vtx[0::2]],
    [y+dy for y in vtx[1::2]])))

#---------------------------------- MAIN --------------------------------------
if __name__ == "__main__":
    # dot ---------------------------------------------------------------------
    pt=batch.add(5, pyglet.gl.GL_LINE_STRIP, wheel,'v2i/static', 'c4B/static')
    pt.colors = (255,0,0,255)*5  # inaccessible color data
    pt.vertices = translate([-3, 0, 3, 0, 0, 0, 0, 3, 0, -3], RADIUS,0)
    # rec ---------------------------------------------------------------------
    still=Sketch()
    red_rec=batch.add(6, pyglet.gl.GL_TRIANGLES, None, 'v2f/static', 'c4B/static')
    red_rec.colors = (255,0,0,230)*6
    red_rec.vertices = (0,0,0,100,100,100,100,100,100,0,0,0)
    # go ----------------------------------------------------------------------
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
