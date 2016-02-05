import brickpi
import time

interface = brickpi.Interface()
motors = [0,1]

def start():
    interface.initialize()
    setupMotors()
    setupSensors()

def setupSensors():
    interface.sensorEnable(0, brickpi.SensorType.SENSOR_TOUCH)
    interface.sensorEnable(1, brickpi.SensorType.SENSOR_TOUCH)    
    

def setupMotors():
    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])

    motorParams = interface.MotorAngleControllerParameters()
    motorParams.maxRotationAcceleration = 7.5
    motorParams.maxRotationSpeed = 11.5
    motorParams.feedForwardGain = 255/20.0
    motorParams.minPWM = 18.0
    motorParams.pidParameters.minOutput = -255
    motorParams.pidParameters.maxOutput = 255
    motorParams.pidParameters.k_p = 0.6 * 700.0
    motorParams.pidParameters.k_i = 1000.0
    motorParams.pidParameters.k_d = 15.75
    
    interface.setMotorAngleControllerParameters(motors[0],motorParams)
    interface.setMotorAngleControllerParameters(motors[1],motorParams)

RADIANS_40CM = 14.72
def move(distance, verbose=False, wait=True):
    radians = distance / 40.0 * RADIANS_40CM
    interface.increaseMotorAngleReferences(motors,[radians,radians])
    if (wait):
        waitUntilStopped(verbose)

RADIANS_90DEG = 4.72
def turnLeft(deg, verbose=False, wait=True):
    radians = deg/90.0 * RADIANS_90DEG
    interface.increaseMotorAngleReferences(motors,[radians,-radians])
    if wait:
        waitUntilStopped(verbose)

def turnRight(deg, verbose=False, wait=True):
    radians = deg/90.0 * RADIANS_90DEG
    interface.increaseMotorAngleReferences(motors,[-radians,radians])
    if wait:
        waitUntilStopped(verbose)

def waitUntilStopped(verbose=False):
    while not interface.motorAngleReferencesReached(motors):
        if(verbose):
            motorAngles = interface.getMotorAngles(motors)
            if motorAngles:
                print "motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
        time.sleep(0.1)

    if(verbose):
        print("Destination Reached!")
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

def done():
    interface.terminate()
