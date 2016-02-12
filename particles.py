import Practical2.robot_utils as ru
import random

SCALE_FACTOR = 15
NUMBER_OF_PARTICLES = 100

# Parameters for random variables
MEAN = 0
SIGMA_X = 10
SIGMA_Y = 10
SIGMA_THETA = 1

ru.start()

x = 50
y = 50
theta = 0

particles = [(x,y,0)]*NUMBER_OF_PARTICLES

def getRandomX(x):
    dx = random.gauss(MEAN, SIGMA_X)
    return x + dx

def getRandomY(y):
    dy = random.gauss(MEAN, SIGMA_Y)
    return y + dy

def getRandomTheta(theta):
    dtheta = random.gauss(MEAN, SIGMA_THETA)
    return theta + dtheta

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
       ru.move(10)
       xstart = x
       ystart = y
       x += SCALE_FACTOR * x_change * 10
       y += SCALE_FACTOR * y_change * 10
       print "drawLine:" + str((xstart,ystart,x,y))  
       
       # Generate particles
       particles = [(getRandomX(x0) + SCALE_FACTOR * x_change*10, getRandomY(y0) + SCALE_FACTOR*y_change*10, getRandomTheta(theta0) + theta) for (x0,y0,theta0) in particles]
       print 'drawParticles:' + str(particles)

   ru.turnLeft(90)

ru.done()
