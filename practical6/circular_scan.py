import robot_utils as ru
from canvas import Canvas
import time
import math

if __name__ == '__main__':
    ru.start()

    canvas = Canvas(map_size=510)

    offset = 255
    x1, y1 = (0, 0)
    theta = 0

    for i in xrange(36):
        readings = []
        while (len(readings) < 5):
            usReading = ru.getUltrasonicSensor()
            readings.append(usReading)
            time.sleep(0.05)
        reading = ru.median(readings)

        x2 = reading * math.cos(math.radians(theta))
        y2 = reading * math.sin(math.radians(theta))

        canvas.draw_line((x1+offset, y1+offset, x2+offset, y2+offset))

        print "Degrees: ", theta, " - Reading: ", reading
        ru.rotateSensor(10)
        theta += 10

    ru.done()

    # ru.start()
    #
    # canvas = Canvas(map_size=510)
    # offset = 255
    # x1, y1 = (0, 0)
    # theta = 0
    #
    # ru.interface.setMotorRotationSpeedReference(3, 1)
    # lastPos = ru.interface.getMotorAngle(3)[0]
    # start = ru.interface.getMotorAngle(3)[0]
    # current = ru.interface.getMotorAngle(3)[0]
    # numReadings = 0
    # readings = []
    #
    # while(lastPos < start + math.radians(360)):
    #     theta = lastPos-360
    #
    #     while(current < lastPos + math.radians(3)):
    #             current = ru.interface.getMotorAngle(3)[0]
    #     lastPos += math.radians(3)
    #     reading = []
    #
    #     while (len(reading) < 5):
    #         usReading = ru.getUltrasonicSensor()
    #         reading.append(usReading)
    #     medianReading = ru.median(reading)
    #     readings.append(medianReading)
    #
    #     x2 = medianReading * math.cos(math.radians(theta))
    #     y2 = medianReading * math.sin(math.radians(theta))
    #     canvas.draw_line((x1+offset, y1+offset, x2+offset, y2+offset))
    #
    #     numReadings += 1
    #
    # ru.interface.setMotorRotationSpeedReference(3, 0.0)
    # print numReadings
    # print readings
    #
    # ru.done()
