import math
import Practical2.robot_utils as ru
from matrixUtils import matmult, transpose, rotationMatrix

def getWaypoint():
    return map(float, raw_input().strip().split(' '))

def receiveWaypoints():
    position = [[0],[0]]
    rotationMat = [[1,0],[0,1]]
    while(True):
        waypoint = getWaypoint()
        print "world waypoint: ", waypoint
        waypoint = matmult(rotationMat, transpose(waypoint))
        print "waypoint after rotation: ", waypoint
        rotation = angleToPoint(position, waypoint)
        distance = euclideanDistance(position, waypoint)
        print 'rotation', rotation
        print 'distance', distance
        #travelToWaypoint(rotation, distance)
        position = waypoint
        print 'new position: ', position
        rotationMat = matmult(rotationMatrix(rotation), rotationMat)
        print 'rotationMat: ', rotationMat

def euclideanDistance(p1, p2):
    x1 = p1[0][0]
    y1 = p1[1][0]
    x2 = p2[0][0]
    y2 = p2[1][0]
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def angleToPoint(original, target):
    x1 = original[0][0]
    y1 = original[1][0]
    x2 = target[0][0]
    y2 = target[1][0]
    dx = x2 - x1  # targetX - originalX
    dy = y2 - y1  # targetY - originalY
    if (dx > 0 and dy > 0):    # Q1
        return math.degrees(math.atan(dy/dx))
    elif (dx < 0 and dy > 0):  # Q2
        return 90 + math.degrees(math.atan(abs(dy/dx)))
    elif (dx < 0 and dy < 0):  # Q3
        return 180 + math.degrees(math.atan(abs(dy/dx)))
    elif (dx > 0 and dy < 0):  # Q4
        return 360 - math.degrees(math.atan(abs(dy/dx)))
    elif (dy == 0):  # x-axis
        if (dx >= 0):
            return 0
        else:  # dx < 0
            return 180
    elif (dx == 0):  # y-axis
        if (dy > 0):
            return 90
        elif (dy == 0):
            return 0
        else:  # dy < 0
            return 270

def travelToWaypoint(rotation, distance):
    ru.turnLeft(rotation)
    ru.move(distance * 100)  # convert m to cm

if __name__ == '__main__':
    ru.start()
    receiveWaypoints()

