import math
import random

# Functions to generate some dummy particles data:
def calcX(t):
    return random.gauss(80,3) + 70*(math.sin(t)); # in cm

def calcY(t):
    return random.gauss(70,3) + 60*(math.sin(2*t)); # in cm

def calcW():
    return random.random();

def calcTheta():
    return random.randint(0,360);

class Particles:
    def __init__(self):
        self.n = 10;    
        self.data = [];

    def update(self, t):
        self.data = [(calcX(t), calcY(t), calcTheta(), calcW()) for i in range(self.n)];

    def get_particles(self):
        return self.data 

