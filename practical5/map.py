# A Map class containing walls
import math

class Map:
    def __init__(self):
        self.walls = [];

    def add_wall(self,wall):
        self.walls.append(wall);

    def clear(self):
        self.walls = [];

    def get_walls(self):
        return self.walls

    def get_distance_to_wall(self, x, y, theta):
        m = float("inf")
        theta = math.radians(theta)
        for wall in self.walls:
            Ax = wall[0]
            Ay = wall[1]
            Bx = wall[2]
            By = wall[3]
            dist = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
            div = (By - Ay) * math.cos(theta) - (Bx - Ax) * math.sin(theta)
            #div is zero if lines are parallel
            if div == 0: continue
            dist /= div
            if (dist >= 0 and dist < m):
                # check hit point is actually on a wall!
                hit_x = x + dist * math.cos(theta)
                hit_y = y + dist * math.sin(theta)
                if (hit_x >= min(Ax, Bx) and hit_x <= max(Ax, Bx) and 
                    hit_y >= min(Ay, By) and hit_y <= max(Ay, By)):
                    m = dist
        return m
