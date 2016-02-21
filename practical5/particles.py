import math
import random

NUMBER_OF_PARTICLES = 100

# Functions to generate some dummy particles data:
def calcX(t):
    return random.gauss(80,3) + 70*(math.sin(t)) # in cm

def calcY(t):
    return random.gauss(70,3) + 60*(math.sin(2*t)) # in cm

def calcW():
    return random.random()

def calcTheta():
    return random.randint(0,360)

class Particles:
    def __init__(self, x=0, y=0, theta=0):
        self.particles = []
        self.__create_particles(x, y, theta)

    def __create_particles(self, x, y, theta):
        w = 1.0 / NUMBER_OF_PARTICLES
        for i in range(NUMBER_OF_PARTICLES):
            self.particles.append((x, y, theta, w))

    def update(self, t):
        self.particles = [(calcX(t), calcY(t), calcTheta(), calcW()) for i in range(NUMBER_OF_PARTICLES)]

    def get_particles(self):
        return self.particles 

