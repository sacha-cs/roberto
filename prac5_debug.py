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
STEP_SIZE = 20
ANGLE_LIMIT = 15

def add_walls(my_map):
    my_map.add_wall((0,0,0,168))        # a: O to A
    my_map.add_wall((0,168,84,168))     # b: A to B
    my_map.add_wall((84,126,84,210))    # c: C to D
    my_map.add_wall((84,210,168,210))   # d: D to E
    my_map.add_wall((168,210,168,84))   # e: E to F
    my_map.add_wall((168,84,210,84))    # f: F to G
    my_map.add_wall((210,84,210,0))     # g: G to H
    my_map.add_wall((210,0,0,0))        # h: H to O

def travelToWaypoint(rotation, distance, particles, my_map):
    steps = distance // STEP_SIZE
    remainder = distance % STEP_SIZE

    if (rotation > 180):
        ru.turnRight(360 - rotation)
    else:
        ru.turnLeft(rotation)

    particles.update_after_rotation(rotation)

    for i in xrange(int(steps)):
        ru.move(STEP_SIZE)
        measurement_update(STEP_SIZE, particles, my_map)
    
    ru.move(remainder)
    measurement_update(remainder, particles, my_map)

def measurement_update(distance, particles, my_map):
    particles.update_after_straight_line(distance)
    pos = particles.get_position()
    m, incid_ang = my_map.get_distance_to_wall(pos[0], pos[1], pos[2])
    if (incid_ang <= ANGLE_LIMIT):
        # Get z (sensor measurement)
        readings = []
        while (len(readings) < 5):
            usReading = ru.getUltrasonicSensor(2)
            readings.insert(0, usReading)

        z = ru.median(readings)
        print "z = ", z
        print "m = ", m

        particles.weight_update(z, m)
        particles.resample()

if __name__ == '__main__':
    #ru.start()i
    canvas = Canvas()

    my_map = Map()
    add_walls(my_map)

    print "Distance: ", my_map.get_distance_to_wall(114.03757539971585, 167.96543693886713, 540.1869889031709)
    #canvas.draw_map(my_map)

    #init_pos = WAYPOINTS[0]
    #particles = Particles(x=init_pos[0], y=init_pos[1], theta=0)

    #position = particles.get_position()
    #canvas.draw_particles(particles)

    #for waypoint in WAYPOINTS[1:]:
     #   # 1 - Motion prediction
     #   print "Position: ", position
     #   rotation = angleToPoint(position, waypoint)
     #   distance = euclideanDistance(position, waypoint)

     #   travelToWaypoint(rotation, distance, particles, my_map)
     #   canvas.draw_particles(particles)

        # 2 - Measurement update
        # TODO: get ground truth value m and incidence angle
        
    #    position = particles.get_position()


    #ru.done()
