import brickpi
import time

interface = brickpi.Interface()
motors = [0,1]

def setupInterface():
	interface.initialize()

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

RADIANS_40CM = 14.67
def move(distance):
	radians = distance / 40.0 * RADIANS_40CM
	interface.increaseMotorAngleReferences(motors,[radians,radians])

RADIANS_90DEG = 4.40
def turnLeft(deg):
	radians = deg/90 * RADIANS_90DEG
	interface.increaseMotorAngleReferences(motors,[radians,-radians])

def turnRight(deg):
	radians = deg/90 * RADIANS_90DEG
	interface.increaseMotorAngleReferences(motors,[-radians,radians])

def waitUntilStopped(verbose=False):
	while not interface.motorAngleReferencesReached(motors):
		if(verbose):
			motorAngles = interface.getMotorAngles(motors)
			if motorAngles:
				print "motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)

	if(verbose):
		print("Destination Reached!")
	time.sleep(2)


def done():
	interface.terminate()
