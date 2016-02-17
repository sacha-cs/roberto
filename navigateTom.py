import math
import Practical2.robot_utils as ru
from matrixUtils import matmult, transpose, rotationMatrix

def getWaypoint():
    return map(float, raw_input().strip().split(' '))

def receiveWaypoints():
    # [x, y, theta]
    position = [0,0,0]
    while(True):
        waypoint = getWaypoint()
        print "world waypoint: ", waypoint
        rotation = angleToPoint(position, waypoint)
        distance = euclideanDistance(position, waypoint)
        print 'rotation', rotation
        print 'distance', distance
        travelToWaypoint(rotation, distance)
        position = [waypoint[0], waypoint[1], position[2]+rotation]
        print 'new position: ', position

def euclideanDistance(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def norm(p):
    x = p[0]
    y = p[1]
    return math.sqrt(x**2 + y**2)

def angleToPoint(original, target):
    x1 = original[0]
    y1 = original[1]
    # angle robot is to world coords
    t1 = math.radians(original[2])
    x2 = target[0]
    y2 = target[1]
    Vx = x2 - x1 # V vector 
    Vy = y2 - y1 
    Ux = math.cos(t1) # U vector
    Uy = math.sin(t1)
    a = (Ux * Vx + Uy * Vy) / (norm([Ux, Uy]) * norm([Vx, Vy]))
    a = math.acos(a)
    return math.degrees(a)

def travelToWaypoint(rotation, distance):
    ru.turnLeft(rotation)
    ru.move(distance * 100)  # convert m to cm

if __name__ == '__main__':
    ru.start()
    receiveWaypoints()

