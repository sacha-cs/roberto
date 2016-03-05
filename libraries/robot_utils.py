import brickpi

import time
import math

CONTROL_ANGLE = 0
CONTROL_VELOCITY = 1

interface = None
motors = [0,1]
sensorMotor = [3]
sensorPort = 2

def median(l):
    sortedl = sorted(l)
    index = (len(l) - 1) // 2

    if (len(l) % 2 == 1):
        return float(sortedl[index])
    return (sortedl[index] + sortedl[index+1])/2.0;

def mode(l):
    buckets = {}
    for num in l:
        if(num in buckets):
            buckets[num]+=1
        else:
            buckets[num] = 1
    highest = l[0]
    highval = 0
    for num in buckets.keys():
        if(buckets[num] > highval):
            highval = buckets[num]
            highest = num
    return num

def start(control=CONTROL_ANGLE):
    global interface;
    interface = brickpi.Interface()
    interface.initialize()
    setupMotors(control)
    setupSensors()

def setupSensors():
    interface.sensorEnable(2, brickpi.SensorType.SENSOR_ULTRASONIC)

def setupMotors(control=CONTROL_ANGLE):
    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])
    interface.motorEnable(sensorMotor[0])

    # motor parameters values for wheel motors
    motorParams = interface.MotorAngleControllerParameters()
    motorParams.maxRotationAcceleration = 7.5
    motorParams.maxRotationSpeed = 15.0
    motorParams.feedForwardGain = 255/20.0
    motorParams.minPWM = 18.0
    motorParams.pidParameters.minOutput = -255
    motorParams.pidParameters.maxOutput = 255
    motorParams.pidParameters.k_p = 400
    motorParams.pidParameters.k_d = 0

    if(control == CONTROL_ANGLE):
        motorParams.pidParameters.k_i = 1000.0
    elif(control == CONTROL_VELOCITY):
        motorParams.pidParameters.k_i = 25.0

    # motor parameters values for sensor motor
    sensorMotorParams = interface.MotorAngleControllerParameters()
    sensorMotorParams.maxRotationAcceleration = 7.5
    sensorMotorParams.maxRotationSpeed = 3.0
    sensorMotorParams.feedForwardGain = 255/20.0
    sensorMotorParams.minPWM = 0.0
    sensorMotorParams.pidParameters.minOutput = -255
    sensorMotorParams.pidParameters.maxOutput = 255
    sensorMotorParams.pidParameters.k_p = 50.0
    sensorMotorParams.pidParameters.k_i = 0.0
    sensorMotorParams.pidParameters.k_d = 0

    interface.setMotorAngleControllerParameters(motors[0],motorParams)
    interface.setMotorAngleControllerParameters(motors[1],motorParams)

    interface.setMotorAngleControllerParameters(sensorMotor[0],sensorMotorParams)

RADIANS_40CM = 11.67
def move(distance, verbose=False, wait=True, sleepAfter=True):
    radians = distance / 40.0 * RADIANS_40CM
    interface.increaseMotorAngleReferences(motors,[radians,radians])
    if (wait):
        waitUntilStopped(verbose, sleepAfter)

RADIANS_90DEG = 3.8
def turnRight(deg, verbose=False, wait=True, sleepAfter=True):
    radians = deg / 90.0 * RADIANS_90DEG
    interface.increaseMotorAngleReferences(motors,[radians,-radians])
    if wait:
        waitUntilStopped(verbose, sleepAfter)

def turnLeft(deg, verbose=False, wait=True, sleepAfter=True):
    radians = deg / 90.0 * RADIANS_90DEG
    interface.increaseMotorAngleReferences(motors,[-radians,radians])
    if wait:
        waitUntilStopped(verbose, sleepAfter)

RADIANS_90DEG_SENSOR = 1.63
def rotateSensor(deg, verbose=False, wait=True, sleepAfter=True):
    radians = deg / 90.0 * RADIANS_90DEG_SENSOR
    interface.increaseMotorAngleReferences(sensorMotor, [radians])
    if wait:
        waitUntilStopped(verbose, sleepAfter, motors=sensorMotor)

def waitUntilStopped(verbose=False, sleepAfter=True, motors=[0,1]):
    while not interface.motorAngleReferencesReached(motors):
        if(verbose):
            motorAngles = interface.getMotorAngles(motors)
            if motorAngles:
                if len(motors) > 1:
                    print "motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
                else:
                    print "motor angles: ", motorAngles[0][0]
        time.sleep(0.1)

    if(verbose):
        print("Destination Reached!")
    if(sleepAfter):
        time.sleep(1)

def stop():
    interface.motorDisable(0)
    interface.motorDisable(1)
    setupMotors()

def getTouchSensor(port):
    result = interface.getSensorValue(port)
    if(result):
        return result[0]
    print "Error: couldn't get touch sensor result for port " + str(port)
    return False

def getUltrasonicMedian(port=sensorPort, values=5, sleepTime=0.05):
    readings = []
    for _ in xrange(values):
        readings.append(getUltrasonicSensor())
        time.sleep(sleepTime)
    print(readings)
    return median(readings)


#TODO: multithread this to get a median value of the last n results
def getUltrasonicSensor(port=sensorPort):
    usReading = interface.getSensorValue(port)

    if usReading :
        return usReading[0]
    else:
        print "Failed US reading"
    return 255

WAYPOINTS = [(84,30), (180,30), (180,54), (138,54), (138,168)]
def getShortestPath(waypoint_index, num_waypoints=5):
    waypoint_indicies = range(num_waypoints)
    return waypoint_indicies[waypoint_index+1:] + waypoint_indicies[:waypoint_index+1]


def euclideanDistance(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def checkAngle(a):
    return a % 360

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
    a = math.atan2(Ux,Uy) - math.atan2(Vx,Vy)
    return checkAngle(math.degrees(a))

def travelToWaypoint(rotation, distance):
    if (rotation > 180):
        ru.turnRight(360 - rotation)
    else:
        ru.turnLeft(rotation)
    ru.move(distance * 100)  # convert m to cm

if __name__ == '__main__':
    print getShortestPath(2)

def done():
    interface.terminate()
