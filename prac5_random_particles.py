#!/usr/bin/env python 

import time
import random
import math

from practical5.particles import Particles
from practical5.map import Map
from practical5.canvas import Canvas

def add_walls(map):
    map.add_wall((0,0,0,168))        # a: O to A
    map.add_wall((0,168,84,168))     # b: A to B
    map.add_wall((84,126,84,210))    # c: C to D
    map.add_wall((84,210,168,210))   # d: D to E
    map.add_wall((168,210,168,84))   # e: E to F
    map.add_wall((168,84,210,84))    # f: F to G
    map.add_wall((210,84,210,0))     # g: G to H
    map.add_wall((210,0,0,0))        # h: H to O

canvas = Canvas()

map = Map()
add_walls(map)
canvas.draw_map(map)

particles = Particles()

t = 0
while True:
    canvas.draw_particles(particles)
    particles.update(t)
    t += 0.05
    time.sleep(0.05)

