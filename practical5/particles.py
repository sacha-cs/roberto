import math
import random
from utils import mean, gaussian

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
    def __init__(self, num=100, x=0, y=0, theta=0, sigma_e=0.4, \
                    sigma_f=0.6, sigma_g=0.3):
        self.num_particles = num
        self.sigma_e = sigma_e
        self.sigma_f = sigma_f
        self.sigma_g = sigma_g
        self.MEAN = 0
        self.SIGMA_SONAR = 3
        self.K = 0.1 
        self.particles = []
        self.__create_particles(x, y, theta)

    def __create_particles(self, x, y, theta):
        w = 1.0 / self.num_particles
        for i in range(self.num_particles):
            self.particles.append((x, y, theta, w))

    # Computes mean (x, y, theta) of all particles
    def get_position(self):
        sum_weights = sum([w for (_,_,_,w) in self.particles])
        x_arr = [x0*w for (x0, _, _, w) in self.particles]
        y_arr = [y0*w for (_, y0, _, w) in self.particles]
        theta_arr = [theta0*w for (_, _, theta0, w) in self.particles]
        return [sum(x_arr)/sum_weights, sum(y_arr)/sum_weights, sum(theta_arr)/sum_weights]

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

    def weight_update(self, z, map):
        new_particles = []
        for p in self.particles:
            new_weight = p[3] * self.__calculate_likelihood(p, z, map)
            new_particles.append((p[0], p[1], p[2], new_weight))

        self.particles = new_particles
        self.__normalise_particles()

    def resample(self):
        # Compute cumulative weight array
        weight_cdf = [0] * (self.num_particles)
        cumul = 0
        for i in xrange(0, self.num_particles):
            cumul += self.particles[i][3]
            weight_cdf[i] = cumul

        new_particles = []
        for _ in xrange(self.num_particles):
            rand_num = random.uniform(0,1)

            i = 0
            curr_max = 0
            while (curr_max < rand_num and i < self.num_particles):
                curr_max = weight_cdf[i]
                i = i + 1

            new_particles.append(self.particles[i-1])
        self.particles = [(x, y, theta, 1.0/self.num_particles) for (x, y, theta, _) in new_particles]

    def __normalise_particles(self):
        sum_weights = sum([w for (_,_,_,w) in self.particles])
        new_particles = []
        for p in self.particles:
            new_particles.append((p[0], p[1], p[2], p[3]/sum_weights))
        self.particles = new_particles

    def __calculate_likelihood(self, p, z, map):
        m, incidence = map.get_distance_to_wall(p[0], p[1], p[2])
        # Use Normal distributional model (s.d.: 2-3) to compute likelihood value (z-m)
        likelihood = gaussian(z, self.SIGMA_SONAR)(m) + self.K
        return likelihood
