import robot_utils as ru
import math
import threading
from Queue import Queue
import time

orientation = None
orientationChanged = False
rotating = False
resultsQueue = Queue()
orientationLock = threading.Lock()
rotatingLock = threading.Lock()

LEFT = 1
RIGHT = -1

direction = 1
dest = LEFT

def diffAngle(curr, target):
    return fixAngle(target-curr)

def fixAngle(angle):
    while angle > math.pi: angle -= 2 * math.pi
    while angle <= -math.pi: angle += 2 * math.pi
    return angle

def updateOrentation(o):
    global orientation, orientationChanged
    with orientationLock:
        orientation = fixAngle(o)
        orientationChanged = True
    
def setRotating(r):
    global rotating
    with rotatingLock:
        rotating = r

def getAngleFor(pos):
    quadrant = orientation/(math.pi/2)
    if(pos == LEFT):
        return fixAngle(max(math.floor(quadrant), math.ceil(quadrant)) * math.pi/2 - orientation)
    if(pos == RIGHT):
        return fixAngle(min(math.floor(quadrant), math.ceil(quadrant)) * math.pi/2 - orientation)

def getClosest():
    currentRotation = fixAngle(ru.interface.getMotorAngle(ru.sensorMotor[0])[0])
    left = diffAngle(currentRotation, getAngleFor(LEFT))
    right = diffAngle(currentRotation, getAngleFor(RIGHT))

    if(abs(left) < abs(right)): return LEFT
    else: return RIGHT

def rotateTo(pos):
    currentRotation = ru.interface.getMotorAngle(ru.sensorMotor[0])[0]
    print "current: ", currentRotation
    diff = diffAngle(currentRotation, getAngleFor(pos))
    print "to turn: ", diff
    ru.rotateSensor(math.degrees(diff), wait=False)
    return diff + currentRotation

def getOpposite(pos):
    if pos == LEFT: return RIGHT;
    if pos == RIGHT: return LEFT;

def toDegrees(rads):
    if(rads < 0):
        rads += 2 * math.pi
    return math.degrees(rads)

def main():
    global orientation, orientationChanged, rotating, resultsQueue, orientationLock, rotatingLock
    while True:
        with orientationLock:
            if not orientation == None:
                orientationChanged = False
                break
        print "No orientation"
        time.sleep(1)
    
    dest = getClosest()
    while True:
        to = rotateTo(dest)
        while abs(ru.interface.getMotorAngle(ru.sensorMotor[0])[0] - to) < 0.001:
            needToRestart = False
            with orientationLock:
                if(orientationChanged):
                    orientationChanged = False
                    needToRestart = True
            if(needToRestart):
                print "Restarting before getting there"
                dest = getClosest()
                to = rotateTo(dest)
                print ru.interface.getMotorAngle(ru.sensorMotor[0])[0], to

        needToRestart = False
        while True:
            with rotatingLock:
                if not rotating:
                    print "Not rotating!"
                    break;
                else:
                    needToRestart = True

        if(needToRestart):
            print "Restarting because we rotated"
            dest = getClosest()
            continue

        print "Getting a reading!"
        reading = ru.getUltrasonicMedian(values=3)
        print "Got a reading!"
        resultsQueue.put((reading, toDegrees(getAngleFor(dest))))

        dest = getOpposite(dest)
