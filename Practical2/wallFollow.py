import robot_utils as ru
from robot_utils import median
import time

DISTANCE = 30
MAX_SPEED = 10

ru.start()

readings = []

while len(readings) < 5:
    usReading = ru.getUltrasonicSensor(2)
    readings.insert(0, usReading)
    time.sleep(0.1)

ru.interface.startLogging('followlog')

while True:
    usReading = ru.getUltrasonicSensor(2)
    readings.insert(0, usReading)
    readings = readings[:5]
    value = median(readings)
    diff = float(value - DISTANCE)
    speedDiff = diff/2
    speedDiff = max(-1, min(1, speedDiff))
    rightWheelSpeed = MAX_SPEED + speedDiff
    leftWheelSpeed = MAX_SPEED - speedDiff
    ru.interface.setMotorRotationSpeedReferences([0,1], [rightWheelSpeed, leftWheelSpeed])
    time.sleep(0.1)

ru.interface.stopLogging()
