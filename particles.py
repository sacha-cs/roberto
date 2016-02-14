import Practical2.robot_utils as ru
import random
import math

SCALE_FACTOR = 15
NUMBER_OF_PARTICLES = 100

# Parameters for random variables
MEAN = 0
SIGMA_E = 0.5
SIGMA_F = 0.1
SIGMA_G = 0.1

# Offset for drawing particles and path
OFFSET = 100  # pixels

ru.start()

# Initialise coordinates and angle
x = 0
y = 0
theta = 0

# Initialise particles
particles = [(0,0,0)]*NUMBER_OF_PARTICLES

def getNoiseTermE():
    return random.gauss(MEAN, SIGMA_E)

def getNoiseTermF():
    return random.gauss(MEAN, SIGMA_F)

def getNoiseTermG():
    return random.gauss(MEAN, SIGMA_G)

def drawParticles(particles):
    print 'drawParticles:' + str([(OFFSET + SCALE_FACTOR * x, OFFSET + SCALE_FACTOR * y, theta) for (x,y,theta) in particles]) 

def drawLine(xstart, ystart, x, y):
    print 'drawLine:' + str((OFFSET + SCALE_FACTOR * xstart, OFFSET + SCALE_FACTOR * ystart, OFFSET + SCALE_FACTOR * x, OFFSET + SCALE_FACTOR * y))

def updateAfterStraightLine(x, y, theta, distance):
    xNew = x + ( distance + getNoiseTermE() ) * math.cos(theta)
    yNew = y + ( distance + getNoiseTermE() ) * math.sin(theta)
    thetaNew = theta + getNoiseTermF()
    return (xNew, yNew, thetaNew)

def updateAfterRotation(x, y, theta, alpha):
    xNew = x
    yNew = y
    thetaNew = theta + alpha + getNoiseTermG()
    return (xNew, yNew, thetaNew)

theta_change = 90  # turn 90 degrees each time
for i in range(4):

   if (i == 0):
       x_change = 1
       y_change = 0
   elif (i == 1):
       x_change = 0
       y_change = 1
   elif (i==2):
       x_change = -1
       y_change = 0
   else:
       x_change = 0
       y_change = -1
   for _ in xrange(4):
       # Make Roberto move 10cm
       ru.move(10)

       # Update position
       xstart = x
       ystart = y
       x += x_change * 10 
       y += y_change * 10

       # Update particles
       particles = [updateAfterStraightLine(x0,y0,theta0,10*(x_change+y_change)) for (x0,y0,theta0) in particles]

       # Draw lines and particles
       drawLine(xstart, ystart, x, y)
       drawParticles(particles)

   ru.turnLeft(theta_change)
   theta += theta_change  # turned 90 degrees
   particles = [updateAfterRotation(x0,y0,theta0,theta_change) for (x0,y0,theta0) in particles]  # update particles

ru.done()
