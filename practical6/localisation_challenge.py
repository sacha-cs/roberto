#!/usr/bin/env python

import time
import random
import math

from particles import Particles
from map import Map
from canvas import Canvas
import robot_utils as ru
from rec_signature import identify_location
import ultrasonic

import threading

WAYPOINTS = [(84,30), (180,30), (180,54), (138,54), (138,168)]
STEP_SIZE = 20
US_SENSOR_OFFSET = 3.5
DISTANCE_EPSILON = 3.0

def get_angle_diff(a1, a2):
    diff = a1 - a2
    while diff < 0: diff += 360
    while diff > 360: diff -= 360
    return diff

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
        if(i == 0):
            lastPoint = WAYPOINTS[len(WAYPOINTS)-1]
            canvas.draw_line((start[0], start[1], lastPoint[0], lastPoint[1]))
        canvas.draw_line((start[0], start[1], end[0], end[1]))


def turnToWaypoint(waypoint, particles, my_map, canvas):
    position = particles.get_position()

    rotation = ru.angleToPoint(position, waypoint)

    if (rotation > 180):
        ru.turnRight(360 - rotation)
    else:
        ru.turnLeft(rotation)

    particles.update_after_rotation(rotation)

    #update_particles_from_reading(particles, my_map, canvas)

def travelToWaypoint(waypoint, particles, my_map, canvas):
    position = particles.get_position()
    if(ru.euclideanDistance(position, waypoint) < DISTANCE_EPSILON):
        return

    ultrasonic.setRotating(True)
    turnToWaypoint(waypoint, particles, my_map, canvas)
    ultrasonic.setRotating(False)

    position = particles.get_position()

    distance = ru.euclideanDistance(position, waypoint)
    startAngles = ru.interface.getMotorAngles(ru.motors)
    ru.move(distance, wait=False)

    while not interface.motorAngleReferencesReached(ru.motors):
        (reading, orentation) = ultrasonic.resultsQueue.get()
        angles = ru.interface.getMotorAngles(ru.motors)
        radians = ((angles[0][0] - startAngles[0][0]) + 
                   (angles[1][0] - startAngles[1][0]))/2;
        travelled = radians / ru.RADIANS_40CM * 40.0
        measurement_update(travelled, reading, get_angle_diff(orentation, position[2]), particles, my_map, canvas)
        position = particles.get_position()
        canvas.draw_particles(particles)
        distanceLeft = distance - travelled
        estimatedEnd = (position[0] + math.cos(math.radians(position[2])) * distanceLeft,
                        position[1] + math.sin(math.radians(position[2])) * distanceLeft, 
                        position[2])
        if(euclideanDistance(estimatedEnd, waypoint) > DISTANCE_EPSILON)):
            travelToWaypoint(waypoint, particles, my_map, canvas)

    travelToWaypoint(waypoint, particles, my_map, canvas)

def measurement_update(distance, reading, orentation, particles, my_map, canvas):
    particles.update_after_straight_line(distance)
    update_particles_from_reading(particles, reading, orentation, my_map, canvas)

def update_particles_from_reading(particles, reading, orentation, my_map, canvas):
    z = reading + US_SENSOR_OFFSET

    particles.weight_update(z, orentation,  my_map)
    particles.resample()
    canvas.draw_particles(particles)

if __name__ == '__main__':
    ru.start()
    canvas = Canvas()

    my_map = Map()
    add_walls(my_map)
    canvas.draw_map(my_map)

    draw_path(canvas)

    usThread = threading.Thread(target=ultrasonic.main)
    usThread.start()

    rec_location, orientation = identify_location()
    init_pos = WAYPOINTS[rec_location]

    print "\nRoberto is at waypoint ", rec_location+1, " orientation ", orientation
    
    usThread.updateOrentation(orentation)

    particles = Particles(x=init_pos[0], y=init_pos[1], theta=0)
    particles.update_after_recognition(orientation)
    canvas.draw_particles(particles)

    waypoints = ru.getShortestPath(rec_location)

    for waypoint in waypoints:
        print "\nNavigating to waypoint ", waypoint+1
        travelToWaypoint(WAYPOINTS[waypoint], particles, my_map, canvas)
        print "Reached destination"
        time.sleep(1)

    ru.done()
