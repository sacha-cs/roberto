# Simple Particles set
class Particles:
    def __init__(self):
        self.n = 10;    
        self.data = [];

    def update(self):
        self.data = [(calcX(), calcY(), calcTheta(), calcW()) for i in range(self.n)];
    
    def draw(self):
        canvas.drawParticles(self.data);
