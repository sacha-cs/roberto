import robot_utils as ru
from robot_utils import median
import time

ru.start(ru.CONTROL_VELOCITY)

readings = []

while True:
    usReading = ru.getUltrasonicSensor(2)
    readings.insert(0, usReading)
    readings = readings[:3]
    value = median(readings)
    diff = float(value - 30)
    diff /= 2
    diff = min(11.5, max(-11.5, diff))
    ru.interface.setMotorRotationSpeedReferences([0,1], [diff, diff])
    time.sleep(0.1)


 
