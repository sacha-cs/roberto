from map import Map
import math

WAYPOINT_COORDS = [(84,30), (180,30), (180,54), (138,54), (138,168)]
DEG_INTERVAL = 3.0

# Change value to get data for different waypoint
WAYPOINT = 1

def add_walls(my_map):
    my_map.add_wall((0,0,0,168))        # a: O to A
    my_map.add_wall((0,168.0,84,168.0))     # b: A to B
    my_map.add_wall((84,126,84,210))    # c: C to D
    my_map.add_wall((84,210,168,210))   # d: D to E
    my_map.add_wall((168,210,168,84))   # e: E to F
    my_map.add_wall((168,84,210,84))    # f: F to G
    my_map.add_wall((210,84,210,0))     # g: G to H
    my_map.add_wall((210,0,0,0))        # h: H to O

my_map = Map()
add_walls(my_map)

x = WAYPOINT_COORDS[WAYPOINT-1][0]
y = WAYPOINT_COORDS[WAYPOINT-1][1] 

# Theta is angle anticlockwise from x-axis (i.e. robot turning left)
# Sonar rotates clockwise (i.e. turns right wrt robot)
# Theta decremented from 360 to replicate order of readings as if taken from sonar
theta = 360.0
index = 1
while theta > 0:
    dist = my_map.get_distance_to_wall(x,y,theta)[0]
    
    # Simplify comparison to sonar readings
    if not math.isinf(dist):
        dist = int(dist) 
    
    print "Index {:3d} \t Deg {:3d} \t Depth {}".format(index, int(theta), dist)

    theta -= DEG_INTERVAL
    index += 1

'''
theta = 105.0
dist = my_map.get_distance_to_wall(x,y,theta)[0]
print "Distance:", dist
'''
