#!/usr/bin/env python

import time
import random
import math

from particles import Particles
from map import Map
from canvas import Canvas
from robot_utils import angleToPoint, euclideanDistance
import robot_utils as ru

WAYPOINTS = [(84,30), (180,30), (180,54), (138,54), (138,168), \
                (114,168), (114,84), (84,84), (84,30)]
STEP_SIZE = 20
US_SENSOR_OFFSET = 3.5
DISTANCE_EPSILON = 3.0

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

def turnToWaypoint(waypoint, particles, my_map, canvas):
    position = particles.get_position()

    rotation = angleToPoint(position, waypoint)

    if (rotation > 180):
        ru.turnRight(360 - rotation)
    else:
        ru.turnLeft(rotation)

    particles.update_after_rotation(rotation)

    update_particles_from_reading(particles, my_map, canvas)

def travelToWaypoint(waypoint, particles, my_map, canvas):
    position = particles.get_position()
    if(euclideanDistance(position, waypoint) < DISTANCE_EPSILON):
        return

    turnToWaypoint(waypoint, particles, my_map, canvas)

    position = particles.get_position()

    distance = euclideanDistance(position, waypoint)
    move_amount = min(STEP_SIZE, distance)
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
        time.sleep(0.05)

    z = ru.median(readings) + US_SENSOR_OFFSET

    particles.weight_update(z, my_map)
    canvas.draw_particles(particles)

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

    for waypoint in WAYPOINTS[1:]:
        travelToWaypoint(waypoint, particles, my_map, canvas)

    turnToWaypoint(WAYPOINTS[1], particles, my_map, canvas)


    ru.done()
