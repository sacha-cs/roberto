import Practical2.robot_utils as ru
from practical5.canvas import Canvas
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
