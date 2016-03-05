import robot_utils as ru
import math
import time

ru.start()

def turnSlow():
    ru.interface.setMotorRotationSpeedReference(3, 1)
    lastPos = ru.interface.getMotorAngle(3)[0]
    start = ru.interface.getMotorAngle(3)[0]
    current = ru.interface.getMotorAngle(3)[0];
    readings = 0;
    while(lastPos < start + math.radians(360)):
        while(current < lastPos + math.radians(3)):
                current = ru.interface.getMotorAngle(3)[0]
        lastPos += math.radians(3)
        reading = []
        while (len(reading) < 5):
            usReading = ru.getUltrasonicSensor()
            reading.append(usReading)

        #print ru.getUltrasonicSensor(), lastPos;
        readings += 1;
    ru.interface.setMotorRotationSpeedReference(3, 0.0)
    print readings

turnSlow()

ru.done()
