import matplotlib.pyplot as plt

data = []

with open('logfile') as f:
        data = [[float(num) for num in line.strip().split('\t')] for line in f.readlines()]

times = [row[0] for row in data]
motor1 = [row[1] for row in data]
ref1 = [row[2] for row in data]

plt.plot(times, motor1, '', times, ref1)
plt.show()
