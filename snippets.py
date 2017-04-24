# dot -------------------------------------------------------------------------
pt=batch.add(5, pyglet.gl.GL_LINE_STRIP, wheel,'v2i/static', 'c4B/static')
pt.colors = (255,0,0,255)*5  # inaccessible color data
pt.vertices = translate([-3, 0, 3, 0, 0, 0, 0, 3, 0, -3], RADIUS,0)

# rec -------------------------------------------------------------------------
red_rec=batch.add(6, pyglet.gl.GL_TRIANGLES, still, 'v2f/static', 'c4B/static')
red_rec.colors = (255,0,0,230)*6
red_rec.vertices = (0,0,0,100,100,100,100,100,100,0,0,0)

# rec outline -----------------------------------------------------------------
red_rec=batch.add(5, pyglet.gl.GL_LINE_STRIP, still, 'v2f/static', 'c4B/static')
red_rec.colors = (255,0,0,230)*5
red_rec.vertices = (0,0,0,w,w,h,0,h,0,0)


# rec function ----------------------------------------------------------------
def rec(w=100, h=100, color=(255,255,255,255), pos=ORIGIN, sk=still):
    rec=batch.add(6, pyglet.gl.GL_TRIANGLES, sk, 'v2f/static', 'c4B/static')
    rec.colors = color*6
    rec.vertices = translate((0,0,0,h,w,h,w,h,w,0,0,0), pos)
    return(rec) # batch.add() returns a vertex_list

rec_1 = rec(w=width, h=height, color=white, pos=(pox_x, pos_y))

# colors ----------------------------------------------------------------------
orange  =(255, 127,   0, 255)
white   =(255, 255, 255, 255)
black   =(  0,   0,   0, 255)
yellow  =(255, 255,   0, 255)
red     =(255,   0,   0, 255)
blue    =(127, 127, 255, 255)
blue50  =(127, 127, 255, 127)
pink    =(255, 187, 187, 255)
very_light_grey =(242, 242, 242, 255)

# kapla_colors
r_k =(255, 69,   0,   255)  # red kapla
b_k =(  0,  0, 140,   255)  # blue kapla
g_k =(  0, 99,   0,   255)  # green kapla
y_k =(255, 214,  0,   255)  # yellow kapla
kapla_colors=(r_k, g_k, b_k, y_k, b_k)  # addded 1 color for pb  w 4 kaplas     TODO

# pyglet clock ----------------------------------------------------------------

# Schedule a function to be called every frame.
schedule(self, func, *args, **kwargs)
# Schedule a function to be called every interval seconds.
schedule_interval(self, func, interval, *args, **kwargs)
# Schedule a function to be called every interval seconds, beginning at a time that does not coincide with other scheduled events.
schedule_interval_soft(self, func, interval, *args, **kwargs)
# Schedule a function to be called once after delay seconds.
schedule_once(self, func, delay, *args, **kwargs)
# Remove a function from the schedule.
unschedule(self, func)
