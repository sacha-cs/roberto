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
ANGLE_LIMIT = 30
US_SENSOR_OFFSET = 3

def add_walls(my_map):
    my_map.add_wall((0,0,0,168))        # a: O to A
    my_map.add_wall((0,168,84,168))     # b: A to B
    my_map.add_wall((84,126,84,210))    # c: C to D
    my_map.add_wall((84,210,168,210))   # d: D to E
    my_map.add_wall((168,210,168,84))   # e: E to F
    my_map.add_wall((168,84,210,84))    # f: F to G
    my_map.add_wall((210,84,210,0))     # g: G to H
    my_map.add_wall((210,0,0,0))        # h: H to O

def draw_path(canvas):
    for i in xrange(len(WAYPOINTS)-1):
        start = WAYPOINTS[i]
        end = WAYPOINTS[i+1]
        canvas.draw_line((start[0], start[1], end[0], end[1]))

DISTANCE_EPSILON_SQUARED = 0.5
def travelToWaypoint(waypoint, particles, my_map, canvas):
    position = particles.get_position()
    if(((position[0] - waypoint[0])**2 + (position[1] - waypoint[1])**2) < DISTANCE_EPSILON_SQUARED):
        return

    rotation = angleToPoint(position, waypoint)

    if (rotation > 180):
        ru.turnRight(360 - rotation)
    else:
        ru.turnLeft(rotation)

    particles.update_after_rotation(rotation)
    
    update_particles_from_reading(particles, my_map, canvas)

    position = particles.get_position()
    distance = euclideanDistance(position, waypoint)

    move_amount = min(STEP_SIZE, distance)
    distance -= move_amount
    ru.move(move_amount)
    measurement_update(move_amount, particles, my_map, canvas)
    canvas.draw_particles(particles)
    travelToWaypoint(waypoint, particles, my_map, canvas)

def measurement_update(distance, particles, my_map, canvas):
    particles.update_after_straight_line(distance)
    canvas.draw_particles(particles)
    update_particles_from_reading(particles, my_map, canvas)

def update_particles_from_reading(particles, my_map, canvas):
    # Get z (sensor measurement)
    readings = []
    while (len(readings) < 5):
        usReading = ru.getUltrasonicSensor(2)
        readings.append(usReading)
        time.sleep(0.1)

    z = ru.median(readings) + US_SENSOR_OFFSET

    particles.weight_update(z, my_map)
    canvas.draw_particles(particles)

    time.sleep(1)

    particles.resample()
    canvas.draw_particles(particles)

if __name__ == '__main__':
    ru.start()
    canvas = Canvas()

    my_map = Map()
    add_walls(my_map)
    canvas.draw_map(my_map)

    draw_path(canvas)

    init_pos = WAYPOINTS[0]
    particles = Particles(x=init_pos[0], y=init_pos[1], theta=0)
    canvas.draw_particles(particles)
    position = particles.get_position()

    for waypoint in WAYPOINTS[1:]:
        travelToWaypoint(waypoint, particles, my_map, canvas)
        #canvas.draw_particles(particles)

        # 2 - Measurement update

        position = particles.get_position()


    ru.done()
