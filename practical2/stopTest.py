import robot_utils as ru
import time
import random

'''
A control program allowing Roberto to stop and react when it bumps into something whilst driving. 

Usage:
    Two Touch Sensors:
        Left: Port 1
        Right: Port 2
    Two Motors: Motor Ports A and B
'''

ru.start()

ru.move(1000, wait=False)
while(True):
    leftSensor = ru.getTouchSensor(0)
    rightSensor = ru.getTouchSensor(1)
    if(leftSensor and rightSensor):
        ru.stop()
        ru.move(-10)
        if(random.random() > 0.5):
            ru.turnLeft(90)
        else:
            ru.turnRight(90)
        ru.move(1000, wait=False)
    elif(leftSensor):
        ru.stop()
        ru.move(-10)
        ru.turnRight(45)
        ru.move(1000, wait=False)
    elif (rightSensor):
        ru.stop()
        ru.move(-10)
        ru.turnLeft(45)
        ru.move(1000, wait=False)
    time.sleep(0.1)


