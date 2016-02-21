import math

def matmult(a,b):
    zip_b = zip(*b)
    # uncomment next line if python 3 : 
    # zip_b = list(zip_b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) for col_b in zip_b] for row_a in a]

def transpose(m):
    x, y = m
    return [[x],[y]]

def rotationMatrix(theta):
    cosTerm = math.cos(math.radians(theta))
    sinTerm = -math.sin(math.radians(theta))
    return [[cosTerm, -sinTerm], [sinTerm, cosTerm]]



if __name__ == '__main__':
    m1 = [[1,0],[0,1]]
    m2 = [[1,2],[3,4]]
    print 
