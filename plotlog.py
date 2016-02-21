import matplotlib.pyplot as plt

def plot(data, timeCol, motorCol, refCol):
    times = [row[timeCol] for row in data]
    motor = [row[motorCol] - data[0][motorCol] for row in data]
    ref = [row[refCol] - data[0][motorCol] for row in data]
    error = [motor[i] - ref[i] for i in range(len(motor))]

    plt.plot(times, motor, '', times, ref, '', times, error)
    plt.show()

data = []

with open('logfile') as f:
        data = [[float(num) for num in line.strip().split('\t')] for line in f.readlines()]

plot(data, 0, 1, 2)
plot(data, 0, 3, 4)
