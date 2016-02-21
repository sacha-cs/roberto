import math
import random
from utils import mean

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
    def __init__(self, num=1, x=0, y=0, theta=0, sigma_e=0.07, \
                    sigma_f=0.2, sigma_g=0.1):
        self.num_particles = num
        self.sigma_e = sigma_e
        self.sigma_f = sigma_f
        self.sigma_g = sigma_g
        self.MEAN = 0
        self.particles = []
        self.__create_particles(x, y, theta)

    def __create_particles(self, x, y, theta):
        w = 1.0 / self.num_particles
        for i in range(self.num_particles):
            self.particles.append((x, y, theta, w))

    # Computes mean (x, y, theta) of all particles
    def get_position(self):
        x_arr = [x0 for (x0, _, _, _) in self.particles]
        y_arr = [y0 for (_, y0, _, _) in self.particles]
        theta_arr = [theta0 for (_, _, theta0, _) in self.particles]
        return [mean(x_arr), mean(y_arr), mean(theta_arr)]

    def update_after_straight_line(self, distance):
        self.particles = [self.__update_straight(x,y,theta,distance,w) for (x,y,theta,w) in self.particles]

    def __update_straight(self, x, y, theta, distance, w):
        x_new = x + ( distance + self.__get_noise_term(self.sigma_e) ) * math.cos(math.radians(theta))
        y_new = y + ( distance + self.__get_noise_term(self.sigma_e) ) * math.sin(math.radians(theta))
        theta_new = theta + self.__get_noise_term(self.sigma_f)
        return (x_new, y_new, theta_new, w)

    def update_after_rotation(self, alpha):
        self.particles = [self.__update_rotation(x,y,theta,alpha,w) for (x,y,theta,w) in self.particles]

    def __update_rotation(self, x, y, theta, alpha, w):
        if alpha == 0:
            return (x, y, theta, w)  # doesn't change
        theta_new = theta + alpha + self.__get_noise_term(self.sigma_g)
        return (x, y, theta_new, w)

    def __get_noise_term(self, sigma):
        return random.gauss(self.MEAN, sigma)

    # TODO: do we need this?
    def update(self, t):
        self.particles = [(calcX(t), calcY(t), calcTheta(), calcW()) for i in range(self.num_particles)]

    def get_particles(self):
        return self.particles 

