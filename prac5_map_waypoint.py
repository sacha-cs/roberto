#!/usr/bin/env python 

import time
import random
import math

from practical5.particles import Particles
from practical5.map import Map
from practical5.canvas import Canvas
from practical4.navigate import angleToPoint, euclideanDistance
import Practical2.robot_utils as ru

WAYPOINTS = [(84,30), (180,30), (180,54), (138,54), (138,168), \
                (114,168), (114,84), (84,84), (84,30)]

def add_walls(my_map):
    my_map.add_wall((0,0,0,168))        # a: O to A
    my_map.add_wall((0,168,84,168))     # b: A to B
    my_map.add_wall((84,126,84,210))    # c: C to D
    my_map.add_wall((84,210,168,210))   # d: D to E
    my_map.add_wall((168,210,168,84))   # e: E to F
    my_map.add_wall((168,84,210,84))    # f: F to G
    my_map.add_wall((210,84,210,0))     # g: G to H
    my_map.add_wall((210,0,0,0))        # h: H to O

def travelToWaypoint(rotation, distance):
    if (rotation > 180):
        ru.turnRight(360 - rotation)
    else:
        ru.turnLeft(rotation)
    ru.move(distance)

if __name__ == '__main__':
    ru.start()
    canvas = Canvas()

    map = Map()
    add_walls(map)
    canvas.draw_map(map)

    init_pos = WAYPOINTS[0]
    particles = Particles(x=init_pos[0], y=init_pos[1], theta=0)

    position = particles.get_position()
    canvas.draw_particles(particles)

    for waypoint in WAYPOINTS[1:]:
        rotation = angleToPoint(position, waypoint)
        distance = euclideanDistance(position, waypoint)

        travelToWaypoint(rotation, distance)
        particles.update_after_rotation(rotation)
        particles.update_after_straight_line(distance)
        
        canvas.draw_particles(particles)

        position = particles.get_position()

    ru.done()
