#!/usr/bin/env python 

import time
import random
import math

from Particles import Particles
from Map import Map
from Canvas import Canvas

canvas = Canvas()

mymap = Map();
mymap.add_wall((0,0,0,168));        # a: O to A
mymap.add_wall((0,168,84,168));     # b: A to B
mymap.add_wall((84,126,84,210));    # c: C to D
mymap.add_wall((84,210,168,210));   # d: D to E
mymap.add_wall((168,210,168,84));   # e: E to F
mymap.add_wall((168,84,210,84));    # f: F to G
mymap.add_wall((210,84,210,0));     # g: G to H
mymap.add_wall((210,0,0,0));        # h: H to O

canvas.draw_map(mymap)

particles = Particles();

t = 0;
while True:
    particles.update(t); 
    canvas.draw_particles(particles)
    t += 0.05;
    time.sleep(0.05);

