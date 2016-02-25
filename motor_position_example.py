import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 6.0
motorParams.maxRotationSpeed = 11.0
motorParams.feedForwardGain = 255/20.0
motorParams.minPWM = 1.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 400 #700
motorParams.pidParameters.k_i = 1000
motorParams.pidParameters.k_d = 0

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)


while True:

	angle = float(input("Enter a angle to rotate (in radians): "))
	
	interface.startLogging('../roberto/logfile')
	interface.increaseMotorAngleReferences(motors,[angle,angle])

	while not interface.motorAngleReferencesReached(motors) :
		motorAngles = interface.getMotorAngles(motors)
		if motorAngles :
			print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)

	print "Destination reached!"
	
interface.stopLogging()
interface.terminate()
