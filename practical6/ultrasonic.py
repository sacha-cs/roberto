import robot_utils as ru
import math
import threading

orentation = None
orentationChanged = False
orentationLock = None
rotating = False
rotatingLock = None

resultsQueue = None

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
    with orentationLock:
        orentation = fixAngle(diff)
        orentationChanged = True
    
def setRotating(r):
    with rotatingLock:
        rotating = r

def getAngleFor(pos):
    quadrant = orentation/(math.pi/2)
    if(pos == LEFT):
        return fixAngle(max(math.floor(quadrant), math.ceil(quadrant)) * math.pi/2 - orentation)
    if(pos == RIGHT):
        return fixAngle(min(math.floor(quadrant), math.ceil(quadrant)) * math.pi/2 - orentation)

def getClosest():
    currentRotation = fixAngle(ru.interface.getMotorAngle(ru.sensorMotor[0])[0])
    left = diffAngle(currentRotation, getAngleFor(LEFT))
    right = diffAngle(currentRotation, getAngleFor(RIGHT))

    return abs(left) < abs(right) ? LEFT : RIGHT

def rotateTo(pos):
    currentRotation = fixAngle(ru.interface.getMotorAngle(ru.sensorMotor[0])[0])
    diff = diffAngle(currentRotation, getAngleFor(pos))
    ru.rotateSensor(math.degrees(diff), wait=False)

def getOpposite(pos):
    if pos == LEFT: return RIGHT;
    if pos == RIGHT: return LEFT;

def main():
    resultsQueue = threading.Queue()
    orentationLock = threading.Lock()
    while True:
        with orentationLock:
            if not orentation == None:
                break
        time.sleep(0.1)
    
    while True:
        rotateTo(dest)
        while not ru.interface.motorAngleReferenceReached(ru.sensorMotor[0]):
            needToRestart = False
            with orentationLock:
                if(orentationChanged):
                    orentationChanged = False
                    needToRestart = True
            if(needToRestart):
                dest = getClosest()
                continue

        needToRestart = False
        while True:
            with rotatingLock:
                if not rotating:
                    break;
                else:
                    needToRestart = True

        if(needToRestart):
            dest = getClosest()
            continue

        reading = ru.getUltrasonicMedian(values=3)
        resultsQueue.put((reading, getAngleFor(dest)))

        dest = getOpposite(dest)
