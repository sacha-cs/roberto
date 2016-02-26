def mean(data):
    return float(sum(data))/len(data)

def gaussian(mean, sd):
    return lambda x: math.exp(-float(x - mean)**2 / (2.0 * sd ** 2))
