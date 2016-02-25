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
    def __init__(self, num=100, x=0, y=0, theta=0, sigma_e=1.5, \
                    sigma_f=1.0, sigma_g=0.1):
        self.num_particles = num
        self.sigma_e = sigma_e
        self.sigma_f = sigma_f
        self.sigma_g = sigma_g
        self.MEAN = 0
        self.SIGMA_SONAR = 3;
        self.K = 0.1; #TODO
        self.particles = []
        self.__create_particles(x, y, theta)

    def __create_particles(self, x, y, theta):
        w = 1.0 / self.num_particles
        for i in range(self.num_particles):
            self.particles.append((x, y, theta, w))

    # Computes mean (x, y, theta) of all particles
    #TODO: Should take into account weight of particles
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

    def weight_update(self, z, m):
        # print "\n\nWeight Update:"
        # print "Before weight update: ", self.particles
        new_particles = []
        for p in self.particles:
            # print "Old weight: ", p[3]
            new_weight = p[3] * self.__calculate_likelihood(z, m)
            # print "New weight: ", new_weight
            new_particles.append((p[0], p[1], p[2], new_weight))

        # print "After update and before normalising: ", new_particles
        self.particles = self.__normalise_particles(new_particles)
        # print "After normalising: ", self.particles

    def resample(self):
        # print "\n\nResample:"
        # Order particles by weight
        self.particles.sort(key=lambda p:p[3])
        # print "Particles sorted: ", self.particles
        # Compute cumulative weight array
        weight_cdf = [0] * (self.num_particles+1)
        cumul = 0
        for i in xrange(0, self.num_particles):
            cumul += self.particles[i][3]
            weight_cdf[i+1] = cumul
        # print "CDF: ", weight_cdf

        new_particles = []
        for _ in xrange(self.num_particles):
            rand_num = random.uniform(0,1)
            # print "Random num : ", rand_num

            i = 0
            curr_max = 0
            while (curr_max < rand_num and i < self.num_particles):
                # print "Curr max: ", curr_max
                curr_max = weight_cdf[i+1]
                i = i + 1

            # print "Index : ", i

            new_particles.append(self.particles[i-1])

        self.particles = new_particles

    def __normalise_particles(self, particles):
        sum_weights = sum([w for (_,_,_,w) in particles])
        new_particles = []
        for p in particles:
            new_particles.append((p[0], p[1], p[2], p[3]/sum_weights))
        return new_particles

    def __calculate_likelihood(self, z, m):
        print "\nz : {}, m :{}\n".format(z, m)
        # Use Normal distributional model (s.d.: 2-3) to compute likelihood value (z-m)
        print "-float(z-m)**2 : ", (-float(z-m)**2)
        print "(2*self.SIGMA_SONAR**2) : ", (2*self.SIGMA_SONAR**2)
        likelihood = math.exp(-float(z-m)**2 / (2*self.SIGMA_SONAR**2)) + self.K
        print "Likelihood: ", likelihood
        return likelihood
