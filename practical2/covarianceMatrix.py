import matplotlib.pyplot as plt
import numpy as np

data = []

with open('resultsSquare.txt') as f:
        data = [[float(num) for num in line.split(' ')] for line in f.readlines()]

data = np.array(data).T
covMat = np.cov(data)

print covMat
