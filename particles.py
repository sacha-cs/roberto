import Practical2.robot_utils as ru
import random

SCALE_FACTOR = 15
NUMBER_OF_PARTICLES = 100

# Parameters for random variables
MEAN = 0
SIGMA_X = 10
SIGMA_Y = 10
SIGMA_THETA = 1

# Offset for drawing particles and path
OFFSET = 50  # pixels

ru.start()

# Initialise coordinates
x = OFFSET
y = OFFSET
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

def drawParticles(particles):
    print 'drawParticles:' + str([(OFFSET + SCALE_FACTOR * x, OFFSET + SCALE_FACTOR * y, theta) for (x,y,theta) in particles]) 

def drawLine(xstart, ystart, x, y):
    xstart, ystart, x, y = line
    print 'drawLine:' + str((OFFSET + xstart, OFFSET + ystart, OFFSET + x, OFFSET + y))

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
       particles = [(getRandomX(x0), getRandomY(y0), getRandomTheta(theta0)) for (x0,y0,theta0) in particles]

       # Draw lines and particles
       drawLine(xstart, ystart, x, y)
       drawParticles(particles)
       



   ru.turnLeft(90)

ru.done()
