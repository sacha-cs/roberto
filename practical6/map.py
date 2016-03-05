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

    def get_wall_parts(self, wall):
        return wall[0], wall[1], wall[2], wall[3]

    def get_wall_angle(self, wall):
           return math.degrees(math.atan2(wall[3]-wall[1],wall[2]-wall[0]))

    def get_incidence_angle(self, wall, theta):
        theta = math.radians(theta)
        
        Ax, Ay, Bx, By = self.get_wall_parts(wall)
        
        angle = (math.cos(theta) * (Ay - By) + math.sin(theta) * (Bx - Ax)) / (math.sqrt((Ay - By)**2 + (Bx - Ax) ** 2))
        angle = math.acos(angle)
        angle = math.degrees(angle)
        if(angle > 90):
            angle = 180 - angle;
        return angle;


    def get_distance_to_wall(self, x, y, theta):
        m = float("inf")
        wall_angle = None

        theta = math.radians(theta)

        for wall in self.walls:
            Ax, Ay, Bx, By = self.get_wall_parts(wall)

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
                    wall_angle = self.get_incidence_angle(wall, math.degrees(theta))
        return m, wall_angle
