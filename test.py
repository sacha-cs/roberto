def getShortestPath(point):
    points = [0,1,2,3,4]
    index = point
    after = []
    before = []
    for i in xrange(index+1, len(points)):
        after.append(points[i])
    for j in xrange(0,index+1):
        before.append(points[j])
    print before
    print after
